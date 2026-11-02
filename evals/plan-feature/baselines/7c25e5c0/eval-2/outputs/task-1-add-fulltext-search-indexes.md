## Repository
trustify-backend

## Target Branch
main

## Description
Add PostgreSQL full-text search indexes (GIN) on searchable text columns to improve search query performance. This migration adds `tsvector` columns and GIN indexes to the SBOM, advisory, and package entities, enabling efficient full-text search queries using PostgreSQL's built-in text search capabilities.

**Assumption pending clarification:** The feature description states search is "currently too slow" but provides no performance baseline or target latency. This task assumes the bottleneck is the lack of database-level full-text search indexes. If profiling reveals a different bottleneck (e.g., application-level inefficiency, connection pool exhaustion), this approach may need revision.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — new migration adding `tsvector` columns and GIN indexes to SBOM, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration runner

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and SeaORM migration trait implementation.
- Add `tsvector` generated columns on searchable text fields (e.g., SBOM name/version, advisory title/description, package name/namespace).
- Create GIN indexes on the generated `tsvector` columns using `Index::create()`.
- Use `to_tsvector('english', ...)` for English language stemming; consider `'simple'` configuration if multi-language support is needed (assumption pending clarification — no language requirements specified).
- Per docs/constraints.md §5 (Code Change Rules): keep changes scoped to the migration; do not modify service or endpoint code in this task.

## Acceptance Criteria
- [ ] Migration creates `tsvector` generated columns on SBOM, advisory, and package tables
- [ ] GIN indexes are created on all `tsvector` columns
- [ ] Migration runs successfully against a clean database
- [ ] Migration runs successfully against a database with existing data (backward compatible)
- [ ] Existing integration tests in `tests/api/search.rs` continue to pass

## Test Requirements
- [ ] Migration up and down operations execute without errors
- [ ] Verify GIN indexes exist after migration using `\di` or equivalent query
- [ ] Existing `tests/api/search.rs` tests pass without modification (regression check)

## Dependencies
- None
