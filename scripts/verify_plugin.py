#!/usr/bin/env python3
"""Fail-closed source-release validation, independent of directory listing."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "crosstabs"
EXPECTED_PLUGIN_VERSION = "0.3.0"
EXPECTED_PACKAGE_VERSION = "1.3.0"
EXPECTED_PACKAGE_PUBLISHED = True
EXPECTED_REGISTRY_NAME = "io.github.crosstabs/crosstabs"
REGISTRY_RECORD_URL = "https://registry.modelcontextprotocol.io/v0.1/servers/io.github.crosstabs%2Fcrosstabs/versions/1.3.0"
EXPECTED_REGISTRY_RECORD: str | None = None
EXPECTED_STATISTICS_TOOL_COUNT = 40
EXPECTED_HEADLESS_TOOLS = [
    "get_runtime_status",
    "create_analysis_plan",
    "validate_analysis_plan",
    "run_analysis_plan",
    "create_project",
    "import_project",
    "import_dataset",
    "profile_dataset",
    "define_row_set",
    "define_banner",
    "apply_filter",
    "set_weight",
    "run_table",
    "render_project_table",
    "update_variable_metadata",
    "propose_transformation",
    "review_transformation",
    "apply_transformation",
    "undo_transformation",
    "run_complex_survey_method",
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
    "schemaVersion": 3,
    "sourceRelease": {
        "sourceState": "public_source_release",
        "packagePublished": EXPECTED_PACKAGE_PUBLISHED,
        "registryPublished": EXPECTED_REGISTRY_RECORD is not None,
        "pluginVersion": EXPECTED_PLUGIN_VERSION,
        "packageVersion": EXPECTED_PACKAGE_VERSION,
        "registryName": EXPECTED_REGISTRY_NAME,
        "registryRecord": EXPECTED_REGISTRY_RECORD,
        "tag": "v0.3.0",
        "sourceReference": "https://github.com/barangaroo/crosstabs-codex-plugin/tree/v0.3.0",
        "verificationScope": "public_source_release",
    },
    "previousSourceRelease": {
        "sourceState": "public_source_release",
        "packagePublished": True,
        "registryPublished": True,
        "pluginVersion": "0.2.6",
        "packageVersion": "1.2.2",
        "registryName": "io.github.crosstabs/crosstabs",
        "registryRecord": "https://registry.modelcontextprotocol.io/v0.1/servers/io.github.crosstabs%2Fcrosstabs/versions/1.2.2",
        "tag": "v0.2.6",
        "sourceReference": "https://github.com/barangaroo/crosstabs-codex-plugin/tree/v0.2.6",
        "verificationScope": "public_source_release"
    },
    "historicalPublicRelease": {
        "state": "published_marketplace_release",
        "published": True,
        "pluginVersion": "0.2.3",
        "packageVersion": "1.1.3",
        "registryName": "io.github.barangaroo/crosstabs",
        "immutableReference": None,
    },
    "directoryStatus": {
        "openai": {"submitted": False, "approved": False, "listed": False},
        "claude": {"submitted": False, "approved": False, "listed": False},
    },
    "promotionRequirements": [
        "Retain an exact Registry record before claiming Registry publication.",
        "Retain provider submission receipts, approval evidence, and live listings before changing directory states; local stdio is not supported by the OpenAI submission portal.",
        "Verify the public tag resolves to the recorded source SHA and repeat strict host validation and both MCP smoke checks against exact public artifacts.",
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


def verify_registry_publication(published: bool, record: str | None) -> None:
    if (published is True and record == REGISTRY_RECORD_URL) or (published is False and record is None):
        return
    raise ValueError("Registry publication must bind the exact versioned record, independently of directory status")


def verify_release_state(state: dict[str, Any]) -> None:
    if state != EXPECTED_RELEASE_STATE:
        raise ValueError("release-state differs from the public source and separate directory contract")
    release = state["sourceRelease"]
    verify_registry_publication(release["registryPublished"], release["registryRecord"])


def verify_local() -> dict[str, Any]:
    marketplace = read_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    manifest = read_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
    claude_manifest = read_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json")
    mcp_config = read_json(PLUGIN_ROOT / ".mcp.json")
    parity = read_json(PLUGIN_ROOT / "parity.json")
    parity_schema = read_json(PLUGIN_ROOT / "parity.schema.json")
    release_state = read_json(PLUGIN_ROOT / "release-state.json")

    verify_release_state(release_state)

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
    if parity.get("verificationScope") != "public_source_release":
        raise ValueError("parity verification scope must describe the local candidate")
    if distribution.get("package") != "crosstabs":
        raise ValueError("parity package name differs")
    if distribution.get("version") != EXPECTED_PACKAGE_VERSION:
        raise ValueError("parity package version differs")
    if distribution.get("requirement") != requirement:
        raise ValueError("parity package requirement is not exact")
    if distribution.get("packagePublished") is not EXPECTED_PACKAGE_PUBLISHED:
        raise ValueError("package publication state differs from verified release evidence")
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
    if distribution.get("registryRecord") != EXPECTED_REGISTRY_RECORD:
        raise ValueError("Registry record differs from verified release evidence")

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
    if schema_properties.get("verificationScope", {}).get("const") != "public_source_release":
        raise ValueError("parity schema does not pin candidate verification scope")
    if schema_distribution.get("version", {}).get("const") != EXPECTED_PACKAGE_VERSION:
        raise ValueError("parity schema does not pin the package version")
    if schema_distribution.get("packagePublished", {}).get("const") is not EXPECTED_PACKAGE_PUBLISHED:
        raise ValueError("parity schema does not pin verified package state")
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
    if schema_distribution.get("registryRecord") != {"const": EXPECTED_REGISTRY_RECORD}:
        raise ValueError("parity schema does not pin the verified Registry state")
    schema_surface = schema_properties.get("surfaces", {}).get("items", {})
    if set(schema_surface.get("required", [])) != {"id", "label", "status", "boundary"}:
        raise ValueError("parity surface schema required fields differ")
    if schema_surface.get("additionalProperties") is not False:
        raise ValueError("parity surface schema must reject additional properties")
    if set(schema_surface.get("properties", {}).get("status", {}).get("enum", [])) != {
        "public-source",
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
        if surface.get("status") not in {"public-source", "bounded"}:
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
        "source release `0.3.0`",
        "crosstabs==1.3.0",
        "exactly 33 deterministic project-workflow tools",
        "Together the two servers declare 73 tool registrations.",
        "does not imply directory submission, approval, or listing",
        "--ref v0.3.0",
    ):
        if statement not in readme:
            raise ValueError("README does not preserve the source release and directory boundary")

    return {
        "sourceState": release_state["sourceRelease"]["sourceState"],
        "pluginVersion": manifest["version"],
        "packageVersion": EXPECTED_PACKAGE_VERSION,
        "packagePublished": EXPECTED_PACKAGE_PUBLISHED,
        "registryName": EXPECTED_REGISTRY_NAME,
        "registryRecord": EXPECTED_REGISTRY_RECORD,
        "statisticsToolCount": EXPECTED_STATISTICS_TOOL_COUNT,
        "headlessToolCount": len(EXPECTED_HEADLESS_TOOLS),
        "totalToolCount": expected_total,
        "surfaceCount": len(surfaces),
    }


def main() -> None:
    argparse.ArgumentParser(
        description="Validate the public source release contract without implying directory approval."
    ).parse_args()
    result = {"local": verify_local(), "status": "passed"}
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
