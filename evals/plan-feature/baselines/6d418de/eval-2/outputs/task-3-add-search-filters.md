# Task 3 — Add filtering parameters to the search endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add query parameter-based filtering to the `GET /api/v2/search` endpoint, allowing users to narrow search results by entity type, severity level (for advisories), and date range. This addresses the MVP requirement "Add filters — some kind of filtering capability" by providing practical, commonly-needed filters that leverage existing data fields.

The filtering implementation should integrate with the shared query builder infrastructure in `common/src/db/query.rs` to ensure consistency with filtering patterns used by other endpoints (e.g., SBOM list, advisory list).

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add filter query parameters to the `GET /api/v2/search` handler (entity_type, severity, date_from, date_to)
- `modules/search/src/service/mod.rs` — Extend `SearchService` to accept and apply filter criteria to the search query

## Files to Create
- `modules/search/src/model/filter.rs` — `SearchFilter` struct defining the filter parameters (entity_type: Option<EntityType>, severity: Option<String>, date_from: Option<DateTime>, date_to: Option<DateTime>)

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters:
  - `entity_type` (string, optional) — Filter by entity type: "sbom", "advisory", "package"
  - `severity` (string, optional) — Filter advisory results by severity level (e.g., "critical", "high", "medium", "low")
  - `date_from` (ISO 8601 datetime, optional) — Filter results created/modified after this date
  - `date_to` (ISO 8601 datetime, optional) — Filter results created/modified before this date
  - All parameters are optional; when omitted, no filtering is applied (current behavior preserved)

## Implementation Notes
- Use the shared query builder helpers from `common/src/db/query.rs` for integrating filters with the search query. This module already provides filtering, pagination, and sorting infrastructure used by other endpoints
- Follow the pattern used in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` for extracting query parameters via Axum extractors
- The `entity_type` filter should restrict which entity tables are queried (e.g., if entity_type=advisory, only search the advisory table)
- The `severity` filter applies only to advisory entities — if combined with a non-advisory entity_type filter, it should be ignored or return empty results
- Date range filtering should use the entity's created/modified timestamp columns
- Validate date ranges: if date_from > date_to, return a 400 Bad Request with a descriptive error message
- Use `AppError` from `common/src/error.rs` for validation error responses
- The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a severity field — use this as reference for the severity filter values
- Per docs/constraints.md section 5.4: reuse the existing filtering infrastructure from `common/src/db/query.rs` rather than implementing custom filtering logic

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder with filtering helpers; primary reuse target for filter integration
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct with severity field; reference for valid severity values
- `modules/fundamental/src/sbom/endpoints/list.rs` — Example of query parameter extraction pattern in Axum endpoint handlers
- `modules/fundamental/src/advisory/endpoints/list.rs` — Another endpoint handler demonstrating filter parameter patterns

## Acceptance Criteria
- [ ] Search endpoint accepts optional entity_type, severity, date_from, and date_to query parameters
- [ ] Filtering by entity_type correctly restricts results to the specified entity type
- [ ] Filtering by severity correctly narrows advisory results by severity level
- [ ] Date range filtering returns only results within the specified range
- [ ] All filter parameters are optional — omitting all filters returns unfiltered results (backward compatible)
- [ ] Invalid filter values (e.g., unknown entity_type, invalid date format) return 400 Bad Request
- [ ] Filters can be combined (e.g., entity_type=advisory&severity=critical&date_from=2024-01-01)

## Test Requirements
- [ ] Test search with entity_type filter returns only entities of that type
- [ ] Test search with severity filter returns only advisories matching the severity
- [ ] Test search with date range filters returns only results within the range
- [ ] Test search with combined filters returns correctly intersected results
- [ ] Test that omitting all filters returns the same results as the unfiltered search
- [ ] Test that invalid entity_type returns 400
- [ ] Test that date_from > date_to returns 400

## Verification Commands
- `cargo test -p search` — all search module tests pass
- `cargo test -p tests -- search` — integration tests pass
- `curl "http://localhost:8080/api/v2/search?q=test&entity_type=advisory&severity=critical"` — returns only critical advisories matching "test"

## Dependencies
- Depends on: Task 2 — Implement ranked full-text search in SearchService
