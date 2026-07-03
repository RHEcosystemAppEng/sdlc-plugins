## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the SBOM comparison service logic and expose it via a new REST endpoint. The service computes a structured diff between two SBOMs by comparing their package lists, advisory associations, and license data. The endpoint accepts two SBOM IDs as query parameters and returns the comparison result. The comparison must be computed on-the-fly from existing package and advisory data -- no new database tables are required.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` -- Handler for `GET /api/v2/sbom/compare?left={id1}&right={id2}`

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- Add `compare` method to SbomService that computes the structured diff
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Register the comparison route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- NEW: Returns `SbomComparisonResult` JSON with structured diff between two SBOMs. Query parameters `left` and `right` are required SBOM IDs. Returns 400 if parameters missing, 404 if either SBOM not found.

## Implementation Notes
- Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` -- use `axum::extract::Query` for the `left` and `right` query parameters.
- Return `Result<Json<SbomComparisonResult>, AppError>` following the error handling pattern in `common/src/error.rs`. Use `.context()` wrapping on all database operations.
- Comparison service logic steps:
  1. Fetch both SBOMs by ID using existing `SbomService::fetch` method
  2. Load package lists for both SBOMs via the `sbom_package` join table (`entity/src/sbom_package.rs`)
  3. Compute package diffs: added = right_only, removed = left_only, changed = both_with_different_version
  4. Load advisories for both SBOMs via `sbom_advisory` join table (`entity/src/sbom_advisory.rs`)
  5. Compute advisory diffs: new_vulnerabilities = right_only, resolved = left_only
  6. Load licenses via `package_license` entity (`entity/src/package_license.rs`)
  7. Compute license diffs: packages present in both with different licenses
- For version change direction: compare versions to determine "upgrade" vs "downgrade" (use semver comparison if available, or lexicographic as fallback).
- Performance requirement: p95 < 1s for SBOMs with up to 2000 packages each. Consider using database-level set operations (SQL EXCEPT / INTERSECT) instead of loading all packages into memory.
- Register the route in `endpoints/mod.rs` following the existing route registration pattern used by `list.rs` and `get.rs`.
- Per CONVENTIONS.md (Key Conventions) -- Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's endpoint file scope.
- Per CONVENTIONS.md (Key Conventions) -- Module pattern: follow `model/ + service/ + endpoints/` structure. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's service file scope.
- Per CONVENTIONS.md (Key Conventions) -- Endpoint registration: each module's `endpoints/mod.rs` registers routes. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per docs/constraints.md SS2: commit must reference TC-9003 in footer. Per SS3: branch must be named TC-9003.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- existing service with `fetch` and `list` methods for SBOM retrieval
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- advisory lookup for vulnerability comparison
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- package lookup methods
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination
- `modules/fundamental/src/sbom/endpoints/get.rs` -- endpoint handler pattern reference (axum extract, error handling)

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Added packages correctly identified (present in right SBOM, absent in left)
- [ ] Removed packages correctly identified (present in left SBOM, absent in right)
- [ ] Version changes correctly identified with accurate upgrade/downgrade direction
- [ ] New vulnerabilities correctly identified (advisories affecting right but not left)
- [ ] Resolved vulnerabilities correctly identified (advisories affecting left but not right)
- [ ] License changes correctly identified for packages present in both SBOMs

## Test Requirements
- [ ] Test comparison with two SBOMs having added, removed, and changed packages
- [ ] Test comparison with vulnerability changes (new and resolved)
- [ ] Test comparison with license changes
- [ ] Test empty diff (identical SBOMs)
- [ ] Test 404 response for non-existent SBOM IDs
- [ ] Test 400 response for missing query parameters

## Verification Commands
- `cargo test --test api sbom_compare` -- runs comparison endpoint integration tests
- `cargo build` -- expected: compiles without errors

## Documentation Updates
- API endpoint reference should be updated with the new comparison endpoint (covered by Task 10)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 2 -- Add SBOM comparison response model types
