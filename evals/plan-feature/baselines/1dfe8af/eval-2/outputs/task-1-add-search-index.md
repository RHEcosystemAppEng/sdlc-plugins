## Repository
trustify-backend

## Target Branch
main

## Description
Add a PostgreSQL full-text search index to improve search query performance. The current search implementation likely performs sequential scans, which degrades as data volume grows. This migration adds GIN indexes on the text columns used by the search service to enable efficient full-text search at the database level.

**Assumption (pending clarification):** The performance target is assumed to be p95 latency under 500ms for search queries returning up to 100 results. No specific target was provided in TC-9002.

## Files to Create
- `migration/src/m0002_search_index/mod.rs` — Migration that creates GIN indexes for full-text search on SBOM name/description, advisory title/description, and package name fields

## Files to Modify
- `migration/src/lib.rs` — Register the new m0002_search_index migration module

## Implementation Notes
Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs`. The new migration module should create PostgreSQL GIN indexes using `tsvector` columns or expression indexes on the relevant text columns from the entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs`.

The SearchService in `modules/search/src/service/mod.rs` currently performs full-text search across entities. Adding database-level indexes will accelerate these queries without requiring changes to the service layer query logic itself.

**Assumption (pending clarification):** The indexed fields are assumed to be: SBOM name and description, advisory title and description, and package name. The feature does not specify which fields are searched or should be optimized.

## Acceptance Criteria
- [ ] Migration creates GIN indexes for full-text search on SBOM, advisory, and package text columns
- [ ] Migration is registered in `migration/src/lib.rs` and runs successfully against a clean database
- [ ] Migration is reversible (includes down/rollback logic)
- [ ] Existing search queries continue to work after the migration

## Test Requirements
- [ ] Migration applies cleanly on a fresh database
- [ ] Migration rolls back without errors
- [ ] Existing search integration tests in `tests/api/search.rs` still pass after the migration

## Verification Commands
- `cargo run --bin migration -- up` — migration applies without errors

[sdlc-workflow] Description digest: sha256-md:a3b1c4e7f2d890156789abcdef0123456789abcdef0123456789abcdef012345
