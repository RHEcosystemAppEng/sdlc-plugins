## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint. The feature requirement says "some kind of filtering capability" without specifying which filters. **Assumption pending clarification**: MVP filters include `entity_type` (sbom/advisory/package), `created_after`/`created_before` (date range), and `severity` (for advisory results). These are chosen because the corresponding fields already exist in the entity models (`entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs`).

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add optional query parameters for `entity_type`, `created_after`, `created_before`, and `severity` to the `GET /api/v2/search` handler
- `modules/search/src/service/mod.rs` — Accept filter parameters in the search service method and apply them as WHERE clause predicates alongside the full-text search query
- `common/src/db/query.rs` — Add reusable filter predicate builders for date-range filtering and enum-based entity type filtering, following the existing pattern of shared query helpers

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters:
  - `entity_type` (string, optional): Filter by entity type — `sbom`, `advisory`, or `package`
  - `created_after` (ISO 8601 datetime, optional): Filter results created after this timestamp
  - `created_before` (ISO 8601 datetime, optional): Filter results created before this timestamp
  - `severity` (string, optional): Filter advisory results by severity level (e.g., `critical`, `high`, `medium`, `low`)

## Implementation Notes
- In `modules/search/src/endpoints/mod.rs`, add the new query parameters as optional fields in the handler's query extractor struct. Follow the pattern used in existing list endpoints like `modules/fundamental/src/sbom/endpoints/list.rs` for query parameter extraction.
- In `modules/search/src/service/mod.rs`, apply filters as additional WHERE predicates. For `entity_type`, filter the result set to only include the specified entity. For date range, add `created_at >= :created_after AND created_at <= :created_before` predicates. For `severity`, join/filter on the advisory severity field from `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`.
- Add reusable date-range and enum filter helpers in `common/src/db/query.rs` alongside the existing filtering helpers. These should be generic enough for other modules to reuse.
- All new parameters are optional and additive — omitting them returns unfiltered results, preserving backward compatibility.
- All handlers return `Result<T, AppError>` with `.context()` wrapping per the error handling convention.
- Per CONVENTIONS.md: use shared query helpers from `common/src/db/query.rs` for filtering.
  Applies: task modifies `common/src/db/query.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md: endpoint handlers follow Axum extraction patterns.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.

## Reuse Candidates
- `common/src/db/query.rs` — Existing query builder helpers for filtering and pagination; new filter predicates should follow the same pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — Example of query parameter extraction in a list endpoint; follow this pattern for the new filter parameters
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the severity field used for severity filtering

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?entity_type=package` returns only package results
- [ ] `GET /api/v2/search?created_after=2024-01-01T00:00:00Z` returns only results created after the specified date
- [ ] `GET /api/v2/search?created_before=2024-06-01T00:00:00Z` returns only results created before the specified date
- [ ] `GET /api/v2/search?severity=critical` returns only advisory results with critical severity
- [ ] Filters can be combined (e.g., `entity_type=advisory&severity=high`)
- [ ] Omitting all filter parameters returns the same results as before (backward compatible)
- [ ] **Assumption pending clarification**: the chosen filter set (entity_type, date range, severity) covers MVP needs; additional filters may be needed based on stakeholder input

## Test Requirements
- [ ] Each filter parameter correctly narrows the result set when used individually
- [ ] Multiple filters combine with AND semantics
- [ ] Invalid filter values return appropriate error responses (400 Bad Request)
- [ ] Empty result sets return valid empty `PaginatedResults` (not errors)
- [ ] Filtering does not break relevance scoring from Task 2

## Dependencies
- Depends on: Task 1 — Optimize search query performance (requires the full-text search query infrastructure)

## Additional Fields
- priority: Normal
- fixVersions: RHTPA 1.6.0

## Description Digest
[sdlc-workflow] Description digest: sha256-md:<computed-at-creation-time>
(Actual digest computed by re-fetching description from Jira API and running `scripts/sha256-digest.py`)
