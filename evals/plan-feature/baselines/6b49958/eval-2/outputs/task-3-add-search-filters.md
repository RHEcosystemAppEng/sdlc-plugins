## Repository
trustify-backend

## Target Branch
main

## Description
Add filter parameters to the `GET /api/v2/search` endpoint so users can narrow search results by entity type, severity, and date range. This addresses the "Add filters — Some kind of filtering capability" requirement.

**Assumption (pending clarification):** The feature description says "some kind of filtering capability" without specifying which fields or filter types. This task implements three filters inferred from the existing data model:
1. **Entity type filter** (`type`): filter by sbom, advisory, or package — since the search spans multiple entity types
2. **Severity filter** (`severity`): filter advisories by severity level — since `AdvisorySummary` includes a severity field
3. **Date range filter** (`from`/`to`): filter by creation or modification date — since entities have timestamp fields

If additional filters are needed, they should be specified by the product owner.

**Assumption (pending clarification):** Filter parameters are assumed to be query string parameters (not request body), consistent with the existing GET endpoint pattern. Multiple severity values are accepted as comma-separated values.

## Files to Modify
- `modules/search/src/service/mod.rs` — extend `SearchService` to accept filter parameters and apply them as WHERE clauses alongside the full-text search query
- `modules/search/src/endpoints/mod.rs` — add query parameter extraction for `type`, `severity`, `from`, and `to` filter parameters to the `GET /api/v2/search` handler

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters:
  - `type` (string, optional): filter by entity type (`sbom`, `advisory`, `package`)
  - `severity` (string, optional): filter advisories by severity (e.g., `critical`, `high`, `medium`, `low`)
  - `from` (ISO 8601 datetime, optional): filter entities created/modified on or after this date
  - `to` (ISO 8601 datetime, optional): filter entities created/modified on or before this date
  - All parameters are optional — omitting them returns unfiltered results (backward-compatible)

## Implementation Notes
- Inspect `modules/search/src/endpoints/mod.rs` to understand the current query parameter extraction pattern before adding new parameters
- Use Axum's `Query<T>` extractor with a filter struct to deserialize query parameters, following the pattern used in other list endpoints (e.g., `modules/fundamental/src/sbom/endpoints/list.rs`)
- Leverage the shared query builder helpers in `common/src/db/query.rs` for constructing filter WHERE clauses — these helpers already support filtering and pagination patterns
- For entity type filtering, the SearchService needs to conditionally join/query only the specified entity tables
- For severity filtering, apply a WHERE clause on the advisory severity field from `entity/src/advisory.rs` (`AdvisorySummary` includes severity)
- For date range filtering, use standard SQL `>=` and `<=` comparisons on timestamp columns
- Follow the error handling pattern: return `Result<T, AppError>` with `.context()` wrapping per `common/src/error.rs`
- Invalid filter values (e.g., unknown entity type) should return HTTP 400 with a descriptive error message

## Reuse Candidates
- `common/src/db/query.rs` — query builder helpers already implement filtering and pagination patterns that should be reused for the new filter parameters
- `modules/fundamental/src/sbom/endpoints/list.rs` — example of query parameter extraction with Axum's `Query<T>` extractor
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition that the severity filter will match against

## Acceptance Criteria
- [ ] `GET /api/v2/search?type=advisory` returns only advisory entities
- [ ] `GET /api/v2/search?severity=critical` returns only advisories with critical severity
- [ ] `GET /api/v2/search?from=2024-01-01T00:00:00Z&to=2024-12-31T23:59:59Z` returns only entities within the date range
- [ ] Multiple filters can be combined (e.g., `?type=advisory&severity=high`)
- [ ] Omitting all filter parameters returns the same results as before (backward-compatible)
- [ ] Invalid filter values return HTTP 400 with a descriptive error message
- [ ] Existing integration tests in `tests/api/search.rs` continue to pass

## Test Requirements
- [ ] Integration test: filter by entity type returns only entities of the specified type
- [ ] Integration test: filter by severity returns only advisories matching the severity
- [ ] Integration test: filter by date range returns only entities within the range
- [ ] Integration test: combined filters (type + severity) returns correctly intersected results
- [ ] Integration test: invalid filter value (e.g., `type=unknown`) returns HTTP 400
- [ ] Integration test: no filters returns all results (backward compatibility)
- [ ] Regression: all existing tests in `tests/api/search.rs` continue to pass

## Dependencies
- Depends on: Task 2 — Refactor search relevance ranking (filters should be applied alongside the full-text search, not to a separate code path)

[sdlc-workflow] Description digest: sha256:519278771ef0d8f65851ce0577053b459b8eb80c25b1cef40f7e5b4da091c645
