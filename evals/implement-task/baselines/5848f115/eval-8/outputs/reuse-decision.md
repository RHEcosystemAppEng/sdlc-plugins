# Reuse Decision: `describing_packages()` and `suppliers()`

## Decision

**Make the functions public (`pub fn`) and import them in the migration crate.**
Do NOT duplicate or inline the function bodies into `migration/src/m0002_supplier/mod.rs`.

## Rationale

### 1. Dependency relationship already exists

The `migration/Cargo.toml` already declares a dependency on `trustify-module-ingestor`:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

This means the migration crate can already import symbols from the ingestor crate. Making `describing_packages()` and `suppliers()` public adds no new coupling -- the inter-crate dependency is already established and accepted by the project.

### 2. DRY principle

Following the DRY (Don't Repeat Yourself) principle, the extraction logic should live in exactly one place. If a bug is discovered in `describing_packages()` or `suppliers()` -- for example, incorrect handling of an edge case in SBOM metadata parsing -- the fix needs to be applied in only one location. Both the ingestor's runtime path and the migration's batch path will pick up the fix automatically.

Duplicating the function bodies would create two copies of the same logic that must be kept in sync manually. Over time, independent edits to one copy without updating the other would cause the migration and the ingestor to diverge, producing inconsistent data.

### 3. Why duplication is explicitly rejected

The SKILL.md "Reuse over duplication" guidance (Step 6) is clear:

> If the dependency already exists: make the function public (`pub`, `export`, etc.) and import it rather than duplicating the code. This follows the DRY principle and ensures future bug fixes apply in one place.

Duplication or inlining would only be acceptable if adding the dependency were a new cost. Since `trustify-module-ingestor` is already a dependency of `migration`, that cost has already been paid. Copying the function bodies into the migration crate would be a strictly worse option: more code to maintain, higher risk of divergence, and no offsetting benefit.

### 4. Minimal visibility change

The change from `fn` to `pub fn` is the smallest possible API surface increase. These functions accept an `&Sbom` reference and return simple collection types (`Vec<PackageRef>`, `Vec<SupplierInfo>`), so exposing them does not leak internal implementation details or mutable state. They are pure helper functions well-suited to public reuse.

## Summary

| Factor | Assessment |
|---|---|
| Dependency exists? | Yes -- `migration/Cargo.toml` already depends on `trustify-module-ingestor` |
| Approach | Make `describing_packages()` and `suppliers()` `pub fn` in `modules/ingestor/src/graph/sbom/mod.rs`, then import in migration |
| Duplication rejected? | Yes -- violates DRY; future bug fixes would need to be applied in two places |
| New coupling introduced? | No -- the dependency relationship already exists |
