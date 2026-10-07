# Reuse Decision: describing_packages() and suppliers()

## Decision

Make `describing_packages()` and `suppliers()` public (`pub fn`) in
`modules/ingestor/src/graph/sbom/mod.rs` and import them into the migration
crate. Do **not** duplicate or inline the function bodies.

## Context

The task (TC-9206) requires the migration crate to extract describing packages
and supplier information from ingested SBOMs. The ingestor module already
contains two private helper functions that implement this exact logic:

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>`
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>`

These functions are currently private (no `pub` modifier) in
`modules/ingestor/src/graph/sbom/mod.rs`, so they cannot be called from the
migration crate.

## Dependency verification

The key factor in this decision is the existing dependency relationship.
Checking `migration/Cargo.toml` confirms:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

The `migration` crate **already depends on** `trustify-module-ingestor`. This
means making the functions public and importing them introduces zero new
coupling -- the crate relationship is already established. No changes to
`Cargo.toml` are needed.

## Why pub over duplication

### 1. The dependency already exists

Since `migration` already depends on `trustify-module-ingestor`, the coupling
cost of reusing these functions is zero. There is no new dependency to introduce,
no new edge in the crate graph, and no risk of creating a circular dependency.
This is the primary reason for choosing reuse: the import path is already
available and paid for.

### 2. DRY principle

Duplicating the function bodies would create two copies of the same extraction
logic in two different crates. This violates the DRY (Don't Repeat Yourself)
principle and creates a maintenance burden: any future bug fix or behavioral
change to the extraction logic would need to be applied in two places. By
making the functions public and importing them, future fixes apply in exactly
one place -- the canonical implementation in the ingestor crate.

### 3. Consistency guarantee

The migration's purpose is to extract supplier data in the same way the ingestor
does. Using the same functions guarantees identical behavior. Duplicated code
would risk subtle divergence over time as one copy is updated but the other is
forgotten.

## Why not duplication

Duplication (copying the function bodies into the migration crate) would be
acceptable only if adding a new dependency were required -- per the skill's
"Reuse over duplication" guidance, introducing a new cross-package dependency
for a single utility may not be worth the coupling. However, that concern does
not apply here because the dependency already exists. Duplication is therefore
explicitly rejected.

## Risks and mitigations

- **API stability**: making a previously private function public expands the
  crate's public API surface. Mitigation: these are focused helper functions
  with clear semantics. If future API stability is a concern, they could be
  placed behind a `pub(crate)` re-export boundary, but for now `pub` is the
  simplest correct choice since cross-crate access is needed.
- **Breaking changes**: widening visibility from `fn` to `pub fn` is a
  backward-compatible change. No existing callers are affected.

## Summary

| Option | New dependency needed? | Maintenance cost | Decision |
|--------|----------------------|------------------|----------|
| Make `pub` and import | No (already exists) | Single source of truth | **Selected** |
| Duplicate function bodies | N/A | Two copies to maintain | Rejected |

The existing dependency between `migration` and `trustify-module-ingestor` makes
reuse the clear choice. Making the functions public follows the DRY principle and
ensures that bug fixes and improvements to the extraction logic automatically
benefit both the ingestor and the migration.
