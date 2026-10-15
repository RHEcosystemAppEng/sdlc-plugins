## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint so users can narrow search results by entity type, date range, and domain-specific fields. The current search endpoint at `GET /api/v2/search` (defined in `modules/search/src/endpoints/mod.rs`) accepts only a search query term with no filtering options. This task adds query parameters for filtering and implements the filter logic in the SearchService.

**Ambiguity note:** The feature description states "Add filters — Some kind of filtering capability" without specifying which fields to filter on, what filter types to support (exact match, range, multi-select), or how multiple filters interact (AND vs. OR). This is the most underspecified of the MVP requirements.

**Assumption (pending clarification):** The following filters are assumed based on the existing data model in the `entity/` module:
- `type` (string, optional): filter by entity type — one of `sbom`, `advisory`, `package`. Based on entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs`.
- `severity` (string, optional): filter advisories by severity level. Based on the severity field in `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`).
- `license` (string, optional): filter packages by license. Based on the license field in `PackageSummary` (`modules/fundamental/src/package/model/summary.rs`).
- `from_date` / `to_date` (ISO 8601 date strings, optional): filter by creation or modification date range.
- Multiple filters combine with AND logic (conjunctive filtering).

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameters to the `GET /api/v2/search` endpoint handler
- `modules/search/src/service/mod.rs` — implement filter logic in SearchService, building WHERE clauses from filter parameters
- `common/src/db/query.rs` — extend query builder helpers with search-specific filter construction if not already supported
- `tests/api/search.rs` — add integration tests for each filter type and filter combinations

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters: `type` (string), `severity` (string), `license` (string), `from_date` (string, ISO 8601), `to_date` (string, ISO 8601)

## Implementation Notes
- In `modules/search/src/endpoints/mod.rs`, add an Axum `Query` extractor struct for the filter parameters. Follow the pattern used in existing list endpoints (e.g., `modules/fundamental/src/sbom/endpoints/list.rs` for `GET /api/v2/sbom`).
- In `modules/search/src/service/mod.rs`, accept the filter parameters and build conditional WHERE clauses using SeaORM's `Condition::all()` for AND logic. Apply filters only when the parameter is present (optional filtering).
- For the `type` filter, implement entity-type scoping in the search query — this may require conditional joins or subqueries depending on the current SearchService implementation.
- For the `severity` filter, join with the advisory table and filter on the severity column (see `modules/fundamental/src/advisory/model/summary.rs` for the field definition).
- For the `license` filter, join with the package/package_license tables and filter on the license value (see `entity/src/package_license.rs`).
- For date range filters (`from_date`, `to_date`), apply range conditions on the entity's created/modified timestamp columns.
- Leverage the existing query builder helpers in `common/src/db/query.rs` for filtering and pagination. The helpers already support filtering and sorting — extend them with search-specific filter types if needed.
- Validate filter parameter values at the endpoint layer. Return `400 Bad Request` with a descriptive error for invalid values (e.g., invalid date format, unknown entity type).
- Per CONVENTIONS.md §Error Handling: all new or modified handlers must return `Result<T, AppError>` with `.context()` wrapping. Use `AppError` for invalid filter parameter errors.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Response Types: the search endpoint returns `PaginatedResults<T>` from `common/src/model/paginated.rs`. Filtering should not change the response wrapper — only the contents are narrowed.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint `.rs` file scope.
- Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`. See existing usage in `modules/fundamental/src/sbom/service/sbom.rs` and `modules/fundamental/src/advisory/service/advisory.rs`.
  Applies: task modifies `common/src/db/query.rs` matching the convention's query helper `.rs` file scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/` hitting a real PostgreSQL test database using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. See `tests/api/search.rs` for the established test structure.
  Applies: task modifies `tests/api/search.rs` matching the convention's test `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; extend rather than duplicate
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference endpoint pattern for query parameter extraction with Axum `Query` extractor
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference pattern for building filtered SeaORM queries with conditional WHERE clauses

## Acceptance Criteria
- [ ] `GET /api/v2/search?type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?type=package` returns only package results
- [ ] `GET /api/v2/search?severity=critical` returns only advisories with critical severity
- [ ] `GET /api/v2/search?license=MIT` returns only packages with MIT license
- [ ] `GET /api/v2/search?from_date=2024-01-01&to_date=2024-12-31` returns only entities within the date range
- [ ] Multiple filters combine with AND logic (e.g., `type=advisory&severity=high` returns only high-severity advisories)
- [ ] Omitting all filter parameters returns unfiltered results (backward compatible with current behavior)
- [ ] Invalid filter values return `400 Bad Request` with a descriptive error message
- [ ] All existing search integration tests pass without modification

## Test Requirements
- [ ] Integration test: filter by each entity type individually (sbom, advisory, package)
- [ ] Integration test: filter by severity returns only matching advisories
- [ ] Integration test: filter by license returns only matching packages
- [ ] Integration test: filter by date range returns only entities within range
- [ ] Integration test: combine multiple filters (type + severity) and verify AND logic
- [ ] Integration test: omit all filters and verify unfiltered results are returned
- [ ] Integration test: invalid filter value returns 400 status code
- [ ] Regression: all existing tests in `tests/api/search.rs` pass without modification

## Verification Commands
- `cargo test --test search` — run search integration tests, expect all tests to pass
