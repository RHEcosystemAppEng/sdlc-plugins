# Task 3 — Add filter query parameters to the search endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add filter query parameters to the `GET /api/v2/search` endpoint to allow users to
narrow search results by entity type, advisory severity, and package license. This
addresses the TC-9002 MVP requirement to "add filters" with "some kind of filtering
capability."

Filters are implemented as optional query parameters that are AND-combined with the
full-text search query. When no filters are specified, the endpoint behaves exactly
as before (backward-compatible).

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameter extraction (entity_type, severity, license) and pass them to the SearchService
- `modules/search/src/service/mod.rs` — accept filter parameters and apply them as WHERE clause conditions alongside the full-text search query
- `common/src/db/query.rs` — add reusable filter builder helpers for entity_type enum filtering and optional field equality filters

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters:
  - `entity_type` (string, optional) — filter by entity type: `sbom`, `advisory`, or `package`
  - `severity` (string, optional) — filter advisories by severity level (e.g., `critical`, `high`, `medium`, `low`)
  - `license` (string, optional) — filter packages by license identifier
  - All filters are optional and AND-combined; omitting a filter means no restriction on that dimension

## Implementation Notes
- Inspect the existing query parameter handling in `modules/search/src/endpoints/mod.rs` and the filter patterns in `common/src/db/query.rs` before implementing.
- Use Axum's `Query` extractor to deserialize filter parameters from the query string. Define a `SearchFilters` struct with optional fields for each filter.
- In `common/src/db/query.rs`, add helper functions for:
  - Entity type filtering (an enum-based filter that selects which tables to search)
  - Optional field equality filtering (a generic pattern for `WHERE field = value` when the parameter is `Some`)
- Follow the existing pagination and sorting patterns in `common/src/db/query.rs`. The filter helpers should compose with the existing query builder approach.
- When `entity_type` is specified, only search the matching entity table(s) rather than all three. This improves performance for filtered queries.
- When `severity` is specified but `entity_type` is not `advisory`, ignore the severity filter (it only applies to advisories). Similarly for `license` and packages.
- Use the `AdvisorySummary.severity` field and `PackageSummary.license` field as the filter targets — these were identified in the entity model definitions.
- Per docs/constraints.md §2 (Commit Rules): commit messages must follow Conventional Commits, reference TC-9002, and include the Assisted-by trailer.
- Per docs/constraints.md §5 (Code Change Rules): keep changes scoped to the listed files; inspect code before modifying; do not duplicate existing query.rs helpers.

## Reuse Candidates
- `common/src/db/query.rs` — existing shared query builder helpers for filtering, pagination, and sorting; extend with full-text search filter composition
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct with `severity` field; confirms the field name and type for severity filtering
- `modules/fundamental/src/package/model/summary.rs` — `PackageSummary` struct with `license` field; confirms the field name and type for license filtering

## Acceptance Criteria
- [ ] GET /api/v2/search accepts optional `entity_type`, `severity`, and `license` query parameters
- [ ] Filters are AND-combined with the search query
- [ ] entity_type filter restricts results to the specified entity type (sbom, advisory, or package)
- [ ] severity filter restricts advisory results to the specified severity level
- [ ] license filter restricts package results to the specified license
- [ ] Omitting all filters returns unfiltered results (backward-compatible)
- [ ] Invalid filter values return an appropriate error response (400 Bad Request)
- [ ] Filters compose correctly with pagination (total count reflects filtered results)

## Test Requirements
- [ ] Integration test: filter by entity_type=sbom returns only SBOM results
- [ ] Integration test: filter by entity_type=advisory returns only advisory results
- [ ] Integration test: filter by severity=critical returns only critical advisories
- [ ] Integration test: filter by license returns only packages with matching license
- [ ] Integration test: combining entity_type and severity filters works correctly
- [ ] Integration test: no filters returns all results (backward compatibility)
- [ ] Integration test: invalid entity_type returns 400 Bad Request
- [ ] Integration test: filters interact correctly with pagination (offset, limit, total)

## Verification Commands
- `cargo test -p search` — search module tests pass
- `cargo test --test search` — search integration tests pass

## Dependencies
- Depends on: Task 2 — Refactor SearchService to use full-text search with relevance ranking
