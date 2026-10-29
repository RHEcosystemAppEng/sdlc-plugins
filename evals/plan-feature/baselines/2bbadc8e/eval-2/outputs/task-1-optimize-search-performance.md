## Repository
trustify-backend

## Target Branch
main

## Description
Optimize the search query performance in the SearchService by adding database indexes and improving query execution. The current search implementation uses unoptimized queries that result in slow response times. This task adds GIN indexes for full-text search on searchable entity columns and creates a database migration to support the indexing.

**Assumption pending clarification:** No specific performance targets (latency SLA, p95/p99 thresholds) were provided in the Feature description. This task assumes the goal is to add database indexing and optimize the query path, verified by query plan analysis (EXPLAIN ANALYZE showing index usage) rather than a specific latency target.

## Files to Modify
- `modules/search/src/service/mod.rs` — Optimize SearchService query methods to leverage new indexes and reduce query overhead
- `common/src/db/query.rs` — Add or extend query builder helpers to support indexed full-text search patterns

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — Database migration adding GIN indexes on searchable columns (SBOM name/description, advisory title/description, package name)

## API Changes
- `GET /api/v2/search` — MODIFY: no external API contract change; internal query execution optimized to use database indexes for faster response times

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for migration file structure and registration.
- Use PostgreSQL GIN indexes on `tsvector` columns for full-text search optimization. Create `tsvector` generated columns on the SBOM, advisory, and package entity tables for their searchable text fields.
- The `SearchService` in `modules/search/src/service/mod.rs` currently performs full-text search across entities. Refactor the query construction to use `to_tsquery` and GIN index-backed lookups instead of LIKE/ILIKE pattern matching.
- Reuse the shared query builder helpers in `common/src/db/query.rs` for constructing the optimized queries — extend rather than duplicate the existing filtering and pagination logic.
- Register the new migration module in `migration/src/lib.rs` following the existing module registration pattern.
- Per Key Conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping — ensure any new error paths in the optimized query code follow this pattern.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust service file scope.
- Per Key Conventions: use SeaORM for database operations and follow the existing entity definitions in `entity/src/`.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust service file scope.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — Shared filtering, pagination, and sorting utilities used by all list endpoints; extend these for full-text search query construction rather than building standalone query logic
- `common/src/db/limiter.rs::connection pool limiter` — Connection pool management that may need consideration when adding indexed queries to prevent connection exhaustion
- `migration/src/m0001_initial/mod.rs` — Reference migration demonstrating the project's migration file structure, registration pattern, and SeaORM migration conventions

## Acceptance Criteria
- [ ] GIN indexes are created on searchable text columns for SBOM, advisory, and package entities via a database migration
- [ ] SearchService queries use the new indexes (verified via EXPLAIN ANALYZE showing index scans instead of sequential scans)
- [ ] The migration runs successfully on a clean database and is idempotent (re-running does not error)
- [ ] Existing search functionality is not broken — the `GET /api/v2/search` endpoint returns the same results as before for identical queries
- [ ] The migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Integration test verifying the migration applies cleanly and creates the expected indexes
- [ ] Integration test verifying search queries return correct results after index creation (same results as before optimization)
- [ ] Integration test verifying search queries use index scans (query plan verification)

## Verification Commands
- `cargo test -p migration` — migration tests pass
- `cargo test -p search` — search module tests pass
