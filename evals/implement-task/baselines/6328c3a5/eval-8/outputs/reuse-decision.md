# Reuse Decision: Private Functions in the Ingestor Crate

## Functions in Question

Two private helper functions in `modules/ingestor/src/graph/sbom/mod.rs`:

1. `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` -- extracts the list of packages that an SBOM describes
2. `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` -- extracts supplier information from SBOM metadata

Both functions implement the exact extraction logic that the migration step (in `migration/src/m0002_supplier/mod.rs`) needs to populate the `sbom_supplier` table.

## Decision: Make Public and Import (Option 2)

**Make the functions `pub fn` in the ingestor crate and import them in the migration crate.**

## Rationale

### Step 1: Check Dependency Relationship

The migration crate's `Cargo.toml` already declares a dependency on the ingestor crate:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

This dependency already exists -- no new cross-package coupling is introduced.

### Step 2: Apply the DRY Principle

Since the dependency relationship is already established, making the functions public and importing them is the correct choice. This follows the **DRY (Don't Repeat Yourself) principle**:

- **Single source of truth**: The extraction logic lives in one place (`modules/ingestor/src/graph/sbom/mod.rs`). Any bug fix or improvement to the extraction algorithm automatically applies to both the ingestor's runtime usage and the migration step.
- **No drift risk**: Duplicated code inevitably diverges over time as one copy gets updated and the other does not. Making the functions public eliminates this class of bugs entirely.
- **Consistency guarantee**: Both the ingestor and the migration use identical extraction behavior, which is critical when the migration must produce results consistent with what the ingestor would generate.

### Step 3: Why Not Duplicate?

Duplicating the functions would be acceptable only if adding a new dependency were required (per the implement-task skill's "Reuse over duplication" guidance in Step 6). In this case:

- The dependency **already exists** in `migration/Cargo.toml`
- No new coupling is introduced
- The functions are pure extraction helpers with no side effects or complex state dependencies
- Duplicating would mean maintaining two copies of the same parsing logic -- a maintenance burden with no offsetting benefit

Therefore, duplication is not justified.

### Step 4: Visibility Change Impact

Changing `fn` to `pub fn` on these two functions:

- **Does not break existing callers**: Adding `pub` to a private function is a backward-compatible change. All existing internal callers continue to work identically.
- **Minimal API surface increase**: Only two focused helper functions are exposed. They have clear, self-documenting signatures and operate on well-defined input/output types.
- **Documentation obligation**: Since the functions become part of the crate's public API, documentation comments (`///`) must be added describing their purpose, parameters, and return values.

## Summary

| Criterion | Assessment |
|---|---|
| Dependency exists? | Yes -- `trustify-module-ingestor` is already in `migration/Cargo.toml` |
| New coupling introduced? | No |
| Decision | Make `pub fn` and import |
| Principle | DRY -- single source of truth for extraction logic |
| Risk of duplication | Logic drift, double maintenance, inconsistent migration results |
| Risk of making public | Minimal -- additive, backward-compatible visibility change |
