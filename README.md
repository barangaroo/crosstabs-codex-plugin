# Crosstabs for Codex

Complete auditable survey projects from Codex. The plugin installs `crosstabs==1.1.6` on demand with `uvx` and exposes two local MCP servers: 23 end-to-end project operations plus 39 focused statistical tools and versioned evidence resources.

Version 0.2.4 is a local release candidate, not the current public Codex marketplace release. It is prepared to pin `crosstabs==1.1.6` and the `io.github.crosstabs/crosstabs` Registry identity after publication. The currently published marketplace release remains 0.2.3, which pins `crosstabs==1.1.3` and the legacy `io.github.barangaroo/crosstabs` identity. Version 0.2.4 shares the workspace project schema, initial-analysis policy, deterministic statistical kernels, and several project-domain modules. Browser and headless orchestration services are still separate, so full revision, audit, undo, artifact, shared-review, comment, and connector-authorization parity remains explicitly release-gated.

## Install

```bash
codex plugin marketplace add barangaroo/crosstabs-codex-plugin --ref main
codex plugin add crosstabs@crosstabs
```

`--ref main` installs the development/candidate marketplace source; it is not
an immutable reference for reproducing the public 0.2.3 marketplace artifact.

Start a new Codex task after installation, then ask:

> Analyze this survey file and build evidence-linked crosstabs.

The plugin requires `uv`/`uvx`, Python 3.10 or newer, and Node.js 20 or newer for the bundled headless server. Respondent files, projects, calculations, and report generation run locally over stdio. Only `code_open_ends` can invoke Vercel AI Gateway, and it requires explicit external-processing approval.

## Claude Code candidate

The same candidate root now contains a separate
[`plugins/crosstabs/.claude-plugin/plugin.json`](plugins/crosstabs/.claude-plugin/plugin.json)
for Claude Code. It reuses the exact `skills/` tree and `.mcp.json` package pins
instead of maintaining a second behavior fork. Validate or load it locally with:

```bash
npx --yes @anthropic-ai/claude-code@2.1.201 plugin validate --strict plugins/crosstabs
claude --plugin-dir ./plugins/crosstabs
```

This Claude package is an unpublished local candidate. It has not been
submitted to, approved by, or published in Anthropic's plugin directory. The
remote Claude Connector is a separate hosted-MCP submission path.

## Candidate surface (not a public release)

- Candidate Codex plugin: `0.2.4`, unpublished.
- Candidate Python/MCP pin: immutable `crosstabs==1.1.6`.
- Candidate Registry pin: `io.github.crosstabs/crosstabs` 1.1.6, active/latest.
- Current public marketplace artifact: plugin `0.2.3`, `crosstabs==1.1.3`, and `io.github.barangaroo/crosstabs`.
- MCP handshakes: exactly 23 headless workflow tools; 39 statistical tools and two evidence resources over local stdio.
- Machine-readable candidate boundary: [`plugins/crosstabs/parity.json`](plugins/crosstabs/parity.json) and [`plugins/crosstabs/release-state.json`](plugins/crosstabs/release-state.json).

Every push and pull request checks the candidate manifests, exact package requirement, parity contract, PyPI record, official MCP Registry record, and a live stdio handshake. Publication additionally requires committing the candidate and publishing an immutable public marketplace release reference.

- Product: https://www.crosstabs.com/
- MCP documentation: https://www.crosstabs.com/mcp
- Agent product: https://ai.crosstabs.com/
- Remote aggregate MCP: https://mcp.crosstabs.com/mcp
- PyPI: https://pypi.org/project/crosstabs/1.1.6/
- Privacy: https://www.crosstabs.com/privacy
