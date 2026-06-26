## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance-based ranking for search results so that more relevant results appear first. Currently, search results have no defined ranking logic, leading to user complaints about irrelevant results. This task adds a scoring mechanism to the SearchService that ranks results by text match quality and entity-specific attributes.

**Assumption (pending clarification):** Relevance ranking criteria are assumed to be: exact match > prefix match > partial match for text similarity, with advisory severity as a secondary sort factor. TC-9002 provides no definition of "relevant" or ranking criteria.

## Files to Modify
- `modules/search/src/service/mod.rs` — Add relevance scoring logic to SearchService; compute a score per result based on text match quality and entity attributes; sort results by score before returning
- `common/src/db/query.rs` — Add a helper for ordering by a computed relevance score column (ts_rank or equivalent)

## API Changes
- `GET /api/v2/search` — MODIFY: Response results are now ordered by relevance score (descending) by default. No breaking changes to request parameters or response schema.

## Implementation Notes
Modify the SearchService in `modules/search/src/service/mod.rs` to use PostgreSQL `ts_rank()` or `ts_rank_cd()` functions to compute a relevance score for each result. The score should be based on the full-text search match quality against the query string.

Use the shared query builder helpers in `common/src/db/query.rs` to add an `ORDER BY` clause using the relevance score. The existing pagination logic in `common/src/model/paginated.rs` via `PaginatedResults<T>` should continue to work -- results are sorted by score before pagination is applied.

For advisory results specifically, incorporate severity as a secondary sort factor so that higher-severity advisories rank above lower-severity ones at equal text relevance. The severity field is available on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`.

**Assumption (pending clarification):** It is assumed that the default sort order changes to relevance-based, but clients can still request explicit sort orders (e.g., by date) via existing sort parameters. The feature does not clarify whether relevance sort should be mandatory or optional.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for sorting and pagination; extend with relevance score ordering
- `common/src/model/paginated.rs::PaginatedResults<T>` — Existing response wrapper; no changes needed but results will be pre-sorted by relevance

## Acceptance Criteria
- [ ] Search results are returned in relevance-ranked order by default
- [ ] Exact text matches rank above partial matches
- [ ] Advisory results with higher severity rank above lower severity at equal text relevance
- [ ] Existing sort parameters continue to work for clients that specify explicit ordering
- [ ] No breaking changes to the search API response schema

## Test Requirements
- [ ] Integration test verifying exact matches rank above partial matches
- [ ] Integration test verifying advisory severity influences ranking at equal text relevance
- [ ] Integration test verifying explicit sort parameter overrides relevance ranking
- [ ] Existing tests in `tests/api/search.rs` continue to pass

[sdlc-workflow] Description digest: sha256-md:d7e2f5a9c1b348670abcde123456789f0abcde123456789f0abcde1234567890
