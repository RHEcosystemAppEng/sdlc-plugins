# Reuse Decision: Private Functions in Ingestor Crate

## Context

Task TC-9206 requires the migration crate to extract describing packages and supplier
information from ingested SBOMs. The ingestor crate (`modules/ingestor/src/graph/sbom/mod.rs`)
already contains two private helper functions that implement exactly this logic:

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`

Both functions are currently private (no `pub` keyword).

## Decision: Make public and import (Option 2)

**Make the functions `pub` in the ingestor crate and import them in the migration crate.**

## Rationale

Following the implement-task skill's "Reuse over duplication" guidance (Step 6):

### Step 1 -- Check dependency relationship

The migration crate's `Cargo.toml` already declares a dependency on the ingestor crate:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

This is confirmed directly in the task's Implementation Notes. The dependency relationship
already exists -- no new cross-package coupling is introduced.

### Step 2 -- Dependency already exists: make public and import

Since `trustify-module-ingestor` is already a dependency of the migration crate, the
skill prescribes:

> "make the function public (`pub`, `export`, etc.) and import it rather than
> duplicating the code. This follows the DRY principle and ensures future bug fixes
> apply in one place."

This is the correct choice because:

1. **No new coupling**: The migration crate already depends on the ingestor crate. Making
   two functions public does not create any new inter-crate dependency.

2. **DRY principle**: The extraction logic in `describing_packages()` and `suppliers()`
   encodes specific SBOM parsing rules. Duplicating this logic would create two copies
   that must be kept in sync -- any bug fix or format change would need to be applied
   in both places.

3. **Single source of truth**: If the SBOM format evolves or the extraction logic is
   refined, having one implementation in the ingestor crate means the migration
   automatically benefits from improvements.

4. **Minimal change**: The only modification needed in the ingestor crate is changing
   `fn` to `pub fn` on two functions. This is a purely additive change that cannot break
   existing callers within the ingestor crate.

### Why not duplicate (Option 3)?

Option 3 (duplicate/inline) is acceptable when "adding a new dependency would be required"
and "introducing a new cross-package dependency for a single utility may not be worth the
coupling." Neither condition applies here:

- The dependency already exists in `Cargo.toml`
- No new coupling is introduced
- These are not single-use throwaway utilities -- they implement domain-specific SBOM
  parsing logic that should remain canonical

Duplicating would violate DRY without any offsetting benefit.

## Impact Assessment

### Backward compatibility

Changing `fn` to `pub fn` is strictly additive in Rust. It increases visibility without
altering behavior. No existing code within the ingestor crate is affected -- internal
callers continue to work identically. No external callers existed before (the functions
were private), so there are no callers to break.

### API surface

Making these functions public does expand the ingestor crate's public API. This is an
intentional and justified change: the functions implement reusable SBOM parsing logic that
is useful beyond the ingestor's own ingestion pipeline. Adding documentation comments to
the newly-public functions ensures the expanded API is well-documented.

### Future maintenance

With a single implementation, future changes to SBOM parsing logic (format updates,
bug fixes, performance improvements) automatically propagate to all consumers, including
the migration crate.

## Summary

| Factor | Make public | Duplicate |
|--------|-----------|-----------|
| New dependency required? | No | N/A |
| Code duplication | None | Two copies to maintain |
| Bug fix propagation | Automatic | Manual, error-prone |
| API surface increase | Minimal (2 functions) | None |
| Skill guidance | Recommended (Step 6, option 2) | Not applicable |

**Decision: Make `describing_packages()` and `suppliers()` public in the ingestor crate
and import them in the migration crate.**
