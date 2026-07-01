# Task 3 — Add SBOM comparison service and endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the SBOM comparison service logic and the `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint. The service computes a structured diff between two SBOMs by querying existing package, advisory, and SBOM-package/SBOM-advisory join tables — no new database tables are needed. The diff is computed on-the-fly and must meet the p95 < 1s requirement for SBOMs with up to 2000 packages each.

## Files to Create
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomCompareService` (or method on existing `SbomService`) implementing the diff algorithm
- `modules/fundamental/src/sbom/endpoints/compare.rs` — `GET /api/v2/sbom/compare` handler with `left` and `right` query parameters

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` or add comparison method to existing `SbomService`
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route in the SBOM endpoint router

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparisonResult` JSON with added/removed packages, version changes, new/resolved vulnerabilities, and license changes

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `list.rs` — handlers return `Result<Json<T>, AppError>` and use `.context()` for error wrapping.
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` — the service takes a database connection and performs SeaORM queries.
- The diff algorithm should:
  1. Fetch packages for both SBOMs via the `sbom_package` join table (`entity/src/sbom_package.rs`)
  2. Compute set differences for added/removed packages and version changes
  3. Fetch advisories for both SBOMs via the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`)
  4. Compute new/resolved vulnerabilities by comparing advisory sets
  5. Fetch license data for packages via the `package_license` entity (`entity/src/package_license.rs`)
  6. Compute license changes for packages present in both SBOMs
- Use `HashMap` keyed on package name for O(n) diff computation to meet the performance requirement.
- Route registration: follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` where routes are registered via Axum router methods. The `/compare` route should be registered alongside existing SBOM routes.
- Validate that both `left` and `right` query parameters are present; return `AppError` with 400 status if either is missing.
- Validate that both SBOM IDs exist; return `AppError` with 404 status if either is not found.
- The `direction` field for version changes should compare versions to determine `upgrade` vs `downgrade` — use string comparison if no semver library is available, with a note for future semver-aware comparison.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service for fetching SBOM data; reuse its database connection pattern and query methods
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing service for package queries; may have helper methods for bulk package fetching
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing service for advisory queries; reuse for fetching advisory details
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — shared error type for endpoint error handling

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Added packages (in right but not left) are correctly identified
- [ ] Removed packages (in left but not right) are correctly identified
- [ ] Version changes (same package name, different version) are correctly identified with upgrade/downgrade direction
- [ ] New vulnerabilities (advisories affecting right but not left) are correctly identified
- [ ] Resolved vulnerabilities (advisories affecting left but not right) are correctly identified
- [ ] License changes (same package, different license) are correctly identified
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Response time p95 < 1s for SBOMs with up to 2000 packages each

## Test Requirements
- [ ] Integration test: comparison of two SBOMs with known differences returns correct diff structure
- [ ] Integration test: comparison returns empty diff when comparing an SBOM with itself
- [ ] Integration test: returns 400 when left or right parameter is missing
- [ ] Integration test: returns 404 when SBOM ID does not exist
- [ ] Integration test: version changes correctly classify upgrade vs downgrade
- [ ] Integration test: new and resolved vulnerabilities are correctly computed

## Verification Commands
- `cargo test --package trustify-fundamental -- sbom::compare` — run comparison-related tests
- `cargo clippy --package trustify-fundamental` — verify no lint warnings in new code

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison diff model structs
