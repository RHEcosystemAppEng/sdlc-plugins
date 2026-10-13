## Repository
trustify-backend

## Target Branch
main

## Description
Add the data model and service method for advisory severity aggregation. Define an `AdvisorySeveritySummary` struct that holds counts by severity level (critical, high, medium, low, total) and implement a `get_advisory_summary` method on `SbomService` that queries the `sbom_advisory` join table to produce deduplicated severity counts for a given SBOM ID.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add module declaration and re-export for advisory_summary
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_summary` method to SbomService that joins sbom_advisory with advisory, groups by severity, and returns AdvisorySeveritySummary

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — define AdvisorySeveritySummary struct with fields: critical (u64), high (u64), medium (u64), low (u64), total (u64); derive Serialize, Deserialize, Clone, Debug

## Implementation Notes
The aggregation query should join `entity::sbom_advisory` with `entity::advisory` to access the severity field, filter by the given SBOM ID, and use `SELECT COUNT(DISTINCT advisory_id)` grouped by severity to avoid counting duplicate advisories. Return 404 (via `AppError::NotFound`) if the SBOM ID does not exist — check existence first using the existing `SbomService::fetch` method.

Per CONVENTIONS.md §Module pattern: place the struct in `model/advisory_summary.rs` and the service method in `service/sbom.rs`, following the `model/ + service/ + endpoints/` structure.
Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's module directory structure scope.

Per CONVENTIONS.md §Error handling: return `Result<AdvisorySeveritySummary, AppError>` from the service method, using `.context()` to wrap database errors.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust handler/service scope.

Per CONVENTIONS.md §Query helpers: use shared query builder helpers from `common/src/db/query.rs` for constructing the aggregation query.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's database query scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::fetch` — existing method to verify SBOM existence before aggregating; reuse to return 404 for unknown SBOMs
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for severity field name and type used in the advisory entity
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity needed for the aggregation join
- `common/src/error.rs::AppError` — error type for returning 404 and wrapping query errors

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct is defined with critical, high, medium, low, and total fields
- [ ] `SbomService::get_advisory_summary` returns correct counts grouped by severity for a given SBOM ID
- [ ] Duplicate advisories (same advisory ID linked multiple times) are counted only once
- [ ] Returns `AppError::NotFound` when the SBOM ID does not exist
- [ ] Total field equals the sum of critical + high + medium + low

## Test Requirements
- [ ] Unit test: `get_advisory_summary` returns zero counts for an SBOM with no linked advisories
- [ ] Unit test: `get_advisory_summary` returns correct counts when advisories of mixed severities are linked
- [ ] Unit test: `get_advisory_summary` deduplicates advisory IDs correctly
- [ ] Unit test: `get_advisory_summary` returns NotFound error for a non-existent SBOM ID
