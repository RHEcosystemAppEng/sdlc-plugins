## Repository
trustify-backend

## Target Branch
main

## Description
Add a `SeveritySummary` response model and a severity aggregation service method to the SBOM module. The model represents the counts of advisories at each severity level (critical, high, medium, low) plus a total count for a given SBOM. The service method queries the `sbom_advisory` join table, groups by the advisory severity field, deduplicates by advisory ID, and returns the aggregated counts. This provides the data layer for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint (Task 2).

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new `severity_summary` module
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_severity_summary(sbom_id)` method to `SbomService`

## Files to Create
- `modules/fundamental/src/sbom/model/severity_summary.rs` — define `SeveritySummary` struct with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`

## API Changes
- `SbomService::get_advisory_severity_summary(sbom_id: Uuid) -> Result<SeveritySummary, AppError>` — NEW: aggregates advisory severity counts for a given SBOM

## Implementation Notes
- Per CONVENTIONS.md §Module Pattern: follow the established `model/ + service/ + endpoints/` structure for the SBOM domain module. Place the new struct in `model/severity_summary.rs` and the aggregation logic in `service/sbom.rs`.
  Applies: task creates `modules/fundamental/src/sbom/model/severity_summary.rs` matching the convention's model/ directory scope.
- Per CONVENTIONS.md §Error Handling: return `Result<SeveritySummary, AppError>` from the service method and use `.context()` wrapping for database query errors.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust handler scope.
- The aggregation query must join `sbom_advisory` with `advisory` to access the severity field, group by severity, and count distinct advisory IDs to satisfy the deduplication requirement from the feature spec.
- The `SeveritySummary` struct must derive `Serialize` for JSON response serialization.
- Verify that SBOM existence is checked before running the aggregation query — return `AppError::NotFound` if the SBOM ID does not exist (consistent with existing SBOM endpoints).
- The optional `threshold` filtering (e.g., only count severities above "critical") should be supported at the service level via an optional parameter, so the endpoint in Task 2 can pass it through.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the `severity` field definition; reference for severity enum values
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; use this for the aggregation query
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reuse filtering patterns for the threshold parameter
- `common/src/error.rs::AppError` — error enum with `NotFound` variant; use for SBOM existence check

## Acceptance Criteria
- [ ] `SeveritySummary` struct is defined with `critical`, `high`, `medium`, `low`, and `total` fields
- [ ] `SbomService::get_advisory_severity_summary` method exists and returns correct counts
- [ ] Advisories are deduplicated by advisory ID before counting
- [ ] Method returns `AppError::NotFound` when SBOM ID does not exist
- [ ] Optional threshold parameter filters counts to only include severities at or above the specified level

## Test Requirements
- [ ] Unit test: aggregation returns correct counts for an SBOM with known advisories at each severity level
- [ ] Unit test: aggregation deduplicates advisories linked multiple times to the same SBOM
- [ ] Unit test: method returns `NotFound` error for a non-existent SBOM ID
- [ ] Unit test: threshold parameter correctly filters severity levels

## Verification Commands
- `cargo test --package trustify-fundamental -- sbom::service::tests::severity_summary` — verify service method tests pass
- `cargo check --package trustify-fundamental` — verify compilation without errors

## Dependencies
- No dependencies — this is the foundational task
