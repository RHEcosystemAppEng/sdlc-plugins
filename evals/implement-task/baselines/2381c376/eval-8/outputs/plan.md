# Implementation Plan for TC-9206

## Summary

Add supplier information extraction to the SBOM data migration step. The migration
crate needs to extract describing packages and supplier data from ingested SBOMs to
populate the new `sbom_supplier` table.

## Files to Modify

### 1. `modules/ingestor/src/graph/sbom/mod.rs`

**Change**: Make the two private helper functions public so they can be imported by the
migration crate.

- Change `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` to
  `pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- Change `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` to
  `pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`

No logic changes are needed -- only the visibility modifier changes from private to
public. This is the minimal change required to enable reuse.

**Rationale**: The `migration` crate already depends on `trustify-module-ingestor` in
its `Cargo.toml`. Making these functions public avoids code duplication and ensures
future bug fixes apply in one place (see reuse-decision.md for full analysis).

**Backward compatibility**: Use `find_referencing_symbols` (or Grep) to verify that no
existing callers are affected. Since the functions are currently private, they can only
be called within the same module -- making them `pub` is a strictly additive change
that cannot break existing code.

Additionally, verify that the module's `mod.rs` or `lib.rs` re-exports are configured
so the functions are accessible via the crate's public API. If the `graph::sbom` module
is not publicly exposed, its `mod` declaration (and any intermediate modules like
`graph`) would also need `pub` visibility. Check the module tree:
- `modules/ingestor/src/lib.rs` -- verify `pub mod graph;`
- `modules/ingestor/src/graph/mod.rs` -- verify `pub mod sbom;`

### 2. `migration/src/m0002_supplier/mod.rs`

**Change**: Add supplier extraction logic to the migration step.

- Add import for the newly public functions:
  ```rust
  use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
  ```
- Implement the migration logic:
  1. Query all ingested SBOMs from the database
  2. For each SBOM, call `describing_packages(&sbom)` to get the packages it describes
  3. For each SBOM, call `suppliers(&sbom)` to extract supplier information
  4. Insert the extracted supplier data into the `sbom_supplier` table
- Follow the existing migration pattern from `m0001_initial/mod.rs` for structure
  and error handling conventions (use `Result<T, AppError>` with `.context()` wrapping)
- Add documentation comment on the migration function explaining what it does

**Convention conformance**: Examine `m0001_initial/mod.rs` as a sibling migration to
match naming, error handling, and structural patterns.

### 3. `migration/src/lib.rs`

**Change (potential out-of-scope, flag for user approval)**: Register the new
`m0002_supplier` module. This file likely needs a `pub mod m0002_supplier;` declaration
and registration in the migration runner. Since this file is not listed in "Files to
Modify", it would be flagged during Step 9's scope containment check for user approval.

## Files to Create

### 1. `migration/src/m0002_supplier/test.rs`

**Change**: Create unit tests for the supplier extraction migration.

- Add `#[cfg(test)] mod test;` to `m0002_supplier/mod.rs` (or use inline test module)
- Implement test cases per Test Requirements:

**Test 1: Migration correctly extracts suppliers from a sample SBOM**
```rust
/// Verifies that the migration step correctly extracts supplier information
/// from an SBOM that contains supplier metadata.
#[test]
fn test_migration_extracts_suppliers_from_sbom() {
    // Given an SBOM with known supplier information
    // (create test SBOM with supplier data)

    // When the migration step processes the SBOM
    // (call the extraction logic)

    // Then supplier records are produced with the correct values
    // (assert on specific supplier names/fields, not just count)
}
```

**Test 2: SBOMs with no suppliers produce no supplier records**
```rust
/// Verifies that an SBOM with no supplier metadata produces zero supplier records.
#[test]
fn test_migration_produces_no_records_for_sbom_without_suppliers() {
    // Given an SBOM with no supplier information

    // When the migration step processes the SBOM

    // Then no supplier records are produced
    // (assert_eq!(result.len(), 0) or assert!(result.is_empty()))
}
```

**Test conventions**:
- Use value-based assertions (assert on specific supplier names/fields, not just counts)
- Add doc comments on every test function
- Use given-when-then section comments for non-trivial tests
- Follow sibling test patterns from the existing test suite

## Handling Private Functions in the Ingestor Crate

The core decision is to make `describing_packages()` and `suppliers()` public rather
than duplicating them. This is justified by the existing dependency relationship --
see `reuse-decision.md` for full analysis.

## Verification Steps

1. **Build check**: `cargo check -p migration` and `cargo check -p trustify-module-ingestor`
2. **Test run**: `cargo test -p migration` and `cargo test -p trustify-module-ingestor`
3. **Scope containment**: verify `git diff --name-only` matches Files to Modify/Create
4. **Backward compatibility**: confirm no existing callers of the ingestor module break
5. **Data-flow trace**: SBOM record (DB query) -> `describing_packages()` + `suppliers()`
   (extraction) -> `sbom_supplier` table (persistence) -- complete lifecycle
6. **Query-scope verification**: confirm the migration queries all ingested SBOMs (the
   task says "all ingested SBOMs", so a broad query is intentional)

## Commit Message

```
feat(migration): add SBOM supplier extraction to data migration

Reuse existing describing_packages() and suppliers() functions from the
ingestor crate by making them public, rather than duplicating the logic.
The migration crate already depends on trustify-module-ingestor.

Implements TC-9206
```
