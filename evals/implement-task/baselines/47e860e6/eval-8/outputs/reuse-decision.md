# Reuse Decision — TC-9206: private ingestor functions

## Decision

**Make `describing_packages()` and `suppliers()` public in `modules/ingestor/src/graph/sbom/mod.rs` and import them in the migration crate. Do not copy them.**

```rust
// modules/ingestor/src/graph/sbom/mod.rs
/// Returns the packages that the given SBOM declares it describes (its top-level subjects).
pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef> { /* unchanged body */ }

/// Extracts the supplier entries declared in the given SBOM's metadata (empty Vec if none).
pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo> { /* unchanged body */ }

// migration/src/m0002_supplier/mod.rs
use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
```

## How the decision was made (the skill's "Reuse over duplication" rule)

1. **Is the source crate already a dependency of the target crate?** Yes. According to the task's Implementation Notes, `migration/Cargo.toml` already contains:
   ```toml
   trustify-module-ingestor = { path = "../modules/ingestor" }
   ```
   In a live run I would confirm this by reading `migration/Cargo.toml` before making the change.
2. **The dependency exists, so the rule says to make the functions public and import them.** That is the option chosen here.
3. **Copying would only be acceptable if reuse required adding a new dependency.** No new dependency is needed, so that exception does not apply.
4. **Record the decision.** The rationale goes in the commit body and the PR description so that reviewers can see why the ingestor's API grew.

## Why not copy the functions

- **One place to fix bugs.** If the extraction logic is wrong, or changes for new SBOM formats (SPDX or CycloneDX supplier fields), a single fix covers both ingestion and migration. Two copies would drift apart. Rows filled by the migration would then stop matching rows the ingestor writes for SBOMs ingested later.
- **The acceptance criterion requires it.** It says: "The extraction reuses the existing ingestor logic rather than duplicating it."
- **No extra coupling.** The `migration` crate already depends on the ingestor, so making two functions public adds no new dependency between crates.
- **The task asks for it.** Both the Implementation Notes and Files to Modify ("make `describing_packages()` and `suppliers()` public") ask for this approach.

## Notes on the change and possible problems

- **Use `pub`, not `pub(crate)`.** The caller is in a different crate (`migration`), and `pub(crate)` would not let it see the functions.
- **The types in the signatures must be public too.** `Sbom`, `PackageRef` and `SupplierInfo` must be reachable from outside the crate, or the compiler reports `private type in public interface`. If any of them is private and defined in the same file, make it `pub` with a `///` doc comment. That stays inside the listed scope.
- **The module path must be reachable.** `graph` in `lib.rs` and `sbom` in `graph/mod.rs` must be `pub mod`. If they are not, the preferred fix is a `pub use` re-export. Because `lib.rs` and `graph/mod.rs` are not in Files to Modify, I would flag that change for user approval rather than make it without asking.
- **Function bodies stay the same.** Only visibility changes. Existing callers inside the ingestor (found with `find_referencing_symbols`) are not affected.
- **New doc comments.** Both functions are now part of the public API, so each gets a `///` comment, as the skill's code quality rules require.
- **Check for duplicates afterwards.** After implementing, grep the workspace for `fn suppliers` and `fn describing_packages` to confirm the ingestor still holds the only definitions.
