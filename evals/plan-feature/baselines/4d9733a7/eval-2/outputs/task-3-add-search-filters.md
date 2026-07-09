## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint so users can narrow search results by entity type, date range, and entity-specific fields such as severity (advisories) and license (packages). The feature requirement states "Add filters — Some kind of filtering capability" (TC-9002).

**Ambiguity note:** The feature does not specify which fields should be filterable, what filter operators are needed, or whether filters should work across entity types or per-entity. The assumptions below are pending clarification:
- **Assumption:** Filters are applied as query parameters to the existing `GET /api/v2/search` endpoint.
- **Assumption:** Supported filter fields include: `entity_type` (enum: sbom, advisory, package), `created_after` / `created_before` (date range), `severity` (for advisories), and `license` (for packages).
- **Assumption:** The existing shared filtering infrastructure in `common/src/db/query.rs` will be extended rather than creating a parallel filtering mechanism.

## Files to Modify
- `modules/search/src/service/mod.rs` — extend SearchService to accept and apply filter parameters to search queries
- `modules/search/src/endpoints/mod.rs` — parse filter query parameters and pass them to the SearchService
- `common/src/db/query.rs` — extend shared query builder helpers to support the new filter types (entity_type enum filter, date range filter)
- `tests/api/search.rs` — add integration tests for filter combinations

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters: `entity_type` (string enum: sbom|advisory|package), `created_after` (ISO 8601 date), `created_before` (ISO 8601 date), `severity` (string, applies only to advisory results), `license` (string, applies only to package results). Multiple filters are combined with AND semantics.

## Implementation Notes
- Extend `common/src/db/query.rs` to support new filter types. The existing module already provides filtering, pagination, and sorting helpers — add entity_type enum filtering and date range filtering as new filter builder methods following the existing pattern.
- In the search service, apply filters as WHERE clause conditions on the search query. Entity-type filter restricts which entity tables are queried. Date range filters use `>=` / `<=` on created_at columns. Entity-specific filters (severity, license) are applied only when the matching entity type is included in results.
- Parse filter query parameters in the search endpoint handler using Axum's `Query` extractor. Define a `SearchFilters` struct with optional fields for each filter parameter.
- Per CONVENTIONS.md §Query helpers: extend the shared filtering infrastructure in `common/src/db/query.rs` rather than adding ad-hoc filtering logic in the search service. Follow the existing query builder pattern for filter composition.
  Applies: task modifies `common/src/db/query.rs` matching the convention's query helper scope.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` from the service and endpoint, wrapping filter parsing errors with `.context("Invalid search filter parameters")`.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's handler/service file scope.
- Per CONVENTIONS.md §Response types: maintain the existing `PaginatedResults<T>` response format. Filters reduce the result set but do not change the response structure.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint file scope.
- Per CONVENTIONS.md §Module pattern: keep filter-related types (e.g., `SearchFilters` struct) within the search module's model directory if they are search-specific, or in `common/` if they are reusable across modules.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/search.rs` following the existing pattern — hit the real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)`.
  Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; extend with new filter types rather than duplicating filter logic in the search module
- `common/src/model/paginated.rs::PaginatedResults<T>` — existing paginated response wrapper; reuse as-is for filtered results
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — includes severity field; reference for severity filter values
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — includes license field; reference for license filter values

## Acceptance Criteria
- [ ] Search endpoint accepts `entity_type`, `created_after`, `created_before`, `severity`, and `license` query parameters
- [ ] Filters correctly narrow the search result set (AND semantics for multiple filters)
- [ ] Entity-specific filters (severity, license) are applied only to matching entity types
- [ ] Invalid filter values return appropriate error responses (400 Bad Request with descriptive message)
- [ ] Existing search behavior is preserved when no filters are provided

## Test Requirements
- [ ] Integration test filtering by entity_type=sbom returns only SBOM results
- [ ] Integration test filtering by entity_type=advisory returns only advisory results
- [ ] Integration test filtering by date range returns only results within the range
- [ ] Integration test combining entity_type + date range filters returns correctly narrowed results
- [ ] Integration test filtering advisories by severity returns only matching advisories
- [ ] Integration test verifying invalid filter values return 400 status
- [ ] Integration test verifying unfiltered search returns all entity types (backward compatibility)

## Verification Commands
- `cargo test -p search` — verify search module tests pass
- `cargo test -p common` — verify common module tests pass (new filter helpers)
- `cargo test --test search` — verify search integration tests pass

## Dependencies
- Depends on: Task 1 — Optimize search performance (filters should operate on the optimized query infrastructure)
