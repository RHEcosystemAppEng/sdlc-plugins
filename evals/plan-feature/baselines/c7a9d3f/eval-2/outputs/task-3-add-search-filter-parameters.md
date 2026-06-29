# Task 3 — Add filter query parameters to search endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capability to the `GET /api/v2/search` endpoint by introducing optional
query parameters for entity type, advisory severity, and package license. This addresses
the TC-9002 MVP requirement "Add filters — some kind of filtering capability." Filters
are implemented as optional query parameters that narrow search results using the existing
shared filter builder pattern in `common/src/db/query.rs`.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameter extraction to the search endpoint handler; define a `SearchFilterParams` struct for the new optional parameters (entity_type, severity, license)
- `modules/search/src/service/mod.rs` — extend the SearchService query methods to accept and apply filter parameters alongside the full-text search query
- `common/src/db/query.rs` — add filter builder helpers for full-text search-specific filtering if the existing helpers do not support the needed filter types (e.g., enum-based filtering, multi-value filtering)

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters:
  - `entity_type` (optional, string) — filter results by entity type: `sbom`, `advisory`, or `package`
  - `severity` (optional, string) — filter advisory results by severity level (e.g., `critical`, `high`, `medium`, `low`)
  - `license` (optional, string) — filter package results by license identifier
  All parameters are optional and additive (AND semantics). Omitting a parameter means no filtering on that dimension. The existing response shape (`PaginatedResults<T>`) is unchanged.

## Implementation Notes
- Define a `SearchFilterParams` query parameter struct in the search endpoint module using Axum's `Query` extractor, following the pattern established in other list endpoints (e.g., `modules/fundamental/src/sbom/endpoints/list.rs`).
- Each filter parameter should be `Option<String>` to preserve backward compatibility — existing callers that do not supply filters continue to work identically.
- Integrate filters with the shared query builder in `common/src/db/query.rs`. Examine the existing filtering, pagination, and sorting helpers to determine if new filter types need to be added or if existing helpers can be reused.
- For entity_type filtering: filter by the source table/entity discriminator in the search query.
- For severity filtering: apply the filter only when searching advisories — the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a severity field.
- For license filtering: apply the filter only when searching packages — the `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` includes a license field.
- Filters that do not apply to a given entity type should be silently ignored for that entity type (e.g., a `severity` filter does not affect SBOM results).
- Per docs/constraints.md §2 (Commit Rules): commit messages must follow Conventional Commits format, reference TC-9002, and include the `Assisted-by: Claude Code` trailer.
- Per docs/constraints.md §5.2 (Code Change Rules): inspect existing endpoint and query builder code before modifying.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; extend or reuse these for search-specific filter application
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing list endpoint demonstrating query parameter extraction pattern with Axum's `Query` extractor
- `modules/fundamental/src/advisory/model/summary.rs` — AdvisorySummary struct with severity field, relevant for severity filter implementation
- `modules/fundamental/src/package/model/summary.rs` — PackageSummary struct with license field, relevant for license filter implementation
- `common/src/model/paginated.rs` — PaginatedResults<T> response wrapper that must remain unchanged

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=package` returns only package results
- [ ] `GET /api/v2/search?severity=critical` filters advisory results by critical severity
- [ ] `GET /api/v2/search?license=MIT` filters package results by MIT license
- [ ] Filters can be combined (e.g., `?entity_type=advisory&severity=high`)
- [ ] Omitting all filter parameters returns unfiltered results (backward compatible)
- [ ] Response shape remains `PaginatedResults<T>` — no breaking changes to existing consumers
- [ ] Invalid filter values return appropriate error responses (not 500)

## Test Requirements
- [ ] Each filter parameter narrows results correctly when used individually
- [ ] Combined filters apply AND semantics correctly
- [ ] Omitting filters returns unfiltered results (backward compatibility)
- [ ] Invalid entity_type value returns a meaningful error response
- [ ] Severity filter has no effect on SBOM or package results (silent ignore)
- [ ] License filter has no effect on SBOM or advisory results (silent ignore)

## Verification Commands
- `cargo test -p search` — search module tests pass including new filter tests
- `cargo clippy -p search -- -D warnings` — no clippy warnings

## Dependencies
- Depends on: Task 2 — Refactor SearchService to use full-text search with relevance ranking (filters build on top of the refactored search query logic)
