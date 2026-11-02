# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities and Gaps

The following ambiguities in the feature description require clarification before implementation details can be considered fully validated:

1. **"Search should be faster" — no performance baseline or target.** The requirement states search is "currently too slow" but provides no latency measurements, no target response time (e.g., p95 < 200ms), and no indication of which queries are slow (full-text, filtered, paginated). **Assumption pending clarification:** we assume the bottleneck is the lack of database-level full-text search indexes and will target adding PostgreSQL GIN indexes on searchable text columns.

2. **"Results should be more relevant" — no definition of relevance or ranking criteria.** "Irrelevant results" is subjective without specifying what a good result looks like. No ranking signals, weighting factors, or example queries with expected results are provided. **Assumption pending clarification:** we assume relevance improvement means adding PostgreSQL `ts_rank` scoring to order results by text match quality rather than returning unranked results.

3. **"Add filters" — no specification of filter types, fields, or behavior.** "Some kind of filtering capability" does not define which entity fields should be filterable, whether filters are AND/OR combined, or what the filter UI/API contract should look like. **Assumption pending clarification:** we assume filters will cover the entity fields already exposed in list endpoints (severity for advisories, type for SBOMs) and will use query parameter-based filtering consistent with the existing `common/src/db/query.rs` patterns.

4. **"Should be fast enough" — non-functional requirement with no measurable target.** Without a quantitative performance threshold, there is no way to validate this requirement against an acceptance criterion. **Assumption pending clarification:** we assume "fast enough" means search queries should complete within 500ms for typical result sets.

5. **"Don't break existing functionality" — implicit, with no regression test strategy defined.** The feature description does not specify which existing behaviors must be preserved or how to verify them. **Assumption pending clarification:** we assume existing search endpoint integration tests in `tests/api/search.rs` provide the regression baseline and new changes must not break those tests.

## Excluded Requirements

- **"Better UI" (non-MVP):** This requirement cannot be planned. No frontend repository is available in the Repository Registry (only `trustify-backend`), no Figma design mockups are provided, and no design specifications exist to decompose into actionable tasks. This requirement is excluded from the plan scope entirely. It should be revisited when a frontend repository and design mockups are available.

## trustify-backend

### Changes

- Add PostgreSQL full-text search indexes (GIN) on searchable entity columns via a new database migration to improve search query performance
- Refactor `SearchService` in `modules/search/src/service/mod.rs` to use `ts_vector`/`ts_query` with `ts_rank` scoring for relevance-ordered results
- Add query parameter-based filters to the search endpoint in `modules/search/src/endpoints/mod.rs`, leveraging existing filter/pagination patterns from `common/src/db/query.rs`
- Add integration tests covering full-text search ranking, filter combinations, and performance validation in `tests/api/search.rs`

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. Each change (migration, service refactor, filter parameters, tests) can land independently without leaving `main` in a broken state. The migration adds indexes that improve performance without changing behavior; the service refactor improves ranking without breaking the API contract; filter parameters are additive.

## Inherited Field Propagation

- **Priority:** `Normal` — inherited from Feature TC-9002. Will be propagated to all created tasks.
- **fixVersions:** `RHTPA 1.6.0` — inherited from Feature TC-9002. Will be propagated to all created tasks (fixVersion scope defaults to `both` per Jira Field Defaults).

## Task Summary

| # | Task | Repository | Dependencies |
|---|------|-----------|-------------|
| 1 | Add full-text search indexes | trustify-backend | None |
| 2 | Improve search relevance scoring | trustify-backend | Task 1 |
| 3 | Add search filter parameters | trustify-backend | Task 1 |
| 4 | Search integration tests | trustify-backend | Task 2, Task 3 |
