# Task 2 — Add SBOM comparison diff endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint that computes a structured diff between two SBOM versions. The endpoint returns added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The diff is computed on-the-fly from existing package, advisory, and license data — no new database tables are required.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add a `compare` method to `SbomService` that loads both SBOMs' package/advisory/license data and computes the diff
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/compare` route
- `server/src/main.rs` — no changes needed if route registration is handled in the module's endpoints/mod.rs (verify during implementation)

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — define the comparison result structs: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler for `GET /api/v2/sbom/compare` that parses `left` and `right` query params, calls `SbomService::compare`, and returns the result as JSON
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns a structured diff between two SBOMs with sections for added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, and license_changes

## Implementation Notes
- **Response shape** (from Figma design contract):
  ```json
  {
    "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade|downgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical|high|medium|low", "title": "...", "affected_package": "..." }],
    "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
    "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
  }
  ```
- **Module pattern**: follow the existing `model/ + service/ + endpoints/` structure used by `sbom`, `advisory`, and `package` modules
- **Error handling**: return `Result<Json<SbomComparisonResult>, AppError>` from the handler, wrapping database errors with `.context()` as done in `modules/fundamental/src/sbom/endpoints/get.rs`
- **Endpoint registration**: register the compare route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern as `list.rs` and `get.rs`
- **Diff algorithm for packages**: load packages for both SBOMs via `PackageService`, compute set differences by package name. For packages present in both, compare versions to detect changes. Determine "upgrade" vs "downgrade" direction using semantic version comparison
- **Vulnerability diff**: load advisories linked to each SBOM via the `sbom_advisory` join table and `AdvisoryService`. New vulnerabilities = advisories in right SBOM not in left. Resolved = advisories in left not in right
- **License diff**: compare `license` field from `PackageSummary` for packages present in both SBOMs
- **Performance**: the NFR requires p95 < 1s for SBOMs with up to 2000 packages each. Use batch queries to load all packages and advisories per SBOM in single queries rather than N+1 patterns. Consider using `HashSet` for O(1) lookups during diff computation
- **No new database tables**: per the NFR, compute everything on-the-fly from existing `sbom_package`, `sbom_advisory`, `package`, `advisory`, and `package_license` entities
- **Query helpers**: use shared filtering and pagination utilities from `common/src/db/query.rs` for loading package and advisory lists
- Per docs/constraints.md §2: every commit must reference TC-9003 in the footer, use Conventional Commits, and include `--trailer="Assisted-by: Claude Code"`
- Per docs/constraints.md §3: branch must be named after the Jira issue ID
- Per docs/constraints.md §5: do not modify files outside scope, inspect code before modifying

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch and list methods; add the compare method here to reuse existing DB connection patterns and query infrastructure
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — use to load advisories for each SBOM to compute vulnerability diffs
- `modules/fundamental/src/package/service/mod.rs::PackageService` — use to load packages for each SBOM
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct definition patterns and serde serialization
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — has `severity` field needed for vulnerability diff response
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — has `license` field needed for license diff
- `common/src/model/paginated.rs::PaginatedResults` — reference for response type patterns
- `common/src/error.rs::AppError` — use for error handling in the new endpoint
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for querying advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping for license change detection

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with a JSON body containing added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, and license_changes arrays
- [ ] The endpoint returns 400 if either `left` or `right` query parameter is missing
- [ ] The endpoint returns 404 if either SBOM ID does not exist
- [ ] Added packages are correctly identified as packages in the right SBOM not in the left
- [ ] Removed packages are correctly identified as packages in the left SBOM not in the right
- [ ] Version changes include correct left_version, right_version, and direction (upgrade/downgrade)
- [ ] New vulnerabilities include advisories affecting the right SBOM that do not affect the left
- [ ] Resolved vulnerabilities include advisories affecting the left SBOM that do not affect the right
- [ ] License changes identify packages whose license differs between the two SBOMs
- [ ] Severity field is populated for all vulnerability entries

## Test Requirements
- [ ] Integration test: compare two SBOMs where the right has additional packages — verify added_packages contains them
- [ ] Integration test: compare two SBOMs where the left has packages not in the right — verify removed_packages contains them
- [ ] Integration test: compare two SBOMs with a shared package at different versions — verify version_changes and direction
- [ ] Integration test: compare two SBOMs where the right introduces a new advisory — verify new_vulnerabilities
- [ ] Integration test: compare two SBOMs where the left has an advisory resolved in the right — verify resolved_vulnerabilities
- [ ] Integration test: compare two SBOMs where a shared package has a different license — verify license_changes
- [ ] Integration test: request with missing left or right param returns 400
- [ ] Integration test: request with non-existent SBOM ID returns 404
- [ ] All tests follow the `assert_eq!(resp.status(), StatusCode::OK)` pattern used in `tests/api/sbom.rs`

## Verification Commands
- `cargo test --test sbom_compare` — all comparison integration tests pass
- `cargo clippy -- -D warnings` — no warnings

## Documentation Updates
- `README.md` — add the comparison endpoint to the API endpoint listing if one exists

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
