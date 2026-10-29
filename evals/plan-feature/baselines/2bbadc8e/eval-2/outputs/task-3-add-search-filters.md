## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capability to the search endpoint so users can narrow search results by entity type, severity, and date range. The current search endpoint returns all matching entities without any filtering options. This task extends the search API to accept optional filter query parameters and applies them to the search query construction.

**Assumption pending clarification:** The Feature description states "Add filters — Some kind of filtering capability" without specifying which filters. This task assumes the following filter set based on the existing data model: entity type (SBOM, advisory, package), severity (for advisories, using the severity field from AdvisorySummary), and date range (created after/before timestamps). If additional filters are needed (e.g., license type for packages, specific SBOM fields), the filter set should be expanded after clarification.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add filter query parameters to the GET /api/v2/search handler (entity_type, severity, date_from, date_to)
- `modules/search/src/service/mod.rs` — Extend SearchService to accept and apply filter criteria to search queries
- `common/src/db/query.rs` — Add or extend filter construction helpers for the new filter types (enum filtering, date range filtering)

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters:
  - `entity_type` (optional, string enum: `sbom`, `advisory`, `package`) — filter results to a single entity type
  - `severity` (optional, string) — filter advisory results by severity level
  - `date_from` (optional, ISO 8601 datetime) — filter results created on or after this timestamp
  - `date_to` (optional, ISO 8601 datetime) — filter results created on or before this timestamp
  - All parameters are optional — when omitted, the endpoint behaves identically to the current unfiltered behavior (backward compatibility)

## Implementation Notes
- Parse filter query parameters using Axum's `Query<T>` extractor. Define a `SearchFilters` struct with optional fields for each filter parameter. Follow the pattern used in existing list endpoints (e.g., `modules/fundamental/src/sbom/endpoints/list.rs`) for query parameter extraction.
- Extend the `SearchService` query method to accept a filters parameter and conditionally add WHERE clauses based on which filters are provided. Use the shared query builder in `common/src/db/query.rs` to construct filter conditions — extend the existing helpers rather than writing standalone filter logic.
- For `entity_type` filtering: when the search spans multiple entity types (SBOMs, advisories, packages), filter the query to only search the specified entity table. This may require conditional query construction based on the entity type parameter.
- For `severity` filtering: join or filter against the advisory severity field (see `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`). This filter only applies when searching advisories — if `entity_type` is set to a non-advisory type and severity is also set, return an appropriate error or ignore the inapplicable filter.
- For `date_from`/`date_to` filtering: apply range conditions on the created_at timestamp of the matching entities.
- Per Key Conventions: shared filtering, pagination, and sorting via `common/src/db/query.rs` — add filter helpers here for reuse across endpoints.
  Applies: task modifies `common/src/db/query.rs` matching the convention's Rust query helper file scope.
- Per Key Conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping — ensure filter parsing and validation errors are wrapped as AppError.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.
- Per Key Conventions: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs` — filtered results must maintain this response wrapper.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — Shared filtering, pagination, and sorting utilities; extend these with new filter types (enum match, date range) rather than building filter logic from scratch
- `modules/fundamental/src/sbom/endpoints/list.rs` — Example of a list endpoint with query parameter extraction using Axum's Query extractor; follow this pattern for search filter parameters
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the severity field definition used for severity filtering
- `common/src/model/paginated.rs::PaginatedResults<T>` — Response wrapper that filtered results must use

## Acceptance Criteria
- [ ] The search endpoint accepts optional `entity_type` query parameter and returns only results of the specified type when provided
- [ ] The search endpoint accepts optional `severity` query parameter and filters advisory results by severity when provided
- [ ] The search endpoint accepts optional `date_from` and `date_to` query parameters and filters results by creation timestamp range when provided
- [ ] All filter parameters are optional — omitting them produces identical behavior to the current unfiltered endpoint (backward compatibility)
- [ ] Filters compose correctly — applying multiple filters simultaneously narrows results as expected (AND semantics)
- [ ] Invalid filter values (e.g., non-existent entity type, malformed date) return appropriate error responses following the AppError pattern

## Test Requirements
- [ ] Integration test verifying entity_type filter returns only SBOMs when entity_type=sbom
- [ ] Integration test verifying entity_type filter returns only advisories when entity_type=advisory
- [ ] Integration test verifying severity filter narrows advisory results by severity level
- [ ] Integration test verifying date range filter returns only results within the specified time window
- [ ] Integration test verifying multiple filters compose correctly (e.g., entity_type=advisory AND severity=critical)
- [ ] Integration test verifying omitted filters return all results (backward compatibility)
- [ ] Integration test verifying invalid filter values return error responses

## Verification Commands
- `cargo test -p search` — search module tests pass including new filter tests
