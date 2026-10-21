# Implementation Plan for TC-9206: Add SBOM Supplier Extraction to Data Migration

## Task Summary

Add supplier information extraction during the SBOM data migration step. The migration
crate needs to extract describing packages and supplier information from ingested SBOMs
to populate the new `sbom_supplier` table. The ingestor module already has private helper
functions that implement this extraction logic.

## Project Configuration Validation

The mock CLAUDE.md contains all required sections:
- Repository Registry: `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID
- Code Intelligence: Serena with `rust-analyzer`

## Parsed Task Structure

- **Repository**: trustify-backend
- **Target Branch**: main
- **Files to Modify**: 2 files
- **Files to Create**: 1 file
- **Dependencies**: None

---

## Files to Modify

### 1. `modules/ingestor/src/graph/sbom/mod.rs`

**Current state**: Contains two private helper functions:
- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` -- extracts the list of packages that an SBOM describes
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` -- extracts supplier information from SBOM metadata

**Changes**:
- Change `fn describing_packages(...)` to `pub fn describing_packages(...)` -- make it public so it can be imported by the migration crate
- Change `fn suppliers(...)` to `pub fn suppliers(...)` -- make it public so it can be imported by the migration crate
- Add documentation comments (`///`) to both functions, describing their purpose, parameters, and return values, since they are now part of the public API

**Rationale**: The migration crate already depends on `trustify-module-ingestor` in its `Cargo.toml`:
```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```
Since the dependency relationship already exists, making these functions public and importing them is the correct approach. This follows the DRY principle (Don't Repeat Yourself) and maintains a single source of truth for the extraction logic. See `outputs/reuse-decision.md` for full rationale.

**Backward compatibility**: Use `find_referencing_symbols` (or Grep) on both functions to verify no existing callers are affected by the visibility change. Changing from private to public is always backward-compatible for existing callers within the same module -- it only broadens access.

### 2. `migration/src/m0002_supplier/mod.rs`

**Current state**: This file needs to be modified to add the supplier extraction logic to the migration step.

**Changes**:
- Add imports for the newly-public functions from the ingestor crate:
  ```rust
  use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
  ```
- Implement the migration step logic that:
  1. Iterates over all ingested SBOMs
  2. Calls `describing_packages(sbom)` to extract the packages each SBOM describes
  3. Calls `suppliers(sbom)` to extract supplier information from SBOM metadata
  4. Inserts extracted supplier data into the `sbom_supplier` table
- Follow the existing migration pattern from `m0001_initial/mod.rs` (sibling convention conformance)
- Apply defensive property access: use `.unwrap_or_default()` or `if let` guards when accessing nested SBOM data fields, since upstream data may contain partial results
- Add documentation comment on the migration function explaining what it does

**Convention conformance**: Examine `m0001_initial/mod.rs` as the sibling migration module to match:
- Function naming conventions
- Error handling patterns (likely `Result<T, AppError>` with `.context()`)
- Database interaction patterns (SeaORM conventions)
- Transaction handling for batch inserts

## Files to Create

### 1. `migration/src/m0002_supplier/test.rs`

**Purpose**: Unit tests for the supplier extraction migration step.

**Tests to implement**:

1. **`test_migration_extracts_suppliers_from_sbom`**
   - Doc comment: `/// Verifies that the migration step correctly extracts suppliers from a sample SBOM.`
   - Given: A sample SBOM with known supplier metadata
   - When: The migration step processes the SBOM
   - Then: The `sbom_supplier` table contains the expected supplier records with correct data

2. **`test_sbom_with_no_suppliers_produces_no_records`**
   - Doc comment: `/// Verifies that SBOMs with no suppliers produce no supplier records.`
   - Given: An SBOM with no supplier information
   - When: The migration step processes the SBOM
   - Then: No records are inserted into the `sbom_supplier` table

**Test conventions**: Follow the existing test patterns from `tests/api/sbom.rs` and other sibling test files. Use `assert_eq!` with specific values (not just length checks). Include given-when-then section comments for non-trivial tests. Add `///` doc comments on every test function.

**Module registration**: Ensure `test.rs` is registered as a test module in `m0002_supplier/mod.rs`:
```rust
#[cfg(test)]
mod test;
```

## Module Registration

Verify that `m0002_supplier` is registered in `migration/src/lib.rs`. If not already present, add:
```rust
mod m0002_supplier;
```

This file is not in Files to Modify, so if it needs changes, flag it during Step 9 scope containment check for user approval.

## Dependency Verification

The migration crate's `Cargo.toml` already includes:
```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

No new dependencies need to be added. This existing dependency is what makes the reuse-over-duplication decision straightforward.

## Data-Flow Trace

- **Input**: Ingested SBOMs stored in the database
- **Processing**: Migration iterates SBOMs, calls `describing_packages()` and `suppliers()` to extract data
- **Output**: Extracted supplier data persisted to `sbom_supplier` table

All stages are connected. The extraction functions are the bridge between raw SBOM data and structured supplier records.

## Query-Scope Verification

The task description says "extract supplier information from all ingested SBOMs" -- the migration should process all SBOMs (no subset restriction). A broad query (`SELECT * FROM sbom` or equivalent) is intentional for a data migration that backfills a new table.

## Verification Steps

1. Run `cargo test -p trustify-migration` (or the correct crate name from `cargo metadata`) to verify tests pass
2. Run `cargo test -p trustify-module-ingestor` to verify the visibility change does not break existing ingestor tests
3. Check for CI commands in `CONVENTIONS.md` and run them
4. Verify scope containment: only the 3 files listed should be modified/created
5. Run sensitive-pattern check on staged diff
