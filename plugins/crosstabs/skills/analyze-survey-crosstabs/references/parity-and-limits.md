# Plugin parity and limits

## Current local candidate surface

- Plugin candidate: `0.2.5`, unpublished.
- Exact package candidate: `crosstabs==1.2.0`, unpublished.
- Runtime: Python 3.10+ and Node.js 22+ for the bundled headless server.
- Transport: local MCP over stdio.
- Numerical server: 39 focused statistical tools and two evidence resources.
- Project server: exactly 21 deterministic tools, from project creation and data import through approved survey designs, reports, export, and audit history.
- Total declared tool count across both servers: 60.
- Package Registry identity: `io.github.crosstabs/crosstabs`; no `1.2.0` Registry record is claimed.

The 21-tool project catalog and both MCP commands are machine-readable in `../../../parity.json` and `../../../.mcp.json`. Candidate validation uses the current locally built headless bundle so it does not resolve the unpublished package pin.

Publication is held until the current single-file project store has a measured
end-to-end persistence and execution envelope or enforces a lower project
limit. Parser admission ceilings are not a guarantee that a maximum-size
project can be saved, reloaded, and analyzed.

## Project workflows exposed by plugin 0.2.5

- Local CSV, TSV, XLSX, SAV, and inline-record import with profiling and versioned waves.
- Saved filters, row sets, weights, approved survey designs, multibanners, category order, table order, and export recipes.
- Crosstabs and tab books with bases, percentages, significance letters, warnings, complex-sample diagnostics where supported, and evidence metadata.
- Project portability, dataset replacement, schema-drift preview and approved repair, and wave comparison.
- Editable PPTX/DOCX generation and non-overwriting refresh for supported generated regions.
- Project inspection, paginated audit history, definition-only export by default, and explicitly authorized full-data export.

## Operations outside the plugin catalog

- Visual navigation, direct table editing, and interface interaction state.
- Unlisted project mutations or filesystem access outside the configured local roots.
- Any operation that transfers respondent rows or project state out of the local process.

Never imply that an operation absent from the exact 21-tool catalog ran.

## Statistical boundaries

- Association and prediction do not establish causality.
- Pearson chi-square and G-test p-values are asymptotic.
- Fisher's exact test is restricted to eligible unweighted 2×2 integer-frequency tables.
- Ordinary weighted inference is approximate unless weights are genuine frequency weights.
- Complex-sample inference requires an explicit approved survey design and supported Taylor or replicate-weight configuration; unsupported settings fail closed.
- Cellwise residual and column-comparison flags need multiplicity and base-size judgment.
- Tested capacity fixtures are bounded envelopes, not an unlimited-row guarantee.
- The unpublished candidate has no established maximum for persisted project
  rows/cells; do not extrapolate parser admission limits to persistence.

Plugin parity contract: `../../../parity.json`.
