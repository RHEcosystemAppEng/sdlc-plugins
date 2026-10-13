# Reuse Decision: `describing_packages()` and `suppliers()` functions

## Context

Task TC-9206 requires the migration crate (`migration/`) to extract describing packages and supplier information from ingested SBOMs. The ingestor module (`modules/ingestor/src/graph/sbom/mod.rs`) already contains two private helper functions that implement exactly this logic:

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`

These functions are currently private (no `pub` modifier), so they cannot be imported by other crates.

## Dependency Check

The migration crate's `Cargo.toml` already declares a dependency on the ingestor crate:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

This means `migration/` can already import any public symbol from `trustify-module-ingestor`. No new dependency needs to be introduced.

## Decision: Make Functions Public and Import Them

**Recommendation:** Change `fn describing_packages(...)` and `fn suppliers(...)` to `pub fn` in `modules/ingestor/src/graph/sbom/mod.rs`, then import and call them from `migration/src/m0002_supplier/mod.rs`.

**Duplication is explicitly rejected.** The function bodies must NOT be copied, inlined, or reimplemented in the migration crate.

## Rationale

### 1. The dependency already exists

Per the SKILL.md Step 6 "Reuse over duplication" guidance: "If the dependency already exists: make the function public (`pub`, `export`, etc.) and import it rather than duplicating the code." Since `migration/Cargo.toml` already depends on `trustify-module-ingestor`, the only barrier to reuse is the `pub` visibility modifier. Removing that barrier is a one-word change per function.

### 2. DRY principle -- bug fixes apply in one place

Making the functions public and importing them ensures there is exactly one implementation of the describing-packages and supplier-extraction logic. If a bug is discovered in either function, fixing it in `modules/ingestor/src/graph/sbom/mod.rs` automatically fixes it for both the ingestor's own usage and the migration's usage. Duplication would require finding and fixing the same bug in two places -- a maintenance hazard that grows worse over time.

### 3. Widening visibility is backward-compatible

Changing a Rust function from `fn` to `pub fn` is a strictly additive, backward-compatible change. All existing internal callers continue to work identically. No existing API contracts are broken. The only effect is that the function becomes available to external crates -- which is exactly what we need.

### 4. Why duplication is wrong here

Duplicating the function bodies into the migration crate would:
- Violate the DRY principle by maintaining two copies of identical logic
- Create a risk of the copies diverging silently over time
- Increase the surface area for bugs (fix in one place, miss the other)
- Add unnecessary code to the migration crate when a clean import is available
- Contradict the SKILL.md guidance, which states duplication is only acceptable when "adding a new dependency would be required" -- which is not the case here

## Summary

| Option | Verdict | Reason |
|--------|---------|--------|
| Make `pub` and import | **Accepted** | Dependency exists; DRY; single source of truth; backward-compatible |
| Copy/inline function bodies | **Rejected** | Violates DRY; maintenance hazard; unnecessary when dependency exists |
| Add a new shared crate | **Rejected** | Over-engineering; direct dependency already in place |
