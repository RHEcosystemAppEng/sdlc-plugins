# Implementation Plan -- TC-9208

## Overview

Add a REST endpoint `GET /api/v2/sbom/{id}/license-summary` that returns a summary
of license types for packages within an SBOM, categorized as permissive, copyleft,
or unknown, with counts and deduplicated license identifier lists.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/mod.rs`

**What**: Register the new license-summary route in the package endpoints router.

**Changes**:
- Add `mod license_summary;` declaration to import the new endpoint module.
- Add a `.route("/api/v2/sbom/:id/license-summary", get(license_summary::get_license_summary))`
  call in the router builder function, following the same pattern used by sibling
  route registrations (e.g., `list.rs`, `get.rs` in the `sbom/endpoints/` module).

### 2. `modules/fundamental/src/package/model/mod.rs`

**What**: Expose the new `license_summary` model module.

**Changes**:
- Add `pub mod license_summary;` declaration so the `LicenseSummary` response
  struct is accessible from the endpoints module and from tests.

## Files to Create

### 3. `modules/fundamental/src/package/model/license_summary.rs`

**What**: Define the `LicenseSummary` response struct and its nested types.

**Contents**:
- `LicenseCategoryDetail` struct with fields:
  - `count: usize` -- number of deduplicated licenses in this category
  - `licenses: Vec<String>` -- deduplicated list of license identifiers (e.g., "MIT", "GPL-3.0")
- `LicenseSummary` struct with fields:
  - `permissive: LicenseCategoryDetail`
  - `copyleft: LicenseCategoryDetail`
  - `unknown: LicenseCategoryDetail`
- Both structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`.
- Documentation comments on both structs explaining their purpose.
- A helper function `categorize_license(license_id: &str) -> LicenseCategory` that
  maps known SPDX identifiers to categories. Known permissive licenses include MIT,
  Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, etc. Known copyleft licenses include
  GPL-2.0, GPL-3.0, LGPL-2.1, LGPL-3.0, AGPL-3.0, MPL-2.0, etc. Everything else
  maps to unknown.
- A builder function `build_summary(licenses: Vec<String>) -> LicenseSummary` that
  takes a flat list of license identifiers, deduplicates them, categorizes each, and
  produces the summary struct.

### 4. `modules/fundamental/src/package/endpoints/license_summary.rs`

**What**: GET handler for `/api/v2/sbom/{id}/license-summary`.

**Contents**:
- `use` imports for Axum extractors (`Path`), the `AppError` type from
  `common/src/error.rs`, the `LicenseSummary` model, and the SeaORM entity
  types from `entity/src/package_license.rs`, `entity/src/sbom_package.rs`,
  `entity/src/sbom.rs`.
- Handler function signature:
  ```rust
  pub async fn get_license_summary(
      Path(sbom_id): Path<Uuid>,
      db: Extension<DatabaseConnection>,
  ) -> Result<Json<LicenseSummary>, AppError>
  ```
- Implementation:
  1. Query the `sbom` table to verify the SBOM exists; return 404 (`AppError::NotFound`)
     with `.context("SBOM not found")` if absent.
  2. JOIN `sbom_package` and `package_license` to retrieve all license identifiers
     for packages in the given SBOM.
  3. Call `build_summary()` on the collected license identifiers.
  4. Return `Json(summary)`.
- Follow the existing endpoint pattern from `modules/fundamental/src/package/endpoints/list.rs`
  for error handling (`Result<T, AppError>` with `.context()` wrapping) and Axum extractor usage.
- Documentation comment on the handler function.

### 5. `tests/api/package_license.rs`

**What**: Integration tests for the license-summary endpoint.

**Contents**: See test-plan.md for detailed test assertions. Structurally:
- Follow sibling test file organization from `tests/api/sbom.rs` and `tests/api/advisory.rs`
  for setup/teardown, test database bootstrapping, and HTTP client creation.
- Four test functions covering all Test Requirements from the task description.
- Each test function has a `///` documentation comment.
- Non-trivial tests use `// Given` / `// When` / `// Then` section comments.
- Also add `mod package_license;` to `tests/api/mod.rs` (or the test harness entry
  point) if that file exists — verify by inspecting the `tests/` directory structure.

## Dependency and Integration Notes

- **Entity reuse**: The `package_license` entity already exists at `entity/src/package_license.rs`.
  No new entity or migration is needed.
- **No new crate dependencies**: The implementation uses existing SeaORM and Axum types
  already in `Cargo.toml`.
- **Route mounting**: The package endpoints module is already mounted in `server/src/main.rs`
  via the module hierarchy; adding a route inside `package/endpoints/mod.rs` is sufficient.

## Data-Flow Trace

1. **Input**: HTTP GET request to `/api/v2/sbom/{id}/license-summary` with a UUID path parameter.
2. **Validation**: Handler extracts `sbom_id` from path, queries `sbom` table to verify existence (404 if not found).
3. **Processing**: JOIN query across `sbom_package` and `package_license` tables retrieves license identifiers. `build_summary()` deduplicates and categorizes them.
4. **Output**: JSON response with `LicenseSummary` struct containing three categories, each with count and license list.

All stages are connected; no incomplete paths.
