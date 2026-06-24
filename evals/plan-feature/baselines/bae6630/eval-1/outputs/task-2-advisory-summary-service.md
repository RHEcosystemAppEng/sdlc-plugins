## Repository
trustify-backend

## Target Branch
main

## Description
Add a service method to `SbomService` that queries the database to aggregate advisory severity counts for a given SBOM. This method joins the `sbom_advisory` table with the `advisory` table, deduplicates by advisory ID, groups by severity, and returns an `AdvisorySeveritySummary`. It also validates that the SBOM exists and returns a 404-appropriate error if not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `advisory_severity_summary` method to `SbomService`

## Implementation Notes
- Add the method to the existing `SbomService` impl block in `modules/fundamental/src/sbom/service/sbom.rs`, following the patterns of existing methods like `fetch` and `list`.
- Use SeaORM query builder to join `entity::sbom_advisory` with `entity::advisory` on advisory ID. The join table is defined in `entity/src/sbom_advisory.rs` and the advisory entity in `entity/src/advisory.rs`.
- First verify the SBOM exists by querying `entity::sbom` (from `entity/src/sbom.rs`). If not found, return `AppError::NotFound` following the pattern in `common/src/error.rs`.
- Use `SELECT COUNT(DISTINCT advisory.id), advisory.severity` with `GROUP BY advisory.severity` to get counts per severity level.
- Map the severity strings from the database to the corresponding fields in `AdvisorySeveritySummary`. Compute `total` as the sum of all severity counts.
- Use `.context()` error wrapping as documented in the Key Conventions (all handlers/services return `Result<T, AppError>` with `.context()` wrapping).
- Shared query helpers from `common/src/db/query.rs` may be useful for building the query, though this is an aggregation query rather than a paginated list.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service struct where the new method is added; follow its patterns for database access and error handling
- `entity/src/sbom_advisory.rs` — SeaORM entity for the SBOM-Advisory join table; defines the relationship needed for the aggregation query
- `entity/src/advisory.rs` — Advisory entity containing the `severity` column to group by
- `entity/src/sbom.rs` — SBOM entity for existence validation
- `common/src/error.rs::AppError` — Error enum for returning 404 when SBOM is not found

## Acceptance Criteria
- [ ] `SbomService` has a new `advisory_severity_summary` method that accepts an SBOM ID and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Method returns correct counts grouped by severity (critical, high, medium, low)
- [ ] Advisories are deduplicated by advisory ID (no double-counting)
- [ ] Returns an appropriate error when the SBOM ID does not exist
- [ ] Total field equals the sum of all severity counts

## Test Requirements
- [ ] Unit test with mock data: SBOM with known advisory severities returns correct counts
- [ ] Unit test: duplicate advisories (same advisory linked multiple times) are counted only once
- [ ] Unit test: non-existent SBOM ID returns a not-found error

## Dependencies
- Depends on: Task 1 — Advisory summary model (requires `AdvisorySeveritySummary` struct)

## Digest
[sdlc-workflow] Description digest: sha256-md:feedf4b6de42133db1db6a1f2a2c1412d1845b414598ea9d7e64075fcd96370b
