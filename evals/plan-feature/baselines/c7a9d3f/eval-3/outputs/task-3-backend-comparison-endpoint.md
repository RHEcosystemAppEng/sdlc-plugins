## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison service method and HTTP endpoint. The service method computes a structured diff between two SBOMs by comparing their package lists, advisory associations, and license data. The endpoint exposes this as `GET /api/v2/sbom/compare?left={id1}&right={id2}`.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler for `GET /api/v2/sbom/compare` with `left` and `right` query parameters

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `compare()` method to `SbomService` that computes the diff between two SBOMs
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the compare endpoint route
- `tests/api/sbom.rs` — Add integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparisonResult` with structured diff between two SBOMs

## Implementation Notes
- **Service method**: Add `SbomService::compare(left_id, right_id)` that:
  1. Fetches both SBOMs by ID (reuse existing `SbomService::fetch` method in `service/sbom.rs`)
  2. Loads packages for both SBOMs using the `sbom_package` join table (entity in `entity/src/sbom_package.rs`)
  3. Computes set difference for added/removed packages
  4. Computes version changes by matching packages by name across both SBOMs
  5. Loads advisories for both SBOMs using the `sbom_advisory` join table (entity in `entity/src/sbom_advisory.rs`)
  6. Computes new/resolved vulnerabilities by comparing advisory sets
  7. Computes license changes by comparing `package_license` mappings (entity in `entity/src/package_license.rs`)
  8. Returns `SbomComparisonResult` (from Task 2)
- **Endpoint handler**: Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs`. The handler extracts query params `left` and `right`, calls `SbomService::compare()`, and returns `Json<SbomComparisonResult>`.
- **Route registration**: Follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` where routes are registered. Add `.route("/compare", get(compare))` to the SBOM route group.
- **Error handling**: Return `AppError` with `.context()` for database errors, and a 400 Bad Request if either SBOM ID is invalid or not found. Follow the error pattern in `common/src/error.rs`.
- **Performance**: The comparison computes the diff on-the-fly (no new database tables per non-functional requirements). Use efficient set operations (HashSet-based) for package comparison to meet the p95 < 1s target for SBOMs with up to 2000 packages each.
- **Query helpers**: Use the shared query builder from `common/src/db/query.rs` for any database queries that need filtering or pagination.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service with `fetch` and `list` methods; add `compare` alongside these
- `modules/fundamental/src/sbom/endpoints/get.rs` — Pattern for SBOM endpoint handler (extract path/query params, call service, return JSON)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern for adding new endpoints
- `common/src/db/query.rs` — Shared query builder helpers for database operations
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for loading packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for loading advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for comparing licenses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Response correctly identifies added packages (in right but not left)
- [ ] Response correctly identifies removed packages (in left but not right)
- [ ] Response correctly identifies version changes with upgrade/downgrade direction
- [ ] Response correctly identifies new vulnerabilities (advisories affecting right but not left)
- [ ] Response correctly identifies resolved vulnerabilities (advisories affecting left but not right)
- [ ] Response correctly identifies license changes
- [ ] Returns 400 when left or right SBOM ID is invalid or not found
- [ ] Endpoint responds within p95 < 1s for SBOMs with up to 2000 packages each

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences, verify all diff categories are correct
- [ ] Integration test: compare identical SBOMs, verify all diff categories are empty
- [ ] Integration test: request with invalid SBOM ID returns 400
- [ ] Integration test: request with missing left or right parameter returns 400
- [ ] Follow the existing test pattern in `tests/api/sbom.rs` using `assert_eq!(resp.status(), StatusCode::OK)`

## Verification Commands
- `cargo test -p trustify-tests -- sbom::compare` — runs comparison endpoint integration tests
- `cargo check -p trustify-fundamental` — compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Backend comparison model types
