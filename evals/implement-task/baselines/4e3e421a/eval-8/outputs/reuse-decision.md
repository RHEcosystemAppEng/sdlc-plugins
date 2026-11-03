# Reuse Decision — TC-9206

## Decision
**Make the functions public and import them. Do not duplicate them.**

`describing_packages()` and `suppliers()` in `modules/ingestor/src/graph/sbom/mod.rs` change from `fn` to `pub fn`. The migration then imports them:

```rust
use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
```

## Rationale (implement-task "Reuse over duplication" rule)

1. **Dependency check.** The source crate is `trustify-module-ingestor` and the target crate is `migration`. `migration/Cargo.toml` already contains
   `trustify-module-ingestor = { path = "../modules/ingestor" }`. I would confirm this by reading the manifest in Step 4.
2. **The dependency already exists, so make them public and import.** Exporting the functions adds no new coupling between the crates. Copying them would leave two versions of the SBOM supplier parsing logic, and a later bug fix or format change (for example, new SPDX/CycloneDX supplier fields) would have to be made in both places.
3. **The duplication fallback does not apply.** Copying is only acceptable when reuse would require adding a new crate dependency. That is not the case here.
4. **The task agrees.** The Implementation Notes and the acceptance criterion ("The extraction reuses the existing ingestor logic rather than duplicating it") ask for the same thing, and `modules/ingestor/src/graph/sbom/mod.rs` is listed in Files to Modify.

## Safeguards
- Only the visibility changes. The bodies stay as they are, so existing in-crate callers are unaffected (checked with `find_referencing_symbols`).
- Each newly public function gets a `///` doc comment.
- Check that the return and argument types (`Sbom`, `PackageRef`, `SupplierInfo`) are public and reachable through a `pub mod` path. Also check that `graph` and `sbom` are `pub mod` in the ingestor. If either is not, widen visibility only within the in-scope file, or flag the extra file for user approval.
- Use `pub` rather than a narrower visibility. `pub(crate)` would not work because the caller is in another crate.
- The commit message and PR description record this choice so reviewers know why the ingestor's API grew.
