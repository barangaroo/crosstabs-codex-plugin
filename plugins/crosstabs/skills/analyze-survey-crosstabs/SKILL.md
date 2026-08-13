---
name: analyze-survey-crosstabs
description: Build, test, audit, and explain crosstabs for categorical or survey data with the local Crosstabs MCP tools. Use for CSV/XLSX/SAV survey files, contingency tables, chi-square or Fisher test selection, effect sizes, sparse cells, residuals, multiple comparisons, ordinal association, agreement, epidemiology tables, power analysis, and evidence-linked statistical reporting.
---

# Analyze Survey Crosstabs

Use `crosstabs-headless` for end-to-end research projects and `crosstabs-statistics` for focused numerical claims. Keep every conclusion tied to its project revision, table, base, method, assumptions, evidence, and limitations.

## Workflow

1. Inspect the supplied data before choosing tests. Do not replace it with sample data. For a durable job, call `create_project`, `import_dataset`, then `profile_dataset`.
2. State the unit of analysis, missing-value policy, row and column variables, category order, weight meaning, and whether any question is multiple-response.
3. Define reusable row sets, multibanners, filters, and weights inside the project. Inspect the current revision before each mutation and pass its `expectedRevision` and a unique idempotency key.
4. Run a table before the full tab book. Check bases, sparse-cell warnings, significance policy, weighting limitations, and evidence IDs.
5. Use the focused statistics server when a method is not part of the project-table result. Run `check_assumptions` and `recommend_test` before inferential interpretation, then an appropriate effect size.
6. For open ends, call `code_open_ends` only after explicit external-processing approval. Review every theme and evidence example before `approve_coding`; never treat proposals as approved variables.
7. For tracker replacements, run `detect_schema_drift`, review the repair plan, and apply only explicitly approved repair operation IDs. Preserve the prior wave and guarded inverse.
8. Generate editable PPTX/DOCX packs from stable table IDs. For refresh, provide the manually edited source package and a new output path; never overwrite the source file.
9. Read `crosstabs://evidence/limitations` for every material interpretation and `crosstabs://evidence/graph` when the answer needs public supporting URLs.
10. End with the project revision, included/excluded data, tables and bases, methods, warnings, evidence, generated artifacts, approval state, and audit event IDs.

## Privacy and integrity

- Keep respondent-level files local. The remote connector at `https://mcp.crosstabs.com/mcp` is aggregate-only and is not a substitute for `crosstabs-headless`.
- Never infer causality from association or prediction alone.
- Never report a p-value as proof of practical importance; include effect size and base.
- Preserve zero, infinity, undefined, sparse-cell, and workload-limit states. Do not silently continuity-correct or coerce them.
- Explain orientation before epidemiology tools: `[[exposed outcome+, exposed outcome-], [unexposed outcome+, unexposed outcome-]]`.
- Separate observed facts, statistical inference, and recommendations.

## Product parity boundary

The local headless server shares the browser workspace project service for the 23 published operations. This is workflow parity, not UI parity. Do not invent tools for shared cloud review, comments, connector authorization, arbitrary project row editing, or browser interaction state. Use the browser workspace when those surfaces are required.

Read [parity-and-limits.md](references/parity-and-limits.md) when the request asks whether the plugin matches Crosstabs.com, needs unsupported workflows, or depends on scale limits.

## Handoff standard

End analysis with:

- What was analyzed and excluded.
- The numerical result and effect size.
- Assumption and multiplicity status.
- A plain-language interpretation without causal overreach.
- Evidence URLs or the evidence resource version.
- Any app-only collaboration or connector workflow required for the next step.
