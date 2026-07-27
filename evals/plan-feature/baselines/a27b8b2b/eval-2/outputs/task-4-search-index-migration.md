## Repository
trustify-backend

## Target Branch
main

## Description
Create a database migration to add GIN indexes on full-text search columns to improve search query performance. The feature requirement states "Search should be faster — Currently too slow" (MVP). GIN indexes are the standard PostgreSQL index type for tsvector columns used in full-text search, enabling efficient lookup without full table scans.

Note: The feature description does not specify a quantitative performance target. This migration improves query performance for full-text search operations, but the engineer should establish a baseline latency measurement before and after the migration to quantify the improvement.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — migration adding GIN indexes on tsvector columns used by the search service

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration registry

## Implementation Notes
- Follow the migration pattern established in `migration/src/m0001_initial/mod.rs` for the migration structure (up/down functions, SeaORM migration trait implementation).
- Create GIN indexes on any tsvector columns that the SearchService queries against. GIN indexes are preferred over GiST for full-text search because they provide faster lookups at the cost of slightly slower updates.
- Use `CREATE INDEX CONCURRENTLY` if possible to avoid locking the table during index creation on production databases. Note: SeaORM migrations may not support CONCURRENTLY — check the migration framework's capabilities.
- If the search service uses `LIKE` or `ILIKE` queries instead of tsvector/tsquery, add `pg_trgm` extension and GIN trigram indexes (`gin_trgm_ops`) as appropriate.
- The migration should be idempotent — use `IF NOT EXISTS` for index creation.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — reference implementation for SeaORM migration structure

## Acceptance Criteria
- [ ] Migration file exists at `migration/src/m0002_search_indexes/mod.rs`
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] Migration creates GIN indexes on full-text search columns
- [ ] Migration runs successfully against a PostgreSQL test database
- [ ] Migration is reversible (down function drops the created indexes)
- [ ] Search queries show improved execution plans (index scan instead of sequential scan) after migration

## Test Requirements
- [ ] Verify migration runs successfully (up) without errors
- [ ] Verify migration rollback (down) without errors
- [ ] Verify search queries use the new indexes (EXPLAIN ANALYZE shows index scan)

## Verification Commands
- `cargo build -p migration` — compiles without errors
- `cargo test -p migration` — migration tests pass

## Dependencies
- None (index migration is independent of model/service changes; can be applied before or after other tasks)
