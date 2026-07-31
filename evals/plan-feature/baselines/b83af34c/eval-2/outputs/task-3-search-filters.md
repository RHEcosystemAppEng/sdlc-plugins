## Repository
trustify-backend

## Target Branch
main

## Description
Add filter parameters to the search endpoint (GET /api/v2/search) so users can narrow search results by entity type, severity level, and date range. This addresses the requirement to "add filters" with "some kind of filtering capability."

**Assumption (pending clarification):** The feature states "add filters" with "some kind of filtering capability" but does not specify what fields to filter by. This task assumes the following filter parameters based on the existing data model: entity type (sbom, advisory, package), severity level (from advisory severity field), and date range (created/modified timestamps). The specific filter fields should be confirmed with the product owner.

**Assumption (pending clarification):** Filters are assumed to be query parameters on the existing GET /api/v2/search endpoint (e.g., `?type=advisory&severity=high&from=2024-01-01`). An alternative design using POST with a filter body is not considered without explicit direction.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add query parameter extraction for filter fields (entity type, severity, date range) to the GET /api/v2/search handler
- `modules/search/src/service/mod.rs` — Extend SearchService to accept and apply filter criteria to search queries, composing filters with the full-text search predicate
- `common/src/db/query.rs` — Add shared filter builder helpers for entity type, severity, and date range predicates if not already present

## Implementation Notes
Add filter parameter structs to the search endpoint in `modules/search/src/endpoints/mod.rs` using Axum's `Query<T>` extractor. The filter parameters should be optional so the endpoint remains backward compatible. Pass filter criteria to `SearchService` in `modules/search/src/service/mod.rs`, which should compose them as additional WHERE clauses alongside the full-text search predicate. Leverage the existing query builder pattern in `common/src/db/query.rs` for constructing filter predicates — this module already provides shared filtering, pagination, and sorting helpers. Severity filtering should reference the `severity` field in `AdvisorySummary` from `modules/fundamental/src/advisory/model/summary.rs`. All handlers must return `Result<T, AppError>` with `.context()` wrapping.

Per CONVENTIONS.md §Framework: use Axum `Query<T>` extractor for query parameters in endpoint handlers. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust file scope.

Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust file scope.

Per CONVENTIONS.md §Query Helpers: extend shared query builder in `common/src/db/query.rs` for new filter predicates. Applies: task modifies `common/src/db/query.rs` matching the convention's Rust file scope.

Per CONVENTIONS.md §Endpoint Registration: register any new routes or parameter changes through the module's `endpoints/mod.rs`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `common/src/db/query.rs::Query` — Shared query builder with existing filtering helpers; extend with new filter predicates rather than writing custom WHERE clause construction
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the `severity` field definition; reference for severity filter values

## Acceptance Criteria
- [ ] GET /api/v2/search accepts optional `type` query parameter to filter by entity type (sbom, advisory, package)
- [ ] GET /api/v2/search accepts optional `severity` query parameter to filter by advisory severity level
- [ ] GET /api/v2/search accepts optional `from` and `to` query parameters to filter by date range
- [ ] Filters compose correctly with full-text search (results match both search terms and filter criteria)
- [ ] Multiple filters can be combined in a single request
- [ ] Omitting all filters returns unfiltered results (backward compatible)
- [ ] Invalid filter values return appropriate error responses using AppError

## Test Requirements
- [ ] Integration test verifying entity type filter returns only results of the specified type
- [ ] Integration test verifying severity filter returns only advisories matching the severity level
- [ ] Integration test verifying date range filter returns only results within the specified range
- [ ] Integration test verifying combined filters (e.g., type=advisory AND severity=high) work correctly
- [ ] Integration test verifying backward compatibility (no filters = same behavior as before)
- [ ] Integration test verifying invalid filter values produce a 400 error response

## Dependencies
- Depends on: Task 1 — Add database indexes for search performance (indexes on filter columns must exist for acceptable filter query performance)
