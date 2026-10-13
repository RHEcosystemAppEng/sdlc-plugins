# Implementation Plan for TC-9206: Add SBOM supplier extraction to data migration

## Summary

The task requires adding supplier information extraction to the SBOM data migration step. The migration crate must extract describing packages and supplier information from ingested SBOMs to populate a new `sbom_supplier` table. The key implementation challenge is that the required extraction logic already exists as private helper functions in the ingestor module.

## Files to Modify

### 1. `modules/ingestor/src/graph/sbom/mod.rs`

**Current state:** Contains two private helper functions:
- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` -- extracts the list of packages that an SBOM describes
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` -- extracts supplier information from SBOM metadata

**Planned change:** Change the visibility of both functions from private to public:
- `fn describing_packages(...)` becomes `pub fn describing_packages(...)`
- `fn suppliers(...)` becomes `pub fn suppliers(...)`

No changes to the function bodies, signatures, or return types. The only modification is adding the `pub` visibility modifier. This makes them importable by any crate that depends on `trustify-module-ingestor`, which the migration crate already does.

Before making this change, use `find_referencing_symbols` (or Grep) to confirm that no existing callers are affected and that the functions' current internal callers continue to work correctly after the visibility change. Widening visibility from private to public is backward-compatible -- all existing call sites remain valid.

### 2. `migration/src/m0002_supplier/mod.rs`

**Planned changes:**
- Add import statements to bring in the newly public functions from the ingestor crate:
  ```rust
  use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
  ```
- Implement the supplier extraction migration logic that:
  1. Iterates over ingested SBOMs
  2. Calls `describing_packages(&sbom)` to get the packages each SBOM describes
  3. Calls `suppliers(&sbom)` to extract supplier information
  4. Inserts records into the `sbom_supplier` table linking SBOMs to their supplier data
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for structure, error handling, and database interaction conventions
- Add documentation comments on all new public functions and structs

The functions are imported and called directly -- their logic is NOT copied or inlined into this file.

## Files to Create

### 3. `migration/src/m0002_supplier/test.rs`

**Planned contents:**
- Unit tests for the supplier extraction migration step
- Test case: migration correctly extracts suppliers from a sample SBOM (construct a test SBOM with known supplier data, run the extraction, assert on specific supplier values)
- Test case: SBOMs with no suppliers produce no supplier records (construct a test SBOM with empty supplier data, run the extraction, assert the result is empty)
- Each test function will have a `///` documentation comment explaining what it verifies
- Non-trivial tests will use given-when-then section comments
- Assertions will check specific values, not just collection lengths

## How Private Functions Are Handled

The private functions `describing_packages()` and `suppliers()` in `modules/ingestor/src/graph/sbom/mod.rs` are made public (`pub fn`) so the migration crate can import and call them directly. This is the correct approach because:

1. The `migration/Cargo.toml` already declares a dependency on `trustify-module-ingestor` (`trustify-module-ingestor = { path = "../modules/ingestor" }`), so no new dependency is needed
2. The function bodies are NOT copied or inlined into the migration crate
3. The migration module imports the functions via `use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};`

This follows the SKILL.md Step 6 "Reuse over duplication" guidance: when the dependency already exists, make the function public and import it rather than duplicating the code.

## Module Registration

- Ensure `migration/src/m0002_supplier/test.rs` is declared as a test module in `migration/src/m0002_supplier/mod.rs` with `#[cfg(test)] mod test;`
- Ensure the `m0002_supplier` module is registered in `migration/src/lib.rs`
- Ensure the ingestor module's `mod.rs` re-exports the functions appropriately (the `pub` modifier on the functions in the file where they are defined is sufficient if the parent modules also have public visibility)

## Acceptance Criteria Verification

- The migration step extracts supplier information from all ingested SBOMs -- verified by calling the reused `describing_packages()` and `suppliers()` functions
- The extraction reuses the existing ingestor logic rather than duplicating it -- verified by the import-based approach (no function body duplication)
- The `sbom_supplier` table is populated correctly with supplier data -- verified by the migration logic and tests
