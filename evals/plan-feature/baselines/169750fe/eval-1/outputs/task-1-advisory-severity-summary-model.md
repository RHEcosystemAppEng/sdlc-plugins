## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response model struct that represents aggregated advisory severity counts for a given SBOM. This struct will be returned by the new advisory summary endpoint. It must include fields for each severity level (critical, high, medium, low) and a total count, with unique advisory deduplication accounted for in the aggregation logic.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — define `AdvisorySeveritySummary` struct with `critical`, `high`, `medium`, `low`, `total` fields (all `i64`), deriving `Serialize`, `Deserialize`, `Debug`, `Clone`, `utoipa::ToSchema`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
Follow the existing model pattern established by `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` and `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`. These structs derive `Serialize`, `Deserialize`, and `utoipa::ToSchema` for OpenAPI documentation.

The struct should be a flat response object (not paginated) since it returns a single aggregation result, unlike `PaginatedResults<T>` used by list endpoints (`common/src/model/paginated.rs`).

Per CONVENTIONS.md §Module Pattern: follow the `model/ + service/ + endpoints/` structure for the sbom domain module.
Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's Rust module file scope.

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs`
- [ ] Struct has fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`
- [ ] Struct derives `Serialize`, `Deserialize`, `Debug`, `Clone`, `utoipa::ToSchema`
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Verify the struct can be serialized to JSON with the expected field names
- [ ] Verify the struct can be deserialized from JSON

## Dependencies
- None (this is the first task)
