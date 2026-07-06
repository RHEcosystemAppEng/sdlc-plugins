## Repository
trustify-backend

## Target Branch
main

## Description
Add an advisory severity summary model and a service method that aggregates vulnerability advisory severity counts for a given SBOM. This provides the data layer for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint described in TC-9001.

The service method queries the `sbom_advisory` join table, joins with the `advisory` entity to access the severity field, deduplicates by advisory ID, and groups counts by severity level (Critical, High, Medium, Low). It returns a `SeveritySummary` struct containing each severity count and a total.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — SeveritySummary response struct with fields: critical, high, medium, low, total (all u64), and optional threshold filter support

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` to expose the new model
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_summary(&self, sbom_id: Id, threshold: Option<Severity>) -> Result<SeveritySummary, AppError>` method that performs the aggregation query

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) for struct derivations (Serialize, Deserialize, Debug, Clone, ToSchema).
- The aggregation query should use SeaORM to join `entity::sbom_advisory` with `entity::advisory`, group by severity, and count distinct advisory IDs. Use `entity/src/sbom_advisory.rs` for the join table and `entity/src/advisory.rs` for the severity field.
- Return 404 via `AppError` if the SBOM ID does not exist — check SBOM existence before running the aggregation query, following the pattern in `modules/fundamental/src/sbom/service/sbom.rs` (existing fetch method).
- Support the optional `threshold` parameter by filtering severity levels: when threshold is provided (e.g., "critical"), only include counts at or above that severity level.
- No new database tables are required — use existing `sbom_advisory` relationship table.
- Per CONVENTIONS.md §Module Pattern: follow the `model/ + service/ + endpoints/` directory structure for the sbom module. Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Error Handling: return `Result<SeveritySummary, AppError>` with `.context()` wrapping on database queries. See `modules/fundamental/src/sbom/service/sbom.rs` for the established pattern. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's .rs handler scope.
- Per CONVENTIONS.md §Query Helpers: consider using shared query helpers from `common/src/db/query.rs` for the aggregation query if applicable. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's .rs service scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing model struct showing the derivation pattern (Serialize, Deserialize, ToSchema) to follow
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition showing how severity levels are represented
- `common/src/error.rs::AppError` — shared error type for returning 404 and database errors
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `SeveritySummary` struct exists with fields: critical, high, medium, low, total (all u64)
- [ ] `SbomService::get_advisory_summary` method returns correct severity counts for a given SBOM
- [ ] Advisories are deduplicated by advisory ID before counting
- [ ] Method returns 404 AppError when SBOM ID does not exist
- [ ] Optional threshold parameter filters counts to include only severities at or above the threshold

## Test Requirements
- [ ] Unit test: `get_advisory_summary` returns correct counts for an SBOM with known advisories at each severity level
- [ ] Unit test: `get_advisory_summary` deduplicates advisories linked multiple times to the same SBOM
- [ ] Unit test: `get_advisory_summary` returns 404 for a non-existent SBOM ID
- [ ] Unit test: threshold filter correctly excludes severity levels below the threshold

## Dependencies
- None (first task in the chain)
