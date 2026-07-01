# Task 4 — Add filter query parameters to the search endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Extend the search endpoint (`GET /api/v2/search`) to accept optional filter query parameters for entity type, date range, and advisory severity. This addresses the MVP requirement to "add filters" by allowing users to narrow search results without changing the core search query. All filters are optional and additive — when no filters are specified, the endpoint behaves identically to the current implementation (backward compatible).

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add query parameter extraction for filter parameters (entity type, date range, severity) and pass them to `SearchService`
- `modules/search/src/service/mod.rs` — accept filter parameters and apply them as WHERE clauses to the search query
- `common/src/db/query.rs` — add shared filter helper for date range filtering (`created_after`, `created_before`) that can be reused by other endpoints

## Implementation Notes
- Define filter query parameters as an Axum `Query<SearchFilters>` extractor struct:
  - `entity_type: Option<String>` — filter by entity type ("sbom", "advisory", "package"); maps to the entity type discriminator
  - `created_after: Option<DateTime<Utc>>` — only return results created after this timestamp
  - `created_before: Option<DateTime<Utc>>` — only return results created before this timestamp
  - `severity: Option<String>` — filter advisories by severity level (e.g., "critical", "high", "medium", "low"); only applies when `entity_type` is "advisory" or unset
- Each filter is optional. When absent, no filtering is applied for that dimension.
- The `entity_type` filter should exclude entire entity categories from the search results before ranking. When set to "advisory", only advisories are searched — SBOMs and packages are skipped entirely.
- The `severity` filter applies only to advisory entities. When `entity_type` is "sbom" or "package" and `severity` is set, the severity filter is silently ignored (not an error).
- The date range filter helper in `common/src/db/query.rs` should follow the existing pagination and sorting helper patterns for composability.
- Ensure all new query parameters are documented in the endpoint's response — use the existing patterns in list endpoints like `modules/fundamental/src/sbom/endpoints/list.rs`.
- Error handling: invalid filter values (e.g., unparseable dates) should return `400 Bad Request` via `AppError`.

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `entity_type`, `created_after`, `created_before`, `severity`

## Reuse Candidates
- `common/src/db/query.rs` — existing filtering, pagination, and sorting helpers; extend with date range filter
- `modules/fundamental/src/sbom/endpoints/list.rs` — example of list endpoint with query parameter extraction pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity field definition to reference for severity filter values

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=advisory&severity=critical` returns only critical advisories
- [ ] `GET /api/v2/search?created_after=2024-01-01T00:00:00Z` returns only results created after the specified date
- [ ] `GET /api/v2/search` without any filters returns all results (backward compatible)
- [ ] Invalid filter values return 400 Bad Request

## Test Requirements
- [ ] Integration test: filter by entity_type returns only matching entity types
- [ ] Integration test: filter by severity returns only advisories with matching severity
- [ ] Integration test: filter by date range returns only results within range
- [ ] Integration test: combining multiple filters (entity_type + severity) works correctly
- [ ] Integration test: invalid date format returns 400 Bad Request
- [ ] Integration test: no filters returns same results as unfiltered search (backward compatibility)

## Verification Commands
- `cargo test -p tests -- search --test-threads=1` — integration tests pass

## Dependencies
- Depends on: Task 2 — Add search result model types with relevance scoring (requires SearchResultSummary with entity type discriminator)
- Depends on: Task 3 — Implement weighted full-text search ranking (search service must support the new return type before filters can be applied)
