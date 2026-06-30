# Task 3: Add Search Filter Parameters to Search Endpoint

**Parent Feature**: TC-9002 — Improve search experience

## Repository
trustify-backend

## Target Branch
main

## Description
Add query parameter-based filters to the search endpoint (`GET /api/v2/search`) so users can narrow results by entity type, severity, date range, and other domain-specific attributes. Currently the search endpoint accepts only a query string with no way to filter or facet results.

**Ambiguity flag (assumption pending clarification):** The feature description says "Add filters — some kind of filtering capability" but does not specify which filters are needed, how they should be combined (AND vs OR), or whether faceted counts are required. This task assumes the following filter set based on the entity model structure: entity type (sbom/advisory/package), severity (for advisories), date range (created/modified), and license (for packages). Filter combination is assumed to be AND logic. These filter choices should be validated with the product owner and UX team.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add filter query parameters to the GET /api/v2/search endpoint handler
- `modules/search/src/service/mod.rs` — Extend SearchService to accept and apply filter criteria to search queries
- `common/src/db/query.rs` — Add filter predicate builders for entity type, severity, date range, and license fields if not already present

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters: `entity_type` (enum: sbom, advisory, package), `severity` (enum: low, medium, high, critical), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date), `license` (string, partial match)

## Implementation Notes
- Follow the existing endpoint pattern in `modules/search/src/endpoints/mod.rs` for route registration and query parameter extraction
- Use Axum's `Query<SearchFilters>` extractor with a new `SearchFilters` struct that includes optional filter fields
- Leverage the existing query builder helpers in `common/src/db/query.rs` for filtering — extend with new filter predicates as needed
- Entity type filter should determine which tables are included in the search query (e.g., if `entity_type=advisory`, only search the advisory table)
- Severity filter applies only when searching advisories (see `AdvisorySummary` severity field in `modules/fundamental/src/advisory/model/summary.rs`)
- License filter applies only when searching packages (see `PackageSummary` license field in `modules/fundamental/src/package/model/summary.rs`)
- Date range filters apply to all entity types using their created_at/updated_at timestamps
- When entity-specific filters (e.g., severity) are used without a matching entity_type filter, implicitly restrict results to the applicable entity type
- All filter parameters are optional; when omitted, no filtering is applied for that dimension

Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint registration scope.

Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`.
Applies: task modifies `common/src/db/query.rs` matching the convention's query helper scope.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `common/src/db/query.rs` — Existing filtering and pagination helpers to extend with new predicates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Has severity field to filter on
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Has license field to filter on

## Acceptance Criteria
- [ ] GET /api/v2/search accepts entity_type, severity, date_from, date_to, and license query parameters
- [ ] Filtering by entity_type restricts results to only that entity type
- [ ] Filtering by severity returns only advisories matching the specified severity
- [ ] Filtering by date range returns only results within the specified window
- [ ] Filtering by license returns only packages with matching license strings
- [ ] Multiple filters combine with AND logic
- [ ] Invalid filter values return a 400 Bad Request with a descriptive error message
- [ ] Omitting all filters returns unfiltered results (backward compatible)

## Test Requirements
- [ ] Search with entity_type=advisory returns only advisory results
- [ ] Search with severity=critical returns only critical-severity advisories
- [ ] Search with date_from and date_to returns only results within the date window
- [ ] Search with license filter returns only matching packages
- [ ] Search with combined filters (e.g., entity_type + severity) returns correctly narrowed results
- [ ] Invalid entity_type value returns 400
- [ ] Search with no filters returns results from all entity types (backward compatibility)

## Dependencies
- Depends on: Task 2 — Implement Search Relevance Ranking in SearchService (search service refactoring must be complete)

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Normal"}, "fixVersions": [{"name": "RHTPA 1.6.0"}]}

[sdlc-workflow] Description digest: sha256-md:5f5bc54dce8243b9347f52cde7e441426840a5072cd125df5741623b7cbfba4d
