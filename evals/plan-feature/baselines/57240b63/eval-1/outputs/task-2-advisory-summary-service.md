## Repository
trustify-backend

## Target Branch
main

## Description
Add an advisory severity aggregation query method to `SbomService` that counts unique advisories by severity level for a given SBOM ID. This method uses the existing `sbom_advisory` join table and the `advisory` entity's severity field to compute severity counts server-side, avoiding client-side pagination and counting. It returns an `AdvisorySeveritySummary` or a 404 error if the SBOM does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`
- `modules/fundamental/src/sbom/service/mod.rs` — ensure the new method is accessible (update re-exports if needed)

## Implementation Notes
- Follow the existing query pattern in `SbomService` (`modules/fundamental/src/sbom/service/sbom.rs`) for database access — use SeaORM queries with `.context()` error wrapping per the error handling convention.
- Query the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) joined with `advisory` (`entity/src/advisory.rs`) to fetch advisories linked to the given SBOM. Group by severity and count distinct advisory IDs to deduplicate.
- The severity field is on the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` — inspect it to determine the exact column name and enum values (Critical, High, Medium, Low).
- Return `AppError::NotFound` (from `common/src/error.rs`) when the SBOM ID does not exist — check SBOM existence first by attempting to fetch it, consistent with the pattern in the existing `get` method in `sbom.rs`.
- Use a single database query with `GROUP BY severity` and `COUNT(DISTINCT advisory_id)` for p95 < 200ms performance on SBOMs with up to 500 advisories.
- Per Key Conventions §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` service file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — extend this existing service with the new method; follow its constructor, database connection, and error handling patterns
- `entity/src/sbom_advisory.rs` — the join table entity for SBOM-to-advisory relationships; use it for the aggregation query
- `entity/src/advisory.rs` — the advisory entity containing the severity column
- `common/src/error.rs::AppError` — reuse the existing error enum for 404 and internal errors
- `common/src/db/query.rs` — shared query builder helpers; check if any filtering or count helpers are reusable for the aggregation

## Acceptance Criteria
- [ ] `SbomService` has a public method `get_advisory_summary` that accepts an SBOM ID and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] The method counts unique advisories grouped by severity (critical, high, medium, low) using the `sbom_advisory` join table
- [ ] The method returns `AppError::NotFound` (or equivalent 404 error) when the SBOM ID does not exist
- [ ] Advisory deduplication is performed by distinct advisory ID
- [ ] The total field equals the sum of critical + high + medium + low counts

## Test Requirements
- [ ] Unit test: verify correct severity counts for a known set of advisory-SBOM relationships
- [ ] Unit test: verify 404 error when SBOM ID does not exist
- [ ] Unit test: verify deduplication — duplicate advisory links produce correct counts

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model struct

## Jira Fields
- **Labels:** ai-generated-jira
- **Priority:** Major
- **Fix Versions:** RHTPA 1.5.0

[sdlc-workflow] Description digest: sha256-md:5078abbd4f6a5adca34d620486a7273e4d5e2545d3139189ac123cfac070d059
