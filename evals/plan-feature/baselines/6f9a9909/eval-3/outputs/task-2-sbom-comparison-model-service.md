## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison model types and diff service that computes structured differences between two SBOMs. The service queries existing package, advisory, and license data to produce a comparison result containing added/removed packages, version changes, new/resolved vulnerabilities, and license changes. This provides the business logic foundation for the comparison endpoint (Task 3).

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new comparison model types
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare` method to `SbomService`
- `modules/fundamental/src/sbom/service/mod.rs` — re-export comparison service types if needed

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — define `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` structs

## API Changes
- None (this task adds the service layer; the endpoint is added in Task 3)

## Implementation Notes
Follow the existing module pattern in `modules/fundamental/src/sbom/` where model types are defined in `model/` and service logic in `service/`. Use the existing `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` as the home for the `compare` method.

The comparison logic should:
1. Fetch packages for both SBOMs using the existing `PackageService` (`modules/fundamental/src/package/service/mod.rs`)
2. Fetch advisories for both SBOMs using the existing `AdvisoryService` (`modules/fundamental/src/advisory/service/advisory.rs`)
3. Compute set differences for added/removed packages
4. Compare versions for shared packages to produce version changes
5. Compute advisory differences to produce new/resolved vulnerabilities
6. Compare license fields on packages to produce license changes

The response must match the JSON shape specified in the Figma design context:
```json
{
  "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
  "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
  "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade" }],
  "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..." }],
  "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
  "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
}
```

Per the non-functional requirements, the comparison must be computed on-the-fly from existing package and advisory data (no new database tables). Target p95 < 1s for SBOMs with up to 2000 packages each.

Per CONVENTIONS.md (Key Conventions) -- Error handling: all service methods should return `Result<T, AppError>` with `.context()` wrapping for error context.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` service file scope.

Per CONVENTIONS.md (Key Conventions) -- Module pattern: each domain module follows `model/ + service/ + endpoints/` structure.
Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's `.rs` module file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM model struct; follow the same serialization pattern for comparison result types
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — existing detail model; reference for struct field conventions
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains `license` field; reuse for package data in comparison
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains `severity` field; reuse for vulnerability data in comparison
- `common/src/error.rs::AppError` — shared error type; use for error returns

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct defined with all six diff categories: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] `SbomService::compare(left_id, right_id)` method implemented and returns `Result<SbomComparisonResult, AppError>`
- [ ] Comparison correctly identifies added packages (in right but not left)
- [ ] Comparison correctly identifies removed packages (in left but not right)
- [ ] Comparison correctly identifies version changes with upgrade/downgrade direction
- [ ] Comparison correctly identifies new vulnerabilities (advisories affecting right but not left)
- [ ] Comparison correctly identifies resolved vulnerabilities (advisories affecting left but not right)
- [ ] Comparison correctly identifies license changes between the same package in both SBOMs
- [ ] All model types derive `Serialize` for JSON serialization
- [ ] Error handling uses `Result<T, AppError>` with `.context()` wrapping

## Test Requirements
- [ ] Unit test: comparison of two SBOMs with known package differences returns correct added/removed sets
- [ ] Unit test: comparison detects version upgrades and downgrades correctly
- [ ] Unit test: comparison correctly identifies new and resolved vulnerabilities
- [ ] Unit test: comparison correctly identifies license changes
- [ ] Unit test: comparison with identical SBOMs returns empty diff in all categories
- [ ] Unit test: comparison with non-existent SBOM ID returns appropriate error

## Verification Commands
- `cargo test -p trustify-fundamental -- sbom::service::compare` — tests pass for comparison service
- `cargo check -p trustify-fundamental` — no compilation errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
