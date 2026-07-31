# Implementation Plan for TC-9206: Add SBOM supplier extraction to data migration

## Overview

Add supplier information extraction during the SBOM data migration step by reusing existing private helper functions from the ingestor crate rather than duplicating their logic.

## Files to Modify

### 1. `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make two private helper functions public so they can be imported by the migration crate.

- Change `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` to `pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- Change `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` to `pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`

No logic changes are needed in these functions. Only the visibility modifier changes from private to public. Add documentation comments (`///`) to both functions since they are becoming part of the public API, describing what each function extracts and from where.

If these functions are defined inside an `impl` block or a non-public module, also ensure the containing module path is publicly re-exported so that the migration crate can reach them via `trustify_module_ingestor::graph::sbom::{describing_packages, suppliers}` (or the appropriate module path).

### 2. `migration/src/m0002_supplier/mod.rs`

**Change**: Add supplier extraction logic to the migration step using the now-public ingestor functions.

- Add import statements for `describing_packages` and `suppliers` from `trustify_module_ingestor::graph::sbom` (or the appropriate module path based on the crate's public API structure).
- Implement the migration step logic:
  1. Query all ingested SBOMs from the database.
  2. For each SBOM, call `describing_packages(&sbom)` to extract the packages the SBOM describes.
  3. For each SBOM, call `suppliers(&sbom)` to extract supplier information.
  4. Insert the extracted supplier data into the `sbom_supplier` table.
- Follow the existing migration pattern from `m0001_initial/mod.rs` for transaction handling, error wrapping with `.context()`, and migration step structure.
- Handle SBOMs that have no supplier information gracefully (skip insertion, produce no records).

## Files to Create

### 3. `migration/src/m0002_supplier/test.rs`

**Change**: Create unit tests for the supplier extraction migration.

- **Test 1: `test_migration_extracts_suppliers_from_sbom`** -- Verify that the migration step correctly extracts suppliers from a sample SBOM and populates the `sbom_supplier` table. Create a test SBOM fixture with known supplier data, run the migration logic, and assert that the resulting supplier records match the expected values (not just the count).
- **Test 2: `test_migration_handles_sbom_without_suppliers`** -- Verify that SBOMs with no supplier information produce no supplier records. Create a test SBOM fixture with no suppliers, run the migration logic, and assert the result set is empty.
- Follow the project's test conventions: use `assert_eq!` for value-based assertions, add `///` documentation comments on each test function, and include given-when-then section comments for non-trivial tests.

## Additional Considerations

### Module registration

Ensure `m0002_supplier` is registered in `migration/src/lib.rs` so the migration runner discovers and executes it. Follow the pattern established by `m0001_initial`.

### Dependency verification

The `migration/Cargo.toml` already declares a dependency on `trustify-module-ingestor`:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

No new dependency needs to be added. This existing dependency is the key factor in the decision to make the private functions public rather than duplicating them (see `reuse-decision.md`).

### Handling private functions in the ingestor crate

The core decision: **make `describing_packages()` and `suppliers()` public (`pub fn`) and import them in the migration crate.** Do NOT duplicate/copy the function bodies into the migration module. This follows the implement-task skill's "Reuse over duplication" guidance from Step 6, which states:

> If the dependency already exists: make the function public and import it rather than duplicating the code. This follows the DRY principle and ensures future bug fixes apply in one place.

The commit message and PR description will explicitly flag this decision so reviewers understand the rationale.
