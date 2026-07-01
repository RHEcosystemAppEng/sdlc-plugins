## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model struct to represent aggregated advisory severity counts for an SBOM. This model will be used by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint to return a breakdown of advisory counts by severity level (critical, high, medium, low) plus a total count.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add public re-export for the new summary model

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — define `AdvisorySeveritySummary` struct with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`). Each model is a standalone file in the `model/` directory with a re-export in `model/mod.rs`.
- The struct must derive `Serialize`, `Deserialize`, `Clone`, `Debug` at minimum to match sibling model structs.
- The struct does not map to a database entity — it is a computed response model only. Do not create a SeaORM entity for it.
- Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` structure. Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the convention's module model directory scope.
- Per CONVENTIONS.md §Response types: use a flat struct rather than wrapping in `PaginatedResults<T>` since this is an aggregation response, not a list endpoint. Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's Rust model file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct definition patterns, derive macros, and serialization attributes
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the `severity` field definition that shows how severity values are represented in the existing codebase

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with `critical`, `high`, `medium`, `low`, and `total` fields of unsigned integer type
- [ ] Struct derives serialization traits consistent with sibling models
- [ ] Struct is publicly re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Verify struct can be serialized to JSON with the expected field names (`critical`, `high`, `medium`, `low`, `total`)
- [ ] Verify struct can be deserialized from JSON

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors

## Dependencies
- None

[sdlc-workflow] Description digest: sha256-md:df242cadd5bf53acd37dd872a22d0d51aabc99afaf8e45994bc4bbbf41c2d390
