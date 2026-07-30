## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint (`GET /api/v2/search`). Users should be able to narrow search results using filter parameters. This extends both the search endpoint to accept filter query parameters and the SearchService to apply filter criteria to the underlying query.

**Assumption pending clarification:** The feature description specifies "Some kind of filtering capability" without defining which filters to support. This task assumes implementing the following baseline filters, following the existing query builder pattern in `common/src/db/query.rs`:
- **Entity type filter** — filter results by entity type (sbom, advisory, package)
- **Date range filter** — filter results by creation or modification date range

These filter choices are assumptions pending stakeholder clarification on the desired filter set.

**Assumption pending clarification:** It is unclear whether filters should use AND semantics (all filters must match) or support OR/mixed semantics. This task assumes AND semantics as the simpler default.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameters to the `GET /api/v2/search` endpoint handler
- `modules/search/src/service/mod.rs` — extend SearchService to accept and apply filter criteria to the search query
- `common/src/db/query.rs` — extend shared query builder helpers if new filter types are not already supported
- `tests/api/search.rs` — add integration tests for filtered search

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters for filtering:
  - `entity_type` (string, optional) — filter by entity type: `sbom`, `advisory`, `package`
  - `created_after` (ISO 8601 date, optional) — filter results created after this date
  - `created_before` (ISO 8601 date, optional) — filter results created before this date

## Implementation Notes
- Inspect the existing filter/query parameter handling in `common/src/db/query.rs` to understand the established pattern for adding filters. The existing query builder supports filtering, pagination, and sorting — extend this pattern for search-specific filters.
- Look at how other endpoints handle query parameters — for example, `modules/fundamental/src/sbom/endpoints/list.rs` (GET /api/v2/sbom) demonstrates the pattern for extracting query parameters in Axum handlers and passing them to the service layer.
- The filter parameters should be extracted using Axum's query parameter extraction in the endpoint handler, then passed to the `SearchService` which applies them as WHERE clauses in the search query.
- Ensure filter parameters are optional — omitting a filter should not change existing search behavior (backward compatibility).
- Use the existing `AppError` enum from `common/src/error.rs` for invalid filter parameter validation errors (e.g., invalid date format, unknown entity type).
- Entity type filtering should map to the entity tables discovered during search — check how `modules/search/src/service/mod.rs` currently joins or unions across entity types (sbom, advisory, package).

Per CONVENTIONS.md (Key Conventions) - Error handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust handler file scope.

Per CONVENTIONS.md (Key Conventions) - Endpoint registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint registration scope.

Per CONVENTIONS.md (Key Conventions) - Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint response scope.

Per CONVENTIONS.md (Key Conventions) - Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`. Applies: task modifies `common/src/db/query.rs` matching the convention's query helper scope.

Per CONVENTIONS.md (Key Conventions) - Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `common/src/db/query.rs::filtering helpers` — existing shared filter infrastructure that should be extended rather than reimplemented for search-specific filters
- `common/src/model/paginated.rs::PaginatedResults<T>` — filtered results must continue to use the standard paginated response wrapper
- `common/src/error.rs::AppError` — use existing error enum for filter validation errors
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates the established pattern for query parameter extraction in Axum handlers

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?created_after=2024-01-01` returns only results created after the specified date
- [ ] Combining multiple filters narrows results (AND semantics)
- [ ] Omitting all filter parameters returns the same results as before (backward compatibility)
- [ ] Invalid filter values return an appropriate error response
- [ ] Filtered results work correctly with pagination
- [ ] Error handling follows the `Result<T, AppError>` pattern with `.context()` wrapping

## Test Requirements
- [ ] Integration test: search with `entity_type=sbom` returns only SBOMs
- [ ] Integration test: search with `entity_type=advisory` returns only advisories
- [ ] Integration test: search with date range filter returns only results within the range
- [ ] Integration test: search with combined filters (entity type + date range) returns correctly narrowed results
- [ ] Integration test: search with no filters returns same results as before (backward compatibility)
- [ ] Integration test: search with invalid filter value returns error status
- [ ] Existing search integration tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test --test search` — run search integration tests, expected: all pass
- `cargo build` — verify compilation, expected: success with no errors

## Dependencies
- None
