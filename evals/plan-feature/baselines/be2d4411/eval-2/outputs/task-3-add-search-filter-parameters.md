## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the `GET /api/v2/search` endpoint by introducing optional
query parameters for entity type, date range, and severity. Filters use AND semantics —
all specified conditions must match. This addresses the "add filters" MVP requirement.

**Ambiguity note:** The feature description specifies "some kind of filtering capability"
without defining which fields, filter types, or combination semantics. This task assumes
the following filter dimensions based on the domain model: entity type (SBOM, advisory,
package), date range (created after/before), and severity (for advisories). This assumption
is pending stakeholder clarification — additional filter dimensions may be needed.

## Files to Modify
- `modules/search/src/service/mod.rs` — extend `SearchService` search method to accept and apply filter parameters (entity type, date range, severity) to the database query
- `modules/search/src/endpoints/mod.rs` — add filter query parameters (`entity_type`, `created_after`, `created_before`, `severity`) to the `GET /api/v2/search` route handler
- `tests/api/search.rs` — add integration tests for filtered search queries

## Files to Create
- `modules/search/src/model/filter.rs` — define `SearchFilter` struct with optional fields for entity type enum, date range (created_after/created_before as DateTime), and severity string; implement `FromQueryParams` or equivalent Axum extractor

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `entity_type` (enum: sbom, advisory, package), `created_after` (ISO 8601 datetime), `created_before` (ISO 8601 datetime), `severity` (string: low, medium, high, critical). All parameters are optional; when multiple are provided, AND semantics apply.

## Implementation Notes
- Define a `SearchFilter` struct in `modules/search/src/model/filter.rs` with optional fields: `entity_type: Option<EntityType>`, `created_after: Option<DateTime>`, `created_before: Option<DateTime>`, `severity: Option<String>`.
- Create an `EntityType` enum with variants `Sbom`, `Advisory`, `Package` and implement Axum query parameter deserialization for it.
- In `modules/search/src/endpoints/mod.rs`, extract filter parameters from the query string using Axum's `Query<SearchFilter>` extractor — follow the existing endpoint parameter extraction pattern used in other endpoints like `modules/fundamental/src/sbom/endpoints/list.rs`.
- In `modules/search/src/service/mod.rs`, extend the search query to conditionally apply WHERE clauses based on which filter fields are `Some`. Use the shared query builder helpers from `common/src/db/query.rs` for constructing filter conditions.
- Entity type filtering restricts results to a single entity table; date range filtering adds `WHERE created >= ? AND created <= ?` conditions; severity filtering adds `WHERE severity = ?` (only applicable to advisory entities).
- When `severity` is specified but `entity_type` is not "advisory", the severity filter should be silently ignored (rather than returning an error) to maintain a simple API contract.
- All endpoint handlers must return `Result<T, AppError>` using `.context()` error wrapping from `common/src/error.rs`.
- Use the `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs` for the response.
- Follow the module pattern: the new filter model file follows the model/ convention established in `modules/fundamental/src/sbom/model/`.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; reuse the filtering helpers for constructing WHERE clauses from optional filter parameters
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; already used by the search endpoint
- `modules/fundamental/src/sbom/endpoints/list.rs` — SBOM list endpoint; reference for query parameter extraction pattern using Axum extractors
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct with `severity` field; reference for severity values used in filter validation

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?created_after=2024-01-01T00:00:00Z` returns only results created after the specified date
- [ ] `GET /api/v2/search?severity=high` returns only advisory results with high severity
- [ ] Multiple filters combine with AND semantics: `?entity_type=advisory&severity=critical` returns only critical advisories
- [ ] All filter parameters are optional — omitting all filters returns unfiltered results (backward compatible)
- [ ] Invalid filter values return a 400 Bad Request with a descriptive error message

## Test Requirements
- [ ] Integration test: filter by entity_type returns only results of that type
- [ ] Integration test: filter by date range (created_after, created_before) returns correctly bounded results
- [ ] Integration test: filter by severity returns only matching advisory results
- [ ] Integration test: combining multiple filters returns the intersection (AND semantics)
- [ ] Integration test: no filters returns all results (backward compatibility with existing callers)
- [ ] Integration test: invalid entity_type value returns 400 status
- [ ] Integration test: severity filter with non-advisory entity_type is silently ignored

## Verification Commands
- `cargo test -p search` — search module compiles and unit tests pass
- `cargo test -p tests --test search` — search integration tests pass

## Dependencies
- Depends on: Task 2 — Implement full-text search relevance scoring in SearchService

## additional_fields
- priority: Normal
- fixVersions: RHTPA 1.6.0
- labels: ai-generated-jira

[sdlc-workflow] Description digest: sha256-md:f4da177e0bda7e4403c0f00ef52d63d862ba9ada95d82a917ed6188bf1f7ddb9
