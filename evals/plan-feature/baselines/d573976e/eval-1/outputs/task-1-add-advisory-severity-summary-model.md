# Task 1 — Add AdvisorySeveritySummary response model

## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response struct that represents the severity count breakdown for advisories linked to an SBOM. This model is the response type for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. It must include fields for each severity level (critical, high, medium, low) and a total count, with JSON serialization support.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — AdvisorySeveritySummary struct with severity count fields

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` to expose the new model module

## Implementation Notes
- Follow the existing model pattern established by `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` and `SbomDetails` in `modules/fundamental/src/sbom/model/details.rs`
- The struct should derive `Serialize`, `Deserialize`, `Clone`, `Debug` consistent with sibling model structs
- Fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`
- The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a `severity` field — reference this to understand how severity is represented in the existing data model
- Do not use `PaginatedResults<T>` from `common/src/model/paginated.rs` — this endpoint returns a single summary object, not a list

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM model struct to follow as a pattern for struct definition and derive macros
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition showing how severity is typed in the domain model

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct is defined with `critical`, `high`, `medium`, `low`, and `total` fields
- [ ] Struct derives `Serialize` and `Deserialize` for JSON support
- [ ] Module is exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test that `AdvisorySeveritySummary` serializes to the expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test that `AdvisorySeveritySummary` deserializes from valid JSON

## Dependencies
- None
