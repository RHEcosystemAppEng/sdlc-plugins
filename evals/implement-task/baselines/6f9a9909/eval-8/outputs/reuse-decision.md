# Reuse Decision: Private Functions in the Ingestor Crate

## Decision

**Make the functions public and import them.** Do not duplicate.

## Functions in Question

| Function | Location | Current Visibility |
|---|---|---|
| `describing_packages(sbom: &Sbom) -> Vec<PackageRef>` | `modules/ingestor/src/graph/sbom/mod.rs` | private (`fn`) |
| `suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` | `modules/ingestor/src/graph/sbom/mod.rs` | private (`fn`) |

## Analysis

### Step 1: Check dependency relationship

The task description explicitly states that the `migration` crate already depends on `trustify-module-ingestor` in its `Cargo.toml`:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

The dependency relationship already exists. No new cross-crate dependency needs to be introduced.

### Step 2: Apply the "Reuse over duplication" rule

The implement-task skill (Step 6, "Reuse over duplication") defines a clear decision framework:

> 1. Check dependency relationship: determine whether the source package is already a dependency of the target package.
> 2. If the dependency already exists: make the function public and import it rather than duplicating the code. This follows the DRY principle and ensures future bug fixes apply in one place.
> 3. If adding a new dependency would be required: inlining or duplicating the function is acceptable.

Since the dependency already exists (condition 2 applies), the correct action is to make the functions public and import them.

### Step 3: Evaluate risks of making functions public

**Risk: expanding the public API surface of the ingestor crate.**

- These functions perform pure data extraction (parsing SBOM structures into typed results). They have no side effects, no database access, and no state mutation.
- Making them public is an additive, non-breaking change. All existing internal callers continue to work identically.
- The functions encapsulate domain logic that is genuinely shared between ingestion and migration -- they are not implementation details that happen to be useful elsewhere. Their purpose (extracting describing packages and suppliers from an SBOM) is a well-defined, stable operation.

**Conclusion:** The risk is minimal and acceptable. The functions represent stable, well-defined domain logic.

### Step 4: Evaluate the alternative (duplication)

If we duplicated the functions instead:

- **Maintenance burden:** Bug fixes or behavior changes to SBOM parsing would need to be applied in two places. A fix in the ingestor would not automatically propagate to the migration.
- **Consistency risk:** Over time, the two copies could diverge, leading to different extraction results between ingestion and migration -- a subtle and hard-to-diagnose data integrity issue.
- **Code review burden:** Reviewers would need to verify that the duplicated code is identical to the original and flag any drift.
- **Violation of DRY:** The project already has the dependency wired up. Duplicating code that is one import away is unjustified.

## Summary

| Factor | Make Public | Duplicate |
|---|---|---|
| Dependency exists? | Yes -- no new coupling | N/A |
| DRY compliance | Yes | No -- two copies of same logic |
| Bug fix propagation | Automatic -- single source | Manual -- must update both |
| Breaking change risk | None -- additive change | None |
| API surface concern | Minimal -- stable domain logic | None |
| Skill guidance | Preferred (rule 2) | Acceptable only when dependency is new (rule 3) |

**Final decision: Make `describing_packages()` and `suppliers()` public (`pub fn`) and import them in the migration crate.** This is the correct choice per the skill's reuse-over-duplication framework, the existing dependency relationship, and software engineering best practices.

The decision will be flagged in the commit message and PR description so reviewers understand the rationale for the visibility change in the ingestor crate.
