# Task 1: Add AdvisorySeveritySummary response model

## Repository

trustify-backend

## Target Branch

main

## Description

Add a new response struct `AdvisorySeveritySummary` that represents the severity counts for advisories linked to an SBOM. The struct must include fields for critical, high, medium, low, and total counts. It will be used as the response type for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Files to Create

- `modules/fundamental/src/sbom/model/advisory_summary.rs` — New module containing the `AdvisorySeveritySummary` struct

## Files to Modify

- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` to expose the new module

## API Changes

Response schema for `GET /api/v2/sbom/{id}/advisory-summary`:

```json
{
  "critical": 0,
  "high": 0,
  "medium": 0,
  "low": 0,
  "total": 0
}
```

## Implementation Notes

- Follow the pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/advisory/model/summary.rs` for struct layout, derive macros, and serialization attributes.
- Derive `serde::Serialize`, `serde::Deserialize`, `Clone`, `Debug`, `Default`, and `utoipa::ToSchema` to enable OpenAPI documentation generation.
- Use `u64` or `i64` for count fields (match the convention used by SeaORM count queries in the codebase).
- Reference `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` to understand how severity values are represented — the same severity enum or string mapping should be used for grouping in the service layer.
- Per CONVENTIONS.md §Module pattern: place the new model file under `modules/fundamental/src/sbom/model/` following the `model/ + service/ + endpoints/` structure. See `modules/fundamental/src/sbom/model/summary.rs` for the established pattern.
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's Rust module file scope.
- Per CONVENTIONS.md §Framework: use SeaORM-compatible types for the struct fields so the model integrates cleanly with database query results.
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's Rust module file scope.

## Reuse Candidates

- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference for severity field representation
- `modules/fundamental/src/sbom/model/summary.rs` — Pattern for struct definition, derives, and module registration

## Acceptance Criteria

- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical`, `high`, `medium`, `low`, `total`
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, `Default`, `ToSchema`
- [ ] Module is exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Struct compiles and is usable as an Axum JSON response type

## Test Requirements

- [ ] Unit test: verify `AdvisorySeveritySummary` serializes to expected JSON shape
- [ ] Unit test: verify `Default` produces all-zero counts

## Verification Commands

- `cargo check -p trustify-module-fundamental` — verify compilation
- `cargo test -p trustify-module-fundamental -- advisory_severity_summary` — run unit tests
