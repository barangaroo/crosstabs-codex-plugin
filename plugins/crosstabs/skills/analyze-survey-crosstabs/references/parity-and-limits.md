# Plugin parity and limits

## Current verified surface

- PyPI package: `crosstabs==1.1.6`, Python 3.10+, Node.js 20+ for the bundled headless server.
- Transport: local MCP over stdio through `uvx`.
- Numerical tools: 39 registered tools.
- Project tools: exactly 23 registered operations, from `create_project` through `get_audit_history`.
- Evidence resources: `crosstabs://evidence/graph` and `crosstabs://evidence/limitations`.
- Input helpers: bounded records or CSV to a simple two-variable crosstab.
- Inference labels: exact, asymptotic, or simulated where applicable.
- Provenance: PyPI Trusted Publishing from `barangaroo/crosstabs-lite/.github/workflows/release-python-mcp.yml`.

The bundled headless server and browser workspace share the TypeScript `TabBookProject` schema, initial-analysis policy, statistical kernels, and several project-domain modules. They do not yet use one orchestration service; full revision, audit, undo, and artifact-behavior parity remains a release gate. The focused Python statistical server remains a separate numerical implementation covered by overlapping regression fixtures and public reference cases.

## Project workflows exposed by plugin v0.2

- Local CSV, TSV, XLSX, SAV, and inline-record import with profiling and versioned waves.
- Saved filters, row sets, weights, multibanners, category order, table order, and export recipes.
- Crosstabs and tab books with bases, percentages, significance letters, warnings, and evidence.
- Project portability, dataset replacement, schema-drift preview and approved repair, and wave comparison.
- Open-end theme proposals, review, approval, auditable variables, and guarded undo.
- Editable PPTX/DOCX generation, refresh, and manual-edit preservation for supported anchored regions.
- Project inspection, paginated audit history, definition-only export by default, and explicitly authorized full-data export.

## Separate browser or remote surfaces

- Browser navigation, visual table editing, and browser-only interaction state.
- Aggregate share links, shared cloud review, comments, and connector authorization.
- The public remote connector exposes evidence and deterministic aggregate calculators only; it has no raw-file or respondent-row tool.
- `code_open_ends` is the only local generative operation and requires explicit Vercel AI Gateway external-processing approval.

For separate browser or collaboration requests, use `https://www.crosstabs.com/workspace`. Never imply that an unavailable MCP operation ran.

## Statistical boundaries

- Association and prediction do not establish causality.
- Pearson chi-square and G-test p-values are asymptotic.
- Fisher's exact test is restricted to eligible unweighted 2×2 integer-frequency tables.
- Weighted inference is approximate unless weights are genuine frequency weights; complex-survey variance is not implemented.
- Cellwise residual and column-comparison flags need multiplicity and base-size judgment.
- Published capacity fixtures are tested envelopes, not an unlimited-row guarantee.
- Named independent statistical review remains pending until public review evidence is recorded.

Canonical evidence: `https://www.crosstabs.com/evidence.json`.
Full machine-readable reference: `https://www.crosstabs.com/llms-full.txt`.
Plugin parity contract: `../../../parity.json`.
