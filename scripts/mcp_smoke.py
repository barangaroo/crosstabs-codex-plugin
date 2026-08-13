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
    server = mcp_config["mcpServers"]["crosstabs"]
    expected = parity["distribution"]

    parameters = StdioServerParameters(
        command=server["command"],
        args=server["args"],
    )
    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            initialized = await session.initialize()
            tools = await session.list_tools()
            resources = await session.list_resources()

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

    return {
        "serverName": initialized.server_info.name,
        "serverVersion": initialized.server_info.version,
        "toolCount": len(tools.tools),
        "resourceUris": actual_resource_uris,
        "status": "passed",
    }


if __name__ == "__main__":
    print(json.dumps(asyncio.run(smoke()), sort_keys=True))
