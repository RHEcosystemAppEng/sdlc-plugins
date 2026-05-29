## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model struct that represents the aggregated severity counts for advisories linked to a given SBOM. This model will be used as the response type for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The struct includes counts for each severity level (critical, high, medium, low) and a total count.

## Files to Modify
- `modules/fundamental/src/advisory/model/mod.rs` — export the new `AdvisorySeveritySummary` struct

## Files to Create
- `modules/fundamental/src/advisory/model/severity_summary.rs` — define the `AdvisorySeveritySummary` struct with serde serialization

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary` struct) and `modules/fundamental/src/advisory/model/details.rs` (`AdvisoryDetails` struct). Both use `#[derive(Serialize, Deserialize, Debug, Clone)]` and are re-exported from the module's `mod.rs`.
- The struct fields should be: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`.
- Use `serde::Serialize` and `serde::Deserialize` derives to match the serialization pattern used by sibling model structs.
- The severity enum values to match against are already defined in the `AdvisorySummary` struct's `severity` field in `modules/fundamental/src/advisory/model/summary.rs`.
- Per docs/constraints.md §4.7: reference actual file paths and symbol names found during repository analysis.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the `severity` field definition showing the severity enum values used in the system; reuse the same severity classification.
- `common/src/model/paginated.rs::PaginatedResults` — demonstrates the project's pattern for response model structs with serde derives.

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct is defined with fields: `critical`, `high`, `medium`, `low`, `total` (all `u64`)
- [ ] Struct derives `Serialize`, `Deserialize`, `Debug`, `Clone`
- [ ] Struct is re-exported from `modules/fundamental/src/advisory/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Unit test verifying `AdvisorySeveritySummary` serializes to expected JSON shape: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test verifying deserialization from valid JSON produces correct struct values

[sdlc-workflow] Description digest: sha256:02e3b51ec728614d8c312c52ed021a3e4e9f01db7e40825802024eb40b76817f
