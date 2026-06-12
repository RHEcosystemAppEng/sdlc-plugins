# Task 3 — Add filter parameters to the search endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the `GET /api/v2/search` endpoint so users can narrow search results by entity type, date range, and severity. This addresses the TC-9002 requirement to "add filters — some kind of filtering capability."

**Ambiguity note:** The feature description does not specify which fields should be filterable. This task proposes three filter dimensions based on the existing data model: entity type (sbom, advisory, package), date range (created/modified date), and severity (for advisories, which have a severity field per `AdvisorySummary`). The product owner should confirm this filter set or request additional filters (e.g., license for packages, vendor/source for SBOMs).

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add query parameters for `entity_type` (enum: sbom, advisory, package), `date_from`/`date_to` (ISO 8601 date strings), and `severity` (enum matching advisory severity values). Parse and validate these parameters before passing to the service layer.
- `modules/search/src/service/mod.rs` — Extend `SearchService` search method to accept filter parameters and apply them as WHERE clause conditions in the search query. Use the shared query builder helpers for filter construction.
- `common/src/db/query.rs` — Add or extend filter builder helpers for entity type filtering, date range filtering, and enum-based filtering if not already present.

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters:
  - `entity_type` (optional, string enum: `sbom`, `advisory`, `package`) — filter results to a single entity type
  - `date_from` (optional, ISO 8601 date) — include only results created/modified on or after this date
  - `date_to` (optional, ISO 8601 date) — include only results created/modified on or before this date
  - `severity` (optional, string) — filter advisory results by severity level (only applicable when `entity_type=advisory` or when searching across all types)
  - All parameters are optional; when omitted, behavior is unchanged (no filtering applied)

## Implementation Notes
- Use the existing query builder infrastructure in `common/src/db/query.rs` for filter construction. This module already provides "shared query builder helpers (filtering, pagination, sorting)" — inspect it to understand the existing filter pattern and extend it rather than building a parallel system.
- The `entity_type` filter determines which entity tables are included in the search query. If the current `SearchService` searches across all entity types in a single query (UNION or similar), the entity_type filter restricts which branches of the UNION are executed. If it queries each type separately, skip the types that don't match the filter.
- Date range filtering should use the created/modified timestamp fields on each entity. Inspect `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` to identify the correct timestamp column names.
- Severity filtering is specific to advisories — the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a severity field. When `severity` is specified without `entity_type=advisory`, it should only affect advisory results in the mixed-type result set (or the endpoint could reject the combination — check with product owner).
- Error handling: return `AppError` (from `common/src/error.rs`) for invalid filter values (e.g., malformed dates, unknown entity types) following the existing `.context()` wrapping pattern.
- Per docs/constraints.md Section 2 (Commit Rules): use Conventional Commits format and reference TC-9002 in the commit footer.
- Per docs/constraints.md Section 5 (Code Change Rules): inspect existing code before modifying, follow patterns found in the codebase, do not duplicate existing functionality.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering infrastructure; extend for entity type, date range, and severity filters
- `common/src/error.rs` — `AppError` enum for validation error responses
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct with severity field; reference for severity filter values
- `modules/fundamental/src/sbom/endpoints/list.rs` — example of list endpoint with query parameter parsing; follow the same pattern for filter parameter extraction
- `modules/fundamental/src/advisory/endpoints/list.rs` — another example of list endpoint with filtering

## Acceptance Criteria
- [ ] The `GET /api/v2/search` endpoint accepts `entity_type`, `date_from`, `date_to`, and `severity` query parameters
- [ ] Filtering by entity type returns only results of the specified type
- [ ] Filtering by date range returns only results within the specified date window
- [ ] Filtering by severity returns only advisory results matching the specified severity
- [ ] Combining multiple filters applies AND semantics (all filters must match)
- [ ] When no filters are provided, the endpoint returns all results (backward compatible)
- [ ] Invalid filter values return appropriate error responses

## Test Requirements
- [ ] Integration test filtering by each entity type individually (sbom, advisory, package)
- [ ] Integration test filtering by date range (date_from only, date_to only, both)
- [ ] Integration test filtering by severity
- [ ] Integration test combining entity_type and severity filters
- [ ] Integration test verifying invalid filter values return error responses
- [ ] Existing search tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test -p tests --test search` — all search tests pass including new filter tests

## Dependencies
- Depends on: Task 1 — Add full-text search indexes for searchable entities
