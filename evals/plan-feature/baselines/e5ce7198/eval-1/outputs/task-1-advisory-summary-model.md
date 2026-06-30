# Task 1: Define AdvisorySeveritySummary response model

## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` struct that represents the aggregated severity counts returned by the new advisory summary endpoint. This model holds counts for each severity level (critical, high, medium, low) plus a total, and will be serialized as the JSON response body.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct with severity count fields

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary` declaration and re-export the struct

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`). The struct should derive `Serialize`, `Deserialize`, `Clone`, `Debug`, and `PartialEq`.

Fields:
- `critical: i64`
- `high: i64`
- `medium: i64`
- `low: i64`
- `total: i64`

Reference the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` to understand the existing severity field representation.

Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` structure for the sbom domain module.
Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's Rust module file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct layout, derive macros, and serde attributes
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field enum/representation to align with

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct is defined with `critical`, `high`, `medium`, `low`, and `total` fields
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, `PartialEq`
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without warnings

## Test Requirements
- [ ] Unit test verifying `AdvisorySeveritySummary` serializes to expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test verifying deserialization from JSON round-trips correctly

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental advisory_summary` — model tests pass

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

[sdlc-workflow] Description digest: sha256-md:aa18a7007285856daa9215055c2bf861dc0661defdd57ecedcd7d4e6391313d2
