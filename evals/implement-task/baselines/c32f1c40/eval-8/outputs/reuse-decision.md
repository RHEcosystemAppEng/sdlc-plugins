# Reuse Decision: Private Functions in the Ingestor Crate

## Decision

**Make the functions public and import them.** Do not duplicate the code.

## Functions in Question

1. `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` in `modules/ingestor/src/graph/sbom/mod.rs`
2. `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` in `modules/ingestor/src/graph/sbom/mod.rs`

Both are currently private (no `pub` modifier) and need to be used by the migration crate
at `migration/src/m0002_supplier/mod.rs`.

## Analysis

The implement-task skill defines a clear decision framework in Step 6 under "Reuse over
duplication":

> 1. **Check dependency relationship**: determine whether the source package (where the
>    function lives) is already a dependency of the target package (where you need to use it).
> 2. **If the dependency already exists**: make the function public and import it rather
>    than duplicating the code.
> 3. **If adding a new dependency would be required**: inlining or duplicating is acceptable.

### Dependency Check

The `migration` crate's `Cargo.toml` already contains:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

The dependency relationship already exists. No new coupling is introduced by making
these functions public.

### Why Reuse (pub + import)

1. **DRY principle**: The functions implement the exact extraction logic needed. Duplicating
   them means maintaining identical logic in two places. A bug fix in one copy would need to
   be applied to the other -- a common source of drift-related defects.

2. **No new coupling**: The migration crate already depends on the ingestor crate. Making
   two functions public adds no new dependency edges to the crate graph. The only change is
   increasing the surface area of an existing dependency.

3. **Semantic correctness**: The migration is explicitly intended to replicate the same
   extraction logic the ingestor uses. Using the same functions guarantees identical behavior.
   Duplicated code could subtly diverge over time if one copy is updated but not the other.

4. **Task description alignment**: The task's Implementation Notes explicitly state:
   "Since the dependency already exists, make the functions public and import them rather
   than duplicating the code."

### Why Not Duplicate

Duplication would be appropriate if:

- The `migration` crate did not already depend on `trustify-module-ingestor` (introducing
  a new cross-crate dependency for two utility functions would create coupling that may
  not be worth it).
- The functions needed to behave differently in the migration context (e.g., different
  error handling or data transformation). The task description does not indicate this.
- The functions had complex internal dependencies that would require exposing additional
  private types or modules. Based on the signatures (`&Sbom -> Vec<PackageRef>` and
  `&Sbom -> Vec<SupplierInfo>`), the types involved are likely already public since
  they appear in the function signatures.

None of these conditions apply here.

## Implementation

1. In `modules/ingestor/src/graph/sbom/mod.rs`:
   - Change `fn describing_packages(` to `pub fn describing_packages(`
   - Change `fn suppliers(` to `pub fn suppliers(`
   - Add documentation comments to both functions (they become part of the crate's
     public API and must be documented per the skill's code quality practices)

2. In `migration/src/m0002_supplier/mod.rs`:
   - Import both functions: `use trustify_module_ingestor::graph::sbom::{describing_packages, suppliers};`
   - Call them directly in the migration logic

3. Verify no other callers are affected by the visibility change (making a private function
   public is backward-compatible -- no existing callers break).

## Risk Assessment

**Low risk.** Making a private function public is a purely additive change. No existing
code is affected. The only consideration is that the functions become part of the crate's
public API contract, meaning future changes to their signatures would need to consider
the migration crate as a consumer. This is acceptable because:

- The migration crate is in the same workspace and can be updated together.
- The functions implement stable, well-defined extraction logic unlikely to change frequently.
