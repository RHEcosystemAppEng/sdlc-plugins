## Repository
trustify-backend

## Target Branch
main

## Description
Add the `advisory_summary` method to `SbomService` that aggregates advisory severity counts for a given SBOM. The method queries the `sbom_advisory` join table, joins to the `advisory` table to retrieve severity, deduplicates by advisory ID, groups counts by severity level, and returns an `AdvisorySeveritySummary`.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `pub async fn advisory_summary(&self, sbom_id: Id) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
- Follow the existing `SbomService` method patterns in `modules/fundamental/src/sbom/service/sbom.rs` — methods like `fetch` and `list` demonstrate the query builder, error handling, and return type conventions
- Use SeaORM to query `entity/src/sbom_advisory.rs` joined with `entity/src/advisory.rs` to get severity per advisory
- Deduplicate by advisory ID using `group_by` or `distinct` on the advisory ID column before counting
- Group counts by severity level (Critical, High, Medium, Low) and aggregate into the `AdvisorySeveritySummary` struct
- Return 404 (`AppError::NotFound`) if the SBOM does not exist — check SBOM existence first using the existing `fetch` method pattern
- Reference `common/src/db/query.rs` for shared query builder helpers
- Reference `common/src/error.rs` for `AppError` usage with `.context()` wrapping
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service scope.

## Acceptance Criteria
- [ ] `advisory_summary` method exists on `SbomService`
- [ ] Method returns `AdvisorySeveritySummary` with correct severity counts
- [ ] Advisories are deduplicated by advisory ID (same advisory linked multiple times counts once)
- [ ] Returns 404 error when SBOM ID does not exist
- [ ] No new database tables are introduced — uses existing `sbom_advisory` and `advisory` entities

## Test Requirements
- [ ] Test aggregation with an SBOM having advisories at multiple severity levels
- [ ] Test deduplication: same advisory linked to SBOM multiple times produces correct count
- [ ] Test 404 for non-existent SBOM ID
- [ ] Test empty result: SBOM with no advisories returns all zeros

## Dependencies
- Depends on: Task 1 — Advisory severity summary model
