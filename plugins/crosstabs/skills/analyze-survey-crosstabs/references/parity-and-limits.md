# Plugin parity and limits

## Public source release surface

- Plugin source release: `0.3.0`, GitHub tag `v0.3.0`; the exact public 1.3.0 package passed fresh checks of both servers and their runtime status. Registry publication is a separate gate.
- Exact package pin: `crosstabs==1.3.0`; publication evidence is recorded in `../../../release-state.json` separately from the source tag.
- Runtime: Python 3.10+ and Node.js 22+ for the bundled headless server.
- Transport: local MCP over stdio.
- Numerical server: 40 registrations: 39 analytical tools plus runtime status, and two evidence resources.
- Project server: exactly 33 deterministic tools, from project handoff and data import through approved dictionary edits, guarded transformations, design-aware methods, canonical widgets, reports, export, and audit history.
- Total registrations across both servers: 73 (72 distinct names).
- Package Registry identity: `io.github.crosstabs/crosstabs`; no 1.3.0 Registry record is claimed. Historical plugin 0.2.6/package 1.2.2 evidence is retained separately in the release-state file.

The 33-tool project catalog and both MCP commands are machine-readable in `../../../parity.json` and `../../../.mcp.json`. Release validation runs both exact packaged MCP commands. A local-bundle-only check does not prove package publication. Neither check proves directory submission, approval, or listing.

The local JSON store enforces 8 MiB per serialized project including audit/undo
and 32 MiB per combined database including replay. Writes exceeding either
limit fail closed without changing the original database. A disposable fixture
of four projects, each with 3,200 rows, 12 columns, 65-byte categorical cells,
and one full undo snapshot, exercised import/save/reload/analysis at 33,308,653
database bytes and 7,962,576 bytes per project. These measurements are fixture
evidence, not a row-count, memory, or compute guarantee. Exact release artifacts
must repeat the capacity verification before publication.

## Project workflows exposed by plugin 0.3.0

- Local CSV, TSV, XLSX, SAV, and inline-record import with profiling and versioned waves.
- Verified full-data project-package import into a new local copy, without trusting source audit history or overwriting an existing destination.
- Explicitly approved dictionary edits and proposal/review/apply/undo transformations with revision and replay guards.
- Saved filters, row sets, weights, approved survey designs, multibanners, category order, table order, and export recipes.
- Crosstabs and tab books with bases, percentages, significance letters, warnings, complex-sample diagnostics where supported, and evidence metadata.
- Design-aware OLS, logistic, and K-means methods within their supported design boundaries, and canonical aggregate widgets bound to project revision and evidence ID.
- Project portability, dataset replacement, schema-drift preview and approved repair, and wave comparison.
- Editable PPTX/DOCX generation and non-overwriting refresh for supported generated regions.
- Project inspection, paginated audit history, definition-only export by default, and explicitly authorized full-data export.

- Runtime identity and expected-package comparison on both servers; no plugin-version inference.
- Portable ordinary-table analysis plans with readable settings, strict revision/data/definition binding, preflight validation, bounded execution and aggregate review findings. Plans do not mutate project state or save themselves; complex-survey plans remain unsupported.

## Operations outside the plugin catalog

- Visual navigation, direct table editing, and interface interaction state.
- Unlisted project mutations or filesystem access outside the configured local roots.
- Any operation that transfers respondent rows or project state out of the local process.

Never imply that an operation absent from the exact 33-tool catalog ran.

## Statistical boundaries

- Association and prediction do not establish causality.
- Pearson chi-square and G-test p-values are asymptotic.
- Fisher's exact test is restricted to eligible unweighted 2×2 integer-frequency tables.
- Ordinary weighted inference is approximate unless weights are genuine frequency weights.
- Complex-sample inference requires an explicit approved survey design and supported Taylor or replicate-weight configuration; unsupported settings fail closed.
- Cellwise residual and column-comparison flags need multiplicity and base-size judgment.
- Tested capacity fixtures are bounded envelopes, not an unlimited-row guarantee.
- The enforced persistence byte caps include nested metadata, rows, audit,
  undo, and replay as applicable; there is no universal persisted row/cell
  maximum. Do not extrapolate parser admission limits to persistence.

Plugin parity contract: `../../../parity.json`.
