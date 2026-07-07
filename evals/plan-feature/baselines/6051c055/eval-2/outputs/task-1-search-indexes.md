## Repository
trustify-backend

## Target Branch
main

## Description
Add PostgreSQL full-text search indexes to improve query performance for the search endpoint. This involves creating a SeaORM database migration that adds `tsvector` columns and GIN indexes to searchable tables, and updating the query helpers to use these indexes when constructing search queries.

The current search implementation likely uses `LIKE`/`ILIKE` queries which cannot leverage indexes efficiently. By introducing `tsvector` columns maintained via triggers and GIN indexes, the database can perform full-text matching orders of magnitude faster on large datasets.

ASSUMPTION (pending clarification): The "search should be faster" requirement has no latency targets. This task adds indexing infrastructure as a best-practice improvement, but specific performance validation requires defined targets from the Product Owner.

## Files to Modify
- `common/src/db/query.rs` — Extend query builder to support `@@` (full-text match) operator and `to_tsquery`/`plainto_tsquery` construction, replacing or supplementing existing `LIKE`-based search
- `modules/search/src/service/mod.rs` — Update SearchService to use full-text query operators when performing searches, falling back to `ILIKE` for simple substring queries

## Files to Create
- `migration/src/m20250101_000001_add_search_indexes.rs` — SeaORM migration that adds `tsvector` columns and GIN indexes to searchable tables, plus a trigger to keep `tsvector` columns in sync with source text columns

## Implementation Notes
- Per the repo's CONVENTIONS.md, the project uses SeaORM for database access. Migrations should follow the existing SeaORM migration pattern found in the `migration/src/` directory.
- Per the repo's CONVENTIONS.md, error handling uses `Result<T, AppError>` with `.context()`. The migration and query builder changes must follow this pattern.
- Use `sea_orm_migration::prelude::*` for migration definitions.
- The GIN index creation should use `CREATE INDEX CONCURRENTLY` if possible to avoid locking the table during creation on production databases. ASSUMPTION (pending clarification): Whether `CONCURRENTLY` is supported depends on how migrations are run in the deployment pipeline.
- The `tsvector` column should be populated via a PostgreSQL trigger (`tsvector_update_trigger`) so that it stays in sync with the source columns automatically.
- ASSUMPTION (pending clarification): The specific tables and columns to index are not defined in the feature. This task assumes indexing the primary searchable entity tables based on the existing data model.

## Acceptance Criteria
- [ ] A new SeaORM migration exists that adds `tsvector` columns and GIN indexes to searchable tables
- [ ] The migration runs successfully against a clean PostgreSQL database
- [ ] The migration is idempotent (can be re-run without error via SeaORM's migration framework)
- [ ] `common/src/db/query.rs` supports constructing full-text search queries using `@@` and `to_tsquery`
- [ ] `SearchService` uses full-text search operators for text queries when `tsvector` columns are available
- [ ] Existing search functionality is not broken (backward-compatible)

## Test Requirements
- [ ] Migration test: migration applies cleanly on a fresh PostgreSQL instance and rolls back without error
- [ ] Query builder test: verify that the generated SQL contains `@@` and `to_tsquery` when full-text search is used
- [ ] Integration test in `tests/api/search.rs`: verify that search queries return results after the migration is applied
