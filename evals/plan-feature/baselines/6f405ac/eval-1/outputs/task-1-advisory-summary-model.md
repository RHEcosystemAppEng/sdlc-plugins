## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response model struct that represents the severity aggregation response for an SBOM's advisories. This struct will be returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint and contains counts for each severity level (critical, high, medium, low) plus a total.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — Define `AdvisorySeveritySummary` struct with `critical`, `high`, `medium`, `low`, and `total` fields (all `u64`), deriving `Serialize`, `Deserialize`, `Clone`, `Debug`, and `utoipa::ToSchema`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` declaration to expose the new model module

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` which defines `SbomSummary` as a serializable struct. The new `AdvisorySeveritySummary` struct should derive the same traits used by `SbomSummary`.

Reference `modules/fundamental/src/advisory/model/summary.rs` for how severity is represented on `AdvisorySummary` — the new struct aggregates counts by those severity values.

Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` structure by placing the model in `modules/fundamental/src/sbom/model/`.
Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md §Framework: use SeaORM-compatible derives and Axum-compatible serialization traits.
Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's `.rs` Rust scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Existing SBOM model struct; follow its derive pattern and serialization approach
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the severity field definition; reference for severity value representation

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, and `utoipa::ToSchema`
- [ ] Module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Unit test verifying `AdvisorySeveritySummary` serializes to expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test verifying deserialization from valid JSON roundtrips correctly
