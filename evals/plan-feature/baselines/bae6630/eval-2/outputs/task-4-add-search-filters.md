## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint. The feature requirement says "some kind of filtering capability" without specifying which fields, filter types, or combination logic (see Ambiguity 3 in impact map). This task implements filters for entity type, date range, and advisory severity as query parameters on the search endpoint, using AND-combination logic.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add query parameter parsing for filter fields: `entity_type` (enum: sbom, advisory, package), `severity` (enum: low, medium, high, critical), `created_after` (ISO 8601 date), `created_before` (ISO 8601 date). All filters are optional and combined with AND logic.
- `modules/search/src/service/mod.rs` — Extend `SearchService` search method to accept a filter struct and apply filter conditions to the database query. Use the shared query builder helpers from `common/src/db/query.rs` for constructing filter conditions.
- `common/src/db/query.rs` — Add filter builder functions for date range filtering and enum-based filtering, following the existing pattern of shared query helpers (filtering, pagination, sorting) in this file.

## Files to Create
- `modules/search/src/model/mod.rs` — Define a `SearchFilters` struct to hold parsed filter parameters (entity_type, severity, date range) and a `SearchResultItem` enum or struct that can represent results from different entity types. **Assumption (pending clarification):** This model structure is inferred; the search module currently has no `model/` directory, so we create one following the project's `model/ + service/ + endpoints/` module pattern.

## Implementation Notes
- Follow the existing module pattern (`model/ + service/ + endpoints/`) seen in `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/`
- Parse filter parameters using Axum extractors (`Query<SearchFilters>`) in the endpoint handler
- Use the shared `common/src/db/query.rs` helpers for constructing WHERE clauses — extend the existing filtering helpers rather than duplicating logic
- **Assumption (pending clarification):** Filters are limited to `entity_type`, `severity`, and `created_after`/`created_before`. The feature says "some kind of filtering" — additional filter fields (e.g., license, package name, SBOM author) may be needed but are not specified.
- **Assumption (pending clarification):** Severity filter applies only when searching advisories (advisories have a severity field per `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`). When entity_type is not "advisory" and a severity filter is provided, it is silently ignored.
- **Assumption (pending clarification):** Filters combine with AND logic. OR-combination is not supported in this implementation but could be added later if required.
- All filter parameters should be optional — omitting a filter means "no restriction" on that dimension
- Error handling: invalid filter values should return a 400 Bad Request via `AppError`

## Acceptance Criteria
- [ ] GET `/api/v2/search` accepts optional `entity_type`, `severity`, `created_after`, and `created_before` query parameters
- [ ] Filters combine using AND logic
- [ ] Omitting all filters returns unfiltered results (backward compatible)
- [ ] Invalid filter values return 400 Bad Request with a descriptive error message
- [ ] `SearchFilters` struct exists in `modules/search/src/model/mod.rs`
- [ ] Response continues to use `PaginatedResults<T>` from `common/src/model/paginated.rs`

## Test Requirements
- [ ] Test filtering by `entity_type=sbom` returns only SBOM results
- [ ] Test filtering by `severity=critical` returns only critical-severity advisories
- [ ] Test filtering by date range returns only results within the range
- [ ] Test combining multiple filters (e.g., `entity_type=advisory&severity=high`) returns the intersection
- [ ] Test that omitting all filters behaves identically to the existing search (backward compatibility)
- [ ] Test that invalid `entity_type` values return 400 Bad Request

## Dependencies
- None (filter support is independent of indexing/ranking changes, though it benefits from indexes in Task 1)

## Digest
[sdlc-workflow] Description digest: sha256-md:7143215e89dc47960f9ea34ddbb57a1bffae89ebed9eeff27fb8a909668b189d
