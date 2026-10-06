# Task 3 — Add filter parameters to search endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add query parameter filters to the GET /api/v2/search endpoint so users can narrow search results by entity type, date range, and severity. The current search endpoint accepts a text query but provides no filtering capability. This task adds optional query parameters that filter results before returning them, leveraging the existing shared query builder helpers in `common/src/db/query.rs`.

This addresses the "Add filters — some kind of filtering capability" requirement from TC-9002. Note: the feature does not specify which fields should be filterable. This task implements a reasonable set based on the existing entity model fields: entity type (sbom/advisory/package), date range (created_after/created_before), and severity (for advisories).

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add query parameter extraction for filter fields (entity_type, created_after, created_before, severity); pass filter parameters to SearchService
- `modules/search/src/service/mod.rs` — Accept filter parameters in search method; apply filters to database queries before returning results

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters:
  - `entity_type` (string, optional): Filter by entity type — one of `sbom`, `advisory`, `package`
  - `created_after` (ISO 8601 datetime, optional): Return only results created after this timestamp
  - `created_before` (ISO 8601 datetime, optional): Return only results created before this timestamp
  - `severity` (string, optional): Filter advisory results by severity level (e.g., `critical`, `high`, `medium`, `low`)
  - All parameters are optional; when omitted, no filtering is applied (backward compatible)

## Implementation Notes
- Define a `SearchFilters` struct to hold the deserialized query parameters, using Axum's `Query<SearchFilters>` extractor
- Use `Option<T>` for all filter fields to make them optional
- Apply filters in the SearchService by adding `WHERE` clauses to the query builder conditionally (only when the parameter is `Some`)
- For `entity_type`, filter which entity tables are queried (e.g., skip advisory and package queries when `entity_type=sbom`)
- For date range, filter on the `created` timestamp column present on all entity types
- For `severity`, filter only advisory results using the `AdvisorySummary.severity` field
- Leverage the shared filtering helpers in `common/src/db/query.rs` for consistent filter application
- Per CONVENTIONS.md §Error handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md §Endpoint registration: register any new routes in `endpoints/mod.rs`; existing GET /api/v2/search route is modified, not added.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md §Query helpers: use shared filtering from `common/src/db/query.rs` for applying filter conditions.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md §Response types: filtered results must still be returned via `PaginatedResults<T>`.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers already implement filtering, pagination, and sorting; extend the existing filter infrastructure rather than implementing custom filter logic
- `common/src/model/paginated.rs` — PaginatedResults<T>; filtered results use the same pagination wrapper
- `modules/fundamental/src/sbom/endpoints/list.rs` — GET /api/v2/sbom list endpoint; reference for query parameter extraction pattern with Axum
- `modules/fundamental/src/advisory/model/summary.rs` — AdvisorySummary struct; includes the `severity` field used for advisory filtering

## Acceptance Criteria
- [ ] GET /api/v2/search accepts optional `entity_type` query parameter and returns only matching entity types
- [ ] GET /api/v2/search accepts optional `created_after` and `created_before` query parameters and returns only results within the date range
- [ ] GET /api/v2/search accepts optional `severity` query parameter and filters advisory results by severity
- [ ] All filter parameters are optional; omitting them returns unfiltered results (backward compatible)
- [ ] Multiple filter parameters can be combined in a single request
- [ ] Invalid filter values return appropriate error responses (400 Bad Request)
- [ ] Filtered results are returned in `PaginatedResults<T>` format

## Test Requirements
- [ ] Integration test: search with `entity_type=sbom` returns only SBOM results
- [ ] Integration test: search with `entity_type=advisory` returns only advisory results
- [ ] Integration test: search with `created_after` returns only results after the specified date
- [ ] Integration test: search with `severity=critical` returns only critical advisories
- [ ] Integration test: search with multiple filters combined returns correctly filtered results
- [ ] Integration test: search with no filters returns the same results as before (backward compatibility)
- [ ] Integration test: search with invalid `entity_type` value returns 400 error

## Verification Commands
- `cargo test --test search` — All search tests pass (including new filter tests)
- `curl "http://localhost:8080/api/v2/search?q=test&entity_type=sbom"` — Returns only SBOM results
- `curl "http://localhost:8080/api/v2/search?q=test&severity=critical"` — Returns only critical advisory results

## Dependencies
- None (filters are independent of performance optimization; can be implemented in parallel with Tasks 1–2)
