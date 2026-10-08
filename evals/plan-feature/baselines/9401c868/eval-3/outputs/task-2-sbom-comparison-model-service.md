## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the data model types and diff service for SBOM comparison. This task introduces the response structs for the comparison endpoint and the core diffing logic that computes added/removed packages, version changes, new/resolved vulnerabilities, and license changes between two SBOMs. The diff is computed on-the-fly from existing package, advisory, and license data without requiring new database tables.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- re-export the new comparison module
- `modules/fundamental/src/sbom/service/mod.rs` -- re-export the new compare module
- `modules/fundamental/src/sbom/service/sbom.rs` -- add helper methods to SbomService for fetching packages and advisories by SBOM ID for diffing

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` -- define SbomComparison, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, and LicenseChange structs with Serialize derives
- `modules/fundamental/src/sbom/service/compare.rs` -- implement SbomCompareService with a `compare(left_id, right_id)` method that fetches both SBOMs' packages/advisories and computes the structured diff

## Implementation Notes
- Follow the existing module pattern: model types in `model/` and business logic in `service/`. See `modules/fundamental/src/sbom/model/summary.rs` for struct conventions (derive Serialize, field naming).
- The comparison response shape must match the contract specified in the feature:
  ```json
  {
    "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade|downgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "affected_package": "..." }],
    "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
    "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
  }
  ```
- Use `Result<T, AppError>` for all service methods, with `.context()` wrapping for database errors. See `common/src/error.rs` for the AppError enum.
- Query packages via the `sbom_package` join table (`entity/src/sbom_package.rs`) and get license data from `package_license` (`entity/src/package_license.rs`).
- Query advisories via the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) and get severity from `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`).
- Version comparison for upgrade/downgrade direction: use semver parsing when possible; fall back to string comparison.
- NFR: the diff must be computed in-memory without new database tables. Use SeaORM queries to fetch both sets and compute the diff in Rust.
- NFR: target p95 < 1s for SBOMs with up to 2000 packages each. Use efficient set operations (HashMaps keyed by package name) rather than nested loops.
- Per CONVENTIONS.md §Module pattern: follow the model/ + service/ + endpoints/ structure for the new comparison module.
  Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's `.rs` module file scope.
- Per CONVENTIONS.md §Error handling: use `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- existing service with fetch and list methods; extend with helper methods for retrieving packages/advisories per SBOM
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- existing package struct with `license` field; use as the source type for comparison
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- existing advisory struct with `severity` field; use for vulnerability diff entries
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination; reuse for efficient package/advisory lookups
- `entity/src/sbom_package.rs` -- SBOM-Package join table entity; use for querying packages belonging to each SBOM
- `entity/src/sbom_advisory.rs` -- SBOM-Advisory join table entity; use for querying advisories linked to each SBOM

## Acceptance Criteria
- [ ] `SbomComparison` struct is defined with all six diff categories: added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes
- [ ] Each diff category has a dedicated struct with the correct fields matching the API contract
- [ ] `SbomCompareService::compare(left_id, right_id)` computes the correct diff between two SBOMs
- [ ] Added packages: packages in right SBOM not in left are identified
- [ ] Removed packages: packages in left SBOM not in right are identified
- [ ] Version changes: packages in both SBOMs with different versions are identified with upgrade/downgrade direction
- [ ] New vulnerabilities: advisories affecting right SBOM but not left are identified with severity
- [ ] Resolved vulnerabilities: advisories affecting left SBOM but not right are identified
- [ ] License changes: packages whose license changed between SBOMs are identified
- [ ] All methods return `Result<T, AppError>`

## Test Requirements
- [ ] Unit test: compare two SBOMs with known packages produces correct added/removed sets
- [ ] Unit test: compare SBOMs with overlapping packages but different versions produces correct version_changes with direction
- [ ] Unit test: compare SBOMs with different advisory sets produces correct new/resolved vulnerability entries
- [ ] Unit test: compare SBOMs with license changes produces correct license_changes entries
- [ ] Unit test: comparing an SBOM with itself produces empty diff (all categories empty)
- [ ] Unit test: performance with 2000 packages per SBOM completes within acceptable time

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
