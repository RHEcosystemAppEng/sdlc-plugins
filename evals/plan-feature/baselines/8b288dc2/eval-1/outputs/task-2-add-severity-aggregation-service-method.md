## Repository
trustify-backend

## Target Branch
main

## Description
Add a service method to `SbomService` that aggregates advisory severity counts for a given SBOM ID. The method queries the existing `sbom_advisory` join table and the `advisory` entity, deduplicates by advisory ID, counts by severity level, and returns an `AdvisorySeveritySummary`. It returns an appropriate error when the SBOM ID does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_summary(&self, sbom_id: Id) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
- Follow the existing service method pattern in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`). Existing methods like `fetch` and `list` demonstrate how to access the database connection, construct queries, and return results.
- Use SeaORM to query the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) joined with the `advisory` entity (`entity/src/advisory.rs`) to aggregate severity counts.
- Deduplicate by advisory ID before counting — the same advisory may appear multiple times in the join table.
- Group counts by the `severity` field on the `AdvisorySummary`/advisory entity. Map severity string values to the four buckets: critical, high, medium, low. Sum all counts into `total`.
- Return a 404-equivalent error (using `AppError` from `common/src/error.rs` with `.context()` wrapping) when the SBOM ID does not exist. Check SBOM existence before running the aggregation query, consistent with the pattern in `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service file scope.
- Per CONVENTIONS.md §Module pattern: keep aggregation logic in the service layer, not in the endpoint handler. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's module service directory scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct to extend with the new method
- `common/src/db/query.rs` — shared query builder helpers for filtering and constructing database queries
- `common/src/error.rs::AppError` — error type for not-found and internal errors
- `entity/src/sbom_advisory.rs` — the join table entity linking SBOMs to advisories
- `entity/src/advisory.rs` — the advisory entity containing the severity field

## Acceptance Criteria
- [ ] `SbomService::get_advisory_summary` method exists and compiles
- [ ] Method returns `AdvisorySeveritySummary` with correct severity counts when given a valid SBOM ID
- [ ] Method deduplicates advisories by advisory ID before counting
- [ ] Method returns a not-found error when SBOM ID does not exist
- [ ] `total` field equals the sum of critical + high + medium + low

## Test Requirements
- [ ] Unit or integration test: valid SBOM with known advisories returns correct severity counts
- [ ] Unit or integration test: SBOM with duplicate advisory links returns deduplicated counts
- [ ] Unit or integration test: non-existent SBOM ID returns not-found error

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental` — service tests pass

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model

[sdlc-workflow] Description digest: sha256-md:17ff7ffc3c1b696d05d7e27003de11f872861dbc2a6c7e6b6e5e1fa426945349
