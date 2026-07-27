## Repository
trustify-backend

## Target Branch
main

## Description
Enhance the SearchService to implement relevance-based result ranking using PostgreSQL full-text search capabilities. Currently, the search in `modules/search/src/service/mod.rs` returns results without meaningful relevance ordering, leading to user complaints about irrelevant results.

This task addresses the TC-9002 requirement "Results should be more relevant" by integrating `ts_rank` (or equivalent) scoring into search queries and ordering results by relevance score.

**Assumption (pending clarification):** "Relevant results" means results ranked by text match quality using PostgreSQL's built-in full-text search ranking (`ts_rank` / `ts_rank_cd`). No specific ranking algorithm, weighting scheme, or relevance criteria were specified in the feature description. If domain-specific ranking logic is needed (e.g., weighting advisory severity higher than name match), the ranking implementation would need to be revised.

**Assumption (pending clarification):** Relevance ranking should consider matches across all searchable entity types (SBOMs, advisories, packages) and order the combined result set by match quality. If per-entity-type ranking is preferred, the approach would differ.

## Files to Modify
- `modules/search/src/service/mod.rs` — Update SearchService to use `ts_vector`/`ts_query` with `ts_rank` for relevance scoring and result ordering
- `tests/api/search.rs` — Add integration tests for relevance-ranked search results

## Implementation Notes
- Per CONVENTIONS.md §Framework: use SeaORM query builder with raw SQL expressions for PostgreSQL full-text search functions (`to_tsvector`, `to_tsquery`, `ts_rank`). SeaORM supports raw expressions via `Expr::cust()` or similar.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's .rs file scope.
- Per CONVENTIONS.md §Error handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping for any new error paths introduced.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's .rs file scope.
- Per CONVENTIONS.md §Response types: search results must continue to use `PaginatedResults<T>` from `common/src/model/paginated.rs`. Add a relevance score field to the search result items if the response model supports it, or order results by score without exposing the score.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's .rs file scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/search.rs` following the existing pattern (`assert_eq!(resp.status(), StatusCode::OK)`) with a real PostgreSQL test database. Test that results for a known query are returned in relevance-ranked order.
  Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.
- Inspect the current SearchService implementation in `modules/search/src/service/mod.rs` to understand the existing query structure before modifying it.
- Use `common/src/db/query.rs` query builder helpers for pagination and sorting integration with the new ranking logic.
- The search endpoint (`modules/search/src/endpoints/mod.rs` — `GET /api/v2/search`) should not need structural changes — ranking is a service-layer concern.

## Reuse Candidates
- `modules/search/src/service/mod.rs::SearchService` — Existing search implementation to extend with ranking
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting that the ranking query should integrate with
- `common/src/model/paginated.rs::PaginatedResults` — Response wrapper that search results must conform to
- `common/src/error.rs::AppError` — Error type for service-layer error handling

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (best matches first) when a text query is provided
- [ ] Results that match the search term more closely (e.g., exact name match) appear before partial or tangential matches
- [ ] Search with no query term continues to work (backward compatible — returns results in default order)
- [ ] Response shape remains compatible with existing `PaginatedResults<T>` contract
- [ ] Existing search API contract (`GET /api/v2/search`) is preserved — no breaking changes to request parameters or response structure

## Test Requirements
- [ ] Integration test: search for a known term returns results ordered by relevance (insert test data with varying match quality, verify ordering)
- [ ] Integration test: search with an empty query returns results without error (backward compatibility)
- [ ] Integration test: search results still conform to `PaginatedResults` response shape
- [ ] Integration test: pagination continues to work correctly with relevance-ranked results

## Verification Commands
- `cargo test --test search` — search integration tests pass
- `cargo clippy --all-targets` — no new warnings introduced

## Dependencies
- Depends on: Task 1 — Add database indexes for search performance (indexes support the full-text search ranking queries)
