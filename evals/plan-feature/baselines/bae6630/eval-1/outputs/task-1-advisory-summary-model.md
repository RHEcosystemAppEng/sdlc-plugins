## Repository
trustify-backend

## Target Branch
main

## Description
Define the response model for the advisory severity aggregation endpoint. This struct will carry the severity counts (critical, high, medium, low, total) returned by `GET /api/v2/sbom/{id}/advisory-summary`. Also define a `SeverityThreshold` enum to represent the optional `?threshold` query parameter values.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — Response struct `AdvisorySeveritySummary` and `SeverityThreshold` enum

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary` and `SeverityThreshold`

## Implementation Notes
- Follow the pattern in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/advisory/model/summary.rs` (AdvisorySummary) for struct definition conventions: derive `Serialize`, `Deserialize`, and `utoipa::ToSchema`.
- `AdvisorySeveritySummary` fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`. All counts are non-negative integers.
- `SeverityThreshold` enum variants: `Critical`, `High`, `Medium`, `Low`. Derive `Deserialize` so it can be parsed from query parameters. Use `#[serde(rename_all = "lowercase")]` for case-insensitive URL query parsing.
- Register the new module in `modules/fundamental/src/sbom/model/mod.rs` following the existing `pub mod summary;` and `pub mod details;` declarations.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference for struct definition patterns, derive macros, and serde configuration
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the `severity` field definition showing how severity is represented in the existing codebase

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct is defined with `critical`, `high`, `medium`, `low`, `total` fields (all `u64`)
- [ ] `SeverityThreshold` enum is defined with `Critical`, `High`, `Medium`, `Low` variants
- [ ] Both types derive `Serialize`, `Deserialize`, and `ToSchema`
- [ ] Module is registered in `modules/fundamental/src/sbom/model/mod.rs` and types are re-exported
- [ ] Code compiles without errors

## Test Requirements
- [ ] `AdvisorySeveritySummary` serializes to JSON with keys `critical`, `high`, `medium`, `low`, `total`
- [ ] `SeverityThreshold` deserializes from lowercase strings (`"critical"`, `"high"`, `"medium"`, `"low"`)

## Digest
[sdlc-workflow] Description digest: sha256-md:5ba0c057360a6a05cb1f5df34b9b0138fb6c1962bceb517f136612f6d398b763
