# Implementation Plan: TC-9208 -- Add Package License Summary Endpoint

## Task Summary

Add a REST endpoint `GET /api/v2/sbom/{id}/license-summary` that aggregates package
licenses within an SBOM by type (permissive, copyleft, unknown) and returns counts
plus deduplicated license identifier lists for each category.

## Project Configuration Validation

The mock CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend with serena_backend instance
- Jira Configuration: Project key TC, Cloud ID, Feature/PR/GitHub Issue fields
- Code Intelligence: serena_backend with rust-analyzer

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/mod.rs`

**What**: Register the new `/api/v2/sbom/{id}/license-summary` route.

**How**: Add `pub mod license_summary;` declaration and register the route in the
router builder function. Follow the pattern used by sibling endpoint modules
(`list.rs`, and the equivalent `get.rs` in the `sbom/endpoints/` directory) for
route registration syntax. The route mounts a GET handler pointing to
`license_summary::handler`.

### 2. `modules/fundamental/src/package/model/mod.rs`

**What**: Add `pub mod license_summary;` to expose the new model module.

**How**: Add a single line `pub mod license_summary;` following the pattern of
existing module declarations (e.g., `pub mod summary;` is already present).

## Files to Create

### 3. `modules/fundamental/src/package/model/license_summary.rs`

**What**: Define the `LicenseSummary` response struct and its nested category struct.

**How**:
- Define a `LicenseCategory` struct with fields:
  - `count: usize` -- number of unique licenses in this category
  - `licenses: Vec<String>` -- deduplicated license identifiers
- Define a `LicenseSummary` struct with fields:
  - `permissive: LicenseCategory`
  - `copyleft: LicenseCategory`
  - `unknown: LicenseCategory`
- Derive `Serialize`, `Deserialize`, `Debug`, `Clone` on both structs (matching
  sibling model patterns in `summary.rs`, `details.rs`).
- Add doc comments on both structs explaining their purpose.
- Implement a constructor or `From` trait to build `LicenseSummary` from a list of
  raw license strings, classifying each license into the appropriate category. The
  classification logic maps well-known SPDX identifiers (MIT, Apache-2.0, BSD-*,
  ISC, etc.) to "permissive", copyleft identifiers (GPL-*, LGPL-*, AGPL-*, MPL-*,
  EUPL-*, CPAL-*, OSL-*) to "copyleft", and all others to "unknown".
- Deduplicate licenses within each category using a `HashSet` before converting to
  `Vec<String>`.

### 4. `modules/fundamental/src/package/endpoints/license_summary.rs`

**What**: Implement the GET handler for `/api/v2/sbom/{id}/license-summary`.

**How**:
- Follow the existing endpoint pattern from `list.rs` (sibling in same directory).
- Define an async handler function `handler` taking:
  - `Path(id)` -- the SBOM ID from the URL
  - Database connection / state extractor (matching sibling handler signatures)
- Query logic:
  1. Verify the SBOM exists by querying the `sbom` entity. If not found, return
     `Err(AppError::NotFound(...).context("SBOM not found"))`.
  2. Query `sbom_package` JOIN `package_license` WHERE `sbom_id = id` to get all
     license strings for packages in this SBOM.
  3. Use the `package_license` entity from `entity/src/package_license.rs` for the
     JOIN (as specified in Implementation Notes).
  4. Classify and deduplicate licenses using the `LicenseSummary` model.
- Return `Ok(Json(license_summary))`.
- Error handling: use `Result<Json<LicenseSummary>, AppError>` with `.context()`
  wrapping on all fallible operations (matching project conventions).
- Add doc comment on the handler function.

### 5. `tests/api/package_license.rs`

**What**: Integration tests for the license summary endpoint.

**How**: See test-plan.md for detailed assertion approach. Four test functions:
1. `test_license_summary_valid_sbom` -- valid SBOM with known licenses returns correct counts and identifiers
2. `test_license_summary_not_found` -- non-existent SBOM ID returns 404
3. `test_license_summary_empty_sbom` -- SBOM with no packages returns all zeros and empty lists
4. `test_license_summary_deduplication` -- duplicate licenses within a category are counted once

Follow sibling test file patterns (`advisory.rs`, `sbom.rs`) for structure, imports,
test database setup, and HTTP client usage. Deviate on assertion style per skill
guidance (see conventions.md for the conflict and resolution).

## Data Flow Trace

1. **Input**: HTTP GET request to `/api/v2/sbom/{id}/license-summary`
2. **Validation**: SBOM existence check via `sbom` entity query
3. **Processing**: JOIN query `sbom_package` + `package_license`, classification into
   permissive/copyleft/unknown, deduplication via HashSet
4. **Output**: JSON response with `LicenseSummary` struct serialized

All stages are connected. The 404 error path is also complete (SBOM not found
returns AppError immediately).

## Out-of-Scope Considerations

- `server/src/main.rs` may need a route mount change if the package module's routes
  are not already mounted. If the package endpoints module is already registered in
  the server's route tree (which it should be given `list.rs` already exists), no
  change is needed. If a change is needed, it would be flagged in Step 9's scope
  containment check.
- `tests/Cargo.toml` may need updating if the test file requires new dependencies.
  This would also be flagged during scope containment.
- No OpenAPI spec file is listed in the repo structure, so no spec update is planned.
