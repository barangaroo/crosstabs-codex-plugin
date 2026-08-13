# Plugin parity and limits

## Current verified surface

- PyPI package: `crosstabs==1.0.4`, Python 3.10+.
- Transport: local MCP over stdio through `uvx`.
- Numerical tools: 39 registered tools.
- Evidence resources: `crosstabs://evidence/graph` and `crosstabs://evidence/limitations`.
- Input helpers: bounded records or CSV to a simple two-variable crosstab.
- Inference labels: exact, asymptotic, or simulated where applicable.
- Provenance: PyPI Trusted Publishing from `barangaroo/crosstabs-lite/.github/workflows/release-python-mcp.yml`.

The Python package and browser application are separate implementations. Regression fixtures cover overlapping headline measures and public reference cases, but a shared source kernel does not make every application result automatically identical.

## Browser workflows not exposed by plugin v0.1

- XLSX/SAV import UI and type-detection workflow.
- Saved filters, row sets, weights, multibanners, category order, and export recipes.
- Column-proportion significance letters and multiple-response-set workflow.
- Tab-book persistence, project portability, replace/refresh, schema repair, and waves.
- Open-end theme coding and approval history.
- Editable PPTX/DOCX generation, refresh, and manual-edit preservation.
- Aggregate share links, cloud review, comments, and connector authorization.
- Vercel AI Gateway analysis and application activation analytics.

For these requests, use the browser workspace at `https://www.crosstabs.com/workspace` or perform a clearly documented local workflow with other available Codex tools. Never imply that an unavailable MCP operation ran.

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
