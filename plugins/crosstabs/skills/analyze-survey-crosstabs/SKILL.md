---
name: analyze-survey-crosstabs
description: Build, test, audit, and explain crosstabs for categorical or survey data with the local Crosstabs MCP tools. Use for CSV/XLSX/SAV survey files, contingency tables, chi-square or Fisher test selection, effect sizes, sparse cells, residuals, multiple comparisons, ordinal association, agreement, epidemiology tables, power analysis, and evidence-linked statistical reporting.
---

# Analyze Survey Crosstabs

Use the local MCP server for numerical claims. Keep every conclusion tied to its table, base, method, assumptions, and limitations.

## Workflow

1. Inspect the supplied data before choosing tests. Do not replace it with sample data.
2. State the unit of analysis, missing-value policy, row and column variables, category order, weight meaning, and whether any question is multiple-response.
3. Aggregate raw records locally. Use `crosstab_from_data` or `crosstab_from_csv` only when the bounded input fits the tool; otherwise compute the matrix locally and pass only the aggregate table to the numerical tools.
4. Run `check_assumptions` and `recommend_test` before inferential interpretation.
5. Run the selected test and an appropriate effect size. Use Fisher only for eligible unweighted 2×2 integer-frequency tables. Use Monte Carlo or a defensible category/design alternative when asymptotic assumptions fail.
6. Use residual or post-hoc tools only with an explicit multiplicity policy. Distinguish exploratory cell flags from confirmatory inference.
7. Read `crosstabs://evidence/limitations` for every material interpretation and `crosstabs://evidence/graph` when the answer needs public supporting URLs.
8. Report the table, bases, statistic, degrees of freedom where applicable, p-value, effect size, assumptions, warnings, and evidence links. Label exact, asymptotic, and simulated results correctly.

## Privacy and integrity

- Keep respondent-level files local unless the user explicitly authorizes another boundary.
- Never infer causality from association or prediction alone.
- Never report a p-value as proof of practical importance; include effect size and base.
- Preserve zero, infinity, undefined, sparse-cell, and workload-limit states. Do not silently continuity-correct or coerce them.
- Explain orientation before epidemiology tools: `[[exposed outcome+, exposed outcome-], [unexposed outcome+, unexposed outcome-]]`.
- Separate observed facts, statistical inference, and recommendations.

## Product parity boundary

This plugin is not the browser application. Do not invent MCP tools for weights, multibanners, significance letters, tab-book projects, open-end coding, editable PPTX/DOCX refresh, schema repair, waves, collaboration, or Vercel AI analysis. Use the browser workspace when those workflows are required, or implement the requested local workflow transparently with available file and document tools.

Read [parity-and-limits.md](references/parity-and-limits.md) when the request asks whether the plugin matches Crosstabs.com, needs unsupported workflows, or depends on scale limits.

## Handoff standard

End analysis with:

- What was analyzed and excluded.
- The numerical result and effect size.
- Assumption and multiplicity status.
- A plain-language interpretation without causal overreach.
- Evidence URLs or the evidence resource version.
- Any app-only workflow required for the next step.
