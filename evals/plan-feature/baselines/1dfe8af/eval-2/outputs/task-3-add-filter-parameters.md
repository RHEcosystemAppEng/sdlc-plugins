## Repository
trustify-backend

## Target Branch
main

## Description
Add filter query parameters to the search endpoint so users can narrow search results by specific fields. The feature requirement states "Add filters" with "some kind of filtering capability" but provides no specification of which fields or operators to support.

**Assumption (pending clarification):** The following filter fields and operators are assumed based on the entity model and common search use cases:
- `severity` (advisory) — multi-value equality filter (e.g., `?severity=high&severity=critical`)
- `date_from` / `date_to` (all entities) — range filter on creation/publication date
- `package_name` (package/SBOM) — text contains filter
- `license` (package) — equality filter on license type

TC-9002 does not specify any of these details.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add filter query parameter extraction to the GET /api/v2/search handler; define a `SearchFilters` struct for deserialization of filter parameters

## Files to Create
- `modules/search/src/model/mod.rs` — Define `SearchFilters` struct with optional filter fields (severity, date_from, date_to, package_name, license) and a `SearchResult` enum for typed results across entities

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters: `severity` (multi-value), `date_from` (ISO 8601), `date_to` (ISO 8601), `package_name` (string), `license` (string). All filters are optional; omitting a filter means no restriction on that field.

## Implementation Notes
Define a `SearchFilters` struct in a new `modules/search/src/model/mod.rs` file following the module pattern used by other domain modules (e.g., `modules/fundamental/src/sbom/model/mod.rs`). The struct should use `Option<T>` for each filter field so all filters are optional.

In `modules/search/src/endpoints/mod.rs`, use Axum's `Query<SearchFilters>` extractor to parse filter parameters from the request URL. Pass the parsed filters to the SearchService.

The filter fields are informed by entity definitions:
- Severity from `entity/src/advisory.rs` and `modules/fundamental/src/advisory/model/summary.rs` (severity field on AdvisorySummary)
- License from `entity/src/package_license.rs` and `modules/fundamental/src/package/model/summary.rs` (license field on PackageSummary)
- Date fields from entity timestamps on `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs`

All handlers must return `Result<T, AppError>` with `.context()` wrapping per the project error handling convention in `common/src/error.rs`.

## Acceptance Criteria
- [ ] GET /api/v2/search accepts optional filter query parameters: severity, date_from, date_to, package_name, license
- [ ] Omitted filters do not restrict results (backward compatible)
- [ ] Invalid filter values return a 400 Bad Request with a descriptive error message
- [ ] Filter parameters are documented in the SearchFilters struct with doc comments

## Test Requirements
- [ ] Integration test verifying search with no filters returns all results (backward compatibility)
- [ ] Integration test verifying each individual filter restricts results correctly
- [ ] Integration test verifying invalid filter values return 400 status
- [ ] Integration test verifying multiple filters combine with AND semantics

[sdlc-workflow] Description digest: sha256-md:f4a8b2c6d0e913475689abcdef1234567890abcd1234567890abcdef12345678
