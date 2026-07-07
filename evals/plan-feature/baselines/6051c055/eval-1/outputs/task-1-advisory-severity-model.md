## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response struct that represents aggregated advisory severity counts for an SBOM. This model is the return type for the new GET /api/v2/sbom/{id}/advisory-summary endpoint. The struct contains integer counts for each severity level (critical, high, medium, low) plus a total count, and must derive Serialize for JSON responses.

## Files to Create
- `modules/fundamental/src/advisory/model/severity_summary.rs` — new AdvisorySeveritySummary struct with critical, high, medium, low, and total fields

## Files to Modify
- `modules/fundamental/src/advisory/model/mod.rs` — re-export the new severity_summary module

## Implementation Notes
Follow the pattern established by `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`, which already has a `severity` field. The new struct should derive `Clone`, `Debug`, `Serialize`, `Deserialize`, `utoipa::ToSchema` consistent with sibling model structs in the same module.
Per CONVENTIONS.md §Module pattern: place the model in model/ following the model/ + service/ + endpoints/ module structure. Applies: task creates `modules/fundamental/src/advisory/model/severity_summary.rs` matching the convention's Rust module scope.

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, `utoipa::ToSchema`
- [ ] Struct is re-exported from `modules/fundamental/src/advisory/model/mod.rs`
- [ ] Project compiles without errors

## Test Requirements
- [ ] Unit test verifying `AdvisorySeveritySummary` serializes to expected JSON format `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test verifying deserialization from JSON round-trips correctly
