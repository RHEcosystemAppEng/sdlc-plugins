## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison service logic and REST endpoint. The service method computes a structured diff between two SBOMs by comparing their linked packages, advisories, and licenses. The endpoint exposes this as `GET /api/v2/sbom/compare?left={id1}&right={id2}` and returns an `SbomComparisonResult`.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare(&self, left_id: Id, right_id: Id) -> Result<SbomComparisonResult, AppError>` method to SbomService
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/compare` route in the router

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — GET handler for `/api/v2/sbom/compare`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparisonResult` with structured diff of two SBOMs

## Implementation Notes
- Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` — handlers return `Result<Json<T>, AppError>` and use `.context()` for error wrapping.
- The `compare` handler should:
  1. Parse `left` and `right` query parameters (both required; return 400 if missing)
  2. Fetch both SBOMs using existing `SbomService::fetch()` — return 404 if either is not found
  3. Call the new `SbomService::compare()` method
  4. Return the `SbomComparisonResult` as JSON
- The `SbomService::compare()` method should:
  1. Fetch packages for both SBOMs using the existing `PackageService` (see `modules/fundamental/src/package/service/mod.rs`)
  2. Compute set differences for added/removed packages by comparing package name+version tuples
  3. Compute version changes by finding packages with the same name but different versions, determining upgrade vs downgrade direction
  4. Fetch advisories for both SBOMs using the existing `AdvisoryService` (see `modules/fundamental/src/advisory/service/advisory.rs`)
  5. Compute new/resolved vulnerabilities by comparing advisory sets
  6. Compute license changes by comparing license fields for packages present in both SBOMs
- No new database tables — compute diff on-the-fly from existing data per non-functional requirements.
- Performance: for SBOMs with up to 2000 packages, use `HashMap` for O(1) lookups during diff computation to meet p95 < 1s requirement.
- Per CONVENTIONS.md §Error handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping for all fallible operations. Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust endpoint file scope. See `modules/fundamental/src/sbom/endpoints/get.rs` for the established pattern.
- Per CONVENTIONS.md §Endpoint registration: register the route in the module's `endpoints/mod.rs`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope. See `modules/fundamental/src/sbom/endpoints/mod.rs` for existing route registrations.
- Per CONVENTIONS.md §Module pattern: place service logic in `service/` and endpoint handler in `endpoints/`, following the `model/ + service/ + endpoints/` structure. Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's endpoint module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — extend with the new `compare` method; reuse existing `fetch` method for SBOM retrieval
- `modules/fundamental/src/package/service/mod.rs::PackageService` — use to fetch packages for each SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — use to fetch advisories affecting each SBOM
- `common/src/db/query.rs` — reuse query builder helpers for filtering packages/advisories by SBOM ID
- `common/src/error.rs::AppError` — use for consistent error handling

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Added packages (present in right but not left) are correctly identified
- [ ] Removed packages (present in left but not right) are correctly identified
- [ ] Version changes (same package name, different version) include correct direction (upgrade/downgrade)
- [ ] New vulnerabilities (advisories in right but not left) are correctly identified
- [ ] Resolved vulnerabilities (advisories in left but not right) are correctly identified
- [ ] License changes (same package, different license) are correctly identified
- [ ] Response time meets p95 < 1s for SBOMs with up to 2000 packages each

## Test Requirements
- [ ] Unit test for `SbomService::compare()` with known left/right package sets, verifying all six diff categories
- [ ] Unit test for edge case: comparing an SBOM to itself returns empty diff in all categories
- [ ] Unit test for edge case: comparing against an empty SBOM returns all packages as added or removed
- [ ] Unit test for version change direction detection (upgrade vs downgrade)

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental sbom::service` — service tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model types
