## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration that introduces full-text search support for the three searchable entity types (SBOMs, advisories, and packages). This migration creates `tsvector` columns on the `sbom`, `advisory`, and `package` tables and adds GIN indexes to enable efficient full-text search queries. This is the foundational data layer change required before the SearchService can be optimized to use full-text search in subsequent tasks.

**Ambiguity note:** The exact fields to include in each `tsvector` column are assumed based on the entity structures discovered in the repository. This assumption is pending clarification from the product owner — see the impact map for details.

## Files to Create
- `migration/src/m0002_full_text_search/mod.rs` — Migration module that adds `search_vector` columns of type `tsvector` to the `sbom`, `advisory`, and `package` tables, creates GIN indexes on each, and adds trigger functions to keep the vectors in sync on INSERT/UPDATE

## Files to Modify
- `migration/src/lib.rs` — Register the new `m0002_full_text_search` migration module

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for module structure, table alteration syntax, and registration in `lib.rs`.
- Add a `search_vector` column of type `tsvector` to each of the three entity tables:
  - `sbom` (entity defined in `entity/src/sbom.rs`) — include SBOM name/title fields in the tsvector
  - `advisory` (entity defined in `entity/src/advisory.rs`) — include advisory title, description, and severity fields (reference `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` which includes a severity field)
  - `package` (entity defined in `entity/src/package.rs`) — include package name and license fields (reference `PackageSummary` in `modules/fundamental/src/package/model/summary.rs` which includes a license field)
- Create GIN indexes on each `search_vector` column for efficient full-text search lookups.
- Add PostgreSQL trigger functions (using `tsvector_update_trigger` or a custom `CREATE FUNCTION`) to automatically populate and update the `search_vector` column on INSERT and UPDATE.
- Use the `'english'` text search configuration for the tsvector columns.
- Include a data backfill step in the migration to populate `search_vector` for existing rows.
- The project uses SeaORM for database access — ensure the migration is compatible with SeaORM's migration runner.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Existing migration module to follow for structure, table creation/alteration syntax, and registration pattern in `lib.rs`
- `common/src/db/query.rs` — Shared query builder helpers; review to understand how queries are constructed so the tsvector columns integrate smoothly with existing query patterns

## Acceptance Criteria
- [ ] A new migration module exists at `migration/src/m0002_full_text_search/mod.rs`
- [ ] The migration adds a `search_vector` column of type `tsvector` to the `sbom`, `advisory`, and `package` tables
- [ ] GIN indexes are created on each `search_vector` column
- [ ] Trigger functions automatically update `search_vector` on row insert and update
- [ ] Existing rows are backfilled with correct `search_vector` values during migration
- [ ] The migration is registered in `migration/src/lib.rs`
- [ ] The migration runs successfully against a PostgreSQL test database without errors
- [ ] Existing integration tests continue to pass after the migration is applied

## Test Requirements
- [ ] Verify the migration applies cleanly on a fresh database (up migration)
- [ ] Verify the migration rolls back cleanly (down migration)
- [ ] Verify that inserting a new SBOM, advisory, or package row automatically populates the `search_vector` column via the trigger
- [ ] Verify that updating a searchable field on an existing row updates the `search_vector` column

## Verification Commands
- `cargo test -p migration` — migration tests pass
- `cargo test` — all existing tests continue to pass after migration
