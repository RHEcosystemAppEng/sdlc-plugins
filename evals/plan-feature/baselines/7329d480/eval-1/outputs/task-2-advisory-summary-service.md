# Task 2 — Implement advisory severity aggregation query in SbomService

additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }

## Repository
trustify-backend

## Target Branch
main

## Description
Add an `advisory_summary` method to `SbomService` that queries the `sbom_advisory` join table, groups advisories by severity, deduplicates by advisory ID, and returns an `AdvisorySeveritySummary`. This method validates that the SBOM exists (returning an appropriate error for 404 propagation) and performs the aggregation as a single database query for performance.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `pub async fn advisory_summary(&self, sbom_id: Uuid, db: &DatabaseConnection) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`
- `modules/fundamental/src/sbom/service/mod.rs` — ensure the new method is accessible (may already be via `SbomService` re-export)

## Implementation Notes
The new method should:

1. Verify the SBOM exists by querying the `sbom` entity. If not found, return `AppError::NotFound` (see `common/src/error.rs` for the error variant).
2. Query `entity/src/sbom_advisory.rs` (the SBOM-Advisory join table) filtered by the given SBOM ID.
3. Join with `entity/src/advisory.rs` to access the `severity` field on each advisory.
4. Use a `GROUP BY severity` with `COUNT(DISTINCT advisory_id)` to deduplicate advisories and produce counts per severity level.
5. Map the query result rows into the `AdvisorySeveritySummary` struct, defaulting missing severity levels to 0.
6. Compute `total` as the sum of all severity counts.

Follow the existing patterns in `SbomService` (see `modules/fundamental/src/sbom/service/sbom.rs`) for database connection usage, error handling, and method signatures.

Per CONVENTIONS.md §Error handling: return `Result<AdvisorySeveritySummary, AppError>` and wrap database errors with `.context()`.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` error-handling scope.

Per CONVENTIONS.md §Query helpers: use shared query builder helpers from `common/src/db/query.rs` if applicable for filtering.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` service scope.

Per CONVENTIONS.md §Module pattern: add the service method within the existing `service/` layer of the SBOM module.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's module directory pattern.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct; add the new method here alongside `fetch`, `list`, `ingest`
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; may be useful for constructing the aggregation query
- `common/src/error.rs::AppError` — error enum for not-found and internal server error responses
- `entity/src/sbom_advisory.rs` — the join table entity to query for SBOM-to-advisory relationships
- `entity/src/advisory.rs` — advisory entity containing the `severity` field to group by
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference for how existing services query advisory entities

## Acceptance Criteria
- [ ] `SbomService::advisory_summary` method exists and compiles
- [ ] Method returns `AdvisorySeveritySummary` with correct severity counts for a given SBOM
- [ ] Method returns an error (suitable for 404 response) when the SBOM ID does not exist
- [ ] Advisory counts are deduplicated by advisory ID (no double-counting)
- [ ] Severity levels not present in the data default to 0
- [ ] `total` field equals the sum of `critical + high + medium + low`

## Test Requirements
- [ ] Unit or integration test: SBOM with advisories at multiple severity levels returns correct counts
- [ ] Unit or integration test: SBOM with no advisories returns all-zero counts
- [ ] Unit or integration test: non-existent SBOM ID returns not-found error

## Dependencies
- Depends on: Task 1 — Define advisory severity summary response model
