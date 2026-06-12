# Task 1 — Add full-text search indexes for searchable entities

## Repository
trustify-backend

## Target Branch
main

## Description
Add PostgreSQL GIN indexes on searchable text fields across the SBOM, Advisory, and Package entities to improve full-text search query performance. Currently the search module (`modules/search/`) performs full-text search across entities but lacks dedicated indexes, causing sequential scans on large datasets. This task creates a new SeaORM migration that adds `tsvector` columns (or GIN indexes on existing text columns) for the fields used by `SearchService` queries.

**Ambiguity note:** The feature description (TC-9002) does not specify performance targets. This task assumes that adding GIN indexes is the appropriate first step to address "search should be faster." The product owner should confirm acceptable latency SLAs (e.g., p95 < 200ms) so that subsequent optimization can be targeted if indexes alone are insufficient.

## Files to Modify
- `modules/search/src/service/mod.rs` — Update `SearchService` queries to use the new indexed columns/tsvector for full-text matching instead of raw LIKE or ILIKE patterns
- `entity/src/sbom.rs` — Add tsvector column mapping if using stored tsvector columns (depends on migration approach)
- `entity/src/advisory.rs` — Add tsvector column mapping if using stored tsvector columns
- `entity/src/package.rs` — Add tsvector column mapping if using stored tsvector columns

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New migration adding GIN indexes on searchable text fields (SBOM name/description, Advisory title/description/severity, Package name/version/license)

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and SeaORM migration conventions.
- Use PostgreSQL GIN indexes on `to_tsvector('english', column)` expressions for full-text search. Consider whether to store a precomputed `tsvector` column or use expression-based indexes — expression indexes avoid schema changes to entity structs but precomputed columns are faster for multi-column search.
- The `SearchService` in `modules/search/src/service/mod.rs` currently performs "full-text search across entities." Inspect the current query implementation to determine whether it uses `LIKE`, `ILIKE`, or already uses `to_tsvector`/`to_tsquery`. Adapt the migration accordingly.
- Reference the query builder helpers in `common/src/db/query.rs` — these provide shared filtering, pagination, and sorting infrastructure. Ensure the indexed search queries integrate with these helpers rather than bypassing them.
- Use `tower-http` caching middleware configuration in endpoint route builders for cache invalidation awareness — index changes should not require cache configuration changes, but verify.
- Per docs/constraints.md Section 2 (Commit Rules): use Conventional Commits format and reference TC-9002 in the commit footer.
- Per docs/constraints.md Section 5 (Code Change Rules): inspect existing code before modifying, follow patterns found in the codebase.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; extend rather than duplicate for full-text search query construction
- `migration/src/m0001_initial/mod.rs` — reference migration pattern for SeaORM migration structure and idioms

## Acceptance Criteria
- [ ] A new database migration exists that adds GIN indexes on searchable text fields for SBOM, Advisory, and Package entities
- [ ] The migration runs successfully against a clean database and as an incremental migration on an existing database
- [ ] `SearchService` queries leverage the new indexes (verified via EXPLAIN ANALYZE showing index scans instead of sequential scans)
- [ ] Existing search functionality is not broken — current search queries continue to return correct results

## Test Requirements
- [ ] Migration applies cleanly in the test database setup
- [ ] Integration test in `tests/api/search.rs` continues to pass after migration
- [ ] Add a test verifying that search queries use the GIN index (optional: EXPLAIN-based assertion or query plan check)

## Verification Commands
- `cargo test -p tests --test search` — existing search tests pass
- `cargo run --bin migration -- up` — migration applies successfully

## Dependencies
- None (this is the foundational task)
