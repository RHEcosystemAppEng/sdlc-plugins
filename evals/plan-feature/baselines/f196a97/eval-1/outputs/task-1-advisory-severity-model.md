# Task 1 — Add AdvisorySeveritySummary response model

## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response struct that represents the aggregated severity counts for advisories linked to an SBOM. This model will be returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The struct must include fields for `critical`, `high`, `medium`, `low`, and `total` counts, and derive `Serialize` for JSON responses.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — new struct `AdvisorySeveritySummary` with severity count fields

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` declaration and re-export `AdvisorySeveritySummary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: u64, high: u64, medium: u64, low: u64, total: u64 }`

## Implementation Notes
- Follow the existing model pattern established by `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`). These structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`, and use `serde` for JSON serialization.
- The struct should derive at minimum `Serialize`, `Debug`, `Clone` (and `Deserialize` for symmetry/testing).
- Use `u64` for count fields to accommodate large advisory sets.
- Include the `total` field as a convenience sum of all severity levels.
- The `threshold` query parameter filtering will be handled at the endpoint/service layer (Task 2), not in this model.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — established pattern for SBOM-related response structs; follow its derive macros and module registration pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the `severity` field definition that maps to the severity levels this struct aggregates

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with `critical`, `high`, `medium`, `low`, and `total` fields of type `u64`
- [ ] Struct derives `Serialize` and is re-exported from the sbom model module
- [ ] Struct compiles and can be serialized to JSON with the expected field names

## Test Requirements
- [ ] Unit test verifying `AdvisorySeveritySummary` serializes to the expected JSON shape: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test verifying default/zero-value struct serializes correctly

## Dependencies
- None
