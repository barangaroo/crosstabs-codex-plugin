# Crosstabs for Codex

Complete auditable survey projects from Codex. The plugin installs `crosstabs==1.1.3` on demand with `uvx` and exposes two local MCP servers: 23 end-to-end project operations plus 39 focused statistical tools and versioned evidence resources.

This is the official public Codex marketplace for Crosstabs. Version 0.2.3 shares the workspace project schema, initial-analysis policy, deterministic statistical kernels, and several project-domain modules. Browser and headless orchestration services are still separate, so full revision, audit, undo, artifact, shared-review, comment, and connector-authorization parity remains explicitly release-gated.

## Install

```bash
codex plugin marketplace add barangaroo/crosstabs-codex-plugin --ref main
codex plugin add crosstabs@crosstabs
```

Start a new Codex task after installation, then ask:

> Analyze this survey file and build evidence-linked crosstabs.

The plugin requires `uv`/`uvx`, Python 3.10 or newer, and Node.js 20 or newer for the bundled headless server. Respondent files, projects, calculations, and report generation run locally over stdio. Only `code_open_ends` can invoke Vercel AI Gateway, and it requires explicit external-processing approval.

## Verified release surface

- Codex plugin: `0.2.3`.
- Python/MCP package: immutable `crosstabs==1.1.3`.
- Official MCP Registry: `io.github.barangaroo/crosstabs` 1.1.3, active/latest.
- MCP handshakes: exactly 23 headless workflow tools; 39 statistical tools and two evidence resources over local stdio.
- Machine-readable boundary: [`plugins/crosstabs/parity.json`](plugins/crosstabs/parity.json).

Every push and pull request checks the manifests, exact package requirement, parity contract, PyPI record, official MCP Registry record, and a live stdio handshake.

- Product: https://www.crosstabs.com/
- MCP documentation: https://www.crosstabs.com/mcp
- Agent product: https://ai.crosstabs.com/
- Remote aggregate MCP: https://mcp.crosstabs.com/mcp
- PyPI: https://pypi.org/project/crosstabs/1.1.3/
- Privacy: https://www.crosstabs.com/privacy
