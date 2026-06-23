## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Create the data model structs for the SBOM comparison diff response. These structs define the shape of the comparison result returned by the new endpoint, covering all six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add module declarations for the new comparison model

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — define `SbomComparisonDiff`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, and `LicenseChange` structs with `serde::Serialize` derives

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/`. The `SbomDetails` struct in `modules/fundamental/src/sbom/model/details.rs` and `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` demonstrate the conventions for deriving `Serialize`, `Deserialize`, and `utoipa::ToSchema`.

Each sub-struct should include the fields matching the API response shape from the feature description:
- `AddedPackage` / `RemovedPackage`: `name`, `version`, `license`, `advisory_count`
- `VersionChange`: `name`, `left_version`, `right_version`, `direction` (enum: upgrade/downgrade)
- `NewVulnerability` / `ResolvedVulnerability`: `advisory_id`, `severity`, `title`, `affected_package` / `previously_affected_package`
- `LicenseChange`: `name`, `left_license`, `right_license`

Reuse existing types where applicable — `PackageSummary` in `modules/fundamental/src/package/model/summary.rs` has `license` field conventions, and `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` has `severity` field conventions.

Per CONVENTIONS.md §Module pattern: follow `model/ + service/ + endpoints/` structure.
Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's Rust module file scope.

Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the convention's Rust module file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — pattern for struct layout and serde derives
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity field type and serialization pattern
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — license field type convention

## Acceptance Criteria
- [ ] `SbomComparisonDiff` struct contains all six diff category vectors
- [ ] All sub-structs have correct fields matching the API response shape
- [ ] All structs derive `Serialize`, `Deserialize`, and `utoipa::ToSchema`
- [ ] Module compiles without errors (`cargo check -p trustify-fundamental`)

## Test Requirements
- [ ] Unit test in `comparison.rs` verifies `SbomComparisonDiff` serializes to the expected JSON shape
- [ ] Unit test verifies `VersionChange.direction` enum serializes as lowercase strings ("upgrade", "downgrade")

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental -- comparison` — model tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch

sha256-md:b5bbdf97608fec0994fa1e997d4bf2377066bd8eea6230521d53809358275df4
