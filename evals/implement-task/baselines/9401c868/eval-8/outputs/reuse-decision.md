# Reuse Decision -- TC-9206: Private Functions in the Ingestor Crate

## Decision

**Make the functions public (`pub fn`) and import them** in the migration crate. Do not duplicate the code.

## Functions in Question

Both functions reside in `modules/ingestor/src/graph/sbom/mod.rs`:

1. `fn describing_packages(sbom: &Sbom) -> Vec<PackageRef>` -- extracts the list of packages that an SBOM describes
2. `fn suppliers(sbom: &Sbom) -> Vec<SupplierInfo>` -- extracts supplier information from SBOM metadata

These are currently private (`fn`, not `pub fn`), meaning they can only be called from within the ingestor crate.

## Analysis

### Step 1 -- Check Dependency Relationship

The task description states that `migration/Cargo.toml` already contains:

```toml
[dependencies]
trustify-module-ingestor = { path = "../modules/ingestor" }
```

The migration crate **already depends on** the ingestor crate. No new dependency needs to be introduced.

### Step 2 -- Evaluate the Reuse-vs-Duplication Trade-off

The SKILL.md "Reuse over duplication" guidance (Step 6) defines two scenarios:

| Scenario | Guidance |
|---|---|
| Dependency already exists | Make the function public and import it (DRY principle) |
| Adding a new dependency would be required | Duplication is acceptable to avoid new coupling |

This case falls squarely into the first scenario. The dependency is already established, so making the functions public introduces zero additional coupling between the crates.

### Step 3 -- Assess Risk of Making Functions Public

**Risks (minimal)**:
- Making a private function public is a non-breaking change -- all existing callers within the ingestor crate continue to work without modification.
- The functions have clear, well-defined signatures (`&Sbom -> Vec<T>`) that represent a stable interface. They take an SBOM reference and return extracted data -- this is unlikely to change in a way that would break the migration consumer.
- The functions implement domain logic (SBOM parsing/extraction) that is inherently reusable across modules that work with SBOM data.

**Benefits**:
- **Single source of truth**: If the supplier extraction logic has a bug or needs updating (e.g., to handle a new SBOM format), fixing it in one place fixes it everywhere.
- **Consistency**: Both the ingestor's runtime path and the migration path use the exact same extraction logic, guaranteeing identical results.
- **Reduced maintenance**: No risk of the duplicated copies diverging over time.

### Step 4 -- Why Not Duplicate

Duplicating these functions would:
- Violate the DRY principle when the dependency already exists
- Create a maintenance burden: two copies of the same logic that must stay in sync
- Risk divergence: a future bug fix in one copy might not be applied to the other
- Contradict the task's own acceptance criteria, which explicitly states: "The extraction reuses the existing ingestor logic rather than duplicating it"

## Summary

| Factor | Assessment |
|---|---|
| Dependency exists? | Yes -- `trustify-module-ingestor` is already in `migration/Cargo.toml` |
| Breaking change risk? | None -- widening visibility from private to public is non-breaking |
| Logic stability? | High -- SBOM extraction is well-defined domain logic |
| Maintenance benefit? | Significant -- single source of truth for extraction logic |
| Task requirement? | Explicit -- acceptance criteria mandate reuse over duplication |

**Conclusion**: Make `describing_packages()` and `suppliers()` public in `modules/ingestor/src/graph/sbom/mod.rs` and import them in `migration/src/m0002_supplier/mod.rs`. This is the correct choice per the SKILL.md reuse-over-duplication guidance, the DRY principle, and the task's own acceptance criteria. Add doc comments to both functions since they are becoming part of the crate's public API.
