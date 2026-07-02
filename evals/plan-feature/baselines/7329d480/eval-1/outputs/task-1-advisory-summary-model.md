# Task 1 — Define advisory severity summary response model

additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }

## Repository
trustify-backend

## Target Branch
main

## Description
Define the `AdvisorySeveritySummary` response struct that represents aggregated advisory severity counts for a given SBOM. This struct is the foundation for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. It holds counts for each severity level (critical, high, medium, low) and a total, matching the response shape specified in TC-9001.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct with `critical`, `high`, `medium`, `low`, and `total` fields (all `u64`), deriving `Serialize`, `Deserialize`, `Debug`, `Clone`, `utoipa::ToSchema`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
Follow the pattern established by existing model structs in the same directory. Reference `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) for the derive macro set and struct conventions. The new struct should derive the same set of traits used by `SbomSummary` (at minimum `Serialize`, `Deserialize`, `Debug`, `Clone`, and `utoipa::ToSchema` for OpenAPI generation).

The struct does not map to a database entity directly — it is a computed aggregation result, so it does not use SeaORM derives. This is a pure response model.

Per CONVENTIONS.md §Module pattern: place the new model file under `modules/fundamental/src/sbom/model/` following the `model/ + service/ + endpoints/` structure.
Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's module directory pattern.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for derive macros, struct layout, and documentation conventions
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the `severity` field type that the aggregation will group by; verify the severity enum/type used here to ensure consistency

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`
- [ ] Struct derives `Serialize`, `Deserialize`, `Debug`, `Clone`, and `utoipa::ToSchema`
- [ ] Struct is publicly exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors (`cargo check`)

## Test Requirements
- [ ] `cargo check` passes with the new model file
- [ ] Struct can be serialized to JSON with expected field names (verify with a unit test or doc test)

## Dependencies
- Depends on: None — this is the first task in the chain
