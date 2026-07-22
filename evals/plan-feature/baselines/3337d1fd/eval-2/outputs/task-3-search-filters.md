## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capability to the search endpoint, allowing users to narrow search results by entity type and entity-specific fields. The current `GET /api/v2/search` endpoint accepts only a search query with no way to filter results. This task adds query parameters for filtering by entity type (SBOM, advisory, package) and by key fields (severity for advisories, license for packages), directly addressing the "add filters" requirement.

**Assumption (pending clarification):** The feature description specifies "some kind of filtering capability" without defining which fields, operators, or combination logic. This task assumes: (1) entity-type filter (enum: sbom, advisory, package), (2) severity filter for advisories (using the severity field from `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`), (3) license filter for packages (using the license field from `PackageSummary` in `modules/fundamental/src/package/model/summary.rs`), and (4) filters combine with AND logic. If additional filters or OR logic are required, the scope will need expansion.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add filter query parameters to the `GET /api/v2/search` handler (entity type, severity, license)
- `modules/search/src/service/mod.rs` — Accept filter parameters in `SearchService` and apply them as WHERE clause predicates in the search query
- `common/src/db/query.rs` — Add shared filter predicate builders for entity-type discrimination and field-level filtering, reusable by other endpoints

## Files to Create
- `modules/search/src/model/filter.rs` — `SearchFilter` struct defining the filter parameter types (entity type enum, optional severity, optional license)

## Implementation Notes
- Follow the existing query helper pattern in `common/src/db/query.rs` for building filter predicates. The file already contains shared filtering, pagination, and sorting helpers — extend it with new predicate builders rather than duplicating logic in the search module.
  Applies: task modifies `common/src/db/query.rs` matching the convention's shared query helper scope.
- Define filter query parameters using Axum's `Query<SearchFilter>` extractor pattern, consistent with how list endpoints handle query parameters (e.g., `modules/fundamental/src/sbom/endpoints/list.rs`).
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint scope.
- The `SearchFilter` struct should use `Option<T>` for all filter fields so that omitting a filter parameter means "no filter" (all entities returned). Define an `EntityType` enum with variants `Sbom`, `Advisory`, `Package` using `#[serde(rename_all = "lowercase")]`.
- Severity filtering should match the severity field pattern from `modules/fundamental/src/advisory/model/summary.rs` (the `AdvisorySummary` struct's severity field).
- License filtering should support substring matching (case-insensitive ILIKE) against the license field from `modules/fundamental/src/package/model/summary.rs` (the `PackageSummary` struct's license field).
- Error handling must follow the `Result<T, AppError>` pattern with `.context()` wrapping, consistent with `common/src/error.rs`.
- Re-export the filter model from `modules/search/src/model/mod.rs` (created in Task 2).
- All filter parameters must be documented in the OpenAPI schema if the project uses utoipa or similar — check `modules/search/src/endpoints/mod.rs` for existing schema annotations.

## Acceptance Criteria
- [ ] `GET /api/v2/search?q=term&entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?q=term&entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?q=term&entity_type=package` returns only package results
- [ ] `GET /api/v2/search?q=term&severity=critical` returns only advisories with critical severity
- [ ] `GET /api/v2/search?q=term&license=MIT` returns only packages with MIT in their license (case-insensitive substring match)
- [ ] Multiple filters combine with AND logic (e.g., `entity_type=advisory&severity=high`)
- [ ] Omitting all filter parameters returns all entity types (backward compatible)
- [ ] Invalid filter values return a 400 Bad Request with a descriptive error message
- [ ] Filtered results retain relevance ranking from Task 2

## Test Requirements
- [ ] Integration test in `tests/api/search.rs` verifying entity-type filtering returns only the specified type
- [ ] Integration test verifying severity filtering narrows results to matching advisories
- [ ] Integration test verifying license filtering narrows results to matching packages
- [ ] Integration test verifying multiple filters combine with AND logic
- [ ] Integration test verifying omitted filters return all results (backward compatibility)
- [ ] Integration test verifying invalid filter values return 400 status code

## Dependencies
- Depends on: Task 2 — Implement relevance-ranked search results (this task adds filter parameters to the same endpoint and model structure established in Task 2)
