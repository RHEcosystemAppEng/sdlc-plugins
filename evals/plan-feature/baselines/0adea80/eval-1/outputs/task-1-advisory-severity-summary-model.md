# Task 1 — Add AdvisorySeveritySummary response model

## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response model struct that represents the aggregated severity counts for advisories linked to an SBOM. This struct will be the response type for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The struct must include fields for each severity level (`critical`, `high`, `medium`, `low`) and a `total` count, all as integers. It must derive `Serialize`, `Deserialize`, and `ToSchema` (for OpenAPI documentation) following the existing model patterns in the SBOM module.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — defines the `AdvisorySeveritySummary` struct with severity count fields

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`). These structs derive `Serialize`, `Deserialize`, and use `utoipa::ToSchema` for OpenAPI spec generation.
- The struct fields should be:
  - `critical: i64`
  - `high: i64`
  - `medium: i64`
  - `low: i64`
  - `total: i64`
- Reference the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` to understand how the `severity` field is represented (this is the field that will be grouped on in the service layer query).
- Per docs/constraints.md Section 5 (Code Change Rules): changes must be scoped to the files listed; code must not be modified without first inspecting it; implementation must follow the patterns referenced in these notes.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — demonstrates the derive macros, struct layout, and module export pattern to follow for the new model
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the `severity` field definition showing how severity levels are represented in the existing codebase

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs`
- [ ] Struct has fields: `critical`, `high`, `medium`, `low`, `total` (all integer types)
- [ ] Struct derives `Serialize`, `Deserialize`, and `ToSchema`
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Verify the struct can be serialized to JSON with the expected field names: `{ "critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0 }`
- [ ] Verify the struct can be deserialized from a valid JSON object

## Verification Commands
- `cargo build -p trustify-module-fundamental` — should compile without errors

## Dependencies
- None
