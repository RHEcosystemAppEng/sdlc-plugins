## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response model struct in the sbom module. This struct represents the JSON response shape for the new advisory severity aggregation endpoint (`GET /api/v2/sbom/{id}/advisory-summary`), containing counts of advisories at each severity level (critical, high, medium, low) plus a total count. The struct must derive `Serialize` for JSON serialization in Axum responses.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — defines the `AdvisorySeveritySummary` struct with fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary` struct) for derive macros and serialization attributes. The struct should derive `Clone, Debug, Serialize, Deserialize, PartialEq, Eq` to match sibling models.
- Use `serde::Serialize` and `serde::Deserialize` for JSON serialization, consistent with `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`.
- The struct is a flat response object (not paginated) — do not use `PaginatedResults<T>` from `common/src/model/paginated.rs` since this endpoint returns a single summary, not a list.
- Per Key Conventions §Module pattern: follow the model/ + service/ + endpoints/ structure. Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's `.rs` model file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — follow its derive macros and module re-export pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference its severity field definition to understand the severity enum/values used in the advisory domain

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs` with fields `critical`, `high`, `medium`, `low`, `total` (all `i64`)
- [ ] Struct derives `Serialize` and `Deserialize` for JSON serialization
- [ ] `advisory_summary` module is declared and re-exported in `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Crate compiles without errors

## Test Requirements
- [ ] Verify the struct serializes to the expected JSON shape: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Verify deserialization round-trip produces the same struct values

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors

## Dependencies
None

## Jira Fields
- **Labels:** ai-generated-jira
- **Priority:** Major
- **Fix Versions:** RHTPA 1.5.0

[sdlc-workflow] Description digest: sha256-md:a5551be09cacd7112b0aa94e3ae4054d1f3bb4d56b62d86c6912ae719f6a73d2
