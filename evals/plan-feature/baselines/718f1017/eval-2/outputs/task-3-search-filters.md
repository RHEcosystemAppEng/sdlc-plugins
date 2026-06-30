## Repository
trustify-backend

## Target Branch
main

## Description
Add filter query parameters to the GET /api/v2/search endpoint, allowing users to narrow search results by entity type, advisory severity, and package license. This addresses the "Add filters" MVP requirement from TC-9002.

**Ambiguity note:** The feature specifies "some kind of filtering capability" without defining which filters. Assumption (pending clarification): filters are based on entity type (SBOM, advisory, package) as the primary discriminator, with entity-specific secondary filters — severity for advisories (leveraging the existing `severity` field on `AdvisorySummary`) and license for packages (leveraging the existing `license` field on `PackageSummary`). Filters are additive query parameters that are optional and backward-compatible.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameter parsing to the search endpoint handler (entity type, severity, license)
- `modules/search/src/service/mod.rs` — extend SearchService to accept and apply filter criteria in search queries

## Files to Create
- `modules/search/src/model/mod.rs` — define `SearchFilter` struct to represent parsed filter criteria (entity_type, severity, license)

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `entity_type` (enum: sbom, advisory, package), `severity` (string, for advisory filtering), `license` (string, for package filtering). All parameters are optional; when omitted, no filtering is applied (backward-compatible).

## Implementation Notes
- The search endpoint in `modules/search/src/endpoints/mod.rs` currently handles `GET /api/v2/search`. Extend the Axum handler to parse new optional query parameters using Axum's `Query` extractor.
- Define a `SearchFilter` struct (or extend the existing query params struct) with optional fields: `entity_type: Option<EntityType>`, `severity: Option<String>`, `license: Option<String>`.
- In the `SearchService`, apply filters using the shared query builder helpers from `common/src/db/query.rs`. Use the existing filtering patterns — do not introduce a new filtering mechanism.
- Entity type filtering should control which entity tables are included in the search query (e.g., if `entity_type=advisory`, only search the advisory table).
- Severity filtering should use the `severity` field from the `AdvisorySummary` model (`modules/fundamental/src/advisory/model/summary.rs`).
- License filtering should use the `license` field from the `PackageSummary` model (`modules/fundamental/src/package/model/summary.rs`).
- Follow the endpoint registration pattern in `modules/search/src/endpoints/mod.rs` for route configuration.
- Per CONVENTIONS.md (repo-level): list endpoints return `PaginatedResults<T>`. The filtered search results must continue to use this response wrapper.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md (repo-level): all handlers return `Result<T, AppError>` with `.context()` wrapping. Apply this error handling pattern to filter validation errors.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; use the existing filter application pattern rather than writing custom WHERE clause construction
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — has `severity` field; reference for available filter values
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — has `license` field; reference for available filter values
- `modules/fundamental/src/sbom/endpoints/list.rs` — example of a list endpoint with query parameter parsing; follow the same Axum handler pattern
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper to use for filtered results

## Acceptance Criteria
- [ ] GET /api/v2/search accepts optional `entity_type` query parameter to filter by entity type (sbom, advisory, package)
- [ ] GET /api/v2/search accepts optional `severity` query parameter to filter advisory results by severity
- [ ] GET /api/v2/search accepts optional `license` query parameter to filter package results by license
- [ ] Filters are composable — multiple filter parameters can be combined in a single request
- [ ] Omitting all filter parameters returns unfiltered results (backward-compatible behavior)
- [ ] Invalid filter values return a meaningful error response (not a 500)

## Test Requirements
- [ ] Integration test: search with `entity_type=advisory` returns only advisory results
- [ ] Integration test: search with `entity_type=sbom` returns only SBOM results
- [ ] Integration test: search with `severity=critical` returns only advisories with critical severity
- [ ] Integration test: search with combined filters (`entity_type=advisory&severity=high`) applies both filters
- [ ] Integration test: search without filter parameters returns results from all entity types (backward compatibility)
- [ ] Integration test: search with invalid entity_type returns appropriate error response

## Verification Commands
- `cargo test -p search` — search module tests pass
- `cargo test -p tests --test search` — search integration tests pass
- `curl "http://localhost:8080/api/v2/search?q=test&entity_type=advisory"` — returns only advisory results

## Documentation Updates
- `README.md` — update API documentation to describe the new filter query parameters on the search endpoint

## Dependencies
- Depends on: Task 2 — Refactor SearchService for full-text search (filter logic builds on the refactored search query infrastructure)

<!-- [sdlc-workflow] Description digest: sha256-md:7947ed79e56b9ee7a34b8ef447acf66517ebb02d549c53d9d7d735c21201b0b2 -->
