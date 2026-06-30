# Task 1 — Add AdvisorySeveritySummary response model

## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response model that represents aggregated severity counts for advisories linked to an SBOM. This struct will be returned by the new advisory summary endpoint and contains counts for each severity level (critical, high, medium, low) plus a total count. An optional severity threshold filter enum is also needed for the query parameter support.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new `AdvisorySeveritySummary` struct

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — define `AdvisorySeveritySummary` struct with `critical`, `high`, `medium`, `low`, `total` fields (all `i64`), deriving `Serialize`, `Deserialize`, `Clone`, `Debug`; define `SeverityThreshold` enum with variants `Critical`, `High`, `Medium`, `Low` implementing `FromStr` for query parameter parsing

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`) — these structs derive `Serialize`, `Deserialize`, and use serde attributes for JSON field naming
- The `SeverityThreshold` enum should implement `FromStr` (or use serde `Deserialize`) so Axum can parse it from the `?threshold=critical` query parameter
- Use `serde(rename_all = "camelCase")` or `serde(rename_all = "lowercase")` consistently with the existing response models in the module
- Per the repository's Key Conventions (Module pattern): place the model in the sbom module's `model/` directory since the endpoint is scoped to `/api/v2/sbom/{id}/advisory-summary`
- Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's `.rs` module file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — example of a model struct with serde derives and JSON serialization attributes in the same module
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the `severity` field definition showing how severity is represented in the existing codebase
- `common/src/model/paginated.rs::PaginatedResults` — example of a response wrapper pattern in the common crate

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`
- [ ] `SeverityThreshold` enum exists with variants `Critical`, `High`, `Medium`, `Low`
- [ ] `SeverityThreshold` can be parsed from lowercase string values (e.g., "critical", "high")
- [ ] New model is re-exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test verifying `AdvisorySeveritySummary` serializes to JSON with expected field names (`critical`, `high`, `medium`, `low`, `total`)
- [ ] Unit test verifying `SeverityThreshold` parses from lowercase strings ("critical", "high", "medium", "low")
- [ ] Unit test verifying `SeverityThreshold` returns an error for invalid input

## Dependencies
- None

<!-- [sdlc-workflow] Description digest: sha256-md:8c618b9455bbc6e9215cf7b746f08ef8c9ea52a27d61836acbac6d00bb1ee7dd -->
