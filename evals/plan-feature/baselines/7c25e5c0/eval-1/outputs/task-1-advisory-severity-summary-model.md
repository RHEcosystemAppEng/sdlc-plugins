## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model struct that represents the aggregated severity counts for advisories linked to an SBOM. This model will be returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The struct contains fields for each severity level (`critical`, `high`, `medium`, `low`) and a `total` count.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — new module defining the `AdvisorySeveritySummary` struct with `Serialize`, `ToSchema` (for OpenAPI), and `Debug` derives

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`) for struct definition style, derive macros, and documentation
- The struct fields should be `pub critical: i64`, `pub high: i64`, `pub medium: i64`, `pub low: i64`, `pub total: i64`
- Derive `serde::Serialize`, `utoipa::ToSchema`, `Debug`, `Clone`, and `Default` to match existing model conventions
- Reference `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`) to understand the severity field representation used across the codebase
- Per CONVENTIONS.md §Module pattern: each domain module follows `model/ + service/ + endpoints/` structure.
  Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the convention's Rust module scope.

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct is defined with fields `critical`, `high`, `medium`, `low`, `total` (all `i64`)
- [ ] Struct derives `Serialize`, `ToSchema`, `Debug`, `Clone`, `Default`
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles with `cargo check`

## Test Requirements
- [ ] Verify `AdvisorySeveritySummary` can be serialized to JSON with correct field names
- [ ] Verify `Default::default()` produces zero counts

## Dependencies
- None (first task)
