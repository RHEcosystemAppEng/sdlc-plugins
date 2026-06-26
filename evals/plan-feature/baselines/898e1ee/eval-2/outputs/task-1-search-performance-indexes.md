# Task 1: Add database indexes for search performance

## Repository
trustify-backend

## Target Branch
main

## Description
Add database indexes to improve search query performance. The TC-9002 feature description states that "search is slow" but provides no latency baseline or target. This task addresses the performance requirement by adding PostgreSQL GIN indexes for full-text search on the columns most commonly queried by the search service.

**Ambiguity noted:** "Search should be faster" has no quantitative target. Assumption pending clarification: we target measurable improvement via indexing, without committing to a specific SLA.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` -- New SeaORM migration that creates GIN indexes for full-text search on SBOM name/description, advisory title/description, and package name fields. Also adds a B-tree index on advisory severity and created_at timestamps for filter performance (used by Task 3).

## Files to Modify
- `migration/src/lib.rs` -- Register the new `m0002_search_indexes` migration module in the migration list.

## Implementation Notes
Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs`. The new migration module should implement `MigrationTrait` with `up` and `down` methods.

Create GIN indexes using `to_tsvector('english', column)` for full-text search columns:
- `sbom.name` and `sbom.description` (if description column exists)
- `advisory.title` and `advisory.description`
- `package.name`

Create B-tree indexes for filter/sort columns:
- `advisory.severity`
- `advisory.created_at` (or equivalent timestamp column)
- `sbom.created_at`

Per CONVENTIONS.md §Module pattern: follow `model/ + service/ + endpoints/` structure for the migration module organization. Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's Rust module scope.

Per CONVENTIONS.md §Framework: use SeaORM for database migration definitions. Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's `.rs` file scope.

## Acceptance Criteria
- [ ] New migration `m0002_search_indexes` is created and registered
- [ ] GIN indexes exist for full-text search on SBOM, advisory, and package name/title fields
- [ ] B-tree indexes exist for severity and timestamp fields
- [ ] Migration runs successfully against a clean database (`up`)
- [ ] Migration rolls back cleanly (`down`)
- [ ] Existing tests in `tests/api/search.rs` continue to pass

## Test Requirements
- [ ] Migration applies without error on a fresh database
- [ ] Migration rollback removes all created indexes
- [ ] Existing search integration tests pass with the new indexes in place

## Verification Commands
- `cargo run -p migration -- up` -- migration applies successfully
- `cargo run -p migration -- down` -- migration rolls back cleanly
- `cargo test -p tests --test search` -- existing search tests pass

[sdlc-workflow] Description digest: sha256-md:b0935e2a09f63c7e973d100a9660c60a0f412754a9342c1b71430629152d7ace
