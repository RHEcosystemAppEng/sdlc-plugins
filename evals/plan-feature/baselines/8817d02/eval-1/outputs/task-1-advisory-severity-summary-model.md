## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response model struct that represents the aggregated severity counts for advisories linked to an SBOM. This struct will be returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The struct must include fields for `critical`, `high`, `medium`, `low`, and `total` counts, and support serialization via `serde`.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` — new model struct `AdvisorySeveritySummary` with severity count fields

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_severity_summary;` and re-export the struct

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary` struct) for struct layout, derive macros, and serde configuration.
- The struct should derive `Clone`, `Debug`, `Serialize`, `Deserialize`, `PartialEq`, `Eq` and use `#[serde(rename_all = "camelCase")]` or match the existing casing convention used by `SbomSummary` and `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`.
- Fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`.
- The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` already includes a `severity` field — inspect its type (likely an enum) to determine the exact severity variants the aggregation must count.
- Per docs/constraints.md §5.2: inspect the existing model files before writing new code.
- Per docs/constraints.md §4.6: all file paths are derived from the repository structure analysis.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct layout, derive macros, and serde attributes
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the `severity` field type definition needed for aggregation mapping

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_severity_summary.rs`
- [ ] Struct has `critical`, `high`, `medium`, `low`, `total` fields of unsigned integer type
- [ ] Struct derives `Serialize` and `Deserialize` for JSON serialization
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Project compiles successfully with `cargo check`

## Test Requirements
- [ ] Verify `AdvisorySeveritySummary` can be serialized to JSON with expected field names and deserialized back
- [ ] Verify `total` field correctly represents the sum of all severity counts in unit tests

## Dependencies
- None (this is the foundational model task)

[sdlc-workflow] Description digest: sha256-md:844015336092ab7bf36d469d7f41c9d165fa233ea4e9ee8383a2d7c14572f681
