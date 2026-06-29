# Task 2: Add advisory summary aggregation to SbomService

## Repository

trustify-backend

## Target Branch

main

## Description

Add a service method to `SbomService` that queries the `sbom_advisory` join table, groups linked advisories by severity, counts each severity level, and returns an `AdvisorySeveritySummary`. The method must deduplicate by advisory ID to avoid inflated counts when multiple relationships exist between the same SBOM and advisory.

## Files to Modify

- `modules/fundamental/src/sbom/service/sbom.rs` — Add `async fn advisory_summary(&self, sbom_id: Uuid, db: &impl ConnectionTrait) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes

- Follow the `SbomService` method pattern in `modules/fundamental/src/sbom/service/sbom.rs` — match the method signature style, error handling, and database connection parameter conventions.
- Use SeaORM query builder to join `sbom_advisory` with `advisory` entity, filter by SBOM ID, select distinct advisory IDs, group by severity, and count.
- Reference `entity/sbom_advisory.rs` for the join table entity definition and column names.
- Reference `common/src/db/query.rs` for any shared query builder helpers that may simplify the query.
- Return `AppError::NotFound` (from `common/src/error.rs`) if the SBOM ID does not exist — check SBOM existence before running the aggregation query.
- Deduplicate by advisory ID: use `DISTINCT` on advisory ID before grouping by severity, or use a subquery to select distinct advisory IDs first.
- Map the severity column values (e.g., "critical", "high", "medium", "low") to the corresponding fields in `AdvisorySeveritySummary`. Handle unknown or null severity values gracefully (exclude from named counts but include in total).
- Performance target: p95 < 200ms for SBOMs with up to 500 advisories. Use a single aggregation query rather than loading all advisory records into memory.
- Per CONVENTIONS.md §Error handling: return `Result<AdvisorySeveritySummary, AppError>` and use `.context()` wrapping for error propagation. See `modules/fundamental/src/sbom/service/sbom.rs` for the established pattern.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service file scope.
- Per CONVENTIONS.md §Query helpers: use shared filtering and query utilities from `common/src/db/query.rs` where applicable.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service file scope.
- Per CONVENTIONS.md §Module pattern: add the new method within the existing service layer following the `model/ + service/ + endpoints/` structure.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust module file scope.

## Reuse Candidates

- `common/src/error.rs::AppError` — Error handling, especially `AppError::NotFound` for missing SBOM
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `entity/sbom_advisory.rs` — Join table entity for SBOM-to-advisory relationships
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference for how severity values are stored and accessed
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service method patterns (fetch, list, ingest)

## Acceptance Criteria

- [ ] `SbomService::advisory_summary` method exists and compiles
- [ ] Method returns correct severity counts grouped from the `sbom_advisory` join table
- [ ] Advisory IDs are deduplicated before counting
- [ ] Returns `AppError::NotFound` when the SBOM ID does not exist
- [ ] Uses a single SQL aggregation query (not N+1 or in-memory aggregation)
- [ ] Unknown or null severities are excluded from named counts but included in total

## Test Requirements

- [ ] Unit/integration test: verify correct counts for an SBOM with known advisory severities
- [ ] Unit/integration test: verify deduplication when the same advisory is linked multiple times
- [ ] Unit/integration test: verify `NotFound` error for a non-existent SBOM ID

## Dependencies

- Depends on: Task 1 — Add AdvisorySeveritySummary response model

## Verification Commands

- `cargo check -p trustify-module-fundamental` — verify compilation
- `cargo test -p trustify-module-fundamental -- sbom::service` — run service tests
