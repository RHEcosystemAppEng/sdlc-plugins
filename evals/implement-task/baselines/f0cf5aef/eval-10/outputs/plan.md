# Implementation Plan for TC-9208

## Summary

Add a REST endpoint `GET /api/v2/sbom/{id}/license-summary` that returns a categorized
summary of package licenses within an SBOM, grouped by type (permissive, copyleft, unknown)
with counts and deduplicated license identifier lists.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/mod.rs`

**Change:** Register the new `license_summary` route in the endpoint module.

- Add `pub mod license_summary;` to the module declarations.
- In the route registration function (following the pattern used by `list.rs` and
  similar siblings), add a `.route("/api/v2/sbom/:id/license-summary", get(license_summary::handler))` call
  to the router builder.
- Follow the existing pattern visible in `modules/fundamental/src/sbom/endpoints/mod.rs`
  and `modules/fundamental/src/advisory/endpoints/mod.rs` for how routes are registered.

### 2. `modules/fundamental/src/package/model/mod.rs`

**Change:** Add `pub mod license_summary;` to expose the new model module.

- Insert the module declaration alongside the existing `pub mod summary;` line.
- No other changes needed in this file.

## Files to Create

### 3. `modules/fundamental/src/package/model/license_summary.rs`

**Purpose:** Define the `LicenseSummary` response struct.

**Contents:**
- Define a `LicenseCategory` struct with fields:
  - `count: usize` -- number of deduplicated licenses in this category
  - `licenses: Vec<String>` -- list of specific license identifiers (SPDX IDs)
- Define a `LicenseSummary` struct with fields:
  - `permissive: LicenseCategory`
  - `copyleft: LicenseCategory`
  - `unknown: LicenseCategory`
- Derive `Serialize`, `Deserialize`, `Debug`, `Clone` on both structs (following sibling
  model pattern from `summary.rs` and `details.rs`).
- Add doc comments on both structs explaining their purpose.
- Include a constructor or `From` impl that takes raw license data and categorizes it:
  - Permissive licenses: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, Unlicense, etc.
  - Copyleft licenses: GPL-2.0, GPL-3.0, LGPL-2.1, LGPL-3.0, AGPL-3.0, MPL-2.0, etc.
  - Unknown: any license identifier not in the permissive or copyleft lists.
- Deduplication: use a `HashSet` or `BTreeSet` to ensure each license identifier appears
  only once per category. Set `count` to the length of the deduplicated list.

### 4. `modules/fundamental/src/package/endpoints/license_summary.rs`

**Purpose:** GET handler for `/api/v2/sbom/{id}/license-summary`.

**Contents:**
- Follow the existing endpoint pattern from `modules/fundamental/src/package/endpoints/list.rs`
  and `modules/fundamental/src/sbom/endpoints/get.rs`.
- Handler signature: `async fn handler(Path(id): Path<Uuid>, State(db): State<DatabaseConnection>) -> Result<Json<LicenseSummary>, AppError>`
- Implementation:
  1. Query for the SBOM by `id` -- return 404 (`AppError::NotFound`) if it does not exist.
  2. JOIN `sbom_package` and `package_license` entities to get all licenses for packages
     in this SBOM. Use the `package_license` entity from `entity/src/package_license.rs`.
  3. Categorize each license identifier into permissive, copyleft, or unknown.
  4. Deduplicate within each category.
  5. Construct and return the `LicenseSummary` response.
- Error handling: wrap database errors with `.context("Failed to fetch license summary")`
  following the `Result<T, AppError>` pattern from `common/src/error.rs`.
- Add a doc comment on the handler function.

### 5. `tests/api/package_license.rs`

**Purpose:** Integration tests for the license summary endpoint.

**Contents:** See `test-plan.md` for detailed test approach.

- Register the test module in `tests/api/` (may require adding `mod package_license;`
  to a `tests/api/mod.rs` or ensuring the test runner discovers it via `Cargo.toml`).
- Follow the sibling test structure from `tests/api/sbom.rs` and `tests/api/advisory.rs`
  for test setup, database initialization, and HTTP client configuration.
- Four test functions corresponding to the four test requirements.
- Use value-based assertions per skill guidance (see `test-plan.md` for details).

## Data Flow Trace

1. **Input:** HTTP GET request to `/api/v2/sbom/{id}/license-summary` with SBOM UUID path parameter.
2. **Processing:**
   - Axum extracts the `id` from the path.
   - Handler validates SBOM existence via database query.
   - Handler queries `sbom_package` JOIN `package_license` to retrieve all license identifiers.
   - Licenses are categorized and deduplicated in-memory using the `LicenseSummary` model.
3. **Output:** JSON response with categorized license data, or 404 error response.

All three stages are connected. No persistence or side effects beyond the read query.

## Dependencies

- No external dependencies to add. The `entity` crate (containing `package_license`)
  is already a dependency of `modules/fundamental` (visible in the repository structure).
- SeaORM query builders from `common/src/db/query.rs` are available for JOIN construction.

## Scope

Changes are strictly limited to the five files listed above. No modifications to
`server/main.rs` are needed if `modules/fundamental/src/package/endpoints/mod.rs` already
handles route mounting (following the existing pattern where each module's endpoint mod
registers its own routes and the server mounts all modules).
