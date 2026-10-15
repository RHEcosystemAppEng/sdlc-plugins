# Reuse Decision: Private Functions in the Ingestor Crate

## Context

Task TC-9206 requires the `migration` crate to extract describing packages and supplier
information from ingested SBOMs. The `modules/ingestor/src/graph/sbom/mod.rs` file
already contains two private helper functions that implement this exact logic:

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`

These functions are currently private (no `pub` modifier), so they cannot be imported
by the `migration` crate.

## Decision

**Make the functions public and import them.** Do not duplicate the code.

Change the visibility of both functions from `fn` to `pub fn` in
`modules/ingestor/src/graph/sbom/mod.rs`, then import them in the migration crate via:

```rust
use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};
```

## Rationale

This decision follows the implement-task skill's "Reuse over duplication" guidance
(Step 6), which prescribes a two-step analysis:

### Step 1: Check the dependency relationship

The `migration` crate's `Cargo.toml` already declares a dependency on the ingestor:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

The dependency already exists. No new cross-package coupling is introduced.

### Step 2: Apply the decision rule

Per the skill's guidance:

> "If the dependency already exists: make the function public (pub, export, etc.)
> and import it rather than duplicating the code. This follows the DRY principle
> and ensures future bug fixes apply in one place."

Since the dependency is already declared, making the functions public is the correct
choice.

### Why not duplicate

Duplicating the extraction logic would create two copies of the same algorithm in two
crates. This leads to:

1. **Divergence risk**: A bug fix or behavior change in the ingestor's version would
   not automatically propagate to the migration's copy, creating silent inconsistencies.
2. **Maintenance burden**: Any future change to the SBOM supplier extraction logic
   would need to be applied in two places.
3. **Unnecessary code**: The functions already exist and are tested. Copying them adds
   dead weight with no functional benefit.

### Why not create a shared utility crate

Extracting the functions into a new shared utility crate would be over-engineering for
this case. The dependency already flows in the right direction (migration depends on
ingestor), and the functions are semantically part of the ingestor's domain. A shared
crate would add build complexity and a new package to maintain for no practical gain.

## Risk Assessment

**Risk: Expanding the ingestor crate's public API surface**

Making private functions public increases the API surface of `trustify-module-ingestor`.
This is a minor concern because:

- The functions are pure helpers with well-defined inputs and outputs
- They operate on the crate's own domain types (`Sbom`, `PackageRef`, `SupplierInfo`)
- The visibility change is strictly additive -- it cannot break existing code
- If future API stability is a concern, the functions could be placed behind a
  `pub(crate)` or feature-gated `pub` visibility, but for an internal workspace crate
  this is unnecessary

**Risk: Module path visibility**

The intermediate modules (`graph`, `sbom`) must also be `pub` for the functions to be
accessible from outside the crate. Verify the module declarations in:

- `modules/ingestor/src/lib.rs` -- needs `pub mod graph;`
- `modules/ingestor/src/graph/mod.rs` -- needs `pub mod sbom;`

If these are not already public, they would need to be changed as well (still within
the "Files to Modify" scope since the task lists `modules/ingestor/src/graph/sbom/mod.rs`).

## Summary

| Factor | Value |
|--------|-------|
| Dependency exists? | Yes (`trustify-module-ingestor` in migration's `Cargo.toml`) |
| Decision | Make public and import |
| Functions affected | `describing_packages()`, `suppliers()` |
| Code duplication avoided | Yes |
| New dependencies introduced | None |
| Breaking changes | None (additive visibility change only) |
