# Implementation Plan for TC-9206

## Summary

Add supplier information extraction to the SBOM data migration step by reusing
existing private helper functions from the ingestor crate, making them public
rather than duplicating their logic.

## Step 1 -- Understand the code and verify dependencies

### Private functions in the ingestor crate

The file `modules/ingestor/src/graph/sbom/mod.rs` contains two private helper
functions that implement the exact extraction logic needed:

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` -- extracts the list
  of packages that an SBOM describes
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` -- extracts supplier
  information from SBOM metadata

These functions are currently declared with `fn` (private visibility) and cannot
be called from outside their module.

### Verify the dependency relationship

Before deciding how to reuse these functions, check `migration/Cargo.toml` to
confirm the dependency on the ingestor crate. The task description states that
this dependency already exists:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

This is critical: because `migration` already depends on `trustify-module-ingestor`,
we can make the functions public and import them directly without introducing any
new cross-crate dependency. This verification must happen before proceeding.

### Check referencing symbols

Use `find_referencing_symbols` (or Grep as fallback) on `describing_packages` and
`suppliers` to identify all current callers within the ingestor crate. This ensures
that changing visibility from private to public does not break any existing internal
usage patterns (it will not -- widening visibility is backward-compatible).

## Step 2 -- Files to modify

### `modules/ingestor/src/graph/sbom/mod.rs`

Change the visibility of two functions from private to public:

- Change `fn describing_packages(` to `pub fn describing_packages(`
- Change `fn suppliers(` to `pub fn suppliers(`

No other changes to these functions are needed. The function bodies, signatures,
and return types remain exactly as they are. The only change is the addition of
the `pub` visibility modifier.

Additionally, verify that the module path re-exports these functions (or that
they are accessible via the crate's public API). If `mod.rs` files in the module
hierarchy use `pub mod` declarations, the functions will be reachable as
`trustify_module_ingestor::graph::sbom::describing_packages` and
`trustify_module_ingestor::graph::sbom::suppliers`. If the module is not publicly
re-exported at the crate level, add `pub mod` or `pub use` declarations as needed
to make the functions importable from the migration crate.

### `migration/src/m0002_supplier/mod.rs`

Add the supplier extraction logic to the migration step:

1. Add import statements for the now-public functions:
   ```rust
   use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
   ```

2. Implement the migration logic that:
   - Iterates over ingested SBOMs
   - Calls `describing_packages(&sbom)` to get the packages each SBOM describes
   - Calls `suppliers(&sbom)` to extract supplier information
   - Inserts the extracted supplier data into the `sbom_supplier` table

3. Follow the existing migration pattern established by `m0001_initial/mod.rs`
   for transaction handling, error wrapping, and batch insert patterns.

## Step 3 -- Files to create

### `migration/src/m0002_supplier/test.rs`

Create unit tests for the supplier extraction migration:

1. Test that the migration step correctly extracts suppliers from a sample SBOM
   with known supplier data -- assert on specific supplier values, not just count.

2. Test that SBOMs with no suppliers produce no supplier records -- verify the
   `sbom_supplier` table has zero rows for that SBOM.

3. Follow the project's existing test conventions (identified from sibling test
   files in the migration crate).

4. Add doc comments to every test function explaining what it verifies.

## Step 4 -- What this plan does NOT do

This plan explicitly does **not**:

- Copy or inline the bodies of `describing_packages()` or `suppliers()` into the
  migration crate. Duplication is rejected in favor of reuse (see
  `reuse-decision.md` for the full rationale).
- Introduce any new crate dependencies. The `migration` crate already depends on
  `trustify-module-ingestor`, so no `Cargo.toml` changes are required.
- Modify any files outside the scope defined in the task (Files to Modify and
  Files to Create sections).

## Step 5 -- Verification

1. Run `cargo test -p trustify-module-ingestor` to confirm the visibility change
   does not break existing ingestor tests.
2. Run `cargo test -p migration` (or the correct crate name from `cargo metadata`)
   to verify the new migration tests pass.
3. Run any CI check commands from `CONVENTIONS.md` if present.
4. Verify acceptance criteria:
   - The migration step extracts supplier information from all ingested SBOMs.
   - The extraction reuses the existing ingestor logic (no duplication).
   - The `sbom_supplier` table is populated correctly with supplier data.
