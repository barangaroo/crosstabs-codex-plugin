# Crosstabs for Codex and Claude Code

This repository contains local plugin candidate `0.2.5`. It pins the unpublished package candidate `crosstabs==1.2.0` and is not an installable public release.

The candidate declares two on-device stdio MCP servers:

- `crosstabs-headless`: exactly 21 deterministic project-workflow tools for local files, versioned projects, tabulation, approved survey designs, tracker repair, editable report packs, export, and audit history.
- `crosstabs-statistics`: 39 focused statistical tools plus two local evidence resources.

Together the two servers declare 60 tools. The 21-tool headless catalog is recorded exactly in [`plugins/crosstabs/parity.json`](plugins/crosstabs/parity.json). The package pin is intentionally unpublished, and no package-index, Registry-record, marketplace, directory-review, approval, or availability claim is made for this candidate.

## Local candidate boundary

- Plugin version: `0.2.5`.
- Exact package requirement: `crosstabs==1.2.0`.
- Transport: local stdio only.
- Runtime: Python 3.10 or newer and Node.js 22 or newer.
- Project files, respondent rows, project state, calculations, and generated reports remain in the user-controlled local process and filesystem.
- The declared Registry identity is `io.github.crosstabs/crosstabs`; `1.2.0` has no Registry record in this candidate.
- The historical public plugin boundary is recorded separately in [`plugins/crosstabs/release-state.json`](plugins/crosstabs/release-state.json) and must not be confused with this candidate.

The exact `uvx` commands are present in [`plugins/crosstabs/.mcp.json`](plugins/crosstabs/.mcp.json) for package parity, but they cannot substantiate this candidate until `crosstabs==1.2.0` is independently published. Do not install or promote this repository as part of local candidate validation.

Publication is also held until the headless server's single-file project store
has a measured end-to-end persistence and execution envelope or enforces a
lower project limit. The parser's 50 MiB, 1,000,000-row, and 20,000,000-cell
admission ceilings are not a promise that projects at those maxima can be
safely saved, reloaded, and analyzed.

## Local validation

Run the source-only verifier:

```bash
python3 scripts/verify_plugin.py
```

Validate the shared Claude Code package structure when the Claude CLI is available:

```bash
npx --yes @anthropic-ai/claude-code@2.1.201 plugin validate --strict plugins/crosstabs
```

Smoke the headless contract against a locally built product bundle without resolving the unpublished package:

```bash
uv run --isolated --python 3.12 --with "mcp>=1.0.0" \
  python scripts/mcp_smoke.py \
  --headless-bundle ../crosstabs-lite/mcp-server-python/crosstabs_mcp/headless-mcp.mjs
```

The Codex and Claude manifests reuse the same `skills/` tree and `.mcp.json`; there is no second behavior fork.
