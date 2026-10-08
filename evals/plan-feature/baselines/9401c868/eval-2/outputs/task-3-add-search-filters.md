# Task 3: Add entity type and field filters to the search endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capability to the search endpoint so users can narrow search results by entity type and entity-specific fields. The feature requirement states "add filters -- some kind of filtering capability" (TC-9002) but does not specify which filter types, fields, or operators are needed.

**Assumption pending clarification:** The following filters are planned based on the existing data model. These represent a reasonable minimum set -- the product owner should confirm or adjust before implementation:
- **Entity type filter**: allow filtering by entity type (SBOM, advisory, package) so users can scope search to a single entity kind.
- **Severity filter** (advisories): filter advisories by severity level, based on the `severity` field in `AdvisorySummary`.
- **License filter** (packages): filter packages by license, based on the `license` field in `PackageSummary`.

**Assumption pending clarification:** Filter operators are assumed to be exact match for categorical fields (entity type, severity) and substring match for text fields (license). No range filters (date ranges, version ranges) are planned without explicit requirements.

**Assumption pending clarification:** Filters are implemented as query parameters on the existing `GET /api/v2/search` endpoint rather than a new endpoint. Multiple filters combine with AND semantics.

## Files to Modify
- `modules/search/src/service/mod.rs` -- extend SearchService to accept filter parameters and apply them as WHERE clause conditions in the search query
- `modules/search/src/endpoints/mod.rs` -- add query parameter parsing for filter values (entity_type, severity, license) and pass them to the SearchService
- `common/src/db/query.rs` -- extend query builder helpers to support filter predicate construction if not already supported for the needed filter types
- `tests/api/search.rs` -- add integration tests for filtered search scenarios

## API Changes
- `GET /api/v2/search` -- MODIFY: add optional query parameters `entity_type` (enum: sbom, advisory, package), `severity` (string), `license` (string) for filtering search results

## Implementation Notes
- Per CONVENTIONS.md [Error handling]: all modified handlers must return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` handler file scope.
- Per CONVENTIONS.md [Query helpers]: use the shared query builder in `common/src/db/query.rs` for filter predicate construction. Extend the existing helpers to support the new filter types rather than writing ad-hoc SQL.
  Applies: task modifies `common/src/db/query.rs` matching the convention's query builder scope.
- Per CONVENTIONS.md [Response types]: the search endpoint must continue to return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint file scope.
- Per CONVENTIONS.md [Endpoint registration]: the search endpoint is registered in `modules/search/src/endpoints/mod.rs` for route `GET /api/v2/search`. Filter parameters should be added to the existing route handler's query parameter extraction.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md [Testing]: integration tests must hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's `tests/api/` test file scope.
- Reference the existing list endpoint patterns in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` for how query parameter filtering is implemented in other modules.
- The `severity` field is on `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs`) and `license` is on `PackageSummary` (see `modules/fundamental/src/package/model/summary.rs`). Use these existing model fields for filter matching.
- Define an enum or set of constants for the `entity_type` filter values to ensure type safety.

## Reuse Candidates
- `common/src/db/query.rs` -- existing query builder helpers for filtering and pagination that should be extended for new filter types
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference implementation for list endpoint with query parameter filtering
- `modules/fundamental/src/advisory/endpoints/list.rs` -- reference implementation for advisory list filtering
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- contains the `severity` field used for advisory filtering
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- contains the `license` field used for package filtering

## Acceptance Criteria
- [ ] Search endpoint accepts optional `entity_type` query parameter and returns only entities of that type when specified
- [ ] Search endpoint accepts optional `severity` query parameter and filters advisory results by severity
- [ ] Search endpoint accepts optional `license` query parameter and filters package results by license
- [ ] Multiple filters combine with AND semantics (e.g., entity_type=advisory AND severity=critical)
- [ ] Omitting all filters returns the same results as the unfiltered search (backward compatible)
- [ ] Search endpoint returns appropriate error for invalid filter values
- [ ] All existing search integration tests continue to pass

## Test Requirements
- [ ] Integration test: search with `entity_type=sbom` returns only SBOM entities
- [ ] Integration test: search with `entity_type=advisory` returns only advisory entities
- [ ] Integration test: search with `entity_type=package` returns only package entities
- [ ] Integration test: search with `severity` filter returns only advisories matching the specified severity
- [ ] Integration test: search with `license` filter returns only packages matching the specified license
- [ ] Integration test: search with multiple filters applies AND combination
- [ ] Integration test: search without filters returns all entity types (backward compatibility)
- [ ] Integration test: search with invalid entity_type returns an appropriate error response

## Verification Commands
- `cargo test --test search` -- run search integration tests, expect all tests to pass
- `cargo build` -- verify the project compiles without errors

## Dependencies
- None (filters work independently of performance optimization and relevance ranking)
