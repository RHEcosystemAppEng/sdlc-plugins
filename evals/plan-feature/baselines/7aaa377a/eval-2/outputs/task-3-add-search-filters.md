## Repository
trustify-backend

## Target Branch
main

## Description
Add filter query parameters to the search API endpoint (`GET /api/v2/search`) so that users can narrow search results by entity type, severity, and date range. The feature requirement (TC-9002) calls for "some kind of filtering capability" — this task implements filtering by the most commonly useful dimensions based on the existing data model.

The following filters will be added as optional query parameters:
- `entity_type` — filter by entity kind: `sbom`, `advisory`, or `package` (enum, optional)
- `severity` — filter advisories by severity level (string, optional; applies only when searching advisories)
- `date_from` / `date_to` — filter results by creation or modification date range (ISO 8601 date strings, optional)

All filters are optional and combinable. When no filters are provided, the endpoint behaves identically to the current implementation (backward compatible).

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameters to the `GET /api/v2/search` handler; parse and validate filter inputs; pass filters to `SearchService`
- `modules/search/src/service/mod.rs` — extend `SearchService` to accept filter parameters and apply them to the search query construction
- `common/src/db/query.rs` — add filter builder helpers for entity-type discrimination, severity matching, and date-range filtering

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `entity_type` (enum: sbom|advisory|package), `severity` (string), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date). Response shape remains `PaginatedResults<T>` unchanged.

## Implementation Notes
- Inspect the existing `GET /api/v2/search` handler in `modules/search/src/endpoints/mod.rs` to understand the current query parameter structure and Axum extractor pattern before adding new parameters.
- Use Axum's `Query<T>` extractor with an expanded search params struct to accept the new filter fields. All new fields should be `Option<T>` to maintain backward compatibility.
- For `entity_type` filtering, define an enum (`SearchEntityType`) with variants `Sbom`, `Advisory`, `Package` and use Serde's `rename_all = "lowercase"` for URL-friendly values.
- For date-range filtering, use `chrono::NaiveDate` or `chrono::DateTime<Utc>` depending on the existing date column types in the entity definitions.
- Extend `common/src/db/query.rs` to include filter builder functions following the existing pattern for pagination and sorting helpers. The new filter functions should compose with existing query builders via method chaining.
- Per Key Conventions (Error handling): all handlers return `Result<T, AppError>` with `.context()` wrapping. Apply this to any validation errors for filter parameters (e.g., invalid date format, unknown entity type).
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.
- Per Key Conventions (Response types): the endpoint must continue to return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Filters affect the query, not the response shape.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.
- Per Key Conventions (Query helpers): shared filtering logic goes in `common/src/db/query.rs`, not in the endpoint or service module. This ensures filter logic is reusable across other endpoints.
  Applies: task modifies `common/src/db/query.rs` matching the convention's `.rs` file scope.
- Per Key Conventions (Endpoint registration): verify that any new routes or modified route signatures are properly registered in `modules/search/src/endpoints/mod.rs` and mounted via `server/main.rs`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.
- Reference `modules/fundamental/src/sbom/endpoints/list.rs` for the established pattern of Axum query parameter extraction with pagination in a list endpoint.
- Reference `modules/fundamental/src/advisory/endpoints/list.rs` for the pattern of list endpoints that may include severity-based filtering.

## Reuse Candidates
- `common/src/db/query.rs` — existing query builder helpers for filtering, pagination, and sorting; extend with new filter types rather than duplicating the pattern
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper; reuse as the response type (no changes needed)
- `common/src/error.rs` — `AppError` enum; reuse for filter validation error responses
- `modules/fundamental/src/sbom/endpoints/list.rs` — `GET /api/v2/sbom` list endpoint; demonstrates the established Axum query parameter extraction pattern
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct with `severity` field; reference for severity values

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?entity_type=package` returns only package results
- [ ] `GET /api/v2/search?severity=critical` filters results to advisories with critical severity
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` returns only results within the date range
- [ ] Filters are combinable: `entity_type=advisory&severity=high` returns only high-severity advisories
- [ ] `GET /api/v2/search` without any filter parameters returns the same results as before (backward compatible)
- [ ] Invalid filter values return an appropriate error response (e.g., 400 Bad Request for an invalid entity type)
- [ ] Response shape remains `PaginatedResults<T>` for all filter combinations

## Test Requirements
- [ ] Test each filter individually: entity_type=sbom, entity_type=advisory, entity_type=package
- [ ] Test severity filter with valid severity values
- [ ] Test date range filter with valid date_from and date_to
- [ ] Test filter combinations (entity_type + severity, entity_type + date range)
- [ ] Test backward compatibility: search without filters returns expected results
- [ ] Test error cases: invalid entity_type value, invalid date format, severity on non-advisory entity type
- [ ] Verify response shape matches `PaginatedResults<T>` for all filter scenarios

## Verification Commands
- `cargo test --test search` — all search tests pass including new filter tests
- `curl "http://localhost:8080/api/v2/search?q=test&entity_type=sbom"` — returns only SBOM results
- `curl "http://localhost:8080/api/v2/search?q=test&severity=critical"` — returns only critical advisories

## Documentation Updates
- `README.md` — document the new search filter query parameters in the API section (entity_type, severity, date_from, date_to)

## Dependencies
- Depends on: Task 2 — Optimize SearchService full-text search execution (filter logic builds on the optimized query structure)
