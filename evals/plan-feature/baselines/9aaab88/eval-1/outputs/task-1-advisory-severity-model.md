## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response model struct that represents aggregated severity counts for advisories linked to an SBOM. This struct will be returned by the new advisory summary endpoint and contains fields for each severity level (critical, high, medium, low) plus a total count.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — Define the `AdvisorySeveritySummary` struct with `critical`, `high`, `medium`, `low`, and `total` fields (all `u64`), deriving `Serialize`, `Deserialize`, `Debug`, `Clone`, and `utoipa::ToSchema` for OpenAPI docs

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` declaration and re-export `AdvisorySeveritySummary`

## Implementation Notes
- Follow the existing model pattern in the sbom module: `modules/fundamental/src/sbom/model/summary.rs` defines `SbomSummary` with serde derives and ToSchema — use the same derive set for `AdvisorySeveritySummary`.
- The struct should implement `Default` so that an SBOM with zero advisories returns all-zero counts.
- Reference `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails` struct) for the pattern of how model structs are organized and exported in this module.
- Per Key Conventions (Module pattern): each domain module follows `model/ + service/ + endpoints/` structure. Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's module pattern scope.
- Per Key Conventions (Error handling): all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the convention's `.rs` file scope.

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs` with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`
- [ ] Struct derives `Serialize`, `Deserialize`, `Debug`, `Clone`, and `utoipa::ToSchema`
- [ ] Struct implements `Default` returning all-zero counts
- [ ] Module is registered and re-exported in `modules/fundamental/src/sbom/model/mod.rs`
- [ ] `cargo check` passes with the new module

## Test Requirements
- [ ] Unit test verifying `AdvisorySeveritySummary::default()` returns all zeros
- [ ] Unit test verifying serialization to JSON produces the expected `{ "critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0 }` shape

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors


[sdlc-workflow] Description digest: sha256-md:c3c8e504572dee406c9d7628939287b25cc4271ed4d18a7390f5e3d45ff076f3
