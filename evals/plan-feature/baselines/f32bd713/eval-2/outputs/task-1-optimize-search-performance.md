# Task 1 — Optimize search query performance

## Repository
trustify-backend

## Target Branch
main

## Description
Optimize the search query performance in SearchService by adding database indexes for search-relevant columns and improving query execution patterns. The feature TC-9002 states that "search is slow" but provides no specific latency targets — this task assumes performance issues stem from missing indexes and unoptimized query patterns, and will capture before/after benchmarks to quantify the improvement.

**Assumption:** The primary performance bottleneck is database-level (missing indexes, inefficient query plans). If profiling reveals the bottleneck is elsewhere (e.g., serialization, network), the approach should be adjusted.

**Assumption:** "Faster" is interpreted as measurably reduced query latency on representative data sets, since no specific performance target is provided in the feature description.

## Files to Modify
- `modules/search/src/service/mod.rs` — optimize query construction and execution in SearchService
- `migration/src/lib.rs` — register the new migration module
- `tests/api/search.rs` — add performance-related test assertions

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — add database indexes for full-text search columns and frequently queried fields

## Implementation Notes
- Examine the current SearchService implementation in `modules/search/src/service/mod.rs` to identify query patterns that lack indexes or perform unnecessary joins.
- Add GIN or GiST indexes for PostgreSQL full-text search columns (tsvector) used by the search service.
- Add B-tree indexes for columns commonly used in search filtering (e.g., timestamps, severity fields).
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for index creation syntax and module registration.
- Reuse the query builder helpers in `common/src/db/query.rs` for any query restructuring — do not duplicate filtering or pagination logic.
- Per CONVENTIONS.md §Module pattern: maintain the model/ + service/ + endpoints/ structure for any search module changes.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Error handling: use `Result<T, AppError>` with `.context()` wrapping for all error paths in modified service methods.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` handler scope.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting utilities from `common/src/db/query.rs` rather than writing custom query logic.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` service file scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/` using real PostgreSQL and the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — shared filtering, pagination, and sorting utilities that should be reused for any query restructuring
- `migration/src/m0001_initial/mod.rs` — reference migration showing the module registration and table creation pattern

## Acceptance Criteria
- [ ] Database indexes are created for search-relevant columns via a new migration
- [ ] SearchService query execution is optimized (verified by query plan analysis or benchmark)
- [ ] Existing search functionality continues to work (all existing tests in `tests/api/search.rs` pass)
- [ ] Migration runs successfully against a clean database and against an existing database
- [ ] No regressions in other endpoint response times

## Test Requirements
- [ ] Existing search integration tests in `tests/api/search.rs` continue to pass after index and query changes
- [ ] New migration applies cleanly on both fresh and existing databases
- [ ] Search endpoint returns correct results after query optimization (functional correctness preserved)

## Verification Commands
- `cargo test --test search` — verify search integration tests pass
- `cargo run --bin migration` — verify migration applies successfully

## Dependencies
- None (first task, no prerequisites)
