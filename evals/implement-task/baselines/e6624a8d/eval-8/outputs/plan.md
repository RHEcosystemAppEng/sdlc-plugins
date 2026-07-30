# Implementation Plan for TC-9206: Add SBOM Supplier Extraction to Data Migration

## Task Summary

Add supplier information extraction during the SBOM data migration step. The migration crate needs to extract describing packages and supplier information from ingested SBOMs to populate the new `sbom_supplier` table, reusing existing extraction logic from the ingestor module.

## Repository

trustify-backend

## Target Branch

main

## Files to Modify

### 1. `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make two private helper functions public so they can be imported by the migration crate.

- Change `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` to `pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- Change `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` to `pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`

These are minimal, surgical visibility changes. No logic modifications are needed. The functions already implement the exact extraction logic required by the migration step.

**Verification**: After making them public, use `find_referencing_symbols` (or Grep) to confirm no existing callers are broken by the visibility change. Making a private function public is backward-compatible -- all existing internal call sites continue to work.

### 2. `migration/src/m0002_supplier/mod.rs`

**Change**: Add supplier extraction logic to the migration step by importing and using the newly public functions from the ingestor module.

Specific changes:
- Add import statements for the public functions:
  ```rust
  use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
  ```
- Implement the migration logic that:
  1. Iterates over all ingested SBOMs in the database
  2. For each SBOM, calls `describing_packages(&sbom)` to extract the list of packages the SBOM describes
  3. Calls `suppliers(&sbom)` to extract supplier information from SBOM metadata
  4. Inserts the extracted supplier data into the `sbom_supplier` table
- Follow the migration pattern established by `m0001_initial/mod.rs` for:
  - Error handling (using `Result<T, AppError>` with `.context()` wrapping)
  - Database transaction handling
  - Query patterns (SeaORM conventions)

**Convention conformance**: The implementation should follow the same structure as the existing `m0001_initial` migration module, matching its error handling, transaction boundaries, and naming conventions.

### 3. `migration/src/lib.rs`

**Out-of-scope note**: The `lib.rs` file may need updating to register the new `m0002_supplier` module. This is not listed in Files to Modify, so if registration is required, it would be flagged as an out-of-scope change during self-verification (Step 9) and the user would be asked for approval before proceeding.

## Files to Create

### 1. `migration/src/m0002_supplier/test.rs`

**Purpose**: Unit tests for the supplier extraction migration.

Tests to implement (per Test Requirements):

1. **`test_migration_extracts_suppliers_from_sbom`** -- Verifies that the migration step correctly extracts suppliers from a sample SBOM.
   - Given: A sample SBOM with known supplier metadata
   - When: The migration step processes the SBOM
   - Then: The `sbom_supplier` table contains the expected supplier records with correct data

2. **`test_migration_no_suppliers_produces_no_records`** -- Verifies that SBOMs with no suppliers produce no supplier records.
   - Given: An SBOM with no supplier information in its metadata
   - When: The migration step processes the SBOM
   - Then: No rows are inserted into the `sbom_supplier` table for that SBOM

Test conventions to follow:
- Use `assert_eq!` for value-based assertions (not just length checks)
- Document every test function with `///` doc comments
- Include given-when-then section comments inside each test body
- Follow the `test_<action>_<scenario>` naming pattern
- Match the integration test patterns from `tests/api/` for database setup and teardown

## Handling of Private Functions in the Ingestor Crate

**Decision**: Make the functions public (`pub fn`) and import them.

**Rationale**: The `migration` crate already depends on `trustify-module-ingestor` in its `Cargo.toml`. The dependency relationship exists. Per the skill's "Reuse over duplication" guidance (Step 6), when the dependency already exists, make the function public and import it rather than duplicating the code. This follows the DRY principle and ensures future bug fixes to the extraction logic apply in one place.

See `outputs/reuse-decision.md` for the full decision analysis.

## Acceptance Criteria Verification

1. **The migration step extracts supplier information from all ingested SBOMs** -- Satisfied by the implementation in `m0002_supplier/mod.rs` that iterates all SBOMs and calls `describing_packages()` and `suppliers()`.
2. **The extraction reuses the existing ingestor logic rather than duplicating it** -- Satisfied by making the ingestor functions public and importing them, rather than copying the implementation.
3. **The `sbom_supplier` table is populated correctly with supplier data** -- Satisfied by the migration inserting extracted supplier data into the table, verified by tests.

## Self-Verification Checklist

- Scope containment: verify only the listed files are modified (plus potential `lib.rs` registration with user approval)
- Untracked file check: ensure `test.rs` is staged for commit
- Sensitive-pattern check: scan diff for secrets
- Data-flow trace: SBOM read -> describing_packages() -> suppliers() -> insert into sbom_supplier -> complete path
- Query-scope verification: confirm the migration queries all ingested SBOMs (matching the task's "all ingested SBOMs" scope)
- Duplication check: confirm no existing supplier extraction logic elsewhere in the codebase
- Contract and sibling parity: compare m0002_supplier with m0001_initial for structural parity

## Commit Message

```
feat(migration): add SBOM supplier extraction to data migration

Reuse existing describing_packages() and suppliers() functions from
the ingestor module by making them public. The migration step iterates
all ingested SBOMs and populates the sbom_supplier table.

Implements TC-9206
```
