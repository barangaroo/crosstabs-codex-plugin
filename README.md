# Crosstabs for Codex and Claude Code

This repository contains source release `0.2.5`, identified by GitHub tag `v0.2.5`. It pins `crosstabs==1.2.1` for local execution. Source publication does not imply directory submission, approval, or listing.

The plugin declares two on-device stdio MCP servers:

- `crosstabs-headless`: exactly 29 deterministic project-workflow tools for local files, project handoff, approved dictionary edits, guarded transformations, design-aware methods, canonical aggregate widgets, tabulation, reports, and audit history.
- `crosstabs-statistics`: 39 focused statistical tools plus two local evidence resources.

Together the two servers declare 68 tools. The 29-tool headless catalog is recorded exactly in [`plugins/crosstabs/parity.json`](plugins/crosstabs/parity.json). Package publication and Registry status are recorded separately from source publication in [`release-state.json`](plugins/crosstabs/release-state.json). Both provider-directory submission, approval, and listing states remain false.

## Local execution boundary

- Plugin version: `0.2.5`.
- Exact package requirement: `crosstabs==1.2.1`.
- Transport: local stdio only.
- Runtime: Python 3.10 or newer and Node.js 22 or newer.
- Project files, respondent rows, project state, calculations, and generated reports remain in the user-controlled local process and filesystem.
- The declared Registry identity is `io.github.crosstabs/crosstabs`; no Registry record is claimed without separate evidence.
- The historical public plugin `0.2.3` remains recorded separately in [`plugins/crosstabs/release-state.json`](plugins/crosstabs/release-state.json).

The exact `uvx` commands are present in [`plugins/crosstabs/.mcp.json`](plugins/crosstabs/.mcp.json). Installation requires the exact package to be published and independently verified; check `sourceRelease.packagePublished` before use.

## Install the source release

After the tag and exact package are public, add the GitHub-backed Codex marketplace:

```bash
codex plugin marketplace add barangaroo/crosstabs-codex-plugin --ref v0.2.5
codex plugin add crosstabs@crosstabs
```

For Claude Code, load the tagged source directly without a directory listing:

```bash
git clone --branch v0.2.5 --depth 1 https://github.com/barangaroo/crosstabs-codex-plugin.git
claude --plugin-dir ./crosstabs-codex-plugin/plugins/crosstabs
```

These are opt-in local loading paths, not an official directory listing. The
[OpenAI submission guide](https://developers.openai.com/plugins/guides/submit-claude-plugin)
currently does not support local stdio-only MCP plugins; do not move private
project workflows to a public endpoint to bypass that restriction. A separate
[Claude directory submission](https://claude.com/docs/plugins/submit) requires an
authorized Console or organization session and a retained submission receipt.

The local JSON store enforces 8 MiB per serialized project
(including audit and undo) and 32 MiB per combined database (including replay).
Capacity rejection preserves the original database. A disposable four-project
fixture with 3,200 rows, 12 columns, and one full undo snapshot per project
exercised import, save, reload, and analysis at 33,308,653 database bytes (99.3%
of the file cap). This is a bounded fixture, not a maximum row count or a memory
or compute guarantee. Parser admission ceilings do not override persistence
limits. Release verification must use the exact packaged artifact.

## Local validation

Run the source-only verifier:

```bash
python3 scripts/verify_plugin.py
```

Validate the shared Claude Code package structure when the Claude CLI is available:

```bash
npx --yes @anthropic-ai/claude-code@2.1.201 plugin validate --strict plugins/crosstabs
```

Run the exact packaged servers after PyPI publication:

```bash
uv run --isolated --python 3.12 --with "mcp==1.29.0" --with "packaging==26.2" python scripts/mcp_smoke.py
```

For a source-only headless check without resolving the package:

```bash
uv run --isolated --python 3.12 --with "mcp==1.29.0" --with "packaging==26.2" \
  python scripts/mcp_smoke.py \
  --headless-bundle ../crosstabs-lite/mcp-server-python/crosstabs_mcp/headless-mcp.mjs
```

The Codex and Claude manifests reuse the same `skills/` tree and `.mcp.json`; there is no second behavior fork.
