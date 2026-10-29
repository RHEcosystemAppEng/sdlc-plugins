# Implementation Plan: TC-9208

## Summary

Add a REST endpoint `GET /api/v2/sbom/{id}/license-summary` that returns categorized
license counts (permissive, copyleft, unknown) with deduplicated license identifier
lists for packages within a given SBOM.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/mod.rs`

**Change:** Register the new `license_summary` route in the existing route builder.

- Add `mod license_summary;` to import the new endpoint module.
- In the route registration function (following the pattern used by `list.rs` and other
  endpoints in sibling modules like `sbom/endpoints/mod.rs`), add a `.route()` call for
  `GET /api/v2/sbom/:id/license-summary` pointing to the handler in `license_summary.rs`.

### 2. `modules/fundamental/src/package/model/mod.rs`

**Change:** Add `pub mod license_summary;` to expose the new response model module.

- Add a single line `pub mod license_summary;` alongside existing model module
  declarations (e.g., `pub mod summary;`).

## Files to Create

### 3. `modules/fundamental/src/package/model/license_summary.rs`

**Purpose:** Define the `LicenseSummary` response struct.

**Contents:**
- A `LicenseCategory` struct with fields:
  - `count: usize` -- number of deduplicated licenses in this category
  - `licenses: Vec<String>` -- sorted, deduplicated list of license identifiers
- A `LicenseSummary` struct with fields:
  - `permissive: LicenseCategory`
  - `copyleft: LicenseCategory`
  - `unknown: LicenseCategory`
- Both structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`, `PartialEq`, `Eq`
  following sibling model patterns (`summary.rs`, `details.rs` in the same module).
- Doc comments on both structs explaining their purpose, following the skill's
  requirement for documentation on all new public symbols.

### 4. `modules/fundamental/src/package/endpoints/license_summary.rs`

**Purpose:** GET handler for `/api/v2/sbom/{id}/license-summary`.

**Contents:**
- An async handler function `get_license_summary(Path(sbom_id): Path<Uuid>, State(db): State<DatabaseConnection>) -> Result<Json<LicenseSummary>, AppError>`.
- Query logic:
  1. Verify the SBOM exists by querying the `sbom` entity; return 404 (`AppError::NotFound`) if absent.
  2. JOIN `sbom_package` with `package_license` to get all licenses for packages in the given SBOM.
  3. Classify each license identifier into permissive, copyleft, or unknown using a classification function (a simple match on well-known SPDX identifiers; MIT, Apache-2.0, BSD-* -> permissive; GPL-*, LGPL-*, AGPL-* -> copyleft; everything else -> unknown).
  4. Deduplicate licenses within each category using `HashSet` or `.collect::<BTreeSet<_>>()`.
  5. Build and return the `LicenseSummary` response.
- Error handling: `Result<T, AppError>` with `.context()` wrapping on database operations, following the established pattern from `list.rs` and sibling endpoint files.
- Doc comment on the handler function.

### 5. `tests/api/package_license.rs`

**Purpose:** Integration tests for the license summary endpoint.

**Contents:** Four test functions covering all Test Requirements (see `test-plan.md`
for assertion approach details). Tests use value-based assertions (`assert_eq!` on
specific values) per skill guidance, not the `.filter().any()` / `.count() > 0` pattern
found in sibling tests. See `conventions.md` for conflict analysis.

- `test_license_summary_with_known_packages` -- verifies correct categorization and counts
- `test_license_summary_sbom_not_found` -- verifies 404 response
- `test_license_summary_empty_sbom` -- verifies zero counts with empty lists
- `test_license_summary_deduplication` -- verifies duplicate licenses counted once

Test file follows sibling conventions for module structure, imports, test database
setup/teardown, and naming (see `conventions.md`).

## Module Registration

The new endpoint module (`license_summary.rs`) must be registered in
`modules/fundamental/src/package/endpoints/mod.rs`. No changes to `server/main.rs`
are needed because the package module is already mounted there.

## Out-of-Scope

No files outside the listed Files to Modify and Files to Create will be changed.
If the license classification logic grows complex enough to warrant a shared utility,
that would be flagged in Step 9's scope containment check for user approval rather
than added unilaterally.
