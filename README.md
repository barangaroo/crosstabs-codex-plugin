# Crosstabs for Codex

Run auditable survey crosstabs and 39 local statistical tools from Codex. The plugin installs `crosstabs==1.0.4` on demand with `uvx`, exposes two evidence resources, and adds a workflow for assumption-aware categorical analysis.

This is the official public Codex marketplace for Crosstabs. Version 0.1.0 has verified numerical parity with the published MCP surface; it does not claim browser-workspace workflow parity.

## Install

```bash
codex plugin marketplace add barangaroo/crosstabs-codex-plugin --ref main
codex plugin add crosstabs@crosstabs
```

Start a new Codex task after installation, then ask:

> Analyze this survey file and build evidence-linked crosstabs.

The plugin requires `uv`/`uvx` and Python 3.10 or newer. Statistical calculations run locally over stdio. The browser application's project, weighting, report-refresh, open-end coding, wave, and collaboration workflows are not claimed as plugin v0.1 capabilities.

## Verified release surface

- Codex plugin: `0.1.0`.
- Python/MCP package: immutable `crosstabs==1.0.4`.
- Official MCP Registry: `io.github.barangaroo/crosstabs` 1.0.4, active/latest.
- MCP handshake: 39 tools and two evidence resources over local stdio.
- Machine-readable boundary: [`plugins/crosstabs/parity.json`](plugins/crosstabs/parity.json).

Every push and pull request checks the manifests, exact package requirement, parity contract, PyPI record, official MCP Registry record, and a live stdio handshake.

- Product: https://www.crosstabs.com/
- MCP documentation: https://www.crosstabs.com/mcp
- PyPI: https://pypi.org/project/crosstabs/1.0.4/
- Privacy: https://www.crosstabs.com/privacy
