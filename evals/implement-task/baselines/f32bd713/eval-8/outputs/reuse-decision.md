# Reuse Decision: Private Functions in the Ingestor Crate

## Decision

**Make the functions public (`pub fn`) and import them.** Do not duplicate or inline the function bodies.

## Functions in Question

Two private helper functions in `modules/ingestor/src/graph/sbom/mod.rs`:

1. `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` -- extracts the list of packages that an SBOM describes
2. `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` -- extracts supplier information from SBOM metadata

These functions implement the exact extraction logic needed by the migration step in `migration/src/m0002_supplier/mod.rs`.

## Analysis

### Step 1: Check Dependency Relationship

The migration crate's `Cargo.toml` already declares a dependency on the ingestor crate:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

The dependency relationship already exists. No new cross-crate coupling would be introduced by importing these functions.

### Step 2: Evaluate Options

**Option A -- Make functions public and import (chosen)**:
- Change `fn describing_packages(...)` to `pub fn describing_packages(...)`
- Change `fn suppliers(...)` to `pub fn suppliers(...)`
- Import in the migration crate: `use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};`

**Option B -- Duplicate the function bodies (rejected)**:
- Copy the implementation of both functions into the migration crate
- Maintain two copies of the same logic in parallel

### Step 3: Apply Decision Framework

Following the implement-task skill's "Reuse over duplication" guidance (Step 6):

> 1. **Check dependency relationship**: determine whether the source package (where the
>    function lives) is already a dependency of the target package (where you need to use it).
> 2. **If the dependency already exists**: make the function public and import it rather
>    than duplicating the code. This follows the DRY principle and ensures future bug fixes
>    apply in one place.

The dependency already exists, so the guidance is unambiguous: make the functions public and import them.

## Rationale

### DRY Principle (Don't Repeat Yourself)

The `describing_packages()` and `suppliers()` functions contain domain-specific extraction logic for parsing SBOM structures. This logic encodes knowledge about SBOM formats, field mappings, and edge cases. Duplicating it would mean:

- Two copies of the same logic to maintain
- Risk of the copies diverging when one is updated but not the other
- Bug fixes would need to be applied in two places

### Single Source of Truth

By keeping the extraction logic in the ingestor crate (where it was originally authored and where it is contextually appropriate), the ingestor remains the single source of truth for SBOM parsing logic. The migration crate consumes this logic as a client, which is the correct architectural relationship -- the migration depends on the ingestor's domain knowledge, and the dependency graph already reflects this.

### Minimal Change Surface

Making two functions public requires changing exactly two characters per function (`fn` to `pub fn`) plus adding documentation comments. Duplicating the functions would require copying potentially complex function bodies, their helper types, and any internal dependencies -- a much larger and more error-prone change.

### Backward Compatibility

Broadening visibility from private to public is always backward-compatible. Existing callers within the ingestor module are unaffected. No existing public API contracts change. The only effect is that the functions become available to downstream crates that already depend on the ingestor.

## What Would Change the Decision

If the migration crate did **not** already depend on `trustify-module-ingestor`, the decision would be different. Introducing a new cross-crate dependency solely for two utility functions could create undesirable coupling. In that case, duplicating or inlining the function bodies would be acceptable to avoid the new dependency. But since the dependency already exists, there is no additional coupling cost.
