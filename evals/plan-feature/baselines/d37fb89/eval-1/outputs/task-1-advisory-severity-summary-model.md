## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response struct that represents severity counts for advisories linked to an SBOM. This model will be returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The struct must include fields for `critical`, `high`, `medium`, `low`, and `total` counts, and implement the necessary serialization traits for JSON API responses.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` — New struct `AdvisorySeveritySummary` with `critical`, `high`, `medium`, `low`, and `total` fields (all `u64` or `i64`), deriving `Serialize`, `Deserialize`, `Debug`, `Clone`, `utoipa::ToSchema`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_severity_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`). These structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`, and `utoipa::ToSchema` for OpenAPI spec generation. The new struct is simpler than existing models since it holds only aggregate counts, not entity relationships.

The `AdvisorySeveritySummary` struct should have this shape:
```rust
pub struct AdvisorySeveritySummary {
    pub critical: i64,
    pub high: i64,
    pub medium: i64,
    pub low: i64,
    pub total: i64,
}
```

Use `i64` to match SeaORM's `count()` return type and avoid unnecessary casts.

Per CONVENTIONS.md: the repository's module pattern mandates that each domain concept in `model/` has its own file with a re-export in `mod.rs`.
Applies: task creates `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for derive macros, serde attributes, and utoipa schema annotations used on model structs

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with `critical`, `high`, `medium`, `low`, `total` fields
- [ ] Struct derives `Serialize`, `Deserialize`, `Debug`, `Clone`, and `utoipa::ToSchema`
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Project compiles without errors (`cargo check`)

## Test Requirements
- [ ] Verify struct serialization produces correct JSON shape: `{"critical":0,"high":0,"medium":0,"low":0,"total":0}`
- [ ] Verify struct deserialization from valid JSON succeeds

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors

[sdlc-workflow] Description digest: sha256-md:1649bf34665110b938dfac8d8bc0286a65803019fb211103bced85d8de8379dc
