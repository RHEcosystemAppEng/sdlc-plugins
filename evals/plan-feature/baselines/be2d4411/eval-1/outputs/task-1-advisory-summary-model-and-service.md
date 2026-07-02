## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response model struct and add a severity aggregation method to `SbomService` that queries the `sbom_advisory` join table, deduplicates advisories by ID, groups by severity level (Critical, High, Medium, Low), and returns counts. This provides the data layer for the new advisory-summary endpoint without requiring any new database tables.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — AdvisorySeveritySummary struct with critical, high, medium, low, and total count fields

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary` declaration and re-export `AdvisorySeveritySummary`
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_severity_summary(sbom_id)` method to `SbomService`

## Implementation Notes
- Follow the existing model struct pattern from `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`): derive `Serialize`, `Deserialize`, `Debug`, `Clone`, and use `utoipa::ToSchema` for OpenAPI schema generation.
- The `AdvisorySeveritySummary` struct fields should be: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`.
- The `get_advisory_severity_summary` method in `SbomService` should:
  1. Verify the SBOM exists by querying the `sbom` entity; return `AppError::NotFound` if absent.
  2. Query `sbom_advisory` joined with `advisory` to get severity values.
  3. Use `SELECT severity, COUNT(DISTINCT advisory_id)` grouping to deduplicate advisories that may be linked multiple times.
  4. Map severity strings to the struct fields and compute `total` as the sum.
- Use SeaORM query builder patterns from `common/src/db/query.rs` for constructing the aggregation query.
- Return `Result<AdvisorySeveritySummary, AppError>` with `.context()` wrapping on all database errors.

Per CONVENTIONS.md §Module Pattern: place the model struct in `modules/fundamental/src/sbom/model/advisory_summary.rs` and export from `model/mod.rs`, following the established model/service/endpoints directory structure.
Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's module structure scope.

Per CONVENTIONS.md §Error Handling: return `Result<AdvisorySeveritySummary, AppError>` from the service method with `.context()` wrapping on database errors, following the pattern in existing service methods.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` handler file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — follow the same derive macros and field naming pattern for the new struct
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — extend with the new method following existing fetch/list method patterns
- `common/src/db/query.rs` — reuse shared query builder helpers for constructing the aggregation query
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity to query for advisory links
- `entity/src/advisory.rs` — Advisory entity containing the severity field
- `common/src/error.rs::AppError` — error enum for returning 404 when SBOM not found

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs` with fields: `critical`, `high`, `medium`, `low`, `total` (all integer types)
- [ ] Struct derives `Serialize`, `Deserialize`, `Debug`, `Clone`, and `utoipa::ToSchema`
- [ ] `SbomService::get_advisory_severity_summary` method exists and returns correct severity counts from the database
- [ ] Advisories are deduplicated by advisory ID before counting (same advisory linked twice counts as one)
- [ ] Method returns `AppError::NotFound` when the SBOM ID does not exist
- [ ] Method returns all zeros when the SBOM exists but has no linked advisories

## Test Requirements
- [ ] Unit test: aggregation returns correct counts when advisories span all four severity levels
- [ ] Unit test: deduplication works correctly — same advisory linked to the same SBOM multiple times counts once
- [ ] Unit test: returns `AppError::NotFound` for a non-existent SBOM ID
- [ ] Unit test: returns all-zero counts for an SBOM with no linked advisories

## Dependencies
None

---

[sdlc-workflow] Description digest: sha256-md:970fb32fc6d4a4e58eea933e775d5e15ec0d6d4129383691b9e582a630b9fe80
