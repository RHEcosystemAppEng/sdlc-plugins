# Task 1 — Advisory Severity Summary Model

## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response struct that represents aggregated advisory severity counts for an SBOM. This struct is the response type for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. It holds counts for each severity level (critical, high, medium, low) and a total count. A companion `SeverityThreshold` enum is included to support optional threshold filtering in later tasks.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — Define `AdvisorySeveritySummary` struct with `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64` fields, deriving `Serialize`, `Deserialize`, `Clone`, `Debug`, `PartialEq`. Define `SeverityThreshold` enum with variants `Critical`, `High`, `Medium`, `Low` that implements `FromStr` for query param deserialization.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` declaration and re-export `AdvisorySeveritySummary` and `SeverityThreshold` types.

## Implementation Notes
Follow the existing model struct pattern established in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`). Both derive `Serialize`, `Deserialize`, and related traits. The new struct lives alongside these files in the same `model/` directory.

The `SeverityThreshold` enum should implement `serde::Deserialize` so Axum can extract it from query parameters. Look at how existing query parameter types are defined in the codebase for the deserialization pattern.

Per CONVENTIONS.md §Module pattern: place the model struct in the `model/` subdirectory of the `sbom` module. Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's `.rs` module file scope.

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical`, `high`, `medium`, `low`, `total` (all `u64`)
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, `PartialEq`
- [ ] `SeverityThreshold` enum exists with variants `Critical`, `High`, `Medium`, `Low`
- [ ] `SeverityThreshold` implements `Deserialize` and `FromStr`
- [ ] Types are re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] `cargo check` passes with no errors

## Test Requirements
- [ ] Unit test that `AdvisorySeveritySummary` round-trips through serde JSON serialization (serialize then deserialize, assert equality)
- [ ] Unit test that `SeverityThreshold::from_str("critical")` returns `Ok(SeverityThreshold::Critical)` and invalid values return `Err`

[sdlc-workflow] Description digest: sha256-md:4eed90f1d100cda8230c88f6525edb4af3a36e374d9f7eac5344bfeae6b8fd22
