## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance scoring for search results so that the most relevant matches appear first. Currently, the SearchService in `modules/search/src/service/mod.rs` returns results in default database order (likely insertion order), which does not reflect how well each result matches the search query. This task adds PostgreSQL `ts_rank` scoring to the search query and orders results by relevance score, improving the user experience for search.

**Ambiguity note:** The feature description states "results should be more relevant" and "users complain about irrelevant results" without defining what constitutes a relevant result. No ranking criteria, weighting preferences, or examples of desired vs. undesired result ordering are provided.

**Assumption (pending clarification):** "More relevant" is interpreted as implementing PostgreSQL full-text search ranking using `ts_rank` or `ts_rank_cd` functions. Results will be ordered by descending relevance score. The default normalization and weighting will be used until the product owner provides specific ranking preferences.

## Files to Modify
- `modules/search/src/service/mod.rs` — add ts_rank computation to search queries and order results by relevance score
- `modules/search/src/endpoints/mod.rs` — update the search endpoint response to include relevance score field in results
- `tests/api/search.rs` — add integration tests verifying relevance-based ordering

## API Changes
- `GET /api/v2/search` — MODIFY: response items now include a `relevance_score` field (f32); results are ordered by descending relevance score by default

## Implementation Notes
- In `modules/search/src/service/mod.rs`, add a `ts_rank(to_tsvector('english', <text_column>), to_tsquery('english', <search_term>))` expression to the search query. Use SeaORM's `Expr::cust_with_values` or raw SQL expression for the ranking function.
- Add the relevance score as a computed column in the query SELECT clause and use it for ORDER BY DESC.
- In `modules/search/src/endpoints/mod.rs`, update the response serialization to include the `relevance_score` field. The endpoint currently returns results wrapped in `PaginatedResults<T>` from `common/src/model/paginated.rs` — ensure the wrapper type accommodates the additional score field without breaking existing consumers.
- Consider adding a search result wrapper model that includes both the entity data and the relevance score, following the module pattern in `modules/fundamental/src/sbom/model/summary.rs`.
- Ensure backward compatibility: existing API consumers that ignore the `relevance_score` field should not break.
- Per CONVENTIONS.md §Error Handling: all new or modified handlers must return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ structure when adding new types. If a search result model is needed, place it in `modules/search/src/model/`.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's modules `.rs` scope.
- Per CONVENTIONS.md §Response Types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Ensure the search response maintains this wrapper.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint `.rs` file scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/` using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. See `tests/api/search.rs` for the established test structure.
  Applies: task modifies `tests/api/search.rs` matching the convention's test `.rs` file scope.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults<T>` — existing paginated response wrapper to reuse for search results
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference model struct pattern for creating a SearchResultSummary type
- `common/src/db/query.rs` — shared query builder helpers for pagination and sorting that should be extended or reused

## Acceptance Criteria
- [ ] Search results in `GET /api/v2/search` are ordered by relevance score (descending) when a search query is provided
- [ ] Each search result item includes a `relevance_score` field
- [ ] Search with no query term returns results in a stable default order (not random)
- [ ] Existing API consumers that do not use the `relevance_score` field continue to work (backward compatibility)
- [ ] All existing search integration tests pass without modification

## Test Requirements
- [ ] Integration test: verify that a search for a specific term returns results ordered by relevance (most relevant first)
- [ ] Integration test: verify that each result in the response includes a `relevance_score` field with a numeric value
- [ ] Integration test: verify that a search with no query term returns results without error
- [ ] Regression: all existing tests in `tests/api/search.rs` pass without modification

## Verification Commands
- `cargo test --test search` — run search integration tests, expect all tests to pass

## Dependencies
- Depends on: Task 1 — Add database indexes for search performance optimization (relevance scoring queries benefit from the GIN indexes created in Task 1)
