#!/usr/bin/env python3
"""Fail-closed validation for the Crosstabs Codex candidate and public boundary."""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "crosstabs"
EXPECTED_PLUGIN_VERSION = "0.2.4"
EXPECTED_PACKAGE_VERSION = "1.1.6"
EXPECTED_REGISTRY_NAME = "io.github.crosstabs/crosstabs"
EXPECTED_RELEASE_STATE = {
    "schemaVersion": 1,
    "candidate": {
        "state": "local_release_candidate",
        "published": False,
        "pluginVersion": EXPECTED_PLUGIN_VERSION,
        "packageVersion": EXPECTED_PACKAGE_VERSION,
        "registryName": EXPECTED_REGISTRY_NAME,
        "immutableReference": None,
    },
    "currentPublicRelease": {
        "state": "published_marketplace_release",
        "published": True,
        "pluginVersion": "0.2.3",
        "packageVersion": "1.1.3",
        "registryName": "io.github.barangaroo/crosstabs",
        "immutableReference": None,
    },
    "promotionRequirements": [
        "Commit the 0.2.4 candidate and publish an immutable public marketplace release reference.",
        "Verify the exact published artifact against crosstabs==1.1.6 and io.github.crosstabs/crosstabs.",
    ],
}


def registry_record_url(name: str, version: str) -> str:
    return (
        "https://registry.modelcontextprotocol.io/v0.1/servers/"
        f"{quote(name, safe='')}/versions/{quote(version, safe='')}"
    )


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def fetch_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "crosstabs-plugin-ci/0.1"})
    with urllib.request.urlopen(request, timeout=20) as response:
        value = json.load(response)
    if not isinstance(value, dict):
        raise ValueError(f"{url} did not return a JSON object")
    return value


def verify_local() -> dict[str, Any]:
    marketplace = read_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    manifest = read_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
    claude_manifest = read_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json")
    mcp_config = read_json(PLUGIN_ROOT / ".mcp.json")
    parity = read_json(PLUGIN_ROOT / "parity.json")
    parity_schema = read_json(PLUGIN_ROOT / "parity.schema.json")
    release_state = read_json(PLUGIN_ROOT / "release-state.json")

    if release_state != EXPECTED_RELEASE_STATE:
        raise ValueError("release-state contract differs from the candidate/public boundary")

    if marketplace.get("name") != "crosstabs":
        raise ValueError("marketplace name must be crosstabs")
    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1:
        raise ValueError("marketplace must publish exactly one plugin")
    entry = entries[0]
    expected_entry = {
        "name": "crosstabs",
        "source": {"source": "local", "path": "./plugins/crosstabs"},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "category": "Data & Analytics",
    }
    if entry != expected_entry:
        raise ValueError("marketplace entry metadata differs from the release contract")

    if manifest.get("version") != parity.get("pluginVersion"):
        raise ValueError("manifest version and parity contract version differ")
    if manifest.get("version") != EXPECTED_PLUGIN_VERSION:
        raise ValueError("plugin manifest does not match the immutable release version")
    if manifest.get("repository") != "https://github.com/barangaroo/crosstabs-codex-plugin":
        raise ValueError("plugin repository URL is not canonical")
    if manifest.get("mcpServers") != "./.mcp.json":
        raise ValueError("plugin must reference ./.mcp.json")
    if manifest.get("skills") != "./skills/":
        raise ValueError("plugin must reference ./skills/")
    if claude_manifest.get("version") != EXPECTED_PLUGIN_VERSION:
        raise ValueError("Claude manifest version does not match the candidate version")
    if claude_manifest.get("repository") != manifest.get("repository"):
        raise ValueError("Claude and Codex manifests must use the same repository")
    if claude_manifest.get("mcpServers") != "./.mcp.json":
        raise ValueError("Claude manifest must reference ./.mcp.json")
    if claude_manifest.get("skills") != "./skills/":
        raise ValueError("Claude manifest must reference ./skills/")

    interface = manifest.get("interface", {})
    for asset_field in ("composerIcon", "logo"):
        asset = interface.get(asset_field)
        if not isinstance(asset, str) or not (PLUGIN_ROOT / asset).is_file():
            raise ValueError(f"missing interface asset {asset_field}")

    distribution = parity.get("distribution", {})
    version = distribution.get("version")
    if parity.get("schemaVersion") != 3:
        raise ValueError("parity contract schema version differs")
    if version != EXPECTED_PACKAGE_VERSION:
        raise ValueError("parity package does not match the immutable release version")
    requirement = f"crosstabs=={version}"
    if distribution.get("requirement") != requirement:
        raise ValueError("parity package requirement is not exact")
    expected_statistics_server = {
        "command": "uvx",
        "args": ["--from", requirement, "crosstabs"],
    }
    expected_headless_server = {
        "command": "uvx",
        "args": ["--from", requirement, "crosstabs-headless"],
    }
    expected_servers = {
        "crosstabs-statistics": expected_statistics_server,
        "crosstabs-headless": expected_headless_server,
    }
    if mcp_config.get("mcpServers") != expected_servers:
        raise ValueError("MCP config does not expose both exact parity commands")
    if distribution.get("transport") != "stdio":
        raise ValueError("plugin transport must be stdio")
    registry_name = distribution.get("registryName")
    if registry_name != EXPECTED_REGISTRY_NAME:
        raise ValueError("parity MCP Registry identity is not canonical")
    expected_registry_record = registry_record_url(registry_name, version)
    if distribution.get("registryRecord") != expected_registry_record:
        raise ValueError("parity MCP Registry record URL differs")
    if distribution.get("toolCount") != 39:
        raise ValueError("verified tool count must be 39")
    headless_tools = distribution.get("headlessTools")
    if not isinstance(headless_tools, list) or len(headless_tools) != 23:
        raise ValueError("verified headless tool catalog must contain 23 names")
    if distribution.get("headlessToolCount") != len(headless_tools):
        raise ValueError("headless tool count differs from the exact catalog")
    if distribution.get("headlessResourceTemplates") != [
        "crosstabs://artifacts/{artifactId}"
    ]:
        raise ValueError("verified headless artifact template differs")

    resource_uris = distribution.get("resourceUris")
    if sorted(resource_uris or []) != [
        "crosstabs://evidence/graph",
        "crosstabs://evidence/limitations",
    ]:
        raise ValueError("verified evidence resources differ from the release contract")

    datetime.fromisoformat(parity["verifiedAt"].replace("Z", "+00:00"))
    schema_properties = parity_schema.get("properties", {})
    schema_distribution = schema_properties.get("distribution", {}).get("properties", {})
    if schema_properties.get("schemaVersion", {}).get("const") != parity["schemaVersion"]:
        raise ValueError("parity schema does not pin its contract version")
    if schema_properties.get("pluginVersion", {}).get("const") != EXPECTED_PLUGIN_VERSION:
        raise ValueError("parity schema does not pin the plugin version")
    if schema_distribution.get("version", {}).get("const") != EXPECTED_PACKAGE_VERSION:
        raise ValueError("parity schema does not pin the package version")
    if schema_distribution.get("registryName", {}).get("const") != EXPECTED_REGISTRY_NAME:
        raise ValueError("parity schema does not pin the Registry identity")
    surfaces = parity.get("surfaces")
    if not isinstance(surfaces, list) or not surfaces:
        raise ValueError("parity contract has no surfaces")
    ids = [surface.get("id") for surface in surfaces]
    if len(ids) != len(set(ids)):
        raise ValueError("parity contract repeats a surface id")
    for surface in surfaces:
        if surface.get("status") not in {"verified", "bounded", "app-only"}:
            raise ValueError(f"invalid parity status for {surface.get('id')}")
        if not all(isinstance(surface.get(field), str) and surface[field] for field in ("id", "label", "boundary")):
            raise ValueError("every parity surface needs id, label, and boundary")

    skill = (PLUGIN_ROOT / "skills" / "analyze-survey-crosstabs" / "SKILL.md").read_text()
    if not re.match(r"^---\nname: analyze-survey-crosstabs\ndescription: .+\n---\n", skill):
        raise ValueError("skill frontmatter is missing or invalid")
    if "Product parity boundary" not in skill or "parity-and-limits.md" not in skill:
        raise ValueError("skill does not disclose the parity boundary")

    forbidden = []
    placeholder_pattern = re.compile(r"\b(?:" + "TO" + "DO|FIX" + "ME)\b")
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in {".md", ".json", ".yaml", ".yml", ".py"}:
            continue
        content = path.read_text(errors="replace")
        if placeholder_pattern.search(content):
            forbidden.append(str(path.relative_to(ROOT)))
    if forbidden:
        raise ValueError(f"unresolved placeholders: {', '.join(forbidden)}")

    readme = (ROOT / "README.md").read_text()
    for statement in (
        "Version 0.2.4 is a local release candidate, not the current public Codex marketplace release.",
        "The currently published marketplace release remains 0.2.3",
        "--ref main` installs the development/candidate marketplace source",
        "This Claude package is an unpublished local candidate.",
        "submitted to, approved by, or published in Anthropic's plugin directory.",
    ):
        if statement not in readme:
            raise ValueError("README does not preserve the candidate/public release boundary")

    return {
        "candidateState": release_state["candidate"]["state"],
        "pluginVersion": manifest["version"],
        "packageVersion": version,
        "registryName": registry_name,
        "surfaceCount": len(surfaces),
        "headlessToolCount": len(headless_tools),
    }


def verify_live(local: dict[str, Any]) -> dict[str, Any]:
    version = local["packageVersion"]
    pypi = fetch_json(f"https://pypi.org/pypi/crosstabs/{version}/json")
    if pypi.get("info", {}).get("version") != version:
        raise ValueError("PyPI version does not match the plugin contract")
    if "39 statistical tools" not in pypi.get("info", {}).get("description", ""):
        raise ValueError("PyPI description does not substantiate the tool count")

    registry_name = local["registryName"]
    registry_url = registry_record_url(registry_name, version)
    registry = fetch_json(registry_url)
    server = registry.get("server", {})
    official = registry.get("_meta", {}).get("io.modelcontextprotocol.registry/official", {})
    expected_package = {
        "registryType": "pypi",
        "identifier": "crosstabs",
        "version": version,
        "transport": {"type": "stdio"},
    }
    if server.get("name") != registry_name:
        raise ValueError("MCP Registry server name differs")
    if server.get("version") != version or expected_package not in server.get("packages", []):
        raise ValueError("MCP Registry package differs from the plugin contract")
    if official.get("status") != "active" or official.get("isLatest") is not True:
        raise ValueError("MCP Registry record is not active/latest")

    return {
        "pypi": f"crosstabs {version}",
        "registry": f"{registry_name} {version} active/latest",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    result: dict[str, Any] = {"local": verify_local()}
    if args.live:
        result["live"] = verify_live(result["local"])
    result["status"] = "passed"
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
