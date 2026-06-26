## Repository
trustify-backend

## Target Branch
main

## Description
Define the `AdvisorySeveritySummary` response struct that represents aggregated advisory severity counts for a given SBOM. This model is the foundation for the new endpoint and will be consumed by the endpoint handler and service layer. The struct must serialize to `{ critical, high, medium, low, total }` as specified in the feature requirements.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — AdvisorySeveritySummary struct with serde Serialize/Deserialize derives

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` and re-export the new struct

## Implementation Notes
Follow the existing model pattern established by `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails). The new struct should derive `Clone, Debug, Serialize, Deserialize, PartialEq, Eq` consistent with sibling model types.

The struct fields should be:
- `critical: u64`
- `high: u64`
- `medium: u64`
- `low: u64`
- `total: u64`

Also add a `SeverityThreshold` enum (`Critical`, `High`, `Medium`, `Low`) to support the optional `?threshold` query param in a later task. Derive `Deserialize` on the enum so Axum can parse it from query parameters.

Per CONVENTIONS.md §Error Handling: use Result<T, AppError> with .context() wrapping.
Applies: task modifies `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Follow the same struct layout, derive macros, and module registration pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference the severity field type used in advisory summaries to ensure consistency

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: critical, high, medium, low, total (all u64)
- [ ] `SeverityThreshold` enum exists with variants: Critical, High, Medium, Low
- [ ] Struct derives Serialize and Deserialize for JSON response serialization
- [ ] Module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles with `cargo check -p trustify-fundamental`

## Test Requirements
- [ ] Unit test verifying AdvisorySeveritySummary serializes to expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test verifying SeverityThreshold deserializes from lowercase string values

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors

[sdlc-workflow] Description digest: sha256-md:a3c7e9f1b2d4068573e19a4c5d8f2b6e7a90c1d3e5f478029b1a3c5d7e9f0b2d
