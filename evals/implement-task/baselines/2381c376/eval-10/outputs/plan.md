# Implementation Plan for TC-9208

## Summary

Add a REST endpoint `GET /api/v2/sbom/{id}/license-summary` that returns categorized
license counts (permissive, copyleft, unknown) for packages within an SBOM.

## Project Configuration Validation

- Repository Registry: present (trustify-backend, Serena instance: serena_backend)
- Jira Configuration: present (Project key: TC, Cloud ID, Feature issue type ID)
- Code Intelligence: present (serena_backend with rust-analyzer)

All prerequisites satisfied.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/mod.rs`

**Change**: Register the new license summary route.

- Use `get_symbols_overview` via `mcp__serena_backend__get_symbols_overview` to inspect
  the current route registration pattern.
- Add a `pub mod license_summary;` declaration.
- Add the license summary route to the router builder, following the existing pattern
  from sibling endpoint registrations (e.g., how `list.rs` is registered).
- The route should be mounted at `/api/v2/sbom/{id}/license-summary` as a GET handler.

### 2. `modules/fundamental/src/package/model/mod.rs`

**Change**: Add `pub mod license_summary;` to expose the new model module.

- Use `get_symbols_overview` to inspect the current module declarations.
- Add the module declaration following the existing pattern (alphabetical ordering if
  that is the convention, or positional ordering matching siblings like `summary.rs`).

## Files to Create

### 3. `modules/fundamental/src/package/model/license_summary.rs`

**Purpose**: Define the `LicenseSummary` response struct.

**Contents**:
- A `LicenseCategoryDetail` struct with fields:
  - `count: usize` -- number of deduplicated licenses in this category
  - `licenses: Vec<String>` -- list of specific license identifiers
- A `LicenseSummary` struct with fields:
  - `permissive: LicenseCategoryDetail`
  - `copyleft: LicenseCategoryDetail`
  - `unknown: LicenseCategoryDetail`
- Both structs derive `Serialize`, `Deserialize`, `Debug`, `Clone` and implement
  `utoipa::ToSchema` (following sibling model patterns like `summary.rs`).
- Documentation comments on every struct and field.
- A helper method or function to classify a license identifier string into one of the
  three categories (permissive, copyleft, unknown). This would use a known list of
  SPDX identifiers for classification, with `unknown` as the fallback.
- A constructor or `from_licenses` method that takes a list of license strings,
  deduplicates them, classifies each, and produces a `LicenseSummary`.

**Patterns to follow**: Reference `modules/fundamental/src/package/model/summary.rs`
(PackageSummary) for struct derivations, serde annotations, and documentation style.

### 4. `modules/fundamental/src/package/endpoints/license_summary.rs`

**Purpose**: GET handler for `/api/v2/sbom/{id}/license-summary`.

**Contents**:
- An async handler function `get_license_summary` that:
  1. Extracts the SBOM ID from the path parameter.
  2. Queries the database using the `package_license` entity
     (`entity/src/package_license.rs`) joined with `sbom_package`
     (`entity/src/sbom_package.rs`) to find all licenses for packages in the given SBOM.
  3. Returns 404 (`AppError`) if the SBOM ID does not exist -- check SBOM existence
     first using the pattern from `get.rs` in the SBOM endpoints.
  4. Deduplicates and classifies licenses into the three categories.
  5. Returns `Json<LicenseSummary>` wrapped in `Result<_, AppError>`.
- Error handling uses `Result<T, AppError>` with `.context()` wrapping, per project
  conventions and Implementation Notes.
- The handler follows the pattern in
  `modules/fundamental/src/package/endpoints/list.rs` for database access, error
  handling, and response construction.

**Patterns to follow**: Reference `modules/fundamental/src/sbom/endpoints/get.rs` for
single-resource GET handler pattern, and `list.rs` for query patterns.

### 5. `tests/api/package_license.rs`

**Purpose**: Integration tests for the new endpoint.

**Contents**: See `outputs/test-plan.md` for detailed test approach.

**Structural conventions to follow** (from sibling tests `tests/api/advisory.rs`,
`tests/api/sbom.rs`):
- Test function naming: `test_<noun>_<scenario>`
- Setup: use the shared test database setup pattern from siblings
- HTTP client: use the same test HTTP client pattern as siblings
- Module registration: add `mod package_license;` to `tests/api/mod.rs` or the test
  crate root if that is how siblings are organized

## Data-Flow Trace

1. **Input**: HTTP GET request to `/api/v2/sbom/{id}/license-summary` with SBOM ID path param
2. **Processing**:
   - Validate SBOM exists (query `sbom` entity) -> 404 if not found
   - JOIN `sbom_package` + `package_license` to get all licenses for packages in the SBOM
   - Deduplicate license identifiers
   - Classify each into permissive/copyleft/unknown
   - Count per category
3. **Output**: JSON response with `LicenseSummary` struct (three categories, each with count + license list)

All stages are connected. No incomplete paths.

## Scope Containment

Changes are strictly limited to the files listed in Files to Modify and Files to Create.
If `tests/api/mod.rs` or similar test registration file needs updating to include the
new test module, that would be flagged as an out-of-scope file for user approval in
Step 9.

## CI Verification

- Check for `CONVENTIONS.md` at repository root and extract CI commands.
- Run `cargo test -p trustify-fundamental` (or the correct crate name from
  `cargo metadata`) to verify the implementation compiles and tests pass.
- Run any formatting/linting commands from CONVENTIONS.md.
