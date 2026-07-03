## Repository

trustify-backend

## Target Branch

main

## Description

Optimize search query performance to reduce response latency. The current full-text search implementation in the SearchService performs unindexed queries across entities, resulting in slow response times. This task adds database indexes on commonly searched columns and optimizes the query execution path in the search service.

**Assumption (pending clarification):** The feature description states search is "too slow" but provides no baseline metrics or target latency. This task assumes the goal is to add appropriate database indexes and optimize query construction. Specific latency targets (e.g., p95 < 200ms) should be clarified with the product owner.

**Assumption (pending clarification):** It is assumed that the search covers all three entity types (SBOMs, advisories, packages) as the existing SearchService operates across entities. If search scope should be narrowed or prioritized, this needs clarification.

Priority: Normal
Fix Versions: RHTPA 1.6.0

## Files to Modify

- `modules/search/src/service/mod.rs` — optimize query construction in SearchService, add query hints and limit result scanning
- `common/src/db/query.rs` — add index-aware query builder helpers for full-text search predicates
- `entity/src/sbom.rs` — verify and annotate indexed columns used in search
- `entity/src/advisory.rs` — verify and annotate indexed columns used in search
- `entity/src/package.rs` — verify and annotate indexed columns used in search

## Files to Create

- `migration/src/m0002_search_indexes/mod.rs` — migration to add GIN/GiST indexes on searchable text columns across sbom, advisory, and package tables

## Implementation Notes

- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for the new migration module. Register the new migration in `migration/src/lib.rs`.
- The SearchService in `modules/search/src/service/mod.rs` currently performs full-text search across entities. Refactor to use indexed columns and add `LIMIT` clauses to prevent unbounded scans.
- Use PostgreSQL GIN indexes on `tsvector` columns for full-text search, consistent with the PostgreSQL-backed architecture.
- Reuse the shared query builder helpers in `common/src/db/query.rs` rather than constructing raw SQL. Extend the module with a full-text search predicate helper if one does not exist.
- All service methods must return `Result<T, AppError>` with `.context()` wrapping, per the project error handling convention.
- Applies: task modifies `migration/src/lib.rs` matching the convention's migration registration scope.

## Acceptance Criteria

- [ ] New database migration creates indexes on searchable text columns for sbom, advisory, and package entities
- [ ] SearchService queries leverage the new indexes (no sequential scans on indexed columns)
- [ ] Search endpoint response time is measurably improved (verified via integration test timing or EXPLAIN ANALYZE)
- [ ] Existing search functionality is not broken — all current search queries return the same results
- [ ] Migration is registered in `migration/src/lib.rs` and runs successfully against a clean database

## Test Requirements

- [ ] Add performance-oriented integration test in `tests/api/search.rs` that verifies search returns results within acceptable bounds
- [ ] Verify existing search integration tests in `tests/api/search.rs` continue to pass after index addition
- [ ] Test that the migration applies cleanly and is idempotent (can run against an already-migrated database)

## Dependencies

None — this task can proceed independently.
