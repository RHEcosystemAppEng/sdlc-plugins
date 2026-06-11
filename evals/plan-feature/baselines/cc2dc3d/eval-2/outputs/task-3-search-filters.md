## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint, allowing users to narrow search results by entity type, severity level (for advisories), and date range. The feature description (TC-9002) requires "some kind of filtering capability" but does not specify which filters. This task implements the most commonly useful filters based on the available entity attributes.

**Assumption (pending clarification):** The specific filters to implement were not defined. Implementing entity type filter, severity filter, and date range filter based on available entity fields. Additional filters (e.g., license, package version) can be added in a follow-up once requirements are clarified.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add query parameters for filters (`entity_type`, `severity`, `date_from`, `date_to`) to the `GET /api/v2/search` endpoint handler; validate and pass filter parameters to the service layer
- `modules/search/src/service/mod.rs` — extend `SearchService` to accept filter parameters and apply them as WHERE clause conditions in the search query
- `common/src/db/query.rs` — add reusable filter builder helpers for enum filtering (entity type, severity) and date range filtering that can be used by other modules

## Files to Create
- `modules/search/src/model/mod.rs` — define `SearchFilter` struct to encapsulate filter parameters (entity_type, severity, date_from, date_to) and `SearchableEntityType` enum (Sbom, Advisory, Package)

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters: `entity_type` (enum: sbom, advisory, package), `severity` (enum: low, medium, high, critical), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date). All filters are optional; when multiple are provided, they combine with AND semantics.

## Implementation Notes
- The existing `common/src/db/query.rs` provides shared query builder helpers for filtering, pagination, and sorting. Extend this module with new helper functions for:
  - Enum-based filtering (e.g., `apply_entity_type_filter`) that adds a WHERE clause matching the entity type
  - Date range filtering (e.g., `apply_date_range_filter`) that adds `created_at >= date_from AND created_at <= date_to` conditions
  - Severity filtering that matches against the `severity` field on `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs`)
- Create a `SearchFilter` struct in a new `modules/search/src/model/mod.rs` file following the module pattern (`model/ + service/ + endpoints/`) established by other modules like `modules/fundamental/src/sbom/model/`.
- The `entity_type` filter determines which entity tables to search. When not provided, search across all entity types (current behavior). When provided, limit the search to the specified entity type only.
- The `severity` filter only applies when searching advisories. If `severity` is provided but `entity_type` is not set to `advisory`, either: (a) implicitly set entity_type to advisory, or (b) apply severity filter only to advisory results in a combined search. **Assumption (pending clarification):** Option (a) is used — setting severity implicitly filters to advisories only.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per the error handling convention.
- Results must use `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Use Axum's query parameter extraction (`Query<SearchParams>`) to parse filter parameters from the request URL, following the pattern in existing list endpoints like `modules/fundamental/src/sbom/endpoints/list.rs`.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting to extend with new filter types
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates query parameter extraction pattern for list/search endpoints
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct includes the severity field that the severity filter will match against
- `modules/fundamental/src/sbom/model/summary.rs` — `SbomSummary` struct; model pattern to follow for `SearchFilter`
- `common/src/error.rs` — `AppError` enum for consistent error handling

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?entity_type=package` returns only package results
- [ ] `GET /api/v2/search?severity=critical` returns only critical-severity advisories
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` returns results within the date range
- [ ] Multiple filters combine with AND semantics
- [ ] Omitting all filters returns the same results as before (backward compatible)
- [ ] Invalid filter values return appropriate error responses (400 Bad Request)

## Test Requirements
- [ ] Integration test: filter by each entity type individually and verify only matching entities are returned
- [ ] Integration test: filter by severity and verify only advisories with matching severity are returned
- [ ] Integration test: filter by date range and verify only results within the range are returned
- [ ] Integration test: combine entity_type and date_from filters and verify AND semantics
- [ ] Integration test: no filters provided returns all results (backward compatibility)
- [ ] Integration test: invalid entity_type value returns 400 Bad Request
- [ ] Integration test: invalid date format returns 400 Bad Request
- [ ] Add tests in `tests/api/search.rs` following the existing `assert_eq!(resp.status(), StatusCode::OK)` pattern

## Verification Commands
- `cargo test --test search` — search-specific integration tests pass
- `cargo test` — all tests pass without regression

## Documentation Updates
- `README.md` — document the new filter query parameters for the search endpoint

## Dependencies
- Depends on: Task 2 — Implement full-text search with relevance ranking (the filters extend the search query built by the full-text search service)
