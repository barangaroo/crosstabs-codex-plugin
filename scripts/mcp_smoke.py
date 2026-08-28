#!/usr/bin/env python3
"""Start the exact plugin MCP command and verify its public surface."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "crosstabs"


async def smoke() -> dict[str, object]:
    mcp_config = json.loads((PLUGIN_ROOT / ".mcp.json").read_text())
    parity = json.loads((PLUGIN_ROOT / "parity.json").read_text())
    expected = parity["distribution"]

    async def inspect_server(name: str) -> tuple[object, object, object, object]:
        server = mcp_config["mcpServers"][name]
        parameters = StdioServerParameters(command=server["command"], args=server["args"])
        async with stdio_client(parameters) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                initialized = await session.initialize()
                tools = await session.list_tools()
                resources = await session.list_resources()
                templates = await session.list_resource_templates()
        return initialized, tools, resources, templates

    initialized, tools, resources, _ = await inspect_server("crosstabs-statistics")
    headless_initialized, headless_tools, _, headless_templates = await inspect_server(
        "crosstabs-headless"
    )

    actual_resource_uris = sorted(str(resource.uri) for resource in resources.resources)
    expected_resource_uris = sorted(expected["resourceUris"])
    if len(tools.tools) != expected["toolCount"]:
        raise SystemExit(
            f"expected {expected['toolCount']} tools, received {len(tools.tools)}"
        )
    if actual_resource_uris != expected_resource_uris:
        raise SystemExit(
            f"resource mismatch: expected {expected_resource_uris}, received {actual_resource_uris}"
        )
    actual_headless_tools = [tool.name for tool in headless_tools.tools]
    if actual_headless_tools != expected["headlessTools"]:
        raise SystemExit(
            f"headless tool mismatch: expected {expected['headlessTools']}, "
            f"received {actual_headless_tools}"
        )
    actual_templates = sorted(
        str(template.uri_template)
        for template in headless_templates.resource_templates
    )
    if actual_templates != sorted(expected["headlessResourceTemplates"]):
        raise SystemExit(
            f"headless resource template mismatch: expected {expected['headlessResourceTemplates']}, "
            f"received {actual_templates}"
        )

    return {
        "packageVersion": expected["version"],
        "serverName": initialized.server_info.name,
        "serverVersion": initialized.server_info.version,
        "toolCount": len(tools.tools),
        "resourceUris": actual_resource_uris,
        "headlessServerName": headless_initialized.server_info.name,
        "headlessServerVersion": headless_initialized.server_info.version,
        "headlessToolCount": len(headless_tools.tools),
        "headlessResourceTemplates": actual_templates,
        "status": "passed",
    }


if __name__ == "__main__":
    print(json.dumps(asyncio.run(smoke()), sort_keys=True))
