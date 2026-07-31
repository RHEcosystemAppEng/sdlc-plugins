## Repository
trustify-backend

## Target Branch
main

## Priority
Major

## Fix Versions
RHTPA 1.5.0

## Description
Create the `AdvisorySeveritySummary` response model struct that represents aggregated advisory severity counts for an SBOM. This struct will hold counts for each severity level (critical, high, medium, low) plus a total count, and will be returned by the new advisory-summary endpoint.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — new module defining the `AdvisorySeveritySummary` struct with `Serialize`/`Deserialize` derives and `utoipa::ToSchema` for OpenAPI generation

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export the `AdvisorySeveritySummary` type

## Implementation Notes
The struct should contain fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`. Follow the same derive pattern used in `modules/fundamental/src/sbom/model/summary.rs` for `SbomSummary` — derive `Clone`, `Debug`, `Serialize`, `Deserialize`, and `ToSchema`. The severity field on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` defines the severity categories to match against.

Per CONVENTIONS.md §Framework: use SeaORM-compatible types for the model struct. Applies: task modifies `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's Rust syntax scope.

Per CONVENTIONS.md §Module pattern: place the model in the `model/` subdirectory of the `sbom` domain module. Applies: convention has no file-type restriction (broadly applicable).

Per CONVENTIONS.md §Error handling: derive traits consistent with handlers returning `Result<T, AppError>`. Applies: task modifies `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's Rust syntax scope.

Per CONVENTIONS.md §Response types: model struct should be compatible with `PaginatedResults<T>` patterns from `common/src/model/paginated.rs` even though this endpoint returns a single summary. Applies: task modifies `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Caching: ensure the struct is serializable for cache storage by the `tower-http` caching middleware. Applies: convention has no file-type restriction (broadly applicable).

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs`
- [ ] Struct has fields: `critical`, `high`, `medium`, `low`, `total` (all `u64`)
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, and `ToSchema`
- [ ] Module is registered and re-exported in `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without warnings

## Test Requirements
- [ ] Verify `AdvisorySeveritySummary` serializes to expected JSON shape: `{"critical": N, "high": N, "medium": N, "low": N, "total": N}`
- [ ] Verify deserialization round-trip from JSON produces identical struct
