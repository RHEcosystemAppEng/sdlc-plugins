# Plan Summary — TC-9002: Improve Search Experience

This is the summary that would be posted as a comment on the Jira feature issue TC-9002.

---

## Ambiguities Identified

The feature description is vague in several areas. The following ambiguities were flagged and assumptions documented:

1. **No performance baseline or target** — "Search should be faster" and "Should be fast enough" lack quantified metrics. Assumed: optimize with database indexes and query tuning; actual targets should be defined by product owner.
2. **No relevance definition** — "Results should be more relevant" has no ranking criteria. Assumed: use PostgreSQL ts_rank for full-text search relevance scoring.
3. **No filter specification** — "Add filters" / "Some kind of filtering capability" does not specify which fields or filter types. Assumed: entity type, severity, and date range filters based on data model analysis.
4. **"Better UI" is out of scope** — Marked as non-MVP. No Figma mockups provided. No frontend repository in the Repository Registry. UI improvements cannot be planned without design specifications and a frontend codebase.
5. **Non-functional requirements are unquantified** — "Should be fast enough" and "Don't break existing functionality" need concrete thresholds for verification.

## Tasks Created

| # | Summary | Repository |
|---|---|---|
| 1 | Add full-text search indexes via database migration | trustify-backend |
| 2 | Add relevance scoring to SearchService | trustify-backend |
| 3 | Add filter parameters to search endpoint | trustify-backend |
| 4 | Optimize search query performance | trustify-backend |

## Repositories Affected

- **trustify-backend** — all tasks target this repository (the only repository in the Registry)

## Architecture Summary

The implementation improves the existing `modules/search/` module in four incremental steps:

1. **Database layer** (Task 1): Add tsvector columns and GIN indexes to the sbom, advisory, and package entities via a SeaORM migration. This is the foundation — all subsequent tasks depend on these indexes.
2. **Relevance scoring** (Task 2): Refactor `SearchService` to use `ts_rank()` against the tsvector columns, returning a relevance score with each result and sorting by relevance by default.
3. **Filtering** (Task 3): Add optional filter query parameters (entity_type, severity, date_from, date_to) to `GET /api/v2/search`, composing with AND semantics and maintaining backward compatibility.
4. **Performance** (Task 4): Ensure GIN index utilization, pagination pushdown, cache-control headers, and query timeouts.

All changes use existing patterns from `common/src/db/query.rs` (filtering, pagination, sorting) and `common/src/model/paginated.rs` (response wrapper). The search endpoint API changes are backward compatible — all new parameters are optional.

## Workflow Mode

**direct-to-main** — no atomicity indicators found. All tasks can be merged independently.

## Inherited Field Values

- **Priority:** Normal — propagated from TC-9002 to all 4 tasks
- **Fix Versions:** RHTPA 1.6.0 — propagated from TC-9002 to all 4 tasks (no `fixVersion scope` restriction in Jira Configuration; defaulting to "both" per Step 6a rules)

## CONVENTIONS.md

CONVENTIONS.md was found at the trustify-backend repository root. Conventions were cross-referenced with each task's scope and included in Implementation Notes where applicable (migration patterns for Task 1, module/endpoint patterns for Tasks 2-4). Convention applicability was validated per convention-applicability-rules.md — only conventions whose scope matched the task's files were included.

## Jira Operations (Simulated)

Since this is an eval run, the following Jira operations were simulated:
- 4 tasks would be created with `ai-generated-jira` label, Priority: Normal, Fix Versions: RHTPA 1.6.0
- Feature "incorporates" links would be created from TC-9002 to each task
- Dependency links ("depends on") would be created per the Dependencies section in each task
- A description digest comment would be posted on each created task
- The impact map and plan summary would be posted as comments on TC-9002
