# Implementation Plan: TC-9206 -- Add SBOM supplier extraction to data migration

## Overview

Add supplier information extraction to the SBOM data migration step by reusing existing private helper functions from the ingestor crate. The migration crate already depends on `trustify-module-ingestor`, so the functions will be made public rather than duplicated.

## Pre-implementation: Verify dependency relationship

Before making any code changes, verify that `migration/Cargo.toml` already lists `trustify-module-ingestor` as a dependency:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

This dependency is confirmed in the task's Implementation Notes. Because it already exists, there is no new coupling cost, and the correct approach is to make the private functions public and import them (per the skill's "Reuse over duplication" guidance and the DRY principle).

## Files to Modify

### 1. `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make `describing_packages()` and `suppliers()` public.

- Change `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` to `pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- Change `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` to `pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`
- Add documentation comments (`///`) to both functions explaining their purpose, since they are now part of the crate's public API:
  - `describing_packages`: "Extracts the list of packages that an SBOM describes."
  - `suppliers`: "Extracts supplier information from SBOM metadata."
- No other changes to this file. The function bodies remain identical.

### 2. `migration/src/m0002_supplier/mod.rs`

**Change**: Add supplier extraction logic that reuses the ingestor's public functions.

- Add import statements:
  ```rust
  use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
  ```
- Implement the migration step logic:
  - Query all ingested SBOMs from the database
  - For each SBOM, call `describing_packages(&sbom)` to get the packages it describes
  - For each SBOM, call `suppliers(&sbom)` to extract supplier information
  - Insert the extracted supplier records into the `sbom_supplier` table
- Follow the existing migration pattern from `m0001_initial/mod.rs` for structure and error handling conventions
- The key point: do NOT copy or inline the bodies of `describing_packages()` or `suppliers()` -- import and call them directly

## Files to Create

### 3. `migration/src/m0002_supplier/test.rs`

**Change**: Unit tests for the supplier extraction migration.

- Test 1: `test_migration_extracts_suppliers` -- Create a sample SBOM with known supplier data, run the migration step, and verify the `sbom_supplier` table is populated with the correct supplier records. Assert on specific field values, not just row counts.
- Test 2: `test_migration_no_suppliers` -- Create a sample SBOM with no supplier metadata, run the migration step, and verify that no records are inserted into `sbom_supplier`.
- Each test function gets a `///` doc comment explaining what it verifies.
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments.

## Reuse decision

**Approach**: Make `describing_packages()` and `suppliers()` public and import them. Do NOT duplicate or inline the function bodies.

**Why**: The `migration` crate already depends on `trustify-module-ingestor` (verified in `migration/Cargo.toml`). Since the dependency already exists, making the functions `pub fn` and importing them follows the DRY principle and ensures that any future bug fixes to the extraction logic apply in one place -- both the ingestor's runtime code path and the migration's batch code path will benefit from the fix automatically.

Duplicating the function bodies is explicitly rejected: it would create two copies of the same logic that must be kept in sync manually, with no offsetting benefit since the dependency cost has already been paid.

This decision will be noted in the commit message so reviewers understand why the visibility change was made.

## Commit message

```
feat(migration): add SBOM supplier extraction to data migration

Reuse existing describing_packages() and suppliers() helpers from
the ingestor crate by making them pub fn. The migration crate already
depends on trustify-module-ingestor, so importing is preferred over
duplication (DRY -- future bug fixes apply in one place).

Implements TC-9206
```
