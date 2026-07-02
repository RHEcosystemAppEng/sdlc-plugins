## Repository
trustify-backend

## Target Branch
main

## Description
Create a database migration that adds indexes on commonly searched columns to improve
search query performance. The current search is reported as "too slow" (see Ambiguity 1
in the impact map — no specific performance targets are provided). This task addresses
the database layer by ensuring that columns used in full-text search queries and
filter predicates have appropriate indexes.

**Assumption (pending clarification):** The specific columns to index are based on
the existing entity model — SBOM name/version fields, advisory title/severity fields,
and package name/license fields. The product owner should confirm which fields are
most frequently searched.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New migration module that creates indexes on search-relevant columns in sbom, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` — Register the new m0002_search_indexes migration module in the migration list

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs`.
  Each migration module implements the `MigrationTrait` with `up` and `down` methods.
- Use SeaORM's `Index::create()` to define indexes. Target columns that appear in
  WHERE clauses and full-text search predicates in `modules/search/src/service/mod.rs`.
- Recommended indexes based on entity definitions in `entity/src/`:
  - `sbom` table: index on name and version columns (see `entity/src/sbom.rs`)
  - `advisory` table: index on title and severity columns (see `entity/src/advisory.rs`)
  - `package` table: index on name column (see `entity/src/package.rs`)
- Consider adding a GIN index for full-text search if PostgreSQL `tsvector` columns
  are used (inspect `modules/search/src/service/mod.rs` for current search implementation).
- Per docs/constraints.md section 2 (Commit Rules): commit messages must follow Conventional
  Commits format and reference TC-9002 in the footer.
- Per docs/constraints.md section 5 (Code Change Rules): inspect existing migration code
  before writing new migration.

**Conventions (from Key Conventions):**

Per Key Conventions §Framework: use SeaORM for database migration definitions.
Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's Rust migration file scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Existing migration pattern to follow for structure and SeaORM migration trait implementation

## Acceptance Criteria
- [ ] New migration module `m0002_search_indexes` is created and registered in `migration/src/lib.rs`
- [ ] Indexes are created on search-relevant columns in sbom, advisory, and package tables
- [ ] Migration includes both `up` (create indexes) and `down` (drop indexes) implementations
- [ ] Existing migrations continue to run successfully (no conflicts)

## Test Requirements
- [ ] Migration runs successfully against a clean PostgreSQL test database
- [ ] Migration rollback (`down`) removes the created indexes without errors
- [ ] Existing integration tests in `tests/api/search.rs` continue to pass after migration

## Verification Commands
- `cargo test --test search` — Existing search tests pass after migration
- `cargo run --bin migration -- up` — Migration applies successfully

## Dependencies
- None

## additional_fields
- priority: Normal
- fixVersions: ["RHTPA 1.6.0"]
- labels: ["ai-generated-jira"]
---

[sdlc-workflow] Description digest: sha256-md:a2b3e89982ca7a9edebe736b8502714bad18c696b290ee35b3cea6d839af8398
