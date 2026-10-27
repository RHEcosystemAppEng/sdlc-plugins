## Repository
trustify-backend

## Target Branch
main

## Description
Add filter parameters to the search endpoint to allow users to narrow search results by entity type, severity, and date range. This addresses the MVP requirement "Add filters — Some kind of filtering capability."

**Assumption (pending clarification):** Filters include entity type (SBOM, advisory, package), severity (for advisories: low, moderate, important, critical), and date range (created_after, created_before). Additional filter fields may be needed after stakeholder review.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add query parameters for entity type, severity, and date range filters to `GET /api/v2/search`
- `modules/search/src/service/mod.rs` — add filter predicate construction to the search query in `SearchService`

## Implementation Notes
- Add optional query parameters to the search endpoint handler in `modules/search/src/endpoints/mod.rs`: `entity_type` (enum: sbom, advisory, package), `severity` (string), `created_after` (datetime), `created_before` (datetime).
- Use Axum's `Query` extractor for the filter parameters. Reference the existing query parameter patterns in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs`.
- In `SearchService` (`modules/search/src/service/mod.rs`), build filter predicates using SeaORM's `Condition` builder. Apply filters as `WHERE` clauses combined with the full-text search condition.
- Leverage the shared filtering helpers in `common/src/db/query.rs` — extend the existing filter infrastructure rather than creating a parallel mechanism.
- Severity filtering only applies when searching advisories — document this in the API. The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a `severity` field.
- **Assumption (pending clarification):** Date range filters apply to the entity's creation date. If modification date filtering is also needed, this requires additional implementation.
- Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for all handler and service methods.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination, and sorting helpers that already implement filter predicate patterns
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — includes the severity field definition used for severity filtering

## Acceptance Criteria
- [ ] Search endpoint accepts optional `entity_type` filter parameter
- [ ] Search endpoint accepts optional `severity` filter parameter (applies to advisory results only)
- [ ] Search endpoint accepts optional `created_after` and `created_before` date range parameters
- [ ] Filters can be combined (e.g., entity_type=advisory AND severity=critical)
- [ ] Omitting all filters returns unfiltered results (backward compatible)
- [ ] Invalid filter values return appropriate error responses

## Test Requirements
- [ ] Filtering by entity type returns only results of that type
- [ ] Filtering by severity returns only advisories with matching severity
- [ ] Date range filtering returns only results within the specified range
- [ ] Combining multiple filters returns the intersection of results
- [ ] Omitting filters returns all results (no regression from existing behavior)
- [ ] Invalid entity type value returns a 400 error with descriptive message

## Dependencies
- Depends on: Task 2 — Refactor search service to full-text (builds on the refactored search query construction)
