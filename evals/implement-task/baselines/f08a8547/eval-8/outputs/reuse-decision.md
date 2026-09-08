# Reuse Decision: Private Functions in the Ingestor Crate

## Task Context

TC-9206 requires the `migration` crate to extract supplier information from SBOMs during a data migration step. The `modules/ingestor` crate already contains two private helper functions that implement the exact extraction logic needed:

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`

Both functions are currently private (no `pub` visibility modifier).

## Decision

**Make the functions public (`pub fn`) and import them in the migration crate.**

Do NOT duplicate the function bodies into the migration crate.

## Rationale

This decision follows the SKILL.md Step 6 "Reuse over duplication" protocol, which prescribes a two-step analysis:

### 1. Check dependency relationship

The task description explicitly states that the `migration` crate already depends on `trustify-module-ingestor` in its `Cargo.toml`:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

This means the dependency relationship already exists. No new cross-package coupling is being introduced.

### 2. Apply the decision rule

Per SKILL.md:

> **If the dependency already exists**: make the function public (`pub`, `export`, etc.) and import it rather than duplicating the code. This follows the DRY principle and ensures future bug fixes apply in one place.

Since the dependency already exists, the rule unambiguously prescribes making the functions public and importing them.

### Why not duplicate?

Duplicating the function bodies would violate the DRY (Don't Repeat Yourself) principle without any offsetting benefit:

1. **Maintenance burden**: Any bug fix or behavioral change to the extraction logic would need to be applied in two places. If one is missed, the migration and the ingestor would silently diverge.
2. **No coupling cost**: The coupling between `migration` and `ingestor` already exists via the `Cargo.toml` dependency. Making two additional functions public does not increase the coupling surface in any meaningful way.
3. **Consistency guarantee**: By importing the same functions, the migration is guaranteed to use the same extraction logic as the ingestor, which is the correct semantic behavior -- the migration should extract supplier data exactly the way the ingestor does.

### When would duplication be acceptable?

Per the SKILL.md guidance, duplication would be the right choice if adding a new dependency were required -- i.e., if the `migration` crate did NOT already depend on `trustify-module-ingestor`. In that case, introducing a cross-package dependency for just two utility functions might not justify the additional coupling. That condition does not apply here.

## Changes Required

1. In `modules/ingestor/src/graph/sbom/mod.rs`:
   - Change `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` to `pub fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
   - Change `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` to `pub fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`
   - Ensure the types `PackageRef` and `SupplierInfo` are also publicly exported (they likely already are if used in other public APIs; verify with `find_referencing_symbols`)

2. In `migration/src/m0002_supplier/mod.rs`:
   - Add `use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};`
   - Call these imported functions instead of reimplementing the logic

## Flagging for Reviewers

Per SKILL.md: "Flag the decision -- when choosing between options 2 and 3, state the choice and rationale in the commit message or PR description so reviewers understand why code was reused or duplicated."

The commit message and PR description will explicitly state:
- That `describing_packages()` and `suppliers()` were made public rather than duplicated
- That this was done because the dependency already exists in `migration/Cargo.toml`
- That future fixes to the extraction logic will automatically apply to both the ingestor and the migration
