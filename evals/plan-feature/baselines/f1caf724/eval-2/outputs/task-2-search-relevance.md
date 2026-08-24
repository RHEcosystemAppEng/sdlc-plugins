## Repository
trustify-backend

## Target Branch
main

## Description
Improve search result relevance by implementing PostgreSQL full-text search ranking in the SearchService. Currently, search results are returned without relevance scoring, meaning results that partially match the query appear alongside exact matches with no differentiation. This task adds ts_rank-based scoring so that results are ordered by how well they match the search query.

**Assumptions pending clarification:**
- Relevance ranking will use PostgreSQL's `ts_rank` function with default normalization. The feature description does not specify a ranking algorithm or field weighting scheme. We assume title/name fields should be weighted higher (weight A) than description/body fields (weight D) in the tsvector configuration.
- The search endpoint will return results sorted by relevance score by default when a text query is provided. An optional `sort` query parameter will allow switching to date-based ordering. The feature does not specify whether relevance sorting should be the default or opt-in.
- The relevance score will be included in the response payload as a numeric field so API consumers can use it for display or further sorting. The feature does not specify whether the score should be exposed.

## Files to Modify
- `modules/search/src/service/mod.rs` -- refactor SearchService to use tsvector/tsquery with ts_rank scoring instead of basic text matching
- `modules/search/src/endpoints/mod.rs` -- add relevance score to response model; add optional `sort` query parameter (relevance, date)
- `tests/api/search.rs` -- add tests verifying relevance-ordered results

## Implementation Notes
- Inspect `modules/search/src/service/mod.rs` to understand the current search implementation. Replace basic LIKE or ILIKE queries with PostgreSQL full-text search using `to_tsvector`/`to_tsquery` and `ts_rank`.
- Use SeaORM raw SQL or query builder extensions for tsvector operations if SeaORM does not natively support full-text search functions.
- The response model should include a `relevance_score: f64` field alongside existing result fields. Ensure this integrates with `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- When no text query is provided (empty search string), fall back to date-based ordering since relevance scoring is not applicable.
- Per CONVENTIONS.md §Module pattern: maintain the existing model/ + service/ + endpoints/ structure within the search module. Do not introduce new top-level directories.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Error handling: ensure all new handler code returns `Result<T, AppError>` with `.context()` wrapping for error messages.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` handler scope.
- Per CONVENTIONS.md §Query helpers: use shared query builder helpers from `common/src/db/query.rs` for pagination and sorting integration with the new relevance sort option.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's query helper scope.
- Per CONVENTIONS.md §Testing: follow the established integration test pattern in `tests/api/search.rs` using `assert_eq!(resp.status(), StatusCode::OK)`.
  Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `common/src/db/query.rs::QueryBuilder` -- shared query builder with filtering, pagination, and sorting helpers; extend for relevance sort support
- `common/src/model/paginated.rs::PaginatedResults<T>` -- response wrapper for list endpoints; ensure relevance score integrates with pagination

## Acceptance Criteria
- [ ] Search results are ordered by relevance score by default when a text query is provided
- [ ] Title/name field matches rank higher than description/body-only matches
- [ ] An optional `sort` query parameter allows switching between relevance and date-based ordering
- [ ] The search response includes a `relevance_score` field for each result
- [ ] Queries with no text component (empty string or filter-only) fall back to date-based ordering
- [ ] Existing search API consumers are not broken (the endpoint path and basic parameters remain unchanged)

## Test Requirements
- [ ] Test that a query matching a document title ranks that result above a description-only match
- [ ] Test that the `sort=date` parameter overrides relevance ordering
- [ ] Test that empty query strings return results in date order (no relevance scoring applicable)
- [ ] Test that the `relevance_score` field is present and numeric in the response body

## Verification Commands
- `cargo test -p modules-search` -- search module unit tests pass
- `cargo test -p tests --test search` -- search integration tests pass

## Dependencies
- Depends on: Task 1 -- Add database indexes for search performance (GIN indexes must be in place before full-text search ranking queries can execute efficiently)
