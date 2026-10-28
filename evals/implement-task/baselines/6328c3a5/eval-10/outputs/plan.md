# Implementation Plan for TC-9208

## Task Summary

Add a REST endpoint `GET /api/v2/sbom/{id}/license-summary` that returns a summary of
license types for packages within an SBOM, categorized as permissive, copyleft, or
unknown, with counts and deduplicated license identifier lists.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/mod.rs`

**Change:** Register the new `/api/v2/sbom/{id}/license-summary` route.

- Add `pub mod license_summary;` to the module declarations.
- In the route registration function, add a `.route("/api/v2/sbom/:id/license-summary", get(license_summary::get_license_summary))` entry, following the same pattern used by `list.rs` route registration.

### 2. `modules/fundamental/src/package/model/mod.rs`

**Change:** Declare the new `license_summary` submodule.

- Add `pub mod license_summary;` to the existing module declarations, matching the style of the existing `pub mod summary;` declaration.

## Files to Create

### 3. `modules/fundamental/src/package/model/license_summary.rs`

**Purpose:** Define the `LicenseSummary` response struct.

**Contents:**
- A `LicenseCategory` struct with fields:
  - `count: usize` -- number of deduplicated licenses in this category
  - `licenses: Vec<String>` -- deduplicated list of license identifiers (e.g., "MIT", "Apache-2.0")
- A `LicenseSummary` struct with fields:
  - `permissive: LicenseCategory`
  - `copyleft: LicenseCategory`
  - `unknown: LicenseCategory`
- Both structs derive `Serialize`, `Deserialize`, `Debug`, `Clone` and implement `utoipa::ToSchema` for OpenAPI spec generation (following the sibling `summary.rs` pattern).
- A helper function or method to classify a license string into one of the three categories. This would use a known list of permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, etc.) and copyleft licenses (GPL-2.0, GPL-3.0, LGPL-2.1, LGPL-3.0, AGPL-3.0, MPL-2.0, etc.), with everything else falling into "unknown".
- Documentation comments on each struct and public function following Rust `///` convention.

### 4. `modules/fundamental/src/package/endpoints/license_summary.rs`

**Purpose:** GET handler for `/api/v2/sbom/{id}/license-summary`.

**Contents:**
- Handler function `get_license_summary` accepting the SBOM ID as a path parameter, following the pattern in `list.rs` and `get.rs` endpoint handlers.
- Return type: `Result<Json<LicenseSummary>, AppError>` following the project's error handling convention with `.context()` wrapping.
- Implementation logic:
  1. Validate that the SBOM exists by querying the `sbom` entity; return 404 `AppError` if not found.
  2. Query the `sbom_package` join table to find all packages associated with the SBOM.
  3. Query the `package_license` entity to retrieve licenses for those packages.
  4. Deduplicate licenses within each category using a `HashSet` or `BTreeSet`.
  5. Classify each unique license into permissive, copyleft, or unknown.
  6. Build and return the `LicenseSummary` response with counts matching the length of each category's deduplicated license list.
- Use `PackageService` or direct SeaORM queries following the existing service pattern.
- Documentation comment on the handler function.

### 5. `tests/api/package_license.rs`

**Purpose:** Integration tests for the license summary endpoint.

**Contents:** (See `test-plan.md` for detailed assertion approach.)

- Four test functions matching the four test requirements from the task.
- Follow sibling test conventions for structure, naming, and setup/teardown (see `conventions.md`).
- Use value-based assertions per skill guidance (see `test-plan.md`).
- Each test function has a `///` documentation comment and given-when-then section comments.

## Dependencies and Integration Points

- **Entity layer:** Uses `package_license.rs` from `entity/src/` for the JOIN query -- no changes needed to the entity layer.
- **Common utilities:** Uses `AppError` from `common/src/error.rs` for error handling -- no changes needed.
- **Server mounting:** The route is registered within the package module's `endpoints/mod.rs`, which is already mounted by `server/main.rs` -- no changes needed to the server entry point.

## Out-of-Scope Considerations

- No changes to `entity/src/package_license.rs` (existing entity is sufficient).
- No changes to `server/main.rs` (package module is already mounted).
- No changes to `common/` (AppError and query helpers are already available).
- If the license classification logic grows complex enough to warrant a shared utility, it should live in the model file (`license_summary.rs`) rather than introducing a new module.
