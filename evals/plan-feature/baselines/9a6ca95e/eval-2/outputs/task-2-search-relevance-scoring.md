## Repository

trustify-backend

## Target Branch

main

## Description

Implement relevance-based scoring for search results so that the most relevant matches appear first. The current search returns results without meaningful ranking, leading users to see irrelevant results prominently. This task adds a scoring mechanism based on text match quality and sorts results by relevance score.

**Assumption (pending clarification):** The feature description says results should be "more relevant" but does not define relevance criteria or ranking factors. This task assumes relevance is based on PostgreSQL full-text search ranking (`ts_rank` or `ts_rank_cd`) using term frequency and match proximity. If domain-specific ranking factors are needed (e.g., recency, severity, advisory criticality), those weights need to be specified by the product owner.

**Assumption (pending clarification):** It is assumed that the search endpoint should return a relevance score alongside each result. If the score should be hidden from the API response, this needs clarification.

Priority: Normal
Fix Versions: RHTPA 1.6.0

## Files to Modify

- `modules/search/src/service/mod.rs` — add relevance scoring logic using `ts_rank` and order results by score descending
- `modules/search/src/endpoints/mod.rs` — update the search endpoint to accept an optional `sort` parameter (relevance vs. other fields) and pass it to the service
- `common/src/model/paginated.rs` — extend `PaginatedResults<T>` or add a search-specific response wrapper that includes a relevance score per result

## Files to Create

- `modules/search/src/model/mod.rs` — define `SearchResult` struct with entity reference, match score, and highlighted snippet fields

## Implementation Notes

- Use PostgreSQL `ts_rank` or `ts_rank_cd` functions to compute relevance scores against `tsvector` columns. This builds on the indexes created in task 1.
- Create a `SearchResult` model in `modules/search/src/model/mod.rs` following the module pattern used by `modules/fundamental/src/sbom/model/` and `modules/fundamental/src/advisory/model/`. The struct should include the entity type, entity ID, display name, relevance score, and optionally a text snippet.
- The search endpoint in `modules/search/src/endpoints/mod.rs` should default to sorting by relevance score (descending) when no explicit sort is specified.
- Use the `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs` for the response, parameterized with the new `SearchResult` type.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per the error handling convention.
- Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint registration scope.

## Acceptance Criteria

- [ ] Search results are returned sorted by relevance score by default
- [ ] A `SearchResult` model exists with entity reference, relevance score, and display name
- [ ] The search endpoint supports an optional `sort` query parameter to toggle between relevance and other orderings
- [ ] Higher-quality text matches (exact phrase, all terms present) rank higher than partial matches
- [ ] Response format remains compatible with `PaginatedResults<T>` pattern

## Test Requirements

- [ ] Add integration tests in `tests/api/search.rs` verifying that an exact-match query ranks higher than a partial match
- [ ] Test that the default sort order is by relevance (descending score)
- [ ] Test that the `sort` parameter allows switching to non-relevance orderings
- [ ] Verify the `SearchResult` response structure includes the expected fields

## Dependencies

- Task 1 (optimize-search-performance) — relevance scoring depends on the `tsvector` indexes and full-text search infrastructure.
