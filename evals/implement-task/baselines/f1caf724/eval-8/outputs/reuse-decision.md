# Reuse Decision: Private Functions in Ingestor Crate

## Summary

**Decision**: Make `describing_packages()` and `suppliers()` public (`pub fn`) in the ingestor crate and import them into the migration crate. Do NOT duplicate or inline the function bodies.

## Analysis

### Functions in question

The two private helper functions in `modules/ingestor/src/graph/sbom/mod.rs`:

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` -- extracts the list of packages that an SBOM describes
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` -- extracts supplier information from SBOM metadata

Both are currently private (`fn`, not `pub fn`), meaning they cannot be imported by other crates.

### Dependency relationship verification

**Critical prerequisite**: Before deciding between making the functions public or duplicating them, the dependency relationship between the migration crate and the ingestor crate must be verified.

Checked `migration/Cargo.toml` and confirmed the dependency already exists:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

The migration crate already depends on `trustify-module-ingestor`. This means:
- No new cross-package dependency needs to be introduced
- Public symbols from the ingestor crate are already importable by the migration crate
- Making the functions `pub` only widens their visibility within an existing dependency chain

### Decision rationale: pub fn over duplication

1. **The dependency already exists**: Since `migration/Cargo.toml` already lists `trustify-module-ingestor` as a dependency, making the functions public introduces zero new coupling. The crates are already linked. This is the deciding factor -- per the skill's "Reuse over duplication" guidance (Step 6), when the dependency already exists, make the function public and import it rather than duplicating the code.

2. **DRY principle -- single source of truth**: Duplicating the function bodies would create two independent copies of the same extraction logic. This violates the DRY (Don't Repeat Yourself) principle. If a bug is discovered in the extraction logic (e.g., incorrect parsing of a supplier field, missing edge case handling), the fix would need to be applied in both places. With reuse, future bug fixes apply in one place -- the canonical implementation in the ingestor crate.

3. **Maintenance burden**: Copied code drifts over time. If the ingestor's extraction logic is updated to handle a new SBOM format or fix an edge case, the duplicated version in the migration crate would not automatically receive the fix. Reuse via import ensures both the ingestor and the migration always use the same logic.

4. **Minimal change footprint**: Making two functions `pub` is a two-word change (adding `pub` to each function declaration). Duplicating the functions would require copying potentially complex logic, adding tests for the copies, and maintaining both indefinitely.

### What we explicitly reject

- **Copying the function bodies into migration/src/m0002_supplier/mod.rs**: This would violate DRY and create maintenance burden. Rejected.
- **Inlining the logic directly**: Same problems as copying -- duplication with no benefit since the dependency already exists. Rejected.
- **Creating a new shared crate**: Unnecessary complexity. The dependency relationship already exists via Cargo.toml, so the existing crate boundary is sufficient. Rejected.

### Backward compatibility

Making `fn` into `pub fn` is a backward-compatible change:
- All existing callers within the ingestor crate continue to work unchanged
- No existing public API signatures are modified
- The only effect is widened visibility, allowing the migration crate to import the functions

### Implementation

In `modules/ingestor/src/graph/sbom/mod.rs`:

```rust
// Before:
fn describing_packages(sbom: &Sbom) -> Vec<PackageRef> { ... }
fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo> { ... }

// After:
/// Extracts the list of packages that an SBOM describes.
pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef> { ... }

/// Extracts supplier information from SBOM metadata.
pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo> { ... }
```

In `migration/src/m0002_supplier/mod.rs`:

```rust
use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
```

The function bodies are not touched -- only visibility changes and an import is added.
