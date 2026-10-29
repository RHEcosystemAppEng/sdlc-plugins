# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities Identified

The following ambiguities were identified in the Feature description and must be clarified before implementation can proceed with full confidence. Tasks below document assumptions where they fill in missing details — these are labeled as **assumptions pending clarification**.

1. **"Search should be faster" — no performance baseline or target.** The Feature states search is "currently too slow" but provides no current latency metrics (p50, p95, p99) or target performance thresholds. Without quantitative targets, there is no way to verify the "faster" requirement is met. **Assumption pending clarification:** we assume the goal is to add database indexing and optimize the query path to reduce query execution time, verified by query plan analysis (EXPLAIN ANALYZE) rather than a specific latency SLA.

2. **"Results should be more relevant" — no definition of relevance or ranking criteria.** The Feature does not specify what "relevant" means: should results be ranked by text match quality? By recency? By severity? By a combination? Should different entity types (SBOMs, advisories, packages) be weighted differently? **Assumption pending clarification:** we assume implementing PostgreSQL full-text search with `ts_rank` scoring and GIN indexes will provide relevance-ordered results ranked by text match quality.

3. **"Add filters" — "Some kind of filtering capability" — no filter specification.** The Feature does not specify which filters to add, what entity fields are filterable, or how filters interact with search queries. **Assumption pending clarification:** we assume adding filters for entity type (SBOM, advisory, package), severity (for advisories), and date range (created/modified) based on the existing data model and common search UX patterns.

4. **"Better UI" — cannot be planned.** This requirement cannot be decomposed into actionable tasks for two reasons: (a) no design mockups or Figma links are provided to define the target UI, and (b) the target repository `trustify-backend` is a Rust backend service with no frontend code. UI improvements would require a separate frontend repository and design specifications. This requirement is excluded from the impact map entirely.

5. **"Should be fast enough" (NFR) — no quantitative performance target.** This non-functional requirement restates the vague "faster" goal without adding measurable criteria. No latency, throughput, or resource usage targets are specified.

6. **"Don't break existing functionality" (NFR) — no specific compatibility requirements.** While backward compatibility is implied, the Feature does not specify which existing behaviors must be preserved (e.g., existing search API response shape, pagination behavior, query parameter format). **Assumption pending clarification:** we assume the existing `GET /api/v2/search` endpoint contract is preserved, with filters added as optional query parameters that do not change existing behavior when omitted.

## Impact Map

```
trustify-backend:
  changes:
    - Add database indexes (GIN indexes for full-text search) on searchable fields across SBOM, advisory, and package entities
    - Optimize SearchService query execution in modules/search/src/service/mod.rs to use indexed full-text search instead of unoptimized pattern matching
    - Implement PostgreSQL ts_vector/ts_query full-text search with ts_rank scoring for relevance-ordered results
    - Add filter parameters (entity type, severity, date range) to GET /api/v2/search endpoint
    - Extend the search endpoint handler in modules/search/src/endpoints/mod.rs to accept and apply filter query parameters
    - Add filter query construction logic using common/src/db/query.rs shared query builder helpers
    - Create database migration for GIN indexes and tsvector columns on searchable entity tables
```

## Excluded Requirements

| Requirement | Reason for Exclusion |
|---|---|
| Better UI — "Make it look nicer" | Cannot be planned: (a) no design mockups or Figma URL provided, (b) `trustify-backend` is a backend-only repository with no frontend code. Requires a frontend repository and design specifications. |

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. The three planned tasks (performance optimization, relevance improvement, filter addition) can each be merged independently to `main` without leaving the codebase in a broken state. Each task produces a self-contained improvement to the search module — no coordinated schema migrations, breaking API changes, or cross-cutting refactors require all changes to land together. Filters are additive (optional query parameters), relevance ranking changes the internal implementation without altering the API contract, and indexing is purely additive.

## Field Propagation

- **Priority:** Normal (inherited from Feature TC-9002, will be propagated to all created tasks)
- **Fix Versions:** RHTPA 1.6.0 (inherited from Feature TC-9002, will be propagated to all created tasks per `fixVersion scope: both`)
- **Labels:** All tasks will include the `ai-generated-jira` label

## additional_fields for created issues

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```
