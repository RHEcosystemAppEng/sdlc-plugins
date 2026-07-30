## Repository
trustify-backend

## Target Branch
main

## Description
Add a new response model `AdvisorySeveritySummary` to represent aggregated advisory severity counts for a given SBOM. This struct will be returned by the new advisory-summary endpoint (Task 3) and consumed by frontend dashboard widgets. The model captures counts for each severity level (critical, high, medium, low) plus a total count, matching the response shape specified in the feature requirements.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — AdvisorySeveritySummary struct with serde Serialize/Deserialize and utoipa ToSchema derives

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) for struct definition, derive macros, and field documentation.
- The struct fields should be: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`.
- Use `#[derive(Clone, Debug, Serialize, Deserialize, ToSchema)]` consistent with existing model structs like `SbomSummary` and `AdvisorySummary`.
- Per CONVENTIONS.md: follow the established module pattern (model/ + service/ + endpoints/). The model is the first layer of this pattern.
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's `.rs` module file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct definition pattern, derive macros, and serde attributes
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for the severity field type used in the advisory domain

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: critical, high, medium, low, total (all i64)
- [ ] Struct derives Serialize, Deserialize, and ToSchema for API documentation
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Verify the struct can be serialized to JSON with the expected field names `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Verify the struct can be deserialized from a JSON string with the expected shape

## Dependencies
- None
