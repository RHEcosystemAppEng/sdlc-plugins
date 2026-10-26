# Reuse Decision: Private Functions in the Ingestor Crate

## Decision

**Make the functions public (`pub fn`) and import them** rather than duplicating them in
the migration crate.

## Functions in Question

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` in `modules/ingestor/src/graph/sbom/mod.rs`
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` in `modules/ingestor/src/graph/sbom/mod.rs`

Both are currently private (no `pub` modifier) and implement the exact extraction logic
the migration needs.

## Analysis

Following the "Reuse over duplication" guidance from the implement-task skill (Step 6):

### 1. Check dependency relationship

The migration crate's `Cargo.toml` already declares a dependency on the ingestor module:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

The dependency already exists. No new cross-package coupling is introduced by using it.

### 2. Dependency already exists -- make functions public

Since `trustify-module-ingestor` is already a dependency of the migration crate, the
skill guidance is clear: **make the functions public and import them** rather than
duplicating the code.

Benefits:
- **DRY principle**: The extraction logic lives in one place. If a bug is found or the
  SBOM format evolves, the fix applies everywhere automatically.
- **No new coupling**: The dependency edge already exists in the crate graph. Making two
  functions public does not change the dependency structure at all.
- **Minimal change surface**: Changing `fn` to `pub fn` is a two-line diff in the
  ingestor module. Duplication would copy the full function bodies (potentially dozens of
  lines of parsing logic) into the migration crate.
- **Consistency**: Both the ingestor's runtime path and the migration's backfill path
  will use identical extraction logic, preventing subtle divergence.

### 3. Why not duplicate

Duplicating would be acceptable only if adding a new dependency were required (per the
skill guidance). Since the dependency already exists, duplication would:
- Violate DRY unnecessarily
- Create a maintenance burden: future changes to extraction logic would need to be
  applied in two places
- Risk subtle divergence if one copy is updated but the other is not

### 4. Risk Assessment

Making private functions public is a purely additive, non-breaking change:
- No existing callers are affected (the functions had no external callers before)
- The function signatures do not change
- The ingestor crate's existing tests continue to pass unchanged
- The only risk is that other crates could now also call these functions, but since they
  are pure helper functions with no side effects, this is desirable rather than risky

## Summary

| Factor | Verdict |
|--------|---------|
| Dependency exists? | Yes -- `trustify-module-ingestor` is already in `migration/Cargo.toml` |
| Change required | `fn` to `pub fn` on two functions (two-line diff) |
| Duplication cost | Copy full extraction logic (risk of divergence, violates DRY) |
| Decision | Make public and import |
| Rationale | Dependency already exists; reuse avoids duplication per skill guidance |
