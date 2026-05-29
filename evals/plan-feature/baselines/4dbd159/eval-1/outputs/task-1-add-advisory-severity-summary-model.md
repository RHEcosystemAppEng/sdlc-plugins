# Task 1 -- Add AdvisorySeveritySummary response model

## Repository
trustify-backend

## Target Branch
main

## Description
Create a new `AdvisorySeveritySummary` response model struct that represents the aggregated severity counts for advisories linked to an SBOM. This struct will be used as the response body for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` -- new struct `AdvisorySeveritySummary` with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`). Both derive `serde::Serialize`, `serde::Deserialize`, and `utoipa::ToSchema` for OpenAPI spec generation.
- The struct should derive `Clone`, `Debug`, `Default`, `Serialize`, `Deserialize`, and `ToSchema`.
- Field type should be `u64` (or `i64` if the existing codebase uses signed integers for counts -- check `PaginatedResults` in `common/src/model/paginated.rs` for the convention).
- The `total` field is the sum of all severity counts and must be computed at the service layer, not stored separately.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- reference for struct layout, derive macros, and serde configuration
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- contains the `severity` field definition showing how severity is represented in the existing data model
- `common/src/model/paginated.rs::PaginatedResults` -- reference for response wrapper patterns and serialization conventions

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with `critical`, `high`, `medium`, `low`, and `total` fields
- [ ] Struct derives appropriate serde and schema traits consistent with existing models
- [ ] Struct is publicly exported from the sbom model module

## Test Requirements
- [ ] Unit test verifying that `AdvisorySeveritySummary` serializes to the expected JSON shape: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test verifying default values are all zero

## Dependencies
- None
