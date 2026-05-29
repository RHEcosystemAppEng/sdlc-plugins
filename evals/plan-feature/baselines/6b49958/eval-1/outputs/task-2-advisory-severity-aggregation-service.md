## Repository
trustify-backend

## Target Branch
main

## Description
Add a `get_severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table to aggregate advisory severity counts for a given SBOM ID. This method performs a single database query that groups advisories by severity level and returns deduplicated counts, avoiding the need for client-side pagination and counting.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — add `get_severity_summary` method to `AdvisoryService`

## Implementation Notes
- Follow the existing service method pattern in `modules/fundamental/src/advisory/service/advisory.rs` (`AdvisoryService` methods for fetch, list, search). Each method takes a database connection/pool reference and returns `Result<T, AppError>`.
- Use SeaORM query builder to join `sbom_advisory` with `advisory` table, filter by `sbom_id`, group by severity, and count distinct advisory IDs (to deduplicate as required by the feature spec).
- The join table entity is defined in `entity/src/sbom_advisory.rs` — use this entity for the query.
- The advisory entity in `entity/src/advisory.rs` contains the severity field to group by.
- Return `Result<AdvisorySeveritySummary, AppError>` using the model created in Task 1.
- Handle the case where the SBOM ID does not exist by checking whether the SBOM exists first using the pattern in `modules/fundamental/src/sbom/service/sbom.rs::SbomService` (fetch method), and return an appropriate `AppError` (404) if not found. Reference `common/src/error.rs` for the `AppError` enum.
- Use the shared query helpers in `common/src/db/query.rs` if applicable for building the aggregation query.
- Per docs/constraints.md §5.4: do not duplicate existing functionality — reuse `SbomService::fetch` or similar for SBOM existence validation.

## Reuse Candidates
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing service struct to extend with the new method; follow its method signatures and error handling patterns.
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — contains `fetch` method pattern for validating entity existence and returning 404 on miss.
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; may provide patterns for building the aggregation query.
- `common/src/error.rs::AppError` — error enum with `IntoResponse` implementation; use `.context()` wrapping as established by sibling service methods.
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity needed for the aggregation query.

## Acceptance Criteria
- [ ] `AdvisoryService::get_severity_summary(sbom_id)` method exists and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Method queries the `sbom_advisory` join table grouped by severity with distinct advisory ID counts
- [ ] Method returns 404 `AppError` when the SBOM ID does not exist
- [ ] Method deduplicates advisories by advisory ID before counting
- [ ] `total` field equals the sum of critical + high + medium + low counts

## Test Requirements
- [ ] Integration test: valid SBOM with known advisories returns correct severity counts
- [ ] Integration test: non-existent SBOM ID returns appropriate error
- [ ] Integration test: SBOM with duplicate advisory links (same advisory linked multiple times) returns deduplicated counts
- [ ] Integration test: SBOM with zero advisories returns all-zero counts

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model

[sdlc-workflow] Description digest: sha256:8eca2ddfe76a139589ad57b98cd28dd49e0373d2488826a522e661f37eecf2b2
