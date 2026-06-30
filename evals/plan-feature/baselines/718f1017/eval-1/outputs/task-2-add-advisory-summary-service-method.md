# Task 2 — Add advisory severity aggregation service method

## Repository
trustify-backend

## Target Branch
main

## Description
Add a service method to `SbomService` that queries the `sbom_advisory` join table to aggregate advisory severity counts for a given SBOM ID. The method should deduplicate advisories by advisory ID, group by severity level, and return an `AdvisorySeveritySummary`. It must also handle the case where the SBOM ID does not exist (returning a 404-compatible error) and support an optional severity threshold filter.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_summary` method to `SbomService` that accepts an SBOM ID and optional `SeverityThreshold`, queries the `sbom_advisory` join table joined with the `advisory` table, groups by severity, deduplicates by advisory ID, and returns `Result<AdvisorySeveritySummary, AppError>`

## Implementation Notes
- Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService: fetch, list, ingest`) — these methods accept database connections and return `Result<T, AppError>`
- Use SeaORM query builders from `common/src/db/query.rs` for constructing the aggregation query
- Join `entity/src/sbom_advisory.rs` (SBOM-Advisory join table) with `entity/src/advisory.rs` to access the severity field
- Use `SELECT COUNT(DISTINCT advisory_id)` grouped by severity to avoid double-counting advisories that appear multiple times
- For the 404 case: first verify the SBOM exists using the existing `SbomService::fetch` method, then return `AppError::NotFound` if it does not — this is consistent with the error handling pattern described in `common/src/error.rs` using `.context()` wrapping
- When `SeverityThreshold` is provided, filter the results to only include severity levels at or above the threshold (Critical > High > Medium > Low)
- Per the repository's Key Conventions (Error handling): all service methods return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` service file scope.
- Per the repository's Key Conventions (Query helpers): use shared filtering helpers from `common/src/db/query.rs` for the aggregation query.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` service file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — the service struct where the new method will be added; existing methods show the pattern for database queries and error handling
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — shows how advisory-related queries are constructed with SeaORM
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting
- `entity/src/sbom_advisory.rs` — the SBOM-Advisory join table entity that will be the primary query target
- `entity/src/advisory.rs` — the Advisory entity containing the severity field

## Acceptance Criteria
- [ ] `SbomService::get_advisory_summary` method exists and accepts SBOM ID and optional `SeverityThreshold`
- [ ] Method queries `sbom_advisory` joined with `advisory` table and aggregates counts by severity
- [ ] Advisories are deduplicated by advisory ID (COUNT DISTINCT)
- [ ] Method returns `AdvisorySeveritySummary` with correct counts for critical, high, medium, low, and total
- [ ] Method returns 404 error when SBOM ID does not exist
- [ ] When threshold is provided, only severity levels at or above the threshold are counted (others are zero)

## Test Requirements
- [ ] Integration test: returns correct severity counts for an SBOM with known advisories at mixed severity levels
- [ ] Integration test: returns all zeros (with total=0) for an SBOM with no linked advisories
- [ ] Integration test: returns 404 for a non-existent SBOM ID
- [ ] Integration test: correctly deduplicates advisories that appear multiple times in the join table
- [ ] Integration test: threshold filter returns only counts at or above the specified severity level

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model

<!-- [sdlc-workflow] Description digest: sha256-md:638596ff1b27d4d29c51c59a7fb0400e7826813278870fdb0bc7e7d69c356bfa -->
