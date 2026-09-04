---
name: analyze-survey-crosstabs
description: Build, test, audit, and explain crosstabs for categorical or survey data with the local Crosstabs MCP tools. Use for CSV/XLSX/SAV survey files, contingency tables, chi-square or Fisher test selection, effect sizes, sparse cells, residuals, multiple comparisons, ordinal association, agreement, epidemiology tables, power analysis, and evidence-linked statistical reporting.
---

# Analyze Survey Crosstabs

Use `crosstabs-headless` for end-to-end local research projects and `crosstabs-statistics` for focused numerical claims. Keep every conclusion tied to its project revision, table, base, method, assumptions, evidence, and limitations.

## Workflow

1. Inspect the supplied data before choosing tests. Do not replace it with sample data. For a durable job, call `create_project`, `import_dataset`, then `profile_dataset`. Use `import_project` for a verified full-data package handoff into a new local copy; source audit entries are not trusted local history.
2. State the unit of analysis, missing-value policy, row and column variables, category order, weight meaning, and whether any question is multiple-response.
3. Define reusable row sets, multibanners, filters, and weights inside the project. Inspect the current revision before each mutation and pass its `expectedRevision` and a unique idempotency key. Use `update_variable_metadata` only with explicit approval. For derived data, use `propose_transformation`, `review_transformation`, and `apply_transformation`; retain the guarded `undo_transformation` path.
4. When the sample design affects variance, define the approved strata, primary sampling unit, finite-population correction, or replicate-weight design before interpreting inference. Never substitute an ordinary weighted table for a complex-sample analysis.
5. Run a table before the full tab book. Check bases, sparse-cell warnings, significance policy, weighting limitations, design degrees of freedom, and evidence IDs. Use `render_project_table` only for canonical aggregate evidence from the same project revision and evidence ID.
6. Use `run_complex_survey_method` for supported design-aware OLS, logistic, or K-means work; preserve its design and method limitations. Use the focused statistics server for other supported numerical claims. Run `check_assumptions` and `recommend_test` before inferential interpretation, then an appropriate effect size.
7. For tracker replacements, run `detect_schema_drift`, review the repair plan, and apply only explicitly approved repair operation IDs. Preserve the prior wave and guarded inverse.
8. Generate editable PPTX/DOCX packs from stable table IDs. For refresh, provide the manually edited source package and a new output path; never overwrite the source file.
9. Read `crosstabs://evidence/limitations` for every material interpretation and `crosstabs://evidence/graph` when the answer needs supporting references.
10. End with the project revision, included and excluded data, tables and bases, methods, warnings, evidence, generated artifacts, approval state, and audit event IDs.

## Privacy and integrity

- Keep respondent-level files, project state, and generated artifacts in the local MCP process and user-controlled filesystem.
- Never infer causality from association or prediction alone.
- Never report a p-value as proof of practical importance; include effect size and base.
- Preserve zero, infinity, undefined, sparse-cell, and workload-limit states. Do not silently continuity-correct or coerce them.
- Explain orientation before epidemiology tools: `[[exposed outcome+, exposed outcome-], [unexposed outcome+, unexposed outcome-]]`.
- Separate observed facts, statistical inference, and recommendations.

## Product parity boundary

The headless source release exposes exactly the 29 deterministic project tools recorded in `../../parity.json`. Source publication does not establish directory approval or listing. This is workflow parity, not visual-interface parity. Do not invent tools for arbitrary row editing, visual interaction state, or other operations absent from that exact catalog. Local JSON persistence is capped at 8 MiB per project including audit/undo and 32 MiB per database including replay; a workload-limit rejection must not be reported as a successful save.

Read [parity-and-limits.md](references/parity-and-limits.md) when the request asks whether the plugin matches another Crosstabs surface, needs an unsupported workflow, or depends on scale limits.

## Handoff standard

End analysis with:

- What was analyzed and excluded.
- The numerical result and effect size.
- Assumption, survey-design, and multiplicity status.
- A plain-language interpretation without causal overreach.
- Evidence references or the evidence resource version.
- Any unsupported operation that still requires a separate manual step.
