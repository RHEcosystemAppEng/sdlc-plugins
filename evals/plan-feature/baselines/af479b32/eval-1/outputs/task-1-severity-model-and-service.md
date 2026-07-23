## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model and a severity aggregation method to `SbomService`. This provides the data layer for the new advisory-summary endpoint (TC-9001). The model represents aggregated severity counts (critical, high, medium, low, total) for advisories linked to an SBOM. The service method queries the `sbom_advisory` join table, deduplicates advisories by advisory ID, retrieves each advisory's severity from the `advisory` entity, and groups counts by severity level.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`. Derives `Serialize`, `ToSchema` (for OpenAPI), `Debug`, `Clone`.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`
- `modules/fundamental/src/sbom/service/sbom.rs` — add `pub async fn advisory_severity_summary(&self, sbom_id: Id) -> Result<AdvisorySeveritySummary, AppError>` method that performs the aggregation query

## Implementation Notes
- Follow the existing module pattern: each domain module uses `model/ + service/ + endpoints/` structure. The new `advisory_summary.rs` model file follows the pattern of `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`).
- Per Key Conventions §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping on fallible operations. See `modules/fundamental/src/sbom/service/sbom.rs` for the established pattern.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service file scope.
- The aggregation query should use SeaORM to join `sbom_advisory` with `advisory` entity, group by the advisory's severity field, and count distinct advisory IDs. Reference `entity/sbom_advisory.rs` for the join table schema and `entity/advisory.rs` for the severity field.
- The service method must verify the SBOM exists before running the aggregation. If not found, return `AppError::NotFound` consistent with existing SBOM service methods.
- Deduplication: count each advisory only once per SBOM even if multiple join records exist (use `COUNT(DISTINCT advisory_id)`).
- Per Key Conventions §Response types: this endpoint returns a single summary object, not a paginated list — do not use `PaginatedResults<T>`.
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's Rust model file scope.

## Reuse Candidates
- `entity/sbom_advisory.rs` — SBOM-Advisory join table entity; provides the relationship needed for the aggregation query
- `entity/advisory.rs` — Advisory entity with severity field; source of severity classification
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing advisory summary struct with severity field; reference for severity enum values
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list patterns to follow for the new aggregation method
- `common/src/error.rs::AppError` — error enum used by all service methods

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical`, `high`, `medium`, `low`, `total` (all `u64`)
- [ ] `SbomService::advisory_severity_summary(sbom_id)` returns correct severity counts for a given SBOM
- [ ] Advisory deduplication: each advisory is counted only once regardless of how many join records exist
- [ ] Returns `AppError::NotFound` (mapping to HTTP 404) when the SBOM ID does not exist
- [ ] Severity mapping covers all four levels: Critical, High, Medium, Low

## Test Requirements
- [ ] Unit test: `advisory_severity_summary` returns correct counts for an SBOM with known advisories at each severity level
- [ ] Unit test: `advisory_severity_summary` deduplicates advisories linked via multiple join records
- [ ] Unit test: `advisory_severity_summary` returns all-zero counts for an SBOM with no advisories
- [ ] Unit test: `advisory_severity_summary` returns error for a nonexistent SBOM ID

## Dependencies
- Depends on: None
