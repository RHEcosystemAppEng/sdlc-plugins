## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint (`GET /api/v2/search`) by introducing query parameters for entity type, date range, and entity-specific attributes (e.g., severity for advisories). Integrate the new filter parameters with the existing shared query helpers in `common/src/db/query.rs` and extend the SearchService to apply filter predicates to search queries.

This addresses the "Add filters" requirement from TC-9002.

**Assumption pending clarification:** The minimum filter set includes: entity type filter (sbom, advisory, package), date range filter (created_at from/to), and severity filter (for advisories). Filters combine with AND logic. The specific filter fields and supported operators may need to be expanded based on product owner input.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add filter query parameters (entity_type, date_from, date_to, severity) to the search endpoint handler; parse and validate filter values; pass filters to SearchService
- `modules/search/src/service/mod.rs` — Extend SearchService query logic to apply filter predicates (WHERE clauses) based on provided filter parameters
- `common/src/db/query.rs` — Add or extend shared filter builder helpers for date range filtering and enum-based filtering if not already supported
- `tests/api/search.rs` — Add integration tests for each filter parameter individually and in combination

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters:
  - `entity_type` (string, optional) — Filter by entity type: `sbom`, `advisory`, or `package`
  - `date_from` (ISO 8601 date, optional) — Filter results created on or after this date
  - `date_to` (ISO 8601 date, optional) — Filter results created on or before this date
  - `severity` (string, optional) — Filter advisories by severity level (e.g., `critical`, `high`, `medium`, `low`)
  - Existing parameters (`q`, `offset`, `limit`) remain unchanged

## Implementation Notes
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` with `.context()` wrapping for all handler functions.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's handler .rs file scope.
- Per CONVENTIONS.md §Endpoint Registration: register routes in module's `endpoints/mod.rs`; mount in `server/main.rs`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint .rs file scope.
- Per CONVENTIONS.md §Response Types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint .rs file scope.
- Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting helpers from `common/src/db/query.rs`.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's service .rs file scope.
- Per CONVENTIONS.md §Testing: use integration tests hitting a real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's test .rs file scope.
- Per CONVENTIONS.md §Caching: configure `tower-http` caching middleware in endpoint route builders.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint route builder .rs file scope.
- Define an `SearchFilters` struct to deserialize filter query parameters using `serde::Deserialize` with Axum's `Query` extractor
- Validate `entity_type` against an enum of allowed values; return 400 Bad Request for invalid values
- For the `severity` filter, apply it only when `entity_type` is `advisory` or when searching across all types (filter advisory results only)
- Use `date_from` and `date_to` to construct a `BETWEEN` clause on the `created_at` column
- All filter parameters are optional; when omitted, no filtering is applied (existing behavior preserved)
- Follow the existing filter pattern in `common/src/db/query.rs` for consistency with other list endpoints (e.g., `GET /api/v2/sbom`, `GET /api/v2/advisory`)

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers already implementing filtering, pagination, and sorting for other endpoints; extend rather than duplicate
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper for paginated search results
- `common/src/error.rs` — `AppError` enum for validation error responses (400 Bad Request)
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct includes a severity field; reference for severity enum values
- `modules/fundamental/src/sbom/endpoints/list.rs` — `GET /api/v2/sbom` list endpoint as a reference for filter parameter handling in Axum

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?entity_type=package` returns only package results
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` returns only results within the date range
- [ ] `GET /api/v2/search?severity=critical` returns only advisories with critical severity
- [ ] Combining multiple filters applies AND logic (e.g., `entity_type=advisory&severity=high`)
- [ ] Omitting all filter parameters returns unfiltered results (backward compatibility)
- [ ] Invalid filter values (e.g., `entity_type=invalid`) return 400 Bad Request with a descriptive error message
- [ ] Response shape remains `PaginatedResults<T>` with unchanged structure

## Test Requirements
- [ ] Integration test: search with `entity_type=sbom` returns only SBOMs
- [ ] Integration test: search with `entity_type=advisory` returns only advisories
- [ ] Integration test: search with `date_from` and `date_to` returns only results within the range
- [ ] Integration test: search with `severity=high` returns only high-severity advisories
- [ ] Integration test: combining `entity_type=advisory` and `severity=critical` returns only critical advisories
- [ ] Integration test: invalid `entity_type` value returns 400 status code
- [ ] Integration test: search with no filters returns all results (backward compatibility)

## Verification Commands
- `cargo test -p search` — search module unit tests pass
- `cargo test --test search` — search integration tests pass (tests/api/search.rs)
- `curl "http://localhost:8080/api/v2/search?entity_type=sbom"` — returns only SBOM results
- `curl "http://localhost:8080/api/v2/search?entity_type=invalid"` — returns 400 Bad Request

## Dependencies
- None (this task is independent of Tasks 1 and 2)
