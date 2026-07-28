## Repository
trustify-backend

## Target Branch
main

## Description
Optimize the full-text search query execution in `SearchService` to improve both performance and result relevance. The current search implementation (TC-9002) is reported as slow and returning irrelevant results.

This task modifies the `SearchService` to:
1. Use the database indexes added in Task 1 by ensuring queries target indexed columns directly rather than performing table scans.
2. Introduce basic relevance scoring using PostgreSQL's full-text search ranking functions (`ts_rank` or `ts_rank_cd`) so that results are ordered by match quality rather than insertion order.
3. Leverage the existing pagination infrastructure (`PaginatedResults<T>` from `common/src/model/paginated.rs`) to ensure paginated search results are efficiently fetched using `LIMIT`/`OFFSET` with the optimized queries.

## Files to Modify
- `modules/search/src/service/mod.rs` — refactor `SearchService` query construction to use indexed columns, add relevance ranking via `ts_rank`, and optimize query execution order

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Inspect the current query construction to understand how search terms are matched before modifying.
- Use SeaORM's `Expr::cust()` or raw query support to integrate PostgreSQL `ts_rank()` for relevance scoring. The ranking function should score matches on title/name fields higher than matches on other fields.
- Ensure the optimized queries still return `PaginatedResults<T>` using the shared paginated wrapper from `common/src/model/paginated.rs` — do not introduce a custom response type.
- Per Key Conventions (Error handling): all service methods return `Result<T, AppError>` with `.context()` wrapping. Maintain this pattern in any new or modified methods.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.
- Per Key Conventions (Response types): list/search endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Ensure the optimized search service continues to produce this type.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.
- Per Key Conventions (Query helpers): use shared filtering, pagination, and sorting via `common/src/db/query.rs` rather than implementing custom pagination logic.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.
- Reference `modules/fundamental/src/advisory/service/advisory.rs` (`AdvisoryService`) for the established pattern of building SeaORM queries with filtering and pagination in a service module.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting; reuse for building the optimized search query with pagination
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; the search service must continue to produce this type
- `common/src/error.rs` — `AppError` enum implementing `IntoResponse`; reuse for error handling in modified service methods
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` demonstrates the established pattern for SeaORM query construction with filtering in a service module

## Acceptance Criteria
- [ ] `SearchService` queries target indexed columns directly (verifiable via `EXPLAIN ANALYZE`)
- [ ] Search results are ordered by relevance ranking rather than insertion order
- [ ] Search results still return `PaginatedResults<T>` with correct pagination metadata
- [ ] Existing search behavior is preserved — all current search queries continue to return results
- [ ] Error handling follows the `Result<T, AppError>` pattern with `.context()` wrapping

## Test Requirements
- [ ] Verify that search queries use indexes by running `EXPLAIN ANALYZE` on the generated SQL and confirming index scans (not sequential scans) for indexed columns
- [ ] Verify relevance ordering: a search for a term that appears in a result's title should rank that result higher than one where the term appears only in a description
- [ ] Verify that pagination continues to work correctly with the optimized queries (offset, limit, total count)
- [ ] Run existing search integration tests (`tests/api/search.rs`) to confirm no regressions

## Verification Commands
- `cargo test --test search` — existing search tests pass
- `EXPLAIN ANALYZE SELECT ... FROM sbom WHERE ...` — confirms index usage (manual verification)

## Dependencies
- Depends on: Task 1 — Add search performance indexes via database migration
