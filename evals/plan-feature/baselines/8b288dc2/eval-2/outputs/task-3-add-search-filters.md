## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint, supporting entity type filter, severity filter (for advisories), and date range filter (created/modified). Filters are implemented as optional query parameters on the existing search endpoint, maintaining full backward compatibility.

**Ambiguity flag:** The feature specifies "Add filters — Some kind of filtering capability" without defining which filters to support. This task assumes (Assumption A3) the following filter dimensions: entity type (SBOM, advisory, package), severity (for advisories), and date range (created_after/created_before). The actual filter set must be confirmed with the product owner before implementation.

**Assumption:** Filters are additive optional query parameters that default to no filtering when omitted (Assumption A4). This preserves backward compatibility for existing API consumers.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameters to the search endpoint handler
- `modules/search/src/service/mod.rs` — add filter logic to SearchService query construction
- `common/src/db/query.rs` — add filter predicate builders if not already present for the needed filter types

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters:
  - `entity_type` (string, optional) — filter by entity type: "sbom", "advisory", "package"
  - `severity` (string, optional) — filter advisories by severity level
  - `created_after` (ISO 8601 date, optional) — filter by creation date lower bound
  - `created_before` (ISO 8601 date, optional) — filter by creation date upper bound

## Implementation Notes
- Add filter parameter structs to the search endpoint in `modules/search/src/endpoints/mod.rs`, following the existing Axum `Query` extractor pattern used in other endpoints (e.g., `modules/fundamental/src/sbom/endpoints/list.rs`)
- Implement filter predicate construction in `modules/search/src/service/mod.rs`, applying filters as WHERE clause conditions to the search query
- Use the existing query builder patterns in `common/src/db/query.rs` for filtering and pagination — extend with date range and enum filtering if not already supported
- Reference the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` for the severity field structure
- Validate filter parameters: return `AppError` for invalid entity types or malformed date strings
- When no filters are provided, behavior must be identical to the current search endpoint (backward compatible)
- Per docs/constraints.md §5.2: inspect existing endpoint and query code before modifying
- Per docs/constraints.md §5.4: reuse existing query utilities, do not duplicate filter logic

## Reuse Candidates
- `common/src/db/query.rs` — existing filtering and pagination helpers; extend with date range and enum filter support
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for Axum Query parameter extraction pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity field definition for filter validation

## Acceptance Criteria
- [ ] Search endpoint accepts optional `entity_type` filter parameter and returns only matching entity types
- [ ] Search endpoint accepts optional `severity` filter parameter and returns only advisories matching the severity
- [ ] Search endpoint accepts optional `created_after` and `created_before` date range parameters
- [ ] Filters can be combined (e.g., entity_type=advisory AND severity=critical)
- [ ] When no filters are provided, search behavior is unchanged from before this task (backward compatible)
- [ ] Invalid filter values return appropriate error responses

## Test Requirements
- [ ] Integration test: filter by entity_type=sbom returns only SBOMs
- [ ] Integration test: filter by severity returns only advisories with matching severity
- [ ] Integration test: date range filter returns only entities within the specified range
- [ ] Integration test: combined filters work correctly (intersection semantics)
- [ ] Integration test: no filters returns same results as unfiltered search
- [ ] Integration test: invalid filter values return 400 error response
- [ ] Verify existing tests in `tests/api/search.rs` still pass

## Verification Commands
- `cargo test -p search` — search module tests pass
- `cargo test --test search` — search integration tests pass

## Dependencies
- Depends on: Task 2 — Implement full-text search service with tsvector/tsquery

---

[sdlc-workflow] Description digest: sha256-md:e3f23a65f2647ebb1a2298eb749a17c327f704ab2c6d999fe027496e100a1979
