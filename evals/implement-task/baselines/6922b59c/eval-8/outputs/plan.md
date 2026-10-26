# Implementation Plan for TC-9206

## Task Summary

Add SBOM supplier extraction to the data migration step. The migration crate needs to
extract describing packages and supplier information from ingested SBOMs to populate the
new `sbom_supplier` table.

## Files to Modify

### 1. `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make `describing_packages()` and `suppliers()` public.

- Change `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` to `pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- Change `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` to `pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`

No logic changes are needed -- only the visibility modifier is updated. This is a
minimal, non-breaking change since these functions had no external callers before, and
making them public is purely additive.

**Rationale**: The migration crate already depends on `trustify-module-ingestor` in its
`Cargo.toml`. Rather than duplicating the extraction logic, we make these functions
public so the migration can import and call them directly. See `reuse-decision.md` for
the full analysis.

### 2. `migration/src/m0002_supplier/mod.rs`

**Change**: Add supplier extraction logic to the migration step.

- Add import statements for the now-public functions from the ingestor crate:
  ```rust
  use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
  ```
- Implement the migration step that:
  1. Iterates over all ingested SBOMs in the database
  2. For each SBOM, calls `describing_packages(&sbom)` to get the packages the SBOM describes
  3. Calls `suppliers(&sbom)` to extract supplier information
  4. Inserts records into the `sbom_supplier` table mapping each SBOM to its suppliers
- Follow the existing migration pattern from `m0001_initial/mod.rs` for structure,
  error handling (`Result<T, AppError>` with `.context()` wrapping), and transaction
  management
- Add defensive guards on the return values of `describing_packages()` and `suppliers()`
  -- handle empty vectors gracefully (no suppliers means no records to insert)
- Add a doc comment on the migration function explaining what it does

## Files to Create

### 3. `migration/src/m0002_supplier/test.rs`

**Change**: Create unit tests for the supplier extraction migration.

- Add a test module with `#[cfg(test)]` attribute
- Implement at minimum two tests per the Test Requirements:
  1. **`test_migration_extracts_suppliers_from_sbom`**: Verify that the migration step
     correctly extracts suppliers from a sample SBOM and inserts them into `sbom_supplier`.
     Use given-when-then structure. Assert on actual supplier values, not just count.
  2. **`test_migration_no_suppliers_produces_no_records`**: Verify that SBOMs with no
     suppliers produce no supplier records in the table. Assert the result set is empty.
- Each test function gets a `///` doc comment explaining what it verifies
- Follow the assertion patterns from the existing test suite (e.g.,
  `assert_eq!(resp.status(), StatusCode::OK)` pattern adapted for migration context)
- Register the test module in `migration/src/m0002_supplier/mod.rs` with `#[cfg(test)] mod test;`

## Additional Steps

### Module Registration

- Ensure `m0002_supplier` is registered in `migration/src/lib.rs` if not already present
  (add `mod m0002_supplier;` and include it in the migration runner's list)

### Handling Private Functions in the Ingestor Crate

The key implementation decision is how to handle the private `describing_packages()` and
`suppliers()` functions. The approach is to make them public rather than duplicate them.
Full reasoning is in `reuse-decision.md`.

### Query-Scope Verification

The task description says "extract supplier information from all ingested SBOMs" -- the
migration should process all SBOMs without subset filtering, which is appropriate for a
data migration that populates a new table. A broad query (`SELECT * FROM sbom` or
equivalent ORM call) is intentional here; document this in a code comment.

### Data-Flow Trace

- Input: SBOM records read from the database
- Processing: `describing_packages()` extracts package references, `suppliers()` extracts
  supplier info from SBOM metadata
- Output: Records inserted into `sbom_supplier` table
- All stages are connected through the migration function's loop

### CI Verification

- Run `cargo test -p trustify-migration` (or the correct crate name from `cargo metadata`)
  to verify the migration tests pass
- Run `cargo test -p trustify-module-ingestor` to verify that making functions public did
  not break existing ingestor tests
- Check `CONVENTIONS.md` at repo root for any additional CI commands to run
