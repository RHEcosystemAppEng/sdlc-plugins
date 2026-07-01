## Repository
trustify-backend

## Target Branch
main

## Description
Optimize search query performance by adding a PostgreSQL GIN index for full-text search and refactoring the search service to use indexed queries. The feature requirement states search is "too slow" but provides no baseline or target metrics. **Assumption pending clarification**: we target sub-500ms p95 response time for typical search queries using PostgreSQL full-text search indexing.

## Files to Create
- `migration/src/m0002_search_gin_index/mod.rs` — New SeaORM migration adding a GIN index on searchable text columns (SBOM names, advisory titles, package names) to accelerate full-text search queries

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module `m0002_search_gin_index`
- `modules/search/src/service/mod.rs` — Refactor `SearchService` to use `to_tsvector`/`to_tsquery` with the GIN index instead of naive LIKE/ILIKE pattern matching
- `common/src/db/query.rs` — Add a full-text search query builder helper that generates `tsvector @@ tsquery` predicates, consistent with existing query helpers for filtering and pagination

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for migration structure and registration.
- The migration should create a GIN index using `CREATE INDEX ... USING gin(to_tsvector('english', column))` on relevant entity columns.
- In `modules/search/src/service/mod.rs`, replace any LIKE-based search with `to_tsvector('english', column) @@ plainto_tsquery('english', :query)` for indexed full-text search.
- Add a `full_text_search` helper function in `common/src/db/query.rs` alongside the existing filtering, pagination, and sorting helpers. This function should construct the tsvector/tsquery predicate for reuse across modules.
- All query functions must return `Result<T, AppError>` with `.context()` wrapping, following the error handling pattern used throughout the codebase.
- Per CONVENTIONS.md: follow the SeaORM migration pattern for database schema changes.
  Applies: task creates `migration/src/m0002_search_gin_index/mod.rs` matching the convention's `.rs` migration file scope.
- Per CONVENTIONS.md: use shared query helpers from `common/src/db/query.rs`.
  Applies: task modifies `common/src/db/query.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs::query` — Shared query builder helpers for filtering, pagination, and sorting; the new full-text search helper should follow the same pattern
- `common/src/error.rs::AppError` — Error type for wrapping database errors with context

## Acceptance Criteria
- [ ] GIN index migration runs successfully against PostgreSQL
- [ ] Search queries use the GIN index (verified via EXPLAIN ANALYZE)
- [ ] `SearchService` returns results using full-text search ranking instead of LIKE matching
- [ ] Existing search API contract (`GET /api/v2/search`) is preserved — no breaking changes to request/response format
- [ ] Query helper in `common/src/db/query.rs` is reusable by other modules

## Test Requirements
- [ ] Migration applies and rolls back cleanly in test database
- [ ] `SearchService` returns correct results for exact and partial text matches
- [ ] Performance regression test: search query completes within 500ms for a dataset of 1000+ entities (assumption pending clarification on actual performance targets)

## Verification Commands
- `cargo test -p migration` — migration tests pass
- `cargo test -p search` — search module tests pass

## Additional Fields
- priority: Normal
- fixVersions: RHTPA 1.6.0

## Description Digest
[sdlc-workflow] Description digest: sha256-md:<computed-at-creation-time>
(Actual digest computed by re-fetching description from Jira API and running `scripts/sha256-digest.py`)
