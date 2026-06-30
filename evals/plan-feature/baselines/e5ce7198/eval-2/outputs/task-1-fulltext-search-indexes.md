# Task 1: Add Full-Text Search Indexes via Database Migration

**Parent Feature**: TC-9002 — Improve search experience

## Repository
trustify-backend

## Target Branch
main

## Description
Create a database migration that adds PostgreSQL full-text search (tsvector) indexes on key searchable columns across the SBOM, advisory, and package entities. The current search is slow because it relies on LIKE/ILIKE queries without index support. Adding GIN indexes on tsvector columns will enable PostgreSQL's built-in full-text search engine, dramatically improving query performance.

**Ambiguity flag (assumption pending clarification):** The feature description states "search should be faster" but provides no latency targets or baseline measurements. This task assumes that the primary performance bottleneck is the lack of full-text search indexes, and that PostgreSQL tsvector/GIN indexes are the appropriate solution. The acceptable query latency threshold is assumed to be under 200ms for typical searches (p95). These assumptions should be validated with the product owner.

**Ambiguity flag (assumption pending clarification):** The feature does not specify which entity types need search improvements. This task assumes all three searchable entity types (SBOMs, advisories, packages) require full-text indexing, based on the existing `SearchService` in `modules/search/src/service/mod.rs` which searches across entities.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New migration module that adds tsvector columns and GIN indexes to sbom, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module m0002_search_indexes
- `entity/src/sbom.rs` — Add search_vector tsvector column to the SBOM entity definition
- `entity/src/advisory.rs` — Add search_vector tsvector column to the Advisory entity definition
- `entity/src/package.rs` — Add search_vector tsvector column to the Package entity definition

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for migration structure and naming
- Use PostgreSQL `tsvector` columns with `GIN` indexes for full-text search support
- Create a trigger function to auto-populate tsvector columns on INSERT/UPDATE so search vectors stay in sync with source data
- For SBOMs: index the name/title and description fields
- For Advisories: index the title, description, and severity fields
- For Packages: index the name, version, and license fields
- Use `to_tsvector('english', ...)` for English language stemming support
- The SeaORM entity definitions in `entity/src/` must be updated to include the new tsvector columns

Per CONVENTIONS.md §Framework: use SeaORM for database entity definitions.
Applies: task modifies `entity/src/sbom.rs` matching the convention's SeaORM database scope.

Per CONVENTIONS.md §Module pattern: follow `model/ + service/ + endpoints/` structure.
Applies: convention has no file-type restriction (broadly applicable).

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `migration/src/lib.rs` matching the convention's `.rs` scope.

## Acceptance Criteria
- [ ] Migration creates tsvector columns on sbom, advisory, and package tables
- [ ] GIN indexes are created on all tsvector columns
- [ ] Trigger functions auto-populate tsvector columns on INSERT and UPDATE
- [ ] Migration runs successfully against a clean database
- [ ] Migration runs successfully as an upgrade on an existing database with data
- [ ] SeaORM entity definitions reflect the new tsvector columns

## Test Requirements
- [ ] Migration up/down executes without errors on a test PostgreSQL database
- [ ] Inserting a new SBOM record auto-populates the search_vector column
- [ ] Updating an advisory record updates the search_vector column
- [ ] GIN index is used by the query planner (verify via EXPLAIN ANALYZE)

## Verification Commands
- `cargo test -p migration` — migration tests pass
- `cargo test -p entity` — entity compilation succeeds with new columns

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Normal"}, "fixVersions": [{"name": "RHTPA 1.6.0"}]}

[sdlc-workflow] Description digest: sha256-md:ed4948aa29ebad759ca63bde62c19fab14c0c736b783c8a0a5864d3f6812ddce
