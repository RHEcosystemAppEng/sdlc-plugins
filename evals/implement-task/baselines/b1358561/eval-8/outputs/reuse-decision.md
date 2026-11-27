# Reuse Decision: private ingestor helpers (TC-9206)

## Decision
**Make `describing_packages()` and `suppliers()` public in `modules/ingestor/src/graph/sbom/mod.rs` and import them from the migration crate. Do not duplicate them.**

```rust
// modules/ingestor/src/graph/sbom/mod.rs
/// Returns the packages that the given SBOM declares it describes.
pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef> { /* unchanged */ }

/// Extracts supplier information from the SBOM's metadata (empty if none).
pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo> { /* unchanged */ }

// migration/src/m0002_supplier/mod.rs
use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
```

## Rationale
1. **The skill's Reuse rule covers this case.** Step 6, Reuse, rule 2: "Exists but is not exported: when its package is already a dependency (check `Cargo.toml` ...), make it public (`pub`, `export`) and import it." Inlining a local copy is only for cases where reuse would *add a new* cross-package dependency for one utility.
2. **The dependency already exists.** `migration/Cargo.toml` already declares `trustify-module-ingestor = { path = "../modules/ingestor" }`. Making the functions public adds no edge to the crate graph and no risk of a dependency cycle.
3. **The task requires it.** The Implementation Notes say "make the functions public and import them rather than duplicating the code". An acceptance criterion says "The extraction reuses the existing ingestor logic rather than duplicating it". The task also lists `modules/ingestor/src/graph/sbom/mod.rs` under Files to Modify for exactly this change, so it is in scope.
4. **One source of truth.** These functions define what "describing packages" and "supplier" mean for an SBOM. If the migration had its own copy, the backfilled `sbom_supplier` data could drift from what ingestion produces for new SBOMs whenever the ingestor logic changes (new SBOM formats, bug fixes). Sharing the code keeps backfilled data and newly ingested data consistent.
5. **Small, safe change.** Going from private to `pub` only widens visibility. Existing callers inside the ingestor are unaffected, and the function bodies do not change.

## Alternative considered and rejected
- **Copy the functions into the migration crate.** Rejected. It violates the acceptance criterion and the skill's reuse rule, and creates two copies of the logic that can drift apart. Self-verification check #5 (Duplication) would flag it.
- **`pub(crate)`.** Not enough. The caller is in a different crate (`migration`), so the functions need full `pub`.
- **Move the helpers into `common`.** Not needed. It would widen scope to files that are not listed, and the existing dependency already gives access.

## Follow-ups from the reuse
- If `PackageRef`, `SupplierInfo`, or `Sbom` are private, they must also become `pub` (Rust rejects private types in a public signature). The same applies to the `graph` / `graph::sbom` module declarations if they are not `pub mod`. Changes inside `graph/sbom/mod.rs` are in scope. Changes to `lib.rs` / `graph/mod.rs` would be flagged for approval under scope containment.
- Add `///` doc comments to the newly public functions, as the skill requires for public symbols.
- Record this decision in the commit message body and the PR description (Reuse rule 4).
