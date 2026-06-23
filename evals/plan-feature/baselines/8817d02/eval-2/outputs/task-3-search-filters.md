# Task 3 — Add filter parameters to the search endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capability to the `GET /api/v2/search` endpoint, allowing users to narrow search results by entity type, severity (for advisories), and date range. Filters are implemented as optional query parameters that combine with AND logic. When no filters are provided, behavior is unchanged (backward compatible).

**Ambiguity note (assumption pending clarification):** The feature description says "Add filters — Some kind of filtering capability" without specifying which fields, which entities, or how filters combine. We assume the following filters based on the existing entity model:
- `entity_type` (enum: sbom, advisory, package) — filter results to a single entity type
- `severity` (string, e.g., "critical", "high", "medium", "low") — filter advisories by severity field from `AdvisorySummary`
- `date_from` / `date_to` (ISO 8601 date strings) — filter by creation/publication date range

Stakeholders should confirm the filter set. Additional filters (e.g., license for packages, specific SBOM fields) may be added in follow-up work.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameters to the `GET /api/v2/search` route handler; parse and validate filter values
- `modules/search/src/service/mod.rs` — extend `SearchService` methods to accept filter parameters and apply them to the database query
- `common/src/db/query.rs` — add shared filter builder helpers if needed for reuse across modules

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `entity_type` (string enum), `severity` (string), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date). All parameters are optional. When omitted, no filter is applied (backward compatible). Parameters combine with AND logic.

## Implementation Notes
- In `modules/search/src/endpoints/mod.rs`, add an Axum `Query<SearchFilters>` extractor struct with optional fields for each filter parameter. Use `Option<T>` for all filter fields to maintain backward compatibility.
- In `modules/search/src/service/mod.rs`, extend the search query to apply WHERE clauses based on provided filters. Use the shared query builder helpers from `common/src/db/query.rs` for constructing filter conditions.
- For `entity_type` filter: add a discriminator column or use separate queries per entity type and combine results. The current `SearchService` searches across entities — the filter should restrict which entity queries are executed.
- For `severity` filter: apply to advisory results only. Reference the `severity` field in `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`).
- For `date_from`/`date_to` filter: apply range conditions on entity timestamp columns.
- Validate filter values and return `AppError` (from `common/src/error.rs`) for invalid inputs (e.g., invalid date format, unknown entity type).
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` for query parameter extraction.
- Per `docs/constraints.md` §5.4: reuse `common/src/db/query.rs` query builder helpers rather than writing custom filter logic from scratch.
- Per `docs/constraints.md` §5.1: changes must be scoped to the files listed above.
- Per `docs/constraints.md` §2 (Commit Rules): commit must reference TC-9002 in the footer.

### Convention applicability
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`.
  Applies: task modifies `common/src/db/query.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint registration scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; extend with filter builder functions for entity_type, severity, and date range
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates Axum query parameter extraction pattern for list endpoints; use as reference for `SearchFilters` struct
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct contains the `severity` field referenced by the severity filter
- `modules/fundamental/src/package/model/summary.rs` — `PackageSummary` struct contains the `license` field (potential future filter candidate)

## Acceptance Criteria
- [ ] `GET /api/v2/search` accepts optional `entity_type`, `severity`, `date_from`, and `date_to` query parameters
- [ ] When no filters are provided, search behavior is unchanged from pre-filter implementation (backward compatible)
- [ ] `entity_type=advisory` returns only advisory results; `entity_type=sbom` returns only SBOM results; `entity_type=package` returns only package results
- [ ] `severity=critical` returns only advisories with critical severity
- [ ] `date_from` and `date_to` correctly filter results by date range (inclusive)
- [ ] Multiple filters combine with AND logic (e.g., `entity_type=advisory&severity=high` returns only high-severity advisories)
- [ ] Invalid filter values return appropriate error responses (400 Bad Request with descriptive error message)
- [ ] Response shape remains `PaginatedResults<T>` — no breaking changes

## Test Requirements
- [ ] Integration test: search with `entity_type=sbom` returns only SBOM results
- [ ] Integration test: search with `entity_type=advisory` returns only advisory results
- [ ] Integration test: search with `severity=critical` returns only critical-severity advisories
- [ ] Integration test: search with `date_from` and `date_to` returns only results within the date range
- [ ] Integration test: search with combined filters (entity_type + severity) returns correctly filtered results
- [ ] Integration test: search with no filters returns all results (backward compatibility)
- [ ] Integration test: search with invalid filter value returns 400 error

## Verification Commands
- `cargo test -p search` — search module tests pass
- `cargo test --test search` — integration tests in `tests/api/search.rs` pass

## Documentation Updates
- `README.md` — document the new search filter query parameters and their accepted values

## Dependencies
- Depends on: Task 2 — Optimize SearchService with full-text search and relevance ranking

[sdlc-workflow] Description digest: sha256-md:ea7c9136d4d5da3e892079b1bdfe5f9e64eea781ace6b1f6b44a93705cb9fda6
