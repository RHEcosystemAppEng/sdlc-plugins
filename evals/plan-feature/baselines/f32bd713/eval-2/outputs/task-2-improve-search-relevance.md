# Task 2 — Improve search result relevance ranking

## Repository
trustify-backend

## Target Branch
main

## Description
Add relevance ranking to the SearchService so that search results are returned in order of relevance rather than an arbitrary or insertion order. The feature TC-9002 states that "users complain about irrelevant results" but does not define what makes a result "relevant" or specify ranking criteria.

**Assumption:** Relevance will be implemented using PostgreSQL full-text search ranking functions (ts_rank or ts_rank_cd) applied to existing tsvector columns. If the current SearchService does not use PostgreSQL full-text search, the implementation should introduce it.

**Assumption:** Relevance ranking applies equally to all searchable entity types (SBOMs, advisories, packages) since the feature does not specify a subset.

**Assumption:** "More relevant results" means results matching more search terms or matching in higher-priority fields (e.g., title matches ranked above description matches) are returned first.

## Files to Modify
- `modules/search/src/service/mod.rs` — add relevance scoring and result ordering to SearchService queries
- `tests/api/search.rs` — add tests verifying result ordering by relevance

## Implementation Notes
- Examine the current full-text search implementation in `modules/search/src/service/mod.rs` to understand how queries are constructed and results are returned.
- Add `ts_rank` or `ts_rank_cd` scoring to search queries, ordering results by descending relevance score.
- Consider weighting different fields (e.g., title vs description) using PostgreSQL text search weights (A, B, C, D) to prioritize title matches.
- Ensure the relevance score is computed but does not need to be exposed in the API response — only the ordering matters.
- Review the existing search query patterns and reuse the query construction helpers in `common/src/db/query.rs` for pagination and sorting integration.
- Per CONVENTIONS.md §Module pattern: maintain the model/ + service/ + endpoints/ structure for search module changes.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Error handling: use `Result<T, AppError>` with `.context()` wrapping for all error paths.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` handler scope.
- Per CONVENTIONS.md §Query helpers: integrate relevance ordering with the existing shared sorting utilities from `common/src/db/query.rs`.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` service file scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/` using real PostgreSQL and the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `common/src/db/query.rs::sorting helpers` — existing sorting utilities that should be extended or composed with relevance ordering
- `modules/search/src/service/mod.rs::SearchService` — the existing search implementation to build upon

## Acceptance Criteria
- [ ] Search results are returned in relevance-ranked order (most relevant first)
- [ ] A search for a specific term returns documents containing that term in the title before documents containing it only in the description
- [ ] Existing search functionality continues to work (all existing tests pass)
- [ ] Results remain correct — relevance ranking changes ordering, not the result set

## Test Requirements
- [ ] Integration test: search for a known term and verify that the result with the term in its title appears before results with the term only in the description
- [ ] Integration test: search with multiple terms and verify results matching more terms rank higher
- [ ] Existing search integration tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test --test search` — verify all search integration tests pass

## Dependencies
- None (can be implemented independently of Task 1 and Task 3)
