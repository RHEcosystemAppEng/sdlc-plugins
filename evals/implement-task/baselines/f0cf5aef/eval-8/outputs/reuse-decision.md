# Reuse Decision: Private Functions in the Ingestor Crate

## Decision

**Make the functions public (`pub fn`) and import them in the migration crate.** Do NOT duplicate or inline the function bodies.

## Functions in Question

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` in `modules/ingestor/src/graph/sbom/mod.rs`
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` in `modules/ingestor/src/graph/sbom/mod.rs`

Both are currently private (no `pub` modifier) and need to be used by code in the `migration` crate.

## Dependency Relationship Verification

Before deciding, the dependency relationship must be verified. The task description states that `migration/Cargo.toml` already contains:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

This confirms that the `migration` crate already depends on the `trustify-module-ingestor` crate. No new dependency needs to be introduced.

## Rationale

The implement-task skill's "Reuse over duplication" guidance (Step 6) prescribes a two-part decision process:

1. **Check the dependency relationship**: Does the target package (migration) already depend on the source package (ingestor)? **Yes** -- `migration/Cargo.toml` lists `trustify-module-ingestor` as a dependency.

2. **If the dependency already exists**: "Make the function public (`pub`, `export`, etc.) and import it rather than duplicating the code. This follows the DRY principle and ensures future bug fixes apply in one place."

Since the dependency already exists, the guidance is unambiguous: make the functions public and import them.

## Why NOT Duplicate

Duplicating the function bodies into the migration crate would violate the DRY (Don't Repeat Yourself) principle:

- **Bug fixes would need to be applied in two places.** If a bug is found in `describing_packages()` or `suppliers()` (e.g., incorrect handling of a particular SBOM format), the fix would need to be applied both in the ingestor's copy and the migration's copy. Missing one would leave inconsistent behavior.
- **Logic drift risk.** Over time, the two copies could diverge as one is updated and the other is forgotten, leading to subtle inconsistencies in how supplier information is extracted during ingestion vs. migration.
- **The dependency already exists.** The usual counterargument for duplication -- "introducing a new cross-package dependency for a single utility may not be worth the coupling" -- does not apply here. The coupling already exists; making two functions public adds negligible additional coupling.

## Why Public Visibility is Safe

- **Non-breaking change**: Widening visibility from `fn` to `pub fn` is strictly additive in Rust. No existing code is affected -- private functions have no external callers, so there are no callers to break.
- **Stable signatures**: The function signatures (`describing_packages(sbom: &Sbom) -> Vec<PackageRef>` and `suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`) are well-defined with clear input/output types. Making them public exposes a clean API surface.
- **Logical cohesion**: These functions live in the SBOM graph module of the ingestor, which is the natural home for SBOM extraction logic. Making them public from that location is architecturally sound -- it exposes domain logic from the module that owns it.

## Implementation

In `modules/ingestor/src/graph/sbom/mod.rs`:

```rust
// Before:
fn describing_packages(sbom: &Sbom) -> Vec<PackageRef> { ... }
fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo> { ... }

// After:
pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef> { ... }
pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo> { ... }
```

In `migration/src/m0002_supplier/mod.rs`:

```rust
use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
```

No function bodies are copied. No new dependencies are added. The migration crate calls the canonical implementation through the existing dependency path.
