# Reuse Decision: Private Functions in Ingestor Crate

## Functions Under Consideration

Two private helper functions in `modules/ingestor/src/graph/sbom/mod.rs`:

1. **`fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`** — extracts the list of packages that an SBOM describes
2. **`fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`** — extracts supplier information from SBOM metadata

Both are currently private (`fn`, not `pub fn`).

## Dependency Relationship Check

Before deciding, verify the dependency relationship between the source crate (ingestor) and the target crate (migration):

**Source**: `modules/ingestor/` (crate: `trustify-module-ingestor`)
**Target**: `migration/` (crate: `trustify-migration`)

Check `migration/Cargo.toml`:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

**Result**: The dependency already exists. The migration crate already depends on `trustify-module-ingestor`. No new cross-package dependency needs to be introduced.

## Decision: Make Public and Import (Reuse)

**Recommendation**: Change `fn describing_packages` and `fn suppliers` to `pub fn` and import them in the migration crate.

### Rationale

1. **The dependency already exists**: Since `migration/Cargo.toml` already lists `trustify-module-ingestor` as a dependency, making the functions public introduces zero additional coupling. The crates are already linked — we are simply using more of the existing dependency surface.

2. **DRY principle**: The functions implement non-trivial extraction logic (parsing SBOM structures, extracting package references and supplier metadata). Duplicating this logic would mean maintaining two copies of the same algorithm. Any future bug fix or behavior change would need to be applied in both places — a maintenance burden and a source of subtle divergence bugs.

3. **Single source of truth for bug fixes**: If a bug is discovered in how suppliers are extracted from SBOMs, fixing it in `modules/ingestor/src/graph/sbom/mod.rs` automatically fixes it for both the ingestion path and the migration path. With duplication, a fix in one copy could easily be missed in the other.

4. **No new coupling risk**: The concern with making functions public is typically that it creates a new cross-crate dependency. But here the dependency is pre-existing — the migration crate was designed to consume ingestor functionality. Making two additional functions public is a minimal API surface expansion on an already-established dependency path.

## Rejected Alternative: Duplicate (Copy/Inline)

Duplicating the function bodies into the migration crate would:
- Violate DRY by maintaining two identical copies of extraction logic
- Create a risk of divergence if the extraction logic is updated in the ingestor but not the migration
- Be unnecessary since the dependency already exists — there is no coupling cost to avoid
- Add more code to review and maintain for no benefit

Per the implement-task skill's "Reuse over duplication" guidance: when the source package is already a dependency of the target package, make the function public and import it rather than duplicating the code.

## Implementation

```rust
// In modules/ingestor/src/graph/sbom/mod.rs:
// Change:
//   fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>
//   fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>
// To:
//   pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>
//   pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>

// In migration/src/m0002_supplier/mod.rs:
use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
```

No function bodies are modified — only the visibility keyword changes from implicit private to `pub`.
