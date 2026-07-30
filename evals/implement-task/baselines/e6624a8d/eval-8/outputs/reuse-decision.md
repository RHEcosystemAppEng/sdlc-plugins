# Reuse Decision: Private Functions in the Ingestor Crate

## Decision

**Make the functions public and import them.** Do not duplicate.

## Functions in Question

- `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` in `modules/ingestor/src/graph/sbom/mod.rs`
- `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` in `modules/ingestor/src/graph/sbom/mod.rs`

Both are currently private (`fn`, not `pub fn`). The migration crate (`migration/src/m0002_supplier/mod.rs`) needs to use them.

## Analysis

### Step 1: Check Dependency Relationship

The `migration` crate's `Cargo.toml` already contains:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

The dependency relationship already exists. No new cross-package dependency needs to be introduced.

### Step 2: Evaluate the Options

**Option A -- Make public and import (chosen)**:
- Change `fn` to `pub fn` on both functions in the ingestor module
- Add `use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};` in the migration module
- Minimal code change: two keywords changed, one import added
- Future bug fixes to the extraction logic apply in one place
- Follows the DRY principle
- No risk of the two copies diverging over time

**Option B -- Duplicate the functions (rejected)**:
- Copy both function implementations into the migration crate
- Would create two independent copies of the same extraction logic
- Future changes to extraction logic would need to be applied in two places
- Risk of the copies diverging, leading to subtle bugs where the ingestor and migration produce different results
- No benefit: the dependency already exists, so duplication adds maintenance burden with no reduction in coupling

### Step 3: Decision Rationale

Per the implement-task skill's "Reuse over duplication" guidance:

> If the dependency already exists: make the function public (pub, export, etc.) and import it rather than duplicating the code. This follows the DRY principle and ensures future bug fixes apply in one place.

All criteria for reuse are met:
1. The dependency from `migration` to `trustify-module-ingestor` already exists in `Cargo.toml`
2. The functions implement the exact logic needed -- no adaptation or wrapping is required
3. Making them public is backward-compatible -- all existing internal call sites continue to work unchanged
4. The visibility change is minimal and low-risk

### Step 4: Risk Assessment

**Risk of making functions public**: Low. The functions become part of the crate's public API, which means future changes to their signatures would need to consider external callers. However, since the ingestor and migration crates are in the same workspace and maintained together, this is a manageable constraint. If needed, a `pub(crate)` to `pub` change could later be refined to `pub(in crate::graph)` if tighter visibility scoping is desired, but for now `pub` is the simplest correct choice.

**Risk of duplication (avoided)**: Medium-to-high. Two copies of extraction logic in different crates would likely diverge over time. A bug fix in the ingestor's copy might not be applied to the migration's copy, leading to inconsistent supplier data depending on whether it was extracted during ingestion or migration.

## Summary

| Factor | Make Public | Duplicate |
|---|---|---|
| Dependency exists | Yes -- no new coupling | N/A -- coupling irrelevant |
| Code maintenance | Single source of truth | Two copies to maintain |
| Divergence risk | None | Medium-to-high |
| Change size | 2 keyword changes + 1 import | ~50+ lines copied |
| Backward compatibility | Fully compatible | N/A |

**Verdict**: Make `describing_packages()` and `suppliers()` public in `modules/ingestor/src/graph/sbom/mod.rs` and import them in the migration crate. This is the correct choice given the existing dependency relationship.
