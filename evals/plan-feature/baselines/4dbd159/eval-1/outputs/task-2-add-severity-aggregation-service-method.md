# Task 2 -- Add severity aggregation service method

## Repository
trustify-backend

## Target Branch
main

## Description
Add a `get_advisory_summary` method to `SbomService` that queries the `sbom_advisory` join table, joins to the advisory table to read severity, deduplicates advisories by advisory ID, and returns an `AdvisorySeveritySummary` with counts grouped by severity level (Critical, High, Medium, Low). This method encapsulates the server-side aggregation logic that replaces client-side counting.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- add `get_advisory_summary(&self, sbom_id: Id) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## API Changes
- `SbomService::get_advisory_summary(sbom_id)` -- NEW: returns aggregated advisory severity counts for a given SBOM

## Implementation Notes
- Follow the existing service method pattern in `modules/fundamental/src/sbom/service/sbom.rs` (e.g., the `fetch` or `list` methods). Service methods accept an ID parameter and return `Result<T, AppError>`.
- Use SeaORM to query the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`), joining to the `advisory` table (`entity/src/advisory.rs`) to access the severity field.
- **Deduplication**: The query must deduplicate by advisory ID (use `DISTINCT` or `GROUP BY advisory_id`) before counting, as the same advisory may be linked to an SBOM multiple times through different paths.
- **Severity grouping**: Use a SQL `COUNT ... GROUP BY severity` query or equivalent SeaORM expression. Map severity values to the four buckets (Critical, High, Medium, Low). Handle unknown severity values gracefully (skip or log a warning).
- **SBOM existence check**: Before querying, verify the SBOM exists. If not, return an appropriate error that maps to HTTP 404 via `AppError`. Check the existing `get` handler in `modules/fundamental/src/sbom/endpoints/get.rs` for how 404 is handled for missing SBOMs.
- **Performance**: Use a single SQL query with `GROUP BY` rather than fetching all advisories and counting in Rust. This ensures p95 < 200ms for SBOMs with up to 500 advisories.
- Error handling: wrap database errors with `.context()` per the project convention (see `common/src/error.rs` for `AppError`).

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- existing service struct to add the method to; reference for method signatures, error handling, and database access patterns
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination; may contain useful aggregation helpers
- `entity/src/sbom_advisory.rs` -- the SBOM-Advisory join table entity; this is the primary table to query
- `entity/src/advisory.rs` -- advisory entity containing the severity column
- `common/src/error.rs::AppError` -- error type for wrapping database errors

## Acceptance Criteria
- [ ] `SbomService` has a `get_advisory_summary` method that accepts an SBOM ID
- [ ] Method returns `AdvisorySeveritySummary` with correct counts for each severity level
- [ ] Advisories are deduplicated by advisory ID before counting
- [ ] Returns an error mapped to 404 when the SBOM does not exist
- [ ] Query uses server-side aggregation (GROUP BY), not client-side counting

## Test Requirements
- [ ] Unit/integration test: SBOM with advisories across all severity levels returns correct counts
- [ ] Unit/integration test: SBOM with duplicate advisory links returns deduplicated counts
- [ ] Unit/integration test: SBOM with no advisories returns all-zero counts
- [ ] Unit/integration test: nonexistent SBOM ID returns a 404-mappable error

## Verification Commands
- `cargo test --package fundamental -- sbom::service::test_get_advisory_summary` -- all severity aggregation service tests pass

## Dependencies
- Depends on: Task 1 -- Add AdvisorySeveritySummary response model
