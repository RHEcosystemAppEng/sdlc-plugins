# Reuse Decision: Private Functions in the Ingestor Crate

## Decision

**Make the functions public and import them.** Do NOT duplicate the code.

## Functions in Question

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` in `modules/ingestor/src/graph/sbom/mod.rs`
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` in `modules/ingestor/src/graph/sbom/mod.rs`

Both are currently private (`fn`) and need to be changed to `pub fn`.

## Rationale

### 1. The dependency already exists

The `migration` crate already depends on `trustify-module-ingestor` in its `Cargo.toml`:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

This is the decisive factor. The skill's "Reuse over duplication" guidance (Step 6) establishes a clear rule:

> "If the dependency already exists: make the function public (`pub`, `export`, etc.) and import it rather than duplicating the code. This follows the DRY principle and ensures future bug fixes apply in one place."

Since no new cross-package dependency needs to be introduced, the threshold for reuse is met.

### 2. DRY principle -- single source of truth

The `describing_packages()` and `suppliers()` functions contain the canonical extraction logic for SBOM package references and supplier information. If this logic were duplicated into the migration crate:

- Bug fixes would need to be applied in two places
- Behavioral drift between the ingestor and migration versions could cause data inconsistencies
- Future changes to the SBOM data model would require parallel updates

By reusing the existing functions, the migration always stays in sync with the ingestor's extraction behavior.

### 3. Visibility change is backward-compatible

Changing `fn` to `pub fn` is a purely additive change in Rust. It does not affect existing callers within the ingestor crate -- private functions can still be called from within the same module after they are made public. No existing code breaks.

### 4. Return types must also be public

The return types `PackageRef` and `SupplierInfo` must be publicly accessible from the ingestor crate for the migration crate to use them. If these types are not already public, they need to be made public as well. This is a natural consequence of exposing the functions and is also backward-compatible.

## Why NOT duplicate

The alternative -- copying the function bodies into the migration crate -- would only be justified if:

- The migration crate did NOT already depend on the ingestor crate (introducing a new dependency for a single utility may not be worth the coupling)
- The functions were tightly coupled to ingestor-specific internals that should not be exposed

Neither condition applies here. The dependency exists, and the functions operate on public SBOM types with no ingestor-internal state.

## Implementation

1. In `modules/ingestor/src/graph/sbom/mod.rs`:
   - Change `fn describing_packages(...)` to `pub fn describing_packages(...)`
   - Change `fn suppliers(...)` to `pub fn suppliers(...)`
   - Add/update documentation comments on both functions (they are now public API)
   - Ensure `PackageRef` and `SupplierInfo` types are publicly exported

2. In `migration/src/m0002_supplier/mod.rs`:
   - Add `use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};`
   - Call the imported functions directly in the migration logic

## Flagging for Reviewers

The commit message and PR description will note this decision explicitly so that reviewers understand why the ingestor module's visibility was changed and why code was reused rather than duplicated. This follows the skill's guidance: "Flag the decision: when choosing between options, state the choice and rationale in the commit message or PR description so reviewers understand why code was reused or duplicated."
