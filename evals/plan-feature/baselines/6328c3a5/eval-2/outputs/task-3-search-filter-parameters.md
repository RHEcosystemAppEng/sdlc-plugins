## Repository
trustify-backend

## Target Branch
main

## Description
Add filter query parameters to the search endpoint (`GET /api/v2/search`) so users can narrow search results by entity type, date range, and severity. The current search endpoint returns unfiltered results across all entity types. This task adds structured filtering capabilities to the endpoint, allowing users to constrain results to specific subsets.

**Assumptions pending clarification:**
- The feature description says "some kind of filtering capability" without specifying which filters. The following filter dimensions are assumed: entity type (sbom, advisory, package), date range (created_after, created_before), and severity (for advisories)
- Filters combine with AND semantics (all specified filters must match)
- Filters are additive query parameters on the existing `GET /api/v2/search` endpoint, not a new endpoint
- Severity filter values correspond to the severity field on AdvisorySummary

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add query parameter extraction for filter fields (entity_type, created_after, created_before, severity); pass parsed filters to SearchService
- `modules/search/src/service/mod.rs` — Accept filter parameters in search queries; apply WHERE clauses for each active filter; integrate filters with existing query building and relevance ranking
- `common/src/db/query.rs` — Add or extend shared filter builder helpers for date range and enum filtering if not already present
- `tests/api/search.rs` — Add integration tests for each filter parameter and filter combinations

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters:
  - `entity_type` (string, optional) — filter by entity type: "sbom", "advisory", "package"
  - `created_after` (ISO 8601 datetime, optional) — return only entities created after this timestamp
  - `created_before` (ISO 8601 datetime, optional) — return only entities created before this timestamp
  - `severity` (string, optional) — filter advisories by severity level (e.g., "critical", "high", "medium", "low")
  - All filters are optional; when omitted, no filtering is applied for that dimension
  - Multiple filters combine with AND semantics

## Implementation Notes
- Use Axum's `Query<T>` extractor to parse filter parameters from the query string in `modules/search/src/endpoints/mod.rs`. Define a `SearchFilters` struct with optional fields for each filter dimension.
- In `modules/search/src/service/mod.rs`, apply filters as additional WHERE clauses on the search query. Use SeaORM's `Condition::all()` for AND composition.
- For entity type filtering, apply a discriminator condition that restricts which entity tables are queried.
- For date range filtering, use `>=` and `<=` comparisons on the `created_at` timestamp column.
- For severity filtering, apply a WHERE clause on the `severity` field of the advisory entity (see `entity/src/advisory.rs` for the AdvisorySummary struct which includes a severity field).
- Extend the shared query builder in `common/src/db/query.rs` with reusable filter helpers for date range comparisons if they do not already exist.
- Per CONVENTIONS.md "Error handling" convention: ensure filter validation errors return appropriate `AppError` responses with `.context()` wrapping.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint handler scope.
- Per CONVENTIONS.md "Response types" convention: filtered results continue to use `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's list endpoint scope.
- Per CONVENTIONS.md "Query helpers" convention: extend shared filtering helpers in `common/src/db/query.rs` for date range and enum-based filtering.
  Applies: task modifies `common/src/db/query.rs` matching the convention's query helper scope.
- Per CONVENTIONS.md "Testing" convention: add integration tests in `tests/api/` following the established test patterns against a real PostgreSQL test database.
  Applies: task modifies `tests/api/search.rs` matching the convention's `tests/api/` scope.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers already provide filtering and pagination; extend with date range and enum filter methods rather than implementing ad-hoc filtering
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; reuse as-is
- `modules/fundamental/src/advisory/model/summary.rs` — AdvisorySummary struct includes severity field; reference for severity filter values
- `modules/fundamental/src/sbom/endpoints/list.rs` — Example of a list endpoint with query parameter extraction using Axum's `Query<T>` extractor

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM entities
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory entities
- [ ] `GET /api/v2/search?entity_type=package` returns only package entities
- [ ] `GET /api/v2/search?created_after=<timestamp>` returns only entities created after the specified timestamp
- [ ] `GET /api/v2/search?created_before=<timestamp>` returns only entities created before the specified timestamp
- [ ] `GET /api/v2/search?severity=critical` returns only advisories with critical severity
- [ ] Multiple filters combine with AND semantics (e.g., `entity_type=advisory&severity=high` returns only high-severity advisories)
- [ ] Omitting all filter parameters returns unfiltered results (backward compatible)
- [ ] Invalid filter values return appropriate error responses
- [ ] Filtering integrates correctly with pagination (PaginatedResults total count reflects filtered set)

## Test Requirements
- [ ] Integration test: filter by entity_type=sbom returns only SBOMs
- [ ] Integration test: filter by entity_type=advisory returns only advisories
- [ ] Integration test: filter by entity_type=package returns only packages
- [ ] Integration test: filter by date range returns only entities within the range
- [ ] Integration test: filter by severity returns only matching advisories
- [ ] Integration test: combining multiple filters applies AND semantics
- [ ] Integration test: omitting filters returns all results (backward compatibility)
- [ ] Integration test: invalid entity_type value returns a 400 error
- [ ] Integration test: pagination total reflects the filtered result count
- [ ] Existing search integration tests in `tests/api/search.rs` continue to pass

## Dependencies
- Depends on: Task 1 — Add database indexes for search performance (filter queries benefit from the indexes created in Task 1)
