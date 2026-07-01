## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response model struct that represents the aggregated severity counts for advisories linked to a given SBOM. This struct will be returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The model needs to capture counts for each severity level (critical, high, medium, low) plus a total count, and implement Serialize for JSON responses.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` — AdvisorySeveritySummary struct with severity count fields

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_severity_summary` and re-export the struct

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails) which derive `Serialize`, `Deserialize`, `Clone`, `Debug`.

The struct should contain:
- `critical: u64`
- `high: u64`
- `medium: u64`
- `low: u64`
- `total: u64`

Reference `modules/fundamental/src/advisory/model/summary.rs` for the `AdvisorySummary` struct which includes the `severity` field — this is the source field used for aggregation in downstream tasks.

Use `serde` derives consistent with existing models in the module. The struct should be public and re-exported from `modules/fundamental/src/sbom/model/mod.rs`.

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct is defined with fields: critical, high, medium, low, total (all u64)
- [ ] Struct derives Serialize, Deserialize, Clone, Debug
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without warnings

## Test Requirements
- [ ] Unit test verifying `AdvisorySeveritySummary` serializes to expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test verifying deserialization from JSON round-trips correctly

## additional_fields
- priority: Major
- fixVersions: RHTPA 1.5.0