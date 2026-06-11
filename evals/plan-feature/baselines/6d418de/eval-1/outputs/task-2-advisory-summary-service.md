# Task 2 — Add advisory severity aggregation service method

## Repository
trustify-backend

## Target Branch
main

## Description
Add an `advisory_summary` method to `SbomService` that queries the `sbom_advisory` join table, joins to the `advisory` table, deduplicates advisories by ID, and groups counts by severity level. The method accepts an SBOM ID, verifies the SBOM exists (returning a not-found error if it does not), and returns an `AdvisorySeveritySummary` struct with counts for critical, high, medium, low, and total unique advisories. This is the core business logic for the advisory severity aggregation endpoint.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `advisory_summary` method to `SbomService`

## Implementation Notes
- Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`). The existing methods demonstrate how to obtain a database connection, execute queries, and return typed results.
- The query should:
  1. Verify the SBOM exists by checking the `sbom` entity table — return `AppError` (not found) if the SBOM ID does not exist, consistent with existing SBOM endpoint behavior
  2. Query the `sbom_advisory` join table (entity defined in `entity/src/sbom_advisory.rs`) filtered by the given SBOM ID
  3. Join to the `advisory` entity (`entity/src/advisory.rs`) to access the severity field
  4. Deduplicate by advisory ID to count only unique advisories
  5. Group by severity and count occurrences for each level (critical, high, medium, low)
  6. Compute the total as the sum of all severity counts
- Use SeaORM query building patterns from `common/src/db/query.rs` for query construction.
- Use `.context()` error wrapping per the project's error handling convention (`common/src/error.rs`).
- Performance target: p95 < 200ms for SBOMs with up to 500 advisories. The query should be efficient — use database-level aggregation (GROUP BY + COUNT) rather than fetching all records and counting in Rust.
- Per docs/constraints.md Section 5 (Code Change Rules): changes must be scoped to the files listed; code must not be modified without first inspecting it; implementation must follow the patterns referenced in these notes.
- Per docs/constraints.md Section 2 (Commit Rules): every commit must reference TC-9001, follow Conventional Commits, and include the AI assistance trailer.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — contains existing service methods (fetch, list, ingest) that demonstrate the query pattern, error handling, and database connection usage to follow
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting that may be reusable for the aggregation query
- `common/src/error.rs::AppError` — the error enum that the method should return for not-found and internal errors
- `entity/src/sbom_advisory.rs` — the SBOM-Advisory join table entity used for the aggregation query
- `entity/src/advisory.rs` — the Advisory entity containing the severity field to group on

## Acceptance Criteria
- [ ] `SbomService::advisory_summary(sbom_id)` method exists and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Method returns correct severity counts by querying the database with GROUP BY aggregation
- [ ] Method deduplicates advisories by advisory ID before counting
- [ ] Method returns a not-found error when the SBOM ID does not exist
- [ ] Total field equals the sum of critical + high + medium + low counts

## Test Requirements
- [ ] Unit test: service method returns correct counts for an SBOM with advisories at multiple severity levels
- [ ] Unit test: service method correctly deduplicates advisories (same advisory linked to SBOM multiple times counts as one)
- [ ] Unit test: service method returns not-found error for a non-existent SBOM ID
- [ ] Unit test: service method returns zero counts for an SBOM with no linked advisories

## Verification Commands
- `cargo build -p trustify-module-fundamental` — should compile without errors
- `cargo test -p trustify-module-fundamental` — unit tests pass

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model
