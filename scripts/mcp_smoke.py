#!/usr/bin/env python3
"""Verify the candidate MCP catalog without overstating unpublished artifacts."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import tempfile
from urllib.request import urlopen
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from packaging.requirements import Requirement
from packaging.version import Version


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "crosstabs"


def validate_package_metadata(metadata: dict[str, Any], version: str) -> None:
    info = metadata["info"]
    if info["version"] != version:
        raise SystemExit("PyPI package version does not match the exact plugin pin")
    requirements = [Requirement(value) for value in info.get("requires_dist", [])]
    mcp_requirements = [requirement for requirement in requirements if requirement.name == "mcp"]
    if len(mcp_requirements) != 1:
        raise SystemExit("Package must declare one explicit compatible MCP 1.x dependency")
    requirement = mcp_requirements[0]
    has_major_cap = any(spec.operator == "<" and Version(spec.version) == Version("2")
                        for spec in requirement.specifier)
    if requirement.url or requirement.marker or not has_major_cap or "1.29.0" not in requirement.specifier:
        raise SystemExit("Package must cap the compatible MCP 1.x dependency below 2 and admit 1.29.0")


def verify_published_package(version: str) -> None:
    with urlopen(f"https://pypi.org/pypi/crosstabs/{version}/json", timeout=20) as response:
        payload = response.read(2 * 1024 * 1024 + 1)
    if len(payload) > 2 * 1024 * 1024:
        raise SystemExit("PyPI package metadata exceeds the verification bound")
    validate_package_metadata(json.loads(payload), version)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--headless-bundle",
        type=Path,
        help=(
            "Run only the headless smoke against this local .mjs bundle. "
            "This avoids resolving the unpublished package candidate."
        ),
    )
    parser.add_argument(
        "--node",
        default="node",
        help="Node.js executable for --headless-bundle (default: node)",
    )
    return parser.parse_args()


async def inspect_server(
    server: dict[str, Any],
    *,
    environment: dict[str, str] | None = None,
) -> tuple[types.InitializeResult, types.ListToolsResult, types.ListResourcesResult,
           types.ListResourceTemplatesResult]:
    parameters = StdioServerParameters(
        command=server["command"],
        args=server["args"],
        env=environment,
    )
    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            initialized = await session.initialize()
            tools = await session.list_tools()
            resources = await session.list_resources()
            templates = await session.list_resource_templates()
    return initialized, tools, resources, templates


def validate_headless(
    initialized: types.InitializeResult,
    tools: types.ListToolsResult,
    templates: types.ListResourceTemplatesResult,
    expected: dict[str, Any],
) -> dict[str, Any]:
    actual_tools = [tool.name for tool in tools.tools]
    if actual_tools != expected["headlessTools"]:
        raise SystemExit(
            f"headless tool mismatch: expected {expected['headlessTools']}, "
            f"received {actual_tools}"
        )
    if len(actual_tools) != expected["headlessToolCount"]:
        raise SystemExit(
            f"expected {expected['headlessToolCount']} headless tools, "
            f"received {len(actual_tools)}"
        )

    actual_templates = sorted(
        str(template.uriTemplate) for template in templates.resourceTemplates
    )
    expected_templates = sorted(expected["headlessResourceTemplates"])
    if actual_templates != expected_templates:
        raise SystemExit(
            f"headless resource-template mismatch: expected {expected_templates}, "
            f"received {actual_templates}"
        )

    design_tool = next(
        (tool for tool in tools.tools if tool.name == "define_survey_design"),
        None,
    )
    if design_tool is None:
        raise SystemExit("define_survey_design tool is missing")
    required = design_tool.inputSchema.get("required", [])
    expected_required = {
        "projectId",
        "expectedRevision",
        "idempotencyKey",
        "tableIds",
        "definition",
        "approval",
    }
    if not isinstance(required, list) or not expected_required.issubset(required):
        raise SystemExit("define_survey_design input schema is incomplete")

    server_info = initialized.serverInfo
    if server_info.name != "crosstabs-headless":
        raise SystemExit(f"unexpected headless server name: {server_info.name}")
    if server_info.version != expected["version"]:
        raise SystemExit(
            f"expected headless version {expected['version']}, "
            f"received {server_info.version}"
        )

    return {
        "headlessServerName": server_info.name,
        "headlessServerVersion": server_info.version,
        "headlessToolCount": len(actual_tools),
        "headlessTools": actual_tools,
        "headlessResourceTemplates": actual_templates,
    }


async def smoke(args: argparse.Namespace) -> dict[str, object]:
    mcp_config = json.loads((PLUGIN_ROOT / ".mcp.json").read_text())
    parity = json.loads((PLUGIN_ROOT / "parity.json").read_text())
    expected = parity["distribution"]

    if args.headless_bundle is None:
        verify_published_package(expected["version"])

    with tempfile.TemporaryDirectory(prefix="crosstabs-plugin-smoke-") as state_dir:
        environment = {**os.environ, "CROSSTABS_DATA_DIR": state_dir}

        if args.headless_bundle is not None:
            bundle = args.headless_bundle.expanduser().resolve()
            if not bundle.is_file() or bundle.suffix != ".mjs":
                raise SystemExit("--headless-bundle must name an existing .mjs file")
            initialized, tools, _, templates = await inspect_server(
                {"command": args.node, "args": [str(bundle)]},
                environment=environment,
            )
            headless = validate_headless(initialized, tools, templates, expected)
            return {
                "mode": "local_headless_bundle",
                "bundle": str(bundle),
                "packageVersion": expected["version"],
                "packagePublished": expected["packagePublished"],
                **headless,
                "statisticsServer": "not_run_unpublished_package",
                "status": "passed",
            }

        initialized, tools, resources, _ = await inspect_server(
            mcp_config["mcpServers"]["crosstabs-statistics"],
            environment=environment,
        )
        headless_initialized, headless_tools, _, headless_templates = await inspect_server(
            mcp_config["mcpServers"]["crosstabs-headless"],
            environment=environment,
        )

    actual_resource_uris = sorted(str(resource.uri) for resource in resources.resources)
    expected_resource_uris = sorted(expected["resourceUris"])
    if len(tools.tools) != expected["toolCount"]:
        raise SystemExit(
            f"expected {expected['toolCount']} statistics tools, "
            f"received {len(tools.tools)}"
        )
    if actual_resource_uris != expected_resource_uris:
        raise SystemExit(
            f"resource mismatch: expected {expected_resource_uris}, "
            f"received {actual_resource_uris}"
        )
    headless = validate_headless(
        headless_initialized,
        headless_tools,
        headless_templates,
        expected,
    )

    return {
        "mode": "packaged_candidate",
        "packageVersion": expected["version"],
        "packagePublished": expected["packagePublished"],
        "statisticsServerName": initialized.serverInfo.name,
        "statisticsServerVersion": initialized.serverInfo.version,
        "statisticsToolCount": len(tools.tools),
        "resourceUris": actual_resource_uris,
        **headless,
        "status": "passed",
    }


if __name__ == "__main__":
    print(json.dumps(asyncio.run(smoke(parse_args())), sort_keys=True))
