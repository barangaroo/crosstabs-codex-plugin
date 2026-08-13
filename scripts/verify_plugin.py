#!/usr/bin/env python3
"""Fail-closed validation for the public Crosstabs Codex marketplace."""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "crosstabs"


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
    mcp_config = read_json(PLUGIN_ROOT / ".mcp.json")
    parity = read_json(PLUGIN_ROOT / "parity.json")
    read_json(PLUGIN_ROOT / "parity.schema.json")

    if marketplace.get("name") != "crosstabs":
        raise ValueError("marketplace name must be crosstabs")
    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1:
        raise ValueError("marketplace must publish exactly one plugin")
    entry = entries[0]
    if entry.get("name") != manifest.get("name"):
        raise ValueError("marketplace and plugin names differ")
    if entry.get("source") != {"source": "local", "path": "./plugins/crosstabs"}:
        raise ValueError("marketplace source must resolve to ./plugins/crosstabs")

    if manifest.get("version") != parity.get("pluginVersion"):
        raise ValueError("manifest version and parity contract version differ")
    if manifest.get("repository") != "https://github.com/barangaroo/crosstabs-codex-plugin":
        raise ValueError("plugin repository URL is not canonical")
    if manifest.get("mcpServers") != "./.mcp.json":
        raise ValueError("plugin must reference ./.mcp.json")
    if manifest.get("skills") != "./skills/":
        raise ValueError("plugin must reference ./skills/")

    interface = manifest.get("interface", {})
    for asset_field in ("composerIcon", "logo"):
        asset = interface.get(asset_field)
        if not isinstance(asset, str) or not (PLUGIN_ROOT / asset).is_file():
            raise ValueError(f"missing interface asset {asset_field}")

    distribution = parity.get("distribution", {})
    version = distribution.get("version")
    requirement = f"crosstabs=={version}"
    if distribution.get("requirement") != requirement:
        raise ValueError("parity package requirement is not exact")
    expected_server = {
        "command": "uvx",
        "args": ["--from", requirement, "crosstabs"],
    }
    if mcp_config.get("mcpServers", {}).get("crosstabs") != expected_server:
        raise ValueError("MCP config does not exactly match the parity package")
    if distribution.get("transport") != "stdio":
        raise ValueError("plugin transport must be stdio")
    if distribution.get("toolCount") != 39:
        raise ValueError("verified tool count must be 39")

    resource_uris = distribution.get("resourceUris")
    if sorted(resource_uris or []) != [
        "crosstabs://evidence/graph",
        "crosstabs://evidence/limitations",
    ]:
        raise ValueError("verified evidence resources differ from the release contract")

    datetime.fromisoformat(parity["verifiedAt"].replace("Z", "+00:00"))
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

    return {
        "pluginVersion": manifest["version"],
        "packageVersion": version,
        "surfaceCount": len(surfaces),
    }


def verify_live(local: dict[str, Any]) -> dict[str, Any]:
    version = local["packageVersion"]
    pypi = fetch_json(f"https://pypi.org/pypi/crosstabs/{version}/json")
    if pypi.get("info", {}).get("version") != version:
        raise ValueError("PyPI version does not match the plugin contract")
    if "39 statistical tools" not in pypi.get("info", {}).get("description", ""):
        raise ValueError("PyPI description does not substantiate the tool count")

    registry_url = (
        "https://registry.modelcontextprotocol.io/v0.1/servers/"
        "io.github.barangaroo%2Fcrosstabs/versions/"
        f"{version}"
    )
    registry = fetch_json(registry_url)
    server = registry.get("server", {})
    official = registry.get("_meta", {}).get("io.modelcontextprotocol.registry/official", {})
    expected_package = {
        "registryType": "pypi",
        "identifier": "crosstabs",
        "version": version,
        "transport": {"type": "stdio"},
    }
    if server.get("name") != "io.github.barangaroo/crosstabs":
        raise ValueError("MCP Registry server name differs")
    if server.get("version") != version or expected_package not in server.get("packages", []):
        raise ValueError("MCP Registry package differs from the plugin contract")
    if official.get("status") != "active" or official.get("isLatest") is not True:
        raise ValueError("MCP Registry record is not active/latest")

    return {
        "pypi": f"crosstabs {version}",
        "registry": f"io.github.barangaroo/crosstabs {version} active/latest",
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
