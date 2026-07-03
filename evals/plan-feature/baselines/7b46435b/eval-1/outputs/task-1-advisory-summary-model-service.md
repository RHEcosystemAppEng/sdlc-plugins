# Task 1 — Add AdvisorySeveritySummary model and aggregation service method

## Repository
trustify-backend

## Target Branch
main

## Description
Add the response model and service-layer aggregation method for the advisory severity summary feature. The model represents severity counts (critical, high, medium, low, total) for advisories linked to an SBOM. The service method queries the `sbom_advisory` join table, deduplicates by advisory ID, groups by severity, and returns the counts. This provides the data layer that the endpoint (Task 2) will expose.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new AdvisorySeveritySummary model
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_severity_summary(sbom_id)` method to SbomService

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — AdvisorySeveritySummary struct with fields: critical (i64), high (i64), medium (i64), low (i64), total (i64)

## Implementation Notes
- Follow the existing module pattern: each domain module uses `model/ + service/ + endpoints/` structure. The new model file follows the pattern established by `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails).
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's Rust module file scope.
- The service method should use SeaORM to query the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) joined with the advisory entity (`entity/src/advisory.rs`) to access the severity field.
- Deduplicate by advisory ID before counting — use `SELECT DISTINCT advisory_id, severity` or equivalent SeaORM query to prevent double-counting when an advisory is linked to the same SBOM through multiple paths.
- The severity field is on `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`) — reference this struct for the severity enum or field type.
- Return `Result<AdvisorySeveritySummary, AppError>` from the service method, consistent with the error handling convention where all service methods return `Result<T, AppError>` with `.context()` wrapping (`common/src/error.rs`).
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service file scope.
- The struct should derive `Serialize`, `Deserialize`, `Debug`, `Clone` to match existing model patterns.
- Per constraints doc section 5 (Code Change Rules): implementation must follow the patterns referenced in Implementation Notes and must not duplicate existing functionality.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition; reference for severity enum/type
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for building the aggregation query
- `entity/src/advisory.rs` — Advisory entity with severity data
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; may have reusable query patterns
- `common/src/error.rs::AppError` — error enum for consistent error handling

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: critical, high, medium, low, total (all integer counts)
- [ ] `SbomService::get_advisory_severity_summary(sbom_id)` method returns correct severity counts for a given SBOM
- [ ] Advisory counts are deduplicated by advisory ID (no double-counting)
- [ ] Method returns appropriate error when SBOM ID does not exist

## Test Requirements
- [ ] Unit test: verify `AdvisorySeveritySummary` serializes to expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Service test: verify correct counts when SBOM has advisories at multiple severity levels
- [ ] Service test: verify deduplication — same advisory linked twice produces count of 1
- [ ] Service test: verify total equals sum of individual severity counts
- [ ] Service test: verify error handling when SBOM ID does not exist

## Verification Commands
- `cargo test --package fundamental -- advisory_summary` — all model and service tests pass
- `cargo check --package fundamental` — no compilation errors

## Dependencies
- None (first task in the chain)
