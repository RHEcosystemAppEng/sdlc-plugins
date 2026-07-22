## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response model struct that represents aggregated advisory severity counts for a given SBOM. This struct will be returned by the new advisory-summary endpoint and consumed by frontend dashboard widgets and alerting integrations.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `mod advisory_summary` declaration and re-export the new struct

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — Define the `AdvisorySeveritySummary` struct with severity count fields

## Implementation Notes
Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` for the `SbomSummary` struct. Define `AdvisorySeveritySummary` with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`. Derive `Serialize`, `Deserialize`, `Clone`, `Debug` consistent with other model structs in the module. In `modules/fundamental/src/sbom/model/mod.rs`, add `mod advisory_summary;` and `pub use advisory_summary::AdvisorySeveritySummary;` following the pattern used for `SbomSummary` and `SbomDetails` re-exports.

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct is defined with fields: critical, high, medium, low, total (all u64)
- [ ] Struct derives Serialize, Deserialize, Clone, Debug
- [ ] Struct is publicly re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without warnings

## Test Requirements
- [ ] Verify `AdvisorySeveritySummary` can be serialized to JSON with expected field names
- [ ] Verify deserialization from JSON produces correct field values

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors