# Task 1 — Add database indexes for search-relevant columns

## Repository
trustify-backend

## Target Branch
main

## Description
Create a database migration to add indexes on columns commonly used in full-text search queries. The SearchService performs full-text search across SBOMs, advisories, and packages, but the underlying tables lack indexes on the text columns used for matching. Adding appropriate indexes (GIN indexes for full-text search, B-tree indexes for filtering columns) will reduce query execution time for the search endpoint.

This addresses the "Search should be faster" requirement from TC-9002. Note: the feature does not specify quantified performance targets, so this task focuses on standard indexing best practices for PostgreSQL full-text search.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New migration to create GIN and B-tree indexes on search-relevant columns across SBOM, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration runner

## Implementation Notes
- Create GIN indexes on text columns used for full-text search (e.g., SBOM name/description, advisory title/description, package name)
- Create B-tree indexes on columns likely used for filtering (e.g., advisory severity, SBOM creation timestamp)
- Follow the SeaORM migration pattern established in `migration/src/m0001_initial/mod.rs`
- Use `Index::create()` for index creation, consistent with SeaORM conventions
- Ensure all indexes use `IF NOT EXISTS` semantics for idempotent migrations
- Per CONVENTIONS.md §Framework: use SeaORM migration patterns for schema changes.
  Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's migration file scope.
- Per CONVENTIONS.md §Module pattern: follow the established migration module structure in `migration/src/`.
  Applies: task modifies `migration/src/lib.rs` matching the convention's Rust module scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Existing migration demonstrating the SeaORM migration pattern (table creation, column definitions); follow this pattern for index creation syntax
- `entity/src/sbom.rs` — SBOM entity definition; reference column names for index targets
- `entity/src/advisory.rs` — Advisory entity definition; reference column names (including severity field) for index targets
- `entity/src/package.rs` — Package entity definition; reference column names for index targets

## Acceptance Criteria
- [ ] A new migration module `m0002_search_indexes` exists and is registered in `migration/src/lib.rs`
- [ ] GIN indexes are created on text columns used for full-text search on SBOM, advisory, and package tables
- [ ] B-tree indexes are created on columns used for filtering (severity, timestamps)
- [ ] Migration runs successfully against a PostgreSQL test database without errors
- [ ] Migration is idempotent (can be run multiple times without failure)
- [ ] Existing search functionality continues to work after migration

## Test Requirements
- [ ] Migration applies cleanly on a fresh database
- [ ] Migration applies cleanly on a database with existing data
- [ ] Rollback (down migration) drops the created indexes without affecting tables
- [ ] Search endpoint returns correct results after migration (no regression)

## Verification Commands
- `cargo run --bin migration -- up` — Migration completes without errors
- `psql -c "\di" | grep search` — Newly created indexes appear in the index listing

## Dependencies
- None (this is the first task; no dependencies on other tasks)
