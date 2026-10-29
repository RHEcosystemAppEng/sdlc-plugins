## Repository
trustify-backend

## Target Branch
main

## Description
Add an `AdvisorySeveritySummary` model struct and a service method that aggregates vulnerability advisory severity counts for a given SBOM. The aggregation query must count unique advisories (deduplicated by advisory ID) grouped by severity level (Critical, High, Medium, Low) using the existing `sbom_advisory` join table. This enables the new advisory-summary endpoint (Task 2) to return pre-computed severity breakdowns without client-side counting.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — export new AdvisorySeveritySummary struct
- `modules/fundamental/src/sbom/service/sbom.rs` — add advisory_summary aggregation method to SbomService

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — AdvisorySeveritySummary struct definition with Serialize derive

## Implementation Notes
- Follow the model/ + service/ pattern established by the existing `SbomSummary` struct in `modules/fundamental/src/sbom/model/summary.rs`. The new struct lives alongside it in the model directory.
- Use SeaORM query builder with the `sbom_advisory` entity (`entity/src/sbom_advisory.rs`) to join against the advisory entity (`entity/src/advisory.rs`) which contains the severity field.
- Deduplicate by advisory ID using `SELECT DISTINCT` or `GROUP BY advisory_id` before counting by severity to avoid double-counting advisories linked through multiple paths.
- Return `total` as the sum of critical + high + medium + low counts.
- The service method must return an error (via `AppError`) when the SBOM ID does not exist, not an empty/zero-count result. Check SBOM existence first using the existing `SbomService::fetch` method before running the aggregation query.
- Per CONVENTIONS.md §Module Pattern: follow model/ + service/ + endpoints/ directory structure for domain modules. See `modules/fundamental/src/sbom/model/summary.rs` for the established pattern.
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's .rs module scope.
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` with `.context()` wrapping from the service method. See `common/src/error.rs` for the `AppError` enum.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's .rs handler scope.
- Per CONVENTIONS.md §Query Helpers: use shared query builder helpers from `common/src/db/query.rs` for filtering and pagination where applicable.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's .rs database query scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing model struct pattern to follow for the new AdvisorySeveritySummary struct (derives, field types, serialization)
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list methods; add the advisory_summary aggregation method here following the same patterns
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity needed for the aggregation query
- `entity/src/advisory.rs` — Advisory entity containing the severity field used for grouping
- `common/src/db/query.rs` — shared query builder helpers for filtering

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical` (i64), `high` (i64), `medium` (i64), `low` (i64), `total` (i64)
- [ ] `SbomService` has an `advisory_summary` method that accepts an SBOM ID and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Aggregation query counts unique advisories by severity using the `sbom_advisory` join table with deduplication by advisory ID
- [ ] `total` field equals the sum of `critical + high + medium + low` counts
- [ ] Method returns an error (not empty/zero counts) when the SBOM ID does not exist

## Test Requirements
- [ ] Test that `AdvisorySeveritySummary` can be constructed and serialized to JSON with the expected field names
- [ ] Test that `advisory_summary` correctly counts advisories by severity for a known SBOM with advisories at each severity level
- [ ] Test that duplicate advisories (same advisory ID linked multiple times to the same SBOM) are counted only once
- [ ] Test that `advisory_summary` returns an error for a non-existent SBOM ID

## Verification Commands
- `cargo build -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental` — all tests pass
