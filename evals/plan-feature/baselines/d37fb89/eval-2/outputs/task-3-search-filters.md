## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint, starting with an entity type filter. This addresses the "Add filters" requirement. Users will be able to narrow search results by specifying which entity types to include (sbom, advisory, package).

**Assumption pending clarification:** The feature description says "Some kind of filtering capability" without specifying which filters. This task implements entity type filtering as a broadly useful baseline filter. Additional filters (e.g., date range, severity, license) should be specified by the product owner before implementation.

**Assumption pending clarification:** The filter parameter format is assumed to be a query parameter `type=sbom,advisory` (comma-separated list). Alternative approaches (e.g., repeated parameters `type=sbom&type=advisory`, or a structured filter DSL) could be used instead — product/API design input is needed.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add optional `type` query parameter for entity type filtering; validate allowed values
- `modules/search/src/service/mod.rs` — Add filter logic to search query: restrict results to specified entity types when filter is provided
- `common/src/db/query.rs` — Add filter combinator helper that restricts query results by entity type

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameter `type` (comma-separated list of entity types: `sbom`, `advisory`, `package`). When omitted, all types are returned (backward compatible). When provided, only matching entity types are included in results.

## Implementation Notes
- In `modules/search/src/endpoints/mod.rs`, add an optional `type` query parameter. Parse it as a comma-separated list and validate each value against allowed entity types (`sbom`, `advisory`, `package`). Return a 400 Bad Request via `AppError` for invalid type values.
- In `modules/search/src/service/mod.rs`, accept an optional filter parameter and add a WHERE clause to restrict results by entity type when provided. When the filter is `None` or empty, return all types (preserving backward compatibility).
- In `common/src/db/query.rs`, add a reusable filter combinator that can be composed with existing query builder helpers. This should follow the same pattern as existing filtering/pagination helpers in that file.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per project conventions.

Per CONVENTIONS.md §Error handling: all handlers return Result<T, AppError> with .context() wrapping.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md §Query helpers: shared filtering, pagination, and sorting via common/src/db/query.rs.
Applies: task modifies `common/src/db/query.rs` matching the convention's query helper scope.

## Reuse Candidates
- `common/src/db/query.rs` — Existing query builder helpers for filtering and pagination. The entity type filter should compose with these existing helpers.
- `common/src/error.rs::AppError` — Error type for returning 400 Bad Request on invalid filter values.

## Acceptance Criteria
- [ ] GET /api/v2/search accepts an optional `type` query parameter
- [ ] When `type` is omitted, all entity types are returned (backward compatible)
- [ ] When `type=sbom` is provided, only SBOM results are returned
- [ ] When `type=sbom,advisory` is provided, only SBOM and advisory results are returned
- [ ] Invalid type values return a 400 Bad Request with a descriptive error message
- [ ] Filtering composes correctly with relevance ranking (filtered results are still ranked)
- [ ] Filtering composes correctly with pagination

## Test Requirements
- [ ] Search with `type=sbom` returns only SBOM results
- [ ] Search with `type=advisory,package` returns only advisory and package results
- [ ] Search without `type` parameter returns all entity types (backward compatibility)
- [ ] Search with invalid `type=invalid` returns 400 Bad Request
- [ ] Filtered search results maintain relevance ranking order
- [ ] Pagination works correctly with filtered results

## Dependencies
- Depends on: Task 2 — Implement relevance-ranked search in SearchService

[sdlc-workflow] Description digest: sha256-md:a60fb995d9c3af32aebe2c92ad1ed654a4bc315c378dbc5a361502f78d8aeda2
