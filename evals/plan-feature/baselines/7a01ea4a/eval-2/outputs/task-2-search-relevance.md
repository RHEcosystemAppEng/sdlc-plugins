## Repository
trustify-backend

## Target Branch
main

## Description
Enhance the SearchService's full-text search to apply relevance-weighted ranking so that search results are ordered by match quality rather than insertion order or arbitrary ordering. This addresses TC-9002 requirement: "Results should be more relevant." Currently, the SearchService in `modules/search/src/service/mod.rs` performs full-text search across entities (SBOMs, advisories, packages) without relevance scoring. This task adds ranking using PostgreSQL's `ts_rank` or `ts_rank_cd` function (if the search uses `tsvector`/`tsquery`) or a comparable scoring mechanism, so that exact matches and higher-quality matches appear first in the result set.

## Files to Modify
- `modules/search/src/service/mod.rs` -- add relevance scoring computation and ORDER BY ranking to the search query
- `tests/api/search.rs` -- add integration tests verifying relevance-ordered results

## Implementation Notes
- Inspect `modules/search/src/service/mod.rs` thoroughly before modifying to understand the current search query structure (whether it uses `tsvector`/`tsquery`, `LIKE`/`ILIKE`, or another pattern)
- If the search uses `tsvector`/`tsquery`: use PostgreSQL's `ts_rank()` or `ts_rank_cd()` to compute a relevance score per result row, then `ORDER BY rank DESC` before pagination
- If the search uses `LIKE`/`ILIKE` patterns: consider upgrading to `tsvector`-based search for native ranking support, or implement a simple scoring heuristic (e.g., exact match > prefix match > substring match) using `CASE WHEN` expressions
- Apply the relevance ordering before the pagination limit/offset so that the most relevant results appear on the first page
- Preserve the `PaginatedResults<T>` response wrapper from `common/src/model/paginated.rs` -- relevance scoring changes the result ordering, not the response structure or total count
- Use the query builder helpers from `common/src/db/query.rs` for any sorting integration -- extend the existing sorting logic rather than bypassing it
- Per CONVENTIONS.md section "Error Handling": return `Result<T, AppError>` with `.context()` wrapping for any new error paths introduced during ranking computation. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust service file scope.
- Per CONVENTIONS.md section "Query Helpers": use shared filtering, pagination, and sorting helpers from `common/src/db/query.rs` alongside the new relevance ordering rather than implementing custom pagination logic. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust service/query file scope.
- Per CONVENTIONS.md section "Testing": add integration tests in `tests/api/search.rs` using a real PostgreSQL test database and `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/search.rs` matching the convention's Rust test file scope.

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting -- extend for relevance-based ordering rather than duplicating sort logic
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` wrapper used by all list endpoints -- search results must continue using this wrapper
- `modules/fundamental/src/advisory/service/advisory.rs` -- AdvisoryService implementation may contain result-ordering patterns applicable to relevance sorting
- `common/src/error.rs` -- `AppError` enum for error handling in new code paths

## Acceptance Criteria
- [ ] Search results are ordered by relevance score with best matches first
- [ ] Exact text matches rank higher than partial or substring matches
- [ ] Search results with equal relevance scores maintain stable, deterministic ordering (e.g., secondary sort by creation date or ID)
- [ ] The response structure (`PaginatedResults<T>`) is unchanged -- clients experience no breaking changes
- [ ] Pagination works correctly with relevance ordering (page 2 contains lower-ranked results than page 1)
- [ ] Existing search functionality (returning correct result sets for given queries) is preserved

## Test Requirements
- [ ] Test that searching for an entity's exact name returns it as the top result when multiple entities contain similar text
- [ ] Test that partial matches appear below exact matches in result ordering
- [ ] Test that searching with a term matching multiple entity types returns all types, ordered by relevance across types
- [ ] Test pagination with relevance ordering: page 1 results should have higher relevance than page 2 results
- [ ] Test with an empty search query to verify edge case handling (should return results in a stable default order)
- [ ] All existing search integration tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test -p tests --test search` -- run all search integration tests including new relevance tests

## Dependencies
- None
