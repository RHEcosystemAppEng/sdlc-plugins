## Repository
trustify-backend

## Target Branch
main

## Description
Add database indexes on search-relevant columns and implement PostgreSQL full-text search infrastructure (tsvector/tsquery) to optimize search query performance. The current search is reported as too slow (TC-9002). This task adds the database-level optimizations needed to support fast full-text search across SBOMs, advisories, and packages.

**Ambiguity note:** No baseline performance metrics or target latency thresholds are specified in the feature. The assumption (pending clarification) is that database query execution time is the primary bottleneck, and PostgreSQL full-text search indexing is the appropriate optimization strategy.

## Files to Modify
- `migration/src/lib.rs` — register the new search index migration module
- `modules/search/src/service/mod.rs` — update SearchService to use tsvector/tsquery-based queries instead of LIKE/ILIKE patterns

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — new migration adding GIN indexes on tsvector columns for sbom, advisory, and package tables

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for migration structure and registration.
- Use PostgreSQL GIN indexes on tsvector columns for full-text search. Create tsvector columns or use expression indexes (e.g., `CREATE INDEX idx_sbom_search ON sbom USING GIN(to_tsvector('english', name || ' ' || description))`).
- Update `SearchService::search` in `modules/search/src/service/mod.rs` to use `to_tsquery` and `@@` operator instead of LIKE/ILIKE patterns for full-text matching.
- Per CONVENTIONS.md §Framework: use SeaORM for database operations and migration definitions.
  Applies: task modifies `migration/src/m0002_search_indexes/mod.rs` matching the convention's database framework scope.
- Per CONVENTIONS.md §Error handling: wrap database operations with `.context()` for descriptive error messages in the SearchService.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's handler/service file scope.
- Per CONVENTIONS.md §Module pattern: maintain the existing model/ + service/ + endpoints/ structure within the search module.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's module directory scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration pattern to follow for the new index migration
- `common/src/db/query.rs` — shared query builder helpers; check for existing full-text search utilities before creating new ones

## Acceptance Criteria
- [ ] GIN indexes are created on search-relevant text columns for sbom, advisory, and package entities
- [ ] SearchService uses tsvector/tsquery-based queries for full-text search
- [ ] Migration runs successfully against a PostgreSQL test database
- [ ] Existing search functionality is preserved (backward-compatible response shape)

## Test Requirements
- [ ] Integration test verifying the migration applies cleanly and creates the expected indexes
- [ ] Integration test verifying search queries return correct results using the new full-text search path
- [ ] Integration test verifying that existing search behavior is preserved (no regressions)

## Verification Commands
- `cargo test -p migration` — verify migration compiles and applies
- `cargo test -p search` — verify search module tests pass
- `cargo test --test search` — verify search integration tests pass

## Dependencies
- None
