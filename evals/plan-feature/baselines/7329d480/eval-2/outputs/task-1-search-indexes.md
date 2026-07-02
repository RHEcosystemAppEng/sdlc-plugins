# Task 1: Add database indexes for search query performance

additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Normal"}, "fixVersions": [{"name": "RHTPA 1.6.0"}] }

## Repository
trustify-backend

## Target Branch
main

## Description
Add database migration to create indexes that support full-text search performance across SBOMs, advisories, and packages. The feature TC-9002 states search is "currently too slow" but provides no performance baseline or target. This task adds GIN indexes on text columns used for search to reduce query scan times.

**Assumption**: PostgreSQL full-text search using tsvector/tsquery is the search mechanism, consistent with the existing SearchService implementation. The specific columns to index are assumed to be name/title and description fields on SBOM, advisory, and package entities, as these are the most likely full-text search targets given the data model. This assumption is pending clarification from the product owner.

**Assumption**: No specific performance target has been defined ("should be fast enough" is the only NFR). These indexes represent standard optimization; measurable targets should be established after baselining.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New migration module adding GIN indexes for full-text search on SBOM, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` — Register the new m0002_search_indexes migration module

## Implementation Notes
Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs`. The new migration should:

- Create GIN indexes on tsvector columns for the sbom, advisory, and package tables
- Use SeaORM migration traits consistent with the existing `m0001_initial` module
- Include both `up()` and `down()` methods for reversibility
- Register the new migration in `migration/src/lib.rs` by adding it to the migration list

Reference `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` for the exact column names to index.

Per CONVENTIONS.md §Framework: Use SeaORM migration API for index creation. Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's Rust syntax scope.

## Acceptance Criteria
- [ ] New migration module `m0002_search_indexes` exists and is registered in `migration/src/lib.rs`
- [ ] GIN indexes are created on text/tsvector columns for sbom, advisory, and package tables
- [ ] Migration is reversible (down() drops the indexes)
- [ ] Migration runs successfully against a PostgreSQL test database
- [ ] Existing search functionality is not broken (existing API contracts preserved)

## Test Requirements
- [ ] Migration applies cleanly on a fresh database (up direction)
- [ ] Migration rolls back cleanly (down direction)
- [ ] Existing search endpoint tests in `tests/api/search.rs` continue to pass after migration

## Verification Commands
- `cargo test -p migration` — migration compiles and unit tests pass
- `cargo test -p tests --test search` — existing search integration tests pass
