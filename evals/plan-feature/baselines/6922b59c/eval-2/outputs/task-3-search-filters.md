## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search API endpoint so users can narrow down search results by entity type, severity, and date range. The feature TC-9002 requires "some kind of filtering capability" but does not specify which filters.

**Assumption (pending clarification):** Filters will include entity type (sbom, advisory, package), severity (for advisories, matching existing severity field values), and date range (date_from, date_to as ISO 8601 dates). These are inferred from the domain model and common search patterns for this platform. The exact set of filters should be confirmed with stakeholders.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` -- Add filter query parameters (entity_type, severity, date_from, date_to) to the GET /api/v2/search endpoint handler
- `modules/search/src/service/mod.rs` -- Add filter predicate construction logic to SearchService query building
- `common/src/db/query.rs` -- Extend shared query builder with reusable filter predicate helpers for entity type, severity enum, and date range if not already present

## API Changes
- `GET /api/v2/search` -- MODIFY: Add optional query parameters: `entity_type` (enum: sbom, advisory, package; accepts comma-separated for multiple), `severity` (enum matching advisory severity values), `date_from` (ISO 8601 date string), `date_to` (ISO 8601 date string)

## Implementation Notes
- Per CONVENTIONS.md §Query Helpers: use shared filtering utilities from `common/src/db/query.rs` for constructing filter predicates. Follow the existing patterns for composing WHERE clauses with SeaORM `Condition::all()` for AND logic.
  Applies: task modifies `common/src/db/query.rs` matching the convention's `.rs` query helper scope.
- Per CONVENTIONS.md §Error Handling: validate filter parameter values and return `AppError` with descriptive messages for invalid inputs (e.g., invalid entity_type enum value, malformed date). See `common/src/error.rs::AppError` for the error enum pattern.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` error handling scope.
- Per CONVENTIONS.md §Endpoint Registration: follow existing route registration pattern and Axum `Query` extractor for filter parameters. See `modules/fundamental/src/sbom/endpoints/list.rs` for how query parameters are extracted and validated.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` endpoint registration scope.
- Reference filter implementation patterns in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` for how existing list endpoints handle filtering
- Severity values must match the `AdvisorySummary` severity field from `modules/fundamental/src/advisory/model/summary.rs` -- use the same enum or string values
- Filters are additive (AND logic) -- applying entity_type=sbom AND severity=critical returns SBOMs with critical severity (if applicable) or no results if severity is not a valid SBOM field
- The `severity` filter should only apply when entity_type includes advisory, or when no entity_type filter is set (apply to advisory results only)

## Reuse Candidates
- `common/src/db/query.rs` -- Shared filtering, pagination, and sorting helpers; extend with entity-type and date-range predicates
- `modules/fundamental/src/sbom/endpoints/list.rs` -- Example list endpoint with query parameter extraction and filter handling
- `modules/fundamental/src/advisory/endpoints/list.rs` -- Example list endpoint with filtering for advisory entities
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- Contains severity field definition; use for filter value validation
- `common/src/error.rs::AppError` -- Error enum for returning validation errors on invalid filter values

## Acceptance Criteria
- [ ] Search endpoint accepts optional `entity_type` filter parameter with values: sbom, advisory, package (comma-separated for multiple)
- [ ] Search endpoint accepts optional `severity` filter parameter (applied to advisory results only)
- [ ] Search endpoint accepts optional `date_from` and `date_to` filter parameters (ISO 8601 format)
- [ ] Multiple filters combine with AND logic to narrow results
- [ ] Invalid filter values (unknown entity type, malformed date) return appropriate 400 error responses with descriptive messages
- [ ] Search without any filters returns the same results as before (fully backward compatible)
- [ ] Severity filter is silently ignored when entity_type excludes advisories

## Test Requirements
- [ ] Integration test for filtering by single entity type (e.g., entity_type=sbom returns only SBOM results)
- [ ] Integration test for filtering by multiple entity types (e.g., entity_type=sbom,advisory)
- [ ] Integration test for filtering by severity (returns only advisory results with matching severity)
- [ ] Integration test for filtering by date range (date_from and date_to)
- [ ] Integration test for combined filters (entity_type + severity + date range)
- [ ] Integration test for invalid filter values returning 400 errors
- [ ] Existing tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test --test search` -- search tests pass including new filter tests

## Dependencies
- Depends on: Task 1 -- Add database indexes and optimize search queries for performance
