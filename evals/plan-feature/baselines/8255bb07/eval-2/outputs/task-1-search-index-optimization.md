# Task 1 — Add database indexes and optimize search query performance

## Repository
trustify-backend

## Target Branch
main

## Description
Add PostgreSQL full-text search indexes to improve search query performance across all searchable entities (SBOMs, advisories, packages). The current search implementation in `SearchService` performs full-text search across entities but lacks dedicated indexes, resulting in sequential scans on large datasets.

This task creates a new database migration adding GIN indexes on text columns used for search, and updates the `SearchService` to use `ts_vector`/`ts_query` for indexed full-text search instead of raw `LIKE` or `ILIKE` patterns.

**Assumption:** "Search should be faster" is interpreted as achieving sub-500ms p95 query latency for typical search patterns. No specific baseline or target was provided in the feature description (see TC-9002 ambiguity #1).

**Assumption:** "Don't break existing functionality" is interpreted as preserving all existing search API response shapes and ensuring existing integration tests continue to pass (see TC-9002 ambiguity #5).

## Files to Modify
- `modules/search/src/service/mod.rs` — Refactor search queries to use `ts_vector`/`ts_query` full-text search operators instead of pattern matching, leveraging the new GIN indexes
- `migration/src/lib.rs` — Register the new migration module in the migration sequence
- `tests/api/search.rs` — Add integration tests verifying search performance with indexed queries

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New SeaORM migration adding GIN indexes on full-text search columns for SBOM, advisory, and package entities

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for the migration module structure. The new migration should be registered in `migration/src/lib.rs` alongside the initial migration.
- Use PostgreSQL GIN indexes with `to_tsvector()` stored columns or expression indexes on the text fields used by the `SearchService` for full-text queries.
- The `SearchService` in `modules/search/src/service/mod.rs` currently implements full-text search across entities. Refactor its query construction to use `to_tsquery()` and `@@` operators, which will leverage the new GIN indexes.
- Preserve the existing `GET /api/v2/search` endpoint contract — the optimization is internal to the query layer; the response shape must not change.
- Per CONVENTIONS.md §Error Handling: all database operations must return `Result<T, AppError>` with `.context()` wrapping for meaningful error messages.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust service file scope.
- Per CONVENTIONS.md §Testing: integration tests must be added in `tests/api/search.rs` hitting a real PostgreSQL test database, using the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's integration test file scope.
- Per CONVENTIONS.md §Module Pattern: follow the established `service/` directory structure within the search module.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's module structure scope.
- Relevant constraints from `docs/constraints.md`: commit messages must follow Conventional Commits (§2.2), every commit must reference TC-9002 in the footer (§2.1), and changes must be scoped to the files listed above (§5.1).

## Reuse Candidates
- `common/src/db/query.rs::query` — Shared query builder helpers for filtering, pagination, and sorting. The search optimization should build on these existing query patterns rather than implementing custom query construction.
- `common/src/db/limiter.rs::limiter` — Connection pool limiter. Ensure search queries respect connection pool limits during high-traffic search scenarios.
- `migration/src/m0001_initial/mod.rs` — Reference migration module demonstrating the established SeaORM migration pattern.

## Acceptance Criteria
- [ ] A new database migration exists that adds GIN indexes for full-text search columns on SBOM, advisory, and package entities
- [ ] The migration is registered in `migration/src/lib.rs` and runs successfully
- [ ] `SearchService` queries use `ts_vector`/`ts_query` operators that leverage the new indexes
- [ ] Existing search API responses are unchanged (backward compatible)
- [ ] All existing integration tests in `tests/api/search.rs` continue to pass
- [ ] New integration tests verify that indexed search queries return correct results

## Test Requirements
- [ ] Integration test: verify the migration applies cleanly to a fresh database
- [ ] Integration test: verify `GET /api/v2/search?q=<term>` returns matching results using the new indexed search path
- [ ] Integration test: verify search returns results across all entity types (SBOM, advisory, package)
- [ ] Integration test: verify that search results match the existing API response shape (no regressions)

## Verification Commands
- `cargo test -p migration` — verify migration compiles and the migration module is registered
- `cargo test -p search` — verify search module compiles with the refactored query logic
- `cargo test --test search` — run search integration tests against the test database

## Dependencies
- None (independent task)
