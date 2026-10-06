## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model and a severity aggregation service method that queries the existing `sbom_advisory` join table to produce deduplicated severity counts for a given SBOM. This provides the data layer for the new advisory-summary endpoint defined in TC-9001.

The service method must:
- Accept an SBOM ID and verify the SBOM exists (return an error if not found)
- Query the `sbom_advisory` join table joined with the `advisory` table to retrieve severity values
- Deduplicate advisories by advisory ID before counting
- Group counts by severity level (Critical, High, Medium, Low)
- Return an `AdvisorySeveritySummary` struct with fields: `critical`, `high`, `medium`, `low`, `total`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` to register the new model module
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod advisory_summary;` to register the new service module

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct with serde serialization
- `modules/fundamental/src/sbom/service/advisory_summary.rs` — severity aggregation query method on `SbomService`

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) for struct definition, derive macros, and serde attributes.
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) for method signatures and error handling with `Result<T, AppError>` and `.context()` wrapping (from `common/src/error.rs`).
- Use SeaORM to construct the aggregation query. Join `entity::sbom_advisory` with `entity::advisory` to access the severity field on `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs` for the severity field definition).
- Deduplicate by advisory ID using `SELECT DISTINCT` or `GROUP BY` on the advisory primary key before counting by severity.
- The `AdvisorySeveritySummary` struct should derive `Clone, Debug, Serialize, Deserialize, PartialEq, Eq` and use `#[serde(rename_all = "camelCase")]` if the existing response models use camelCase (check `SbomSummary` for the convention).
- Per repo conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping. The service method should follow this pattern.

## Reuse Candidates
- `entity/src/sbom_advisory.rs` — the SBOM-Advisory join table entity; use this for the aggregation query join
- `entity/src/advisory.rs` — the Advisory entity containing the severity field
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for the severity field type and values
- `common/src/error.rs::AppError` — error type for service method return values
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service to extend or follow as a pattern

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`
- [ ] Service method accepts an SBOM ID and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Service method returns an error (suitable for 404 mapping) when the SBOM ID does not exist
- [ ] Advisories are deduplicated by advisory ID before counting (an advisory linked to the same SBOM twice is counted once)
- [ ] Severity counts are correctly grouped into Critical, High, Medium, Low buckets
- [ ] `total` field equals the sum of all severity counts

## Test Requirements
- [ ] Unit test: aggregation with known advisory-SBOM relationships produces correct counts
- [ ] Unit test: duplicate advisory links to the same SBOM are deduplicated (counted once)
- [ ] Unit test: SBOM with no advisories returns all-zero counts
- [ ] Unit test: non-existent SBOM ID returns an appropriate error

## Dependencies
- None
