## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model and the severity aggregation service method to support the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The model represents a severity count breakdown (`critical`, `high`, `medium`, `low`, `total`) with deduplication by advisory ID. The service method queries the existing `sbom_advisory` join table to produce the aggregated counts without requiring new database tables.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct with Serialize derive and fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_summary(sbom_id)` method to `SbomService` that queries the `sbom_advisory` join table, joins with the `advisory` table to get severity, deduplicates by advisory ID, and returns `AdvisorySeveritySummary`

## Implementation Notes
- Follow the existing module pattern: each domain module uses `model/ + service/ + endpoints/` structure. The `SbomSummary` struct in `modules/fundamental/src/sbom/model/summary.rs` demonstrates the model pattern.
- Use SeaORM for the aggregation query. The `sbom_advisory` entity at `entity/src/sbom_advisory.rs` provides the join between SBOMs and advisories. The `advisory` entity at `entity/src/advisory.rs` contains the severity field.
- Deduplicate by advisory ID in the SQL query (use `DISTINCT` or `GROUP BY` on advisory ID before counting severities) to satisfy the MVP requirement of counting only unique advisories.
- The service method should return `Result<AdvisorySeveritySummary, AppError>` following the error handling convention. See `modules/fundamental/src/sbom/service/sbom.rs` for the existing `SbomService` pattern with `.context()` wrapping.
- Use the shared query helpers in `common/src/db/query.rs` if applicable for filtering.
- NFR: the query must achieve p95 < 200ms for SBOMs with up to 500 advisories. Design the query to minimize joins and use indexed columns.
- Per Key Conventions (Module pattern): follow the `model/ + service/ + endpoints/` structure.
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's model directory scope.
- Per Key Conventions (Error handling): all service methods return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — demonstrates the model struct pattern with Serialize derive for API responses
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition that the aggregation query will group by
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list methods showing the query pattern and error handling
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with `critical`, `high`, `medium`, `low`, and `total` fields
- [ ] `SbomService::get_advisory_summary(sbom_id)` returns correct severity counts for a given SBOM
- [ ] Advisory counts are deduplicated by advisory ID (same advisory linked multiple times is counted once)
- [ ] Method returns `AppError` (not found) when the SBOM ID does not exist
- [ ] No new database tables are created — uses existing `sbom_advisory` relationship table

## Test Requirements
- [ ] Unit test: `get_advisory_summary` returns correct counts for an SBOM with known advisories at different severities
- [ ] Unit test: `get_advisory_summary` deduplicates advisories linked multiple times to the same SBOM
- [ ] Unit test: `get_advisory_summary` returns an error for a non-existent SBOM ID
- [ ] Unit test: `get_advisory_summary` returns all-zero counts for an SBOM with no linked advisories

## Dependencies
- None
