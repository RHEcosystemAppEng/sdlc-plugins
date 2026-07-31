# Reuse Decision: Private Functions in the Ingestor Crate

## Decision

**Make `describing_packages()` and `suppliers()` public (`pub fn`) and import them in the migration crate.** Do NOT duplicate the function bodies.

## Context

Task TC-9206 requires the migration crate (`migration/`) to extract describing packages and supplier information from ingested SBOMs. The ingestor module (`modules/ingestor/src/graph/sbom/mod.rs`) already contains two helper functions that implement exactly this logic:

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`

Both functions are currently private (no `pub` modifier), so they cannot be called from outside the ingestor crate.

## Dependency Relationship Verification

The implement-task skill's "Reuse over duplication" guidance (Step 6) requires checking whether the source package is already a dependency of the target package before deciding.

**Verified**: The `migration/Cargo.toml` already declares a dependency on the ingestor crate:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

The dependency relationship already exists. No new cross-package coupling would be introduced by reusing these functions.

## Rationale

The skill's Step 6 "Reuse over duplication" guidance provides a clear two-part decision framework:

1. **If the dependency already exists**: make the function public and import it rather than duplicating the code. This follows the DRY (Don't Repeat Yourself) principle and ensures future bug fixes apply in one place.
2. **If adding a new dependency would be required**: inlining or duplicating is acceptable, since introducing a new cross-package dependency for a single utility may not be worth the coupling.

Since the migration crate already depends on `trustify-module-ingestor`, case (1) applies. The correct action is to change the visibility of both functions from `fn` to `pub fn` and import them in the migration module.

## Why NOT Duplicate

Duplicating these functions would be the wrong choice for several reasons:

- **DRY violation**: The exact same logic would exist in two places, creating a maintenance burden.
- **Bug fix divergence**: If a bug is found in the extraction logic, it would need to be fixed in both the ingestor and the migration module. Forgetting one location leads to inconsistent behavior.
- **No coupling cost**: The dependency already exists, so making the functions public adds zero new coupling between crates. The migration crate already imports and uses types from the ingestor crate.
- **Skill guidance is explicit**: The implement-task skill unambiguously states that when the dependency exists, reuse is preferred over duplication.

## Visibility Change Impact

Making these functions `pub` has minimal risk:

- They are helper/utility functions with clear, well-scoped signatures.
- Their types (`Sbom`, `PackageRef`, `SupplierInfo`) are already part of the ingestor crate's type system.
- Adding `pub` does not change their behavior -- it only makes them callable from outside the module.
- Documentation comments should be added since they become part of the public API surface.

## Flagging for Reviewers

Per the skill's guidance, this decision will be stated in the commit message and PR description so reviewers understand why the functions were made public rather than having their logic duplicated in the migration crate.
