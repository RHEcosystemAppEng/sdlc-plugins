## Repository

trustify-backend

## Target Branch

main

## Description

Add filtering capabilities to the search endpoint so users can narrow search results by entity type, date range, and entity-specific attributes. The feature description requests "some kind of filtering capability" without specifying which filters, so this task implements a practical set of filters based on the available entity attributes.

**Assumption (pending clarification):** The feature description says "Add filters" with the note "Some kind of filtering capability" but does not specify which filters. This task assumes the following filter set based on the existing entity models: entity type (sbom, advisory, package), date range (created/modified), advisory severity, and package license. If additional or different filters are required, this needs clarification from the product owner.

**Assumption (pending clarification):** It is assumed that filters are applied as query parameters on the existing `GET /api/v2/search` endpoint rather than requiring a new POST-based search endpoint with a request body. If complex filter combinations require a different API design, this needs clarification.

Priority: Normal
Fix Versions: RHTPA 1.6.0

## Files to Modify

- `modules/search/src/endpoints/mod.rs` — add filter query parameters (entity_type, date_from, date_to, severity, license) to the search endpoint handler
- `modules/search/src/service/mod.rs` — extend SearchService to accept filter parameters and apply them as WHERE clauses in the search query
- `common/src/db/query.rs` — add reusable filter predicate builders for date range, enum matching, and string containment

## Files to Create

- `modules/search/src/model/filters.rs` — define `SearchFilters` struct with optional fields for each supported filter dimension

## Implementation Notes

- Define a `SearchFilters` struct in `modules/search/src/model/filters.rs` with optional fields: `entity_type: Option<EntityType>`, `date_from: Option<DateTime>`, `date_to: Option<DateTime>`, `severity: Option<String>`, `license: Option<String>`. Use `serde::Deserialize` for query parameter parsing.
- Follow the query builder pattern in `common/src/db/query.rs` for constructing filter predicates. The existing module handles filtering, pagination, and sorting — extend it with date-range and enum-match helpers.
- Wire the filters into the search endpoint in `modules/search/src/endpoints/mod.rs` using Axum's `Query<SearchFilters>` extractor, consistent with how other list endpoints (e.g., `modules/fundamental/src/sbom/endpoints/list.rs`) handle query parameters.
- The `severity` filter should match against the `AdvisorySummary` severity field from `modules/fundamental/src/advisory/model/summary.rs`.
- The `license` filter should match against the `PackageSummary` license field from `modules/fundamental/src/package/model/summary.rs`.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per the error handling convention.
- Register the new `filters.rs` module in `modules/search/src/model/mod.rs` (created in task 2).
- Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Applies: task modifies `common/src/db/query.rs` matching the convention's shared query helpers scope.

## Acceptance Criteria

- [ ] Search endpoint accepts optional filter query parameters: `entity_type`, `date_from`, `date_to`, `severity`, `license`
- [ ] Filters are combined with AND logic — multiple filters narrow the result set
- [ ] Unrecognized or invalid filter values return a 400 Bad Request with a descriptive error message
- [ ] Omitting all filters returns unfiltered results (backward compatible with current behavior)
- [ ] Filter parameters are documented via the `SearchFilters` struct with appropriate serde attributes

## Test Requirements

- [ ] Add integration tests in `tests/api/search.rs` for each individual filter (entity_type, date_from, date_to, severity, license)
- [ ] Test combined filters (e.g., entity_type=advisory AND severity=critical)
- [ ] Test that omitting filters returns the same results as the unfiltered endpoint
- [ ] Test that invalid filter values (e.g., invalid date format, unknown entity type) return 400 status
- [ ] Verify backward compatibility — existing search tests pass without modification

## Dependencies

- Task 2 (search-relevance-scoring) — the `SearchResult` model and `modules/search/src/model/mod.rs` module created in task 2 are extended here with filter definitions.
