## Repository
trustify-backend

## Target Branch
main

## Description
Add the AdvisorySeveritySummary response model and a severity aggregation service method to SbomService. The model represents the JSON response shape for the advisory-summary endpoint: `{ critical: N, high: N, medium: N, low: N, total: N }`. The service method queries the existing `sbom_advisory` join table to count unique advisories grouped by severity for a given SBOM ID, deduplicating by advisory ID.

This task establishes the data layer that the endpoint (Task 2) will consume.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` — AdvisorySeveritySummary struct with Serialize derive and fields: critical (u64), high (u64), medium (u64), low (u64), total (u64)

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_severity_summary;` and re-export AdvisorySeveritySummary
- `modules/fundamental/src/sbom/service/sbom.rs` — add `pub async fn get_advisory_severity_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method

## Implementation Notes
- Follow the existing module pattern in `modules/fundamental/src/sbom/model/`: see `summary.rs` (SbomSummary) and `details.rs` (SbomDetails) for the struct definition pattern with Serialize derive.
- The aggregation query should join `sbom_advisory` with `advisory` to access the severity field. Use SeaORM query builder, referencing the entities in `entity/src/sbom_advisory.rs` and `entity/src/advisory.rs`.
- Deduplicate by advisory ID before counting — use `GROUP BY` on the advisory entity's severity field with `COUNT(DISTINCT advisory_id)`.
- The service method must return `Result<AdvisorySeveritySummary, AppError>`. Use `.context()` wrapping for error handling as established in the codebase.
- Before querying, verify the SBOM exists by checking the `sbom` entity. Return `AppError::NotFound` (404) if not found, consistent with existing SBOM endpoints (see `modules/fundamental/src/sbom/service/sbom.rs` fetch method).
- Use shared query helpers from `common/src/db/query.rs` if applicable for the aggregation query.
- Per Key Conventions — Module pattern: follow `model/ + service/` structure.
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` matching the convention's module structure scope.
- Per Key Conventions — Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust handler file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — demonstrates the model struct pattern with Serialize derive; follow the same structure for AdvisorySeveritySummary
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service methods (fetch, list) demonstrate the query pattern, error handling, and entity interaction to follow
- `common/src/error.rs::AppError` — the shared error type with NotFound variant for 404 responses
- `entity/src/sbom_advisory.rs` — the SBOM-Advisory join table entity needed for the aggregation query

## Acceptance Criteria
- [ ] AdvisorySeveritySummary struct exists with fields: critical, high, medium, low, total (all u64)
- [ ] AdvisorySeveritySummary is re-exported from sbom model module
- [ ] SbomService has a `get_advisory_severity_summary` method that returns severity counts for a given SBOM ID
- [ ] Advisory counts are deduplicated by advisory ID (each advisory counted once regardless of how many vulnerabilities it contains)
- [ ] Method returns AppError (404) when the SBOM ID does not exist

## Test Requirements
- [ ] Unit test: verify AdvisorySeveritySummary serializes to the expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Service test: verify aggregation returns correct counts for an SBOM with multiple advisories at different severity levels
- [ ] Service test: verify 404 error when SBOM ID does not exist
- [ ] Service test: verify deduplication — linking the same advisory to an SBOM twice does not double-count

## Dependencies
- None
