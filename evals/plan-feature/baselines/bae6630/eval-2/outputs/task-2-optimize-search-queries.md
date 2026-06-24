## Repository
trustify-backend

## Target Branch
main

## Description
Optimize the SearchService query execution to use the new full-text search indexes from Task 1 instead of naive LIKE/ILIKE queries. The feature requirement says search is "too slow" but provides no measurable latency target (see Ambiguity 1 in impact map). This task replaces the current query pattern with PostgreSQL `to_tsquery` to leverage GIN indexes, which should significantly reduce query time for text searches.

## Files to Modify
- `modules/search/src/service/mod.rs` — Refactor `SearchService` to use `to_tsquery`/`plainto_tsquery` instead of LIKE-based pattern matching. Update the search method to build `tsvector @@ tsquery` conditions for each entity type (SBOMs, advisories, packages).
- `common/src/db/query.rs` — Add a shared full-text search query builder helper that constructs `tsquery` conditions, following the existing pattern of filter/pagination/sorting helpers in this file. This helper should accept a search term and return the appropriate `tsvector @@ tsquery` condition.

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Refactor it to use PostgreSQL native full-text search: `WHERE to_tsvector('english', name || ' ' || description) @@ plainto_tsquery('english', $1)`
- Add a `full_text_search` helper function in `common/src/db/query.rs` alongside the existing query builder helpers (filtering, pagination, sorting). This follows the project convention of keeping shared query logic in `common/src/db/`.
- Use `plainto_tsquery` for simple user input (handles spaces and basic terms) and `to_tsquery` for advanced queries if needed
- All handlers must continue to return `Result<T, AppError>` with `.context()` wrapping per project error handling convention
- **Assumption (pending clarification):** The current search implementation uses LIKE/ILIKE queries. If it already uses a different mechanism, the optimization approach may need adjustment.
- **Assumption (pending clarification):** Search should cover all three entity types (SBOMs, advisories, packages) in a single query. The feature does not specify whether results should be unified or per-entity.

## Acceptance Criteria
- [ ] `SearchService` in `modules/search/src/service/mod.rs` uses `tsvector @@ tsquery` for text matching
- [ ] New `full_text_search` helper exists in `common/src/db/query.rs`
- [ ] Search queries utilize the GIN indexes created in Task 1
- [ ] GET `/api/v2/search` continues to work with existing query parameters (backward compatible)
- [ ] Error handling follows `Result<T, AppError>` with `.context()` pattern

## Test Requirements
- [ ] Existing tests in `tests/api/search.rs` continue to pass with the optimized queries
- [ ] Add a test verifying that full-text search returns results for partial word matches
- [ ] Add a test verifying that search with no results returns an empty `PaginatedResults` (not an error)

## Dependencies
- Depends on: Task 1 — Add search indexes (GIN indexes must exist for optimized queries to function)

## Digest
[sdlc-workflow] Description digest: sha256-md:ca4e56c7c344f93ecb2044bfa67bcc86a5fa1c3a6007ab97d63330d6f87d8756
