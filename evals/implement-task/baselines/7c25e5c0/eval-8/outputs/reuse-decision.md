# Reuse Decision — Private Functions in Ingestor Crate

## Functions in Question

Two private functions in `modules/ingestor/src/graph/sbom/mod.rs`:
- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`

Both implement the exact extraction logic needed by the migration crate in `migration/src/m0002_supplier/mod.rs`.

## Dependency Relationship Check

**Verified**: The `migration` crate already depends on `trustify-module-ingestor` in its `Cargo.toml`:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

This existing dependency means importing from the ingestor module introduces **no new coupling** — the relationship already exists in the dependency graph.

## Decision: Make Public (`pub fn`) and Import

**Recommendation**: Change `describing_packages()` and `suppliers()` from `fn` to `pub fn` and import them in the migration crate.

**Rejected alternative**: Duplicating (copying/inlining) the function bodies into the migration crate.

## Rationale

1. **Dependency already exists**: Since `migration/Cargo.toml` already lists `trustify-module-ingestor` as a dependency, making the functions public and importing them does not introduce a new cross-package dependency. This is the key factor — per the implement-task skill's "Reuse over duplication" guidance (Step 6), when the dependency already exists, make the function public and import rather than duplicating.

2. **DRY principle**: The `describing_packages()` and `suppliers()` functions contain non-trivial extraction logic. Duplicating them would create two copies of the same logic that must be maintained in sync. If a bug is found in the extraction logic, fixing it in one place (`modules/ingestor/src/graph/sbom/mod.rs`) ensures the fix applies everywhere — both in ingestion and migration paths.

3. **Single source of truth**: The ingestor module is the authoritative source for SBOM parsing and extraction logic. The migration should defer to it rather than re-implementing the same behavior, which could drift over time.

4. **Minimal change**: Changing `fn` to `pub fn` is a two-word change per function. The function bodies, signatures, and return types remain unchanged. This is far less invasive than copying the entire implementation.

## Why Not Duplicate

Duplication would be acceptable only if adding a new cross-package dependency were required (per Step 6 guidance). Since the dependency from `migration` to `trustify-module-ingestor` already exists, duplication would:
- Violate the DRY principle unnecessarily
- Create maintenance risk — future bug fixes would need to be applied in two places
- Add more code to the migration crate without justification

The implement-task skill explicitly states: "If the dependency already exists: make the function public (pub, export, etc.) and import it rather than duplicating the code."
