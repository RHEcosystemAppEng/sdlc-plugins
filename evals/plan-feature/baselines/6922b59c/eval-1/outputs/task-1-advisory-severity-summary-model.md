## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response model struct for the advisory severity aggregation endpoint (`GET /api/v2/sbom/{id}/advisory-summary`). This struct represents the JSON response shape `{ critical: N, high: N, medium: N, low: N, total: N }` that consumers will receive. The model must support serialization via `serde` and integrate with the existing advisory model module.

## Files to Create
- `modules/fundamental/src/sbom/model/severity_summary.rs` — defines `AdvisorySeveritySummary` struct with `critical`, `high`, `medium`, `low`, and `total` fields (all `u64`), deriving `Serialize`, `Deserialize`, `Clone`, `Debug`, `PartialEq`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod severity_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`) for struct layout, derive macros, and serde attribute conventions.

Per CONVENTIONS.md §Module Pattern: place the new model file under the SBOM module's `model/` directory and register it in the module's `mod.rs`.
Applies: task creates `modules/fundamental/src/sbom/model/severity_summary.rs` matching the convention's Rust module file scope.

Per CONVENTIONS.md §Error Handling: derive appropriate traits for use in `Result<T, AppError>` return types downstream.
Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for struct layout, derive macros, and serde patterns used in the project
- `common/src/model/paginated.rs::PaginatedResults` — reference for how response wrapper structs are defined and serialized

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, `PartialEq`
- [ ] Struct is publicly exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Project compiles successfully with `cargo check`

## Test Requirements
- [ ] Unit test verifying `AdvisorySeveritySummary` serializes to the expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test verifying deserialization from valid JSON produces the correct struct values

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental severity_summary` — model tests pass

## Dependencies
- None
