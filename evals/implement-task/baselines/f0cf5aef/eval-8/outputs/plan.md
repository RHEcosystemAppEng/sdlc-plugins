# Implementation Plan for TC-9206: Add SBOM supplier extraction to data migration

## Overview

This task adds supplier information extraction to the SBOM data migration step. The migration crate needs to extract describing packages and supplier information from ingested SBOMs to populate the new `sbom_supplier` table. The ingestor module already contains the extraction logic in two private helper functions.

## Files to Modify

### 1. `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make two private functions public.

- Change `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` to `pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- Change `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` to `pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`

**Rationale**: These functions implement the exact extraction logic needed by the migration crate. The `migration` crate already depends on `trustify-module-ingestor` in its `Cargo.toml`, so making them public and importing them is the correct approach (see `outputs/reuse-decision.md` for full analysis). No other changes to this file are needed -- the function signatures, parameters, and return types remain the same.

**Backward compatibility**: Since the functions were previously private, no existing external callers exist. Widening visibility from private to public is a non-breaking change. All existing internal callers within the ingestor crate continue to work without modification.

### 2. `migration/src/m0002_supplier/mod.rs`

**Changes**:

- Add import statements for the newly-public functions:
  ```rust
  use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
  ```
- Implement the supplier extraction migration logic:
  - Query all ingested SBOMs from the database
  - For each SBOM, call `describing_packages(&sbom)` to extract the packages the SBOM describes
  - For each SBOM, call `suppliers(&sbom)` to extract supplier information
  - Insert the extracted supplier data into the `sbom_supplier` table
- Follow existing migration patterns from `m0001_initial/mod.rs` for structure, error handling, and database interaction conventions
- Add documentation comments on the migration function explaining what it does

**Error handling**: Follow the established patterns from sibling migration `m0001_initial/mod.rs` -- use `Result<T, AppError>` with `.context()` wrapping as specified in the repository conventions.

**Query scope**: The migration processes all ingested SBOMs (the task description says "all ingested SBOMs"), so a full table scan is appropriate. A comment should document that the broad query is intentional.

## Files to Create

### 3. `migration/src/m0002_supplier/test.rs`

**Contents**:

- Unit tests for the supplier extraction migration:
  1. **Test: migration correctly extracts suppliers from a sample SBOM** -- Create a test SBOM with known supplier data, run the extraction logic, and assert that the correct supplier records are produced. Use value-based assertions (verify specific supplier names, URLs, etc.) rather than length-only checks.
  2. **Test: SBOMs with no suppliers produce no supplier records** -- Create a test SBOM with no supplier metadata, run the extraction logic, and assert the result is empty.
- Each test function must have a `///` documentation comment explaining what it verifies
- Non-trivial tests should include `// Given`, `// When`, `// Then` section comments
- Follow test patterns from sibling test files in the migration crate
- Add `#[cfg(test)] mod test;` declaration in `migration/src/m0002_supplier/mod.rs` to register the test module

## Files NOT Modified

- **`migration/Cargo.toml`**: No changes needed. The dependency on `trustify-module-ingestor` already exists:
  ```toml
  [dependencies]
  trustify-module-ingestor = { path = "../modules/ingestor" }
  ```
  This pre-existing dependency is the key factor enabling the reuse approach.

- **`migration/src/lib.rs`**: Would need to register `m0002_supplier` as a module if not already declared. This is potentially out-of-scope per the task description (not listed in Files to Modify). If the module is not yet registered, flag this as an out-of-scope change during Step 9's scope containment check and ask the user for approval before adding it.

## Handling of Private Functions in the Ingestor Crate

The `describing_packages()` and `suppliers()` functions in `modules/ingestor/src/graph/sbom/mod.rs` are currently private (`fn`, not `pub fn`). The implementation makes them public (`pub fn`) rather than duplicating their code into the migration crate, because:

1. The `migration` crate already depends on `trustify-module-ingestor` (verified in `migration/Cargo.toml`)
2. Per the implement-task skill's "Reuse over duplication" guidance (Step 6): "If the dependency already exists: make the function public and import it rather than duplicating the code"
3. The DRY principle ensures future bug fixes to the extraction logic apply in one place

See `outputs/reuse-decision.md` for the complete decision rationale.

## Data-Flow Trace

- **Input**: SBOMs stored in the database (queried during migration)
- **Processing**: `describing_packages()` extracts package references from each SBOM; `suppliers()` extracts supplier information from SBOM metadata
- **Output**: Rows inserted into the `sbom_supplier` table

The flow is complete: database read -> extraction via reused functions -> database write.

## Verification Steps

1. Run `cargo test -p trustify-migration` (or the migration crate's package name) to verify new tests pass
2. Run `cargo test -p trustify-module-ingestor` to verify existing ingestor tests still pass after the visibility change
3. Run any CI check commands from CONVENTIONS.md (formatting, linting, compilation)
4. Verify scope containment: `git diff --name-only` should show only the three files listed above (plus `migration/src/lib.rs` if module registration was needed and approved)
