## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capability to the search endpoint so users can narrow search results by entity type and key attributes. This addresses the "Add filters" requirement by introducing query parameters that allow filtering by entity type, severity (for advisories), and date range.

**Assumptions pending clarification:**
- Assumes filters are passed as query parameters on `GET /api/v2/search` (e.g., `?type=advisory&severity=high`)
- Assumes the following filter fields as a reasonable starting set: entity type (sbom, advisory, package), severity (for advisories), and created-date range — no specific filter fields were defined in the requirements
- Assumes filters combine with AND semantics (all specified filters must match)
- Assumes filters are optional and the endpoint continues to return unfiltered results when no filter parameters are provided

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters `type` (entity type filter: sbom, advisory, package), `severity` (advisory severity filter), `date_start` and `date_end` (created-date range filter)

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add filter query parameter parsing and pass filter criteria to SearchService
- `modules/search/src/service/mod.rs` — Accept filter criteria and apply them as WHERE clauses in the search query
- `common/src/db/query.rs` — Add reusable filter builder helpers for entity-type, severity, and date-range filtering

## Implementation Notes
Parse filter parameters from the request query string in `modules/search/src/endpoints/mod.rs`. Define a `SearchFilters` struct to hold the optional filter values and deserialize from query parameters using Axum extractors.

In `modules/search/src/service/mod.rs`, apply filters as additional WHERE conditions on the search query. Use SeaORM's `Condition` builder to chain filter predicates.

Extend the shared query helpers in `common/src/db/query.rs` with reusable filter functions for:
- Entity type filtering (enum-based equality check)
- Severity filtering (match against `AdvisorySummary.severity` field from `modules/fundamental/src/advisory/model/summary.rs`)
- Date range filtering (BETWEEN on created timestamp)

Follow the existing pagination and sorting patterns in `common/src/db/query.rs` to maintain consistency.

All handlers must return `Result<T, AppError>` with `.context()` wrapping per `common/src/error.rs`.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — Extend with filter predicates, following existing filtering pattern
- `common/src/model/paginated.rs::PaginatedResults<T>` — Reuse for filtered result responses
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference severity field for severity filter values

## Acceptance Criteria
- [ ] Search endpoint accepts optional `type` parameter to filter by entity type (sbom, advisory, package)
- [ ] Search endpoint accepts optional `severity` parameter to filter advisory results by severity level
- [ ] Search endpoint accepts optional `date_start` and `date_end` parameters for date range filtering
- [ ] Filters combine with AND semantics when multiple are specified
- [ ] Omitting all filters returns the same results as the current unfiltered behavior
- [ ] Invalid filter values return appropriate error responses

## Test Requirements
- [ ] Integration test in `tests/api/search.rs` verifying entity type filter returns only matching entity types
- [ ] Integration test verifying severity filter correctly filters advisory results
- [ ] Integration test verifying date range filter returns results within the specified range
- [ ] Integration test verifying multiple filters combine correctly
- [ ] Integration test verifying the endpoint works without any filters (backward compatibility)
