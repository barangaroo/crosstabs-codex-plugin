#!/usr/bin/env python3
"""Fail-closed validation for the unpublished local Crosstabs plugin candidate."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "crosstabs"
EXPECTED_PLUGIN_VERSION = "0.2.5"
EXPECTED_PACKAGE_VERSION = "1.2.0"
EXPECTED_REGISTRY_NAME = "io.github.crosstabs/crosstabs"
EXPECTED_STATISTICS_TOOL_COUNT = 39
EXPECTED_HEADLESS_TOOLS = [
    "create_project",
    "import_dataset",
    "profile_dataset",
    "define_row_set",
    "define_banner",
    "apply_filter",
    "set_weight",
    "run_table",
    "run_tab_book",
    "compare_waves",
    "undo_change",
    "replace_dataset",
    "detect_schema_drift",
    "repair_schema",
    "generate_report_pack",
    "refresh_report_pack",
    "export_project",
    "list_projects",
    "inspect_project",
    "get_audit_history",
    "define_survey_design",
]
EXPECTED_SURFACE_IDS = [
    "statistical-tools",
    "evidence-resources",
    "raw-data-input",
    "research-workflow",
    "project-model",
    "advanced-tabulation",
    "report-refresh",
    "tracker-workflow",
    "device-local-boundary",
]
EXPECTED_RELEASE_STATE = {
    "schemaVersion": 2,
    "candidate": {
        "state": "local_committed_unpublished_candidate",
        "published": False,
        "packagePublished": False,
        "registryPublished": False,
        "pluginVersion": EXPECTED_PLUGIN_VERSION,
        "packageVersion": EXPECTED_PACKAGE_VERSION,
        "registryName": EXPECTED_REGISTRY_NAME,
        "registryRecord": None,
        "immutableReference": None,
        "verificationScope": "local_candidate",
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
        "Publish crosstabs==1.2.0 and verify its exact Registry record before making a package or Registry availability claim.",
        "Publish plugin 0.2.5 from an immutable source reference before making a marketplace or directory availability claim.",
        "Repeat strict host validation and both MCP server smoke checks against the exact published artifacts.",
    ],
}


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def require_exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ValueError(f"{label} keys differ; missing={missing}, extra={extra}")


def verify_local() -> dict[str, Any]:
    marketplace = read_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    manifest = read_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
    claude_manifest = read_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json")
    mcp_config = read_json(PLUGIN_ROOT / ".mcp.json")
    parity = read_json(PLUGIN_ROOT / "parity.json")
    parity_schema = read_json(PLUGIN_ROOT / "parity.schema.json")
    release_state = read_json(PLUGIN_ROOT / "release-state.json")

    if release_state != EXPECTED_RELEASE_STATE:
        raise ValueError("release-state contract differs from the local unpublished boundary")

    if marketplace.get("name") != "crosstabs":
        raise ValueError("repository marketplace name must be crosstabs")
    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1:
        raise ValueError("repository marketplace must contain exactly one plugin")
    expected_entry = {
        "name": "crosstabs",
        "source": {"source": "local", "path": "./plugins/crosstabs"},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "category": "Data & Analytics",
    }
    if entries[0] != expected_entry:
        raise ValueError("repository marketplace entry metadata differs from the contract")

    for label, candidate_manifest in (
        ("Codex", manifest),
        ("Claude", claude_manifest),
    ):
        if candidate_manifest.get("name") != "crosstabs":
            raise ValueError(f"{label} manifest name differs")
        if candidate_manifest.get("version") != EXPECTED_PLUGIN_VERSION:
            raise ValueError(f"{label} manifest version differs")
        if candidate_manifest.get("repository") != "https://github.com/barangaroo/crosstabs-codex-plugin":
            raise ValueError(f"{label} manifest repository differs")
        if candidate_manifest.get("mcpServers") != "./.mcp.json":
            raise ValueError(f"{label} manifest must reference ./.mcp.json")
        if candidate_manifest.get("skills") != "./skills/":
            raise ValueError(f"{label} manifest must reference ./skills/")

    interface = manifest.get("interface", {})
    for asset_field in ("composerIcon", "logo"):
        asset = interface.get(asset_field)
        if not isinstance(asset, str) or not (PLUGIN_ROOT / asset).is_file():
            raise ValueError(f"missing interface asset {asset_field}")

    requirement = f"crosstabs=={EXPECTED_PACKAGE_VERSION}"
    def expected_server(entrypoint: str) -> dict[str, object]:
        return {
            "command": "uvx",
            "args": ["--from", requirement, entrypoint],
        }

    expected_servers = {
        "crosstabs-statistics": expected_server("crosstabs"),
        "crosstabs-headless": expected_server("crosstabs-headless"),
    }
    if mcp_config.get("mcpServers") != expected_servers:
        raise ValueError("MCP config does not expose both exact candidate commands")

    require_exact_keys(
        parity,
        {
            "$schema",
            "schemaVersion",
            "pluginVersion",
            "verifiedAt",
            "verificationScope",
            "distribution",
            "surfaces",
        },
        "parity contract",
    )
    distribution = parity.get("distribution", {})
    if not isinstance(distribution, dict):
        raise ValueError("parity distribution must be an object")
    require_exact_keys(
        distribution,
        {
            "package",
            "version",
            "requirement",
            "packagePublished",
            "transport",
            "toolCount",
            "headlessToolCount",
            "totalToolCount",
            "headlessTools",
            "headlessResourceTemplates",
            "resourceUris",
            "registryName",
            "registryRecord",
        },
        "parity distribution",
    )
    if parity.get("$schema") != "./parity.schema.json":
        raise ValueError("parity contract schema reference differs")
    if parity.get("schemaVersion") != 4:
        raise ValueError("parity contract schema version differs")
    if parity.get("pluginVersion") != EXPECTED_PLUGIN_VERSION:
        raise ValueError("parity plugin version differs")
    if parity.get("verificationScope") != "local_candidate":
        raise ValueError("parity verification scope must remain local")
    if distribution.get("package") != "crosstabs":
        raise ValueError("parity package name differs")
    if distribution.get("version") != EXPECTED_PACKAGE_VERSION:
        raise ValueError("parity package version differs")
    if distribution.get("requirement") != requirement:
        raise ValueError("parity package requirement is not exact")
    if distribution.get("packagePublished") is not False:
        raise ValueError("candidate package must remain explicitly unpublished")
    if distribution.get("transport") != "stdio":
        raise ValueError("plugin transport must be stdio")
    if distribution.get("toolCount") != EXPECTED_STATISTICS_TOOL_COUNT:
        raise ValueError("statistics tool count differs")
    if distribution.get("headlessTools") != EXPECTED_HEADLESS_TOOLS:
        raise ValueError("headless tool catalog does not match the exact local bundle")
    if distribution.get("headlessToolCount") != len(EXPECTED_HEADLESS_TOOLS):
        raise ValueError("headless tool count differs from the exact catalog")
    expected_total = EXPECTED_STATISTICS_TOOL_COUNT + len(EXPECTED_HEADLESS_TOOLS)
    if distribution.get("totalToolCount") != expected_total:
        raise ValueError("total tool count differs from both local servers")
    if distribution.get("headlessResourceTemplates") != [
        "crosstabs://artifacts/{artifactId}"
    ]:
        raise ValueError("headless artifact template differs")
    if distribution.get("resourceUris") != [
        "crosstabs://evidence/graph",
        "crosstabs://evidence/limitations",
    ]:
        raise ValueError("statistics evidence resources differ")
    if distribution.get("registryName") != EXPECTED_REGISTRY_NAME:
        raise ValueError("candidate Registry identity differs")
    if distribution.get("registryRecord") is not None:
        raise ValueError("unpublished package cannot claim a Registry record")

    datetime.fromisoformat(parity["verifiedAt"].replace("Z", "+00:00"))
    schema_properties = parity_schema.get("properties", {})
    expected_parity_keys = {
        "$schema",
        "schemaVersion",
        "pluginVersion",
        "verifiedAt",
        "verificationScope",
        "distribution",
        "surfaces",
    }
    if set(parity_schema.get("required", [])) != expected_parity_keys:
        raise ValueError("parity schema required fields differ")
    if parity_schema.get("additionalProperties") is not False:
        raise ValueError("parity schema must reject additional properties")
    schema_distribution_contract = schema_properties.get("distribution", {})
    schema_distribution = schema_distribution_contract.get("properties", {})
    if set(schema_distribution_contract.get("required", [])) != set(distribution):
        raise ValueError("parity distribution schema required fields differ")
    if schema_distribution_contract.get("additionalProperties") is not False:
        raise ValueError("parity distribution schema must reject additional properties")
    if schema_properties.get("$schema", {}).get("const") != "./parity.schema.json":
        raise ValueError("parity schema does not admit the instance schema reference")
    if schema_properties.get("schemaVersion", {}).get("const") != parity["schemaVersion"]:
        raise ValueError("parity schema does not pin its contract version")
    if schema_properties.get("pluginVersion", {}).get("const") != EXPECTED_PLUGIN_VERSION:
        raise ValueError("parity schema does not pin the plugin version")
    if schema_properties.get("verificationScope", {}).get("const") != "local_candidate":
        raise ValueError("parity schema does not pin local verification scope")
    if schema_distribution.get("version", {}).get("const") != EXPECTED_PACKAGE_VERSION:
        raise ValueError("parity schema does not pin the package version")
    if schema_distribution.get("packagePublished", {}).get("const") is not False:
        raise ValueError("parity schema does not pin unpublished package state")
    if schema_distribution.get("toolCount", {}).get("const") != EXPECTED_STATISTICS_TOOL_COUNT:
        raise ValueError("parity schema does not pin the statistics tool count")
    if schema_distribution.get("headlessToolCount", {}).get("const") != len(EXPECTED_HEADLESS_TOOLS):
        raise ValueError("parity schema does not pin the headless tool count")
    if schema_distribution.get("totalToolCount", {}).get("const") != expected_total:
        raise ValueError("parity schema does not pin the total tool count")
    if schema_distribution.get("headlessTools", {}).get("const") != EXPECTED_HEADLESS_TOOLS:
        raise ValueError("parity schema does not pin the exact headless catalog")
    if schema_distribution.get("registryName", {}).get("const") != EXPECTED_REGISTRY_NAME:
        raise ValueError("parity schema does not pin the Registry identity")
    if schema_distribution.get("registryRecord", {}).get("type") != "null":
        raise ValueError("parity schema does not prohibit a Registry-record claim")
    schema_surface = schema_properties.get("surfaces", {}).get("items", {})
    if set(schema_surface.get("required", [])) != {"id", "label", "status", "boundary"}:
        raise ValueError("parity surface schema required fields differ")
    if schema_surface.get("additionalProperties") is not False:
        raise ValueError("parity surface schema must reject additional properties")
    if set(schema_surface.get("properties", {}).get("status", {}).get("enum", [])) != {
        "local-candidate",
        "bounded",
    }:
        raise ValueError("parity surface schema statuses differ")

    surfaces = parity.get("surfaces")
    if not isinstance(surfaces, list):
        raise ValueError("parity contract surfaces must be an array")
    if [surface.get("id") for surface in surfaces] != EXPECTED_SURFACE_IDS:
        raise ValueError("parity surfaces differ from the local-only contract")
    for surface in surfaces:
        if not isinstance(surface, dict):
            raise ValueError("every parity surface must be an object")
        require_exact_keys(surface, {"id", "label", "status", "boundary"}, "parity surface")
        if surface.get("status") not in {"local-candidate", "bounded"}:
            raise ValueError(f"invalid local parity status for {surface.get('id')}")
        if not all(
            isinstance(surface.get(field), str) and surface[field]
            for field in ("id", "label", "boundary")
        ):
            raise ValueError("every parity surface needs id, label, and boundary")

    skill_path = PLUGIN_ROOT / "skills" / "analyze-survey-crosstabs" / "SKILL.md"
    skill = skill_path.read_text()
    if not re.match(
        r"^---\nname: analyze-survey-crosstabs\ndescription: .+\n---\n",
        skill,
    ):
        raise ValueError("skill frontmatter is missing or invalid")
    if "Product parity boundary" not in skill or "parity-and-limits.md" not in skill:
        raise ValueError("skill does not disclose the local parity boundary")
    if not (skill_path.parent / "../../parity.json").resolve().is_file():
        raise ValueError("skill parity-contract reference does not resolve")

    forbidden_fragments = [
        "\x63ode_open_ends",
        "\x72eview_themes",
        "\x61pprove_coding",
        "Vercel AI \x47ateway",
        "shared cloud \x72eview",
        "\x72emote connector",
        "\x68osted-MCP",
        "\x63ollaboration",
    ]
    claim_files = [
        ROOT / "README.md",
        PLUGIN_ROOT / ".codex-plugin" / "plugin.json",
        PLUGIN_ROOT / ".claude-plugin" / "plugin.json",
        PLUGIN_ROOT / "parity.json",
        PLUGIN_ROOT / "release-state.json",
        PLUGIN_ROOT / "skills" / "analyze-survey-crosstabs" / "SKILL.md",
        PLUGIN_ROOT
        / "skills"
        / "analyze-survey-crosstabs"
        / "references"
        / "parity-and-limits.md",
    ]
    for path in claim_files:
        content = path.read_text()
        found = [fragment for fragment in forbidden_fragments if fragment in content]
        if found:
            raise ValueError(
                f"{path.relative_to(ROOT)} contains removed claims: {', '.join(found)}"
            )

    placeholder_pattern = re.compile(r"\b(?:" + "TO" + "DO|FIX" + "ME)\b")
    placeholders = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in {".md", ".json", ".yaml", ".yml", ".py"}:
            continue
        if placeholder_pattern.search(path.read_text(errors="replace")):
            placeholders.append(str(path.relative_to(ROOT)))
    if placeholders:
        raise ValueError(f"unresolved placeholders: {', '.join(placeholders)}")

    readme = (ROOT / "README.md").read_text()
    for statement in (
        "local plugin candidate `0.2.5`",
        "unpublished package candidate `crosstabs==1.2.0`",
        "exactly 21 deterministic project-workflow tools",
        "Together the two servers declare 60 tools.",
        "no Registry record in this candidate",
        "Do not install or promote this repository as part of local candidate validation.",
    ):
        if statement not in readme:
            raise ValueError("README does not preserve the local unpublished boundary")

    return {
        "candidateState": release_state["candidate"]["state"],
        "pluginVersion": manifest["version"],
        "packageVersion": EXPECTED_PACKAGE_VERSION,
        "packagePublished": False,
        "registryName": EXPECTED_REGISTRY_NAME,
        "registryRecord": None,
        "statisticsToolCount": EXPECTED_STATISTICS_TOOL_COUNT,
        "headlessToolCount": len(EXPECTED_HEADLESS_TOOLS),
        "totalToolCount": expected_total,
        "surfaceCount": len(surfaces),
    }


def main() -> None:
    argparse.ArgumentParser(
        description="Validate the local unpublished plugin candidate."
    ).parse_args()
    result = {"local": verify_local(), "status": "passed"}
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
