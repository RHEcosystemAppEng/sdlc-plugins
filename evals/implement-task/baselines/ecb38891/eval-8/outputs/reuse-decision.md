# Reuse Decision: Private Functions in the Ingestor Crate

## Context

Task TC-9206 requires the migration crate to extract describing packages and supplier information from ingested SBOMs. The ingestor module (`modules/ingestor/src/graph/sbom/mod.rs`) already contains two private helper functions that implement the exact extraction logic needed:

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` — extracts the list of packages that an SBOM describes
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` — extracts supplier information from SBOM metadata

Both functions are currently private (`fn`, not `pub fn`), meaning they cannot be imported by other crates.

## Decision: Make Public and Import (Not Duplicate)

**Recommendation: Make `describing_packages()` and `suppliers()` public (`pub fn`) in `modules/ingestor/src/graph/sbom/mod.rs` and import them in the migration crate.**

Duplication is explicitly rejected. The function bodies must not be copied or inlined into the migration crate.

## Rationale

### 1. Dependency Already Exists

The first step in the SKILL.md "Reuse over duplication" guidance is to check the dependency relationship. Verified that `migration/Cargo.toml` already declares a dependency on `trustify-module-ingestor`:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

Since the migration crate already depends on the ingestor crate, making the functions public introduces zero new coupling. The dependency relationship is already established, so reuse carries no architectural cost.

### 2. DRY Principle

The DRY (Don't Repeat Yourself) principle dictates that every piece of knowledge should have a single, authoritative representation. Duplicating `describing_packages()` and `suppliers()` would create two copies of the same extraction logic, violating DRY.

Making the functions public ensures that future bug fixes, performance improvements, or behavioral changes to the extraction logic apply in exactly one place. If the functions were duplicated, a bug fix in the ingestor copy could be missed in the migration copy (or vice versa), leading to subtle inconsistencies between ingestion-time and migration-time behavior.

### 3. SKILL.md Guidance

The SKILL.md Step 6 "Reuse over duplication" section provides clear decision criteria:

> 1. **Check dependency relationship**: determine whether the source package is already a dependency of the target package.
> 2. **If the dependency already exists**: make the function public and import it rather than duplicating the code. This follows the DRY principle and ensures future bug fixes apply in one place.
> 3. **If adding a new dependency would be required**: inlining or duplicating is acceptable.

Since the dependency already exists (criterion 1), criterion 2 applies: make public and import.

### 4. Why Not Duplicate

Duplication would be acceptable only if adding a new cross-package dependency were required (criterion 3 from SKILL.md). That is not the case here. Duplicating the functions would:

- Create a maintenance burden: two identical function bodies to keep in sync
- Risk divergence: future changes to extraction logic could be applied to one copy but not the other
- Violate the task's own Acceptance Criteria, which states: "The extraction reuses the existing ingestor logic rather than duplicating it"

## Implementation

1. In `modules/ingestor/src/graph/sbom/mod.rs`, change:
   - `fn describing_packages(...)` to `pub fn describing_packages(...)`
   - `fn suppliers(...)` to `pub fn suppliers(...)`
   - Add doc comments to both functions since they are now part of the public API

2. In `migration/src/m0002_supplier/mod.rs`, add:
   - `use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};`
   - Call the imported functions directly in the migration step

No new dependencies are added. No code is duplicated.
