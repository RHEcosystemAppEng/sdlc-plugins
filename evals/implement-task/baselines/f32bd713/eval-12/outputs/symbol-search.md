# Symbol Deduplication Analysis: SEVERITY_ORDER

## Search Objective

Before declaring any new `SEVERITY_ORDER` constant in the SBOM service module, search the
target package (`modules/fundamental`) for an existing definition. The task description
explicitly references a severity ordering constant in the advisory module -- this search
confirms its location and determines the reuse strategy.

## Search Scope

Searched the entire `modules/fundamental/` crate, which contains both the `sbom` and
`advisory` modules. This is the correct scope because both modules live in the same Rust
crate and can share symbols without introducing a new cross-crate dependency.

## Search Methods

1. **Serena `find_symbol`**: searched for symbol `SEVERITY_ORDER` across the
   `modules/fundamental` crate using the `serena_backend` instance.
2. **Serena `search_for_pattern`**: searched for the pattern `SEVERITY_ORDER` across
   `modules/fundamental/src/` to catch any non-symbolic references (comments, string
   literals, documentation).
3. **Grep fallback**: searched for variations `SEVERITY_ORDER`, `severity_order`,
   `SeverityOrder` across the full `modules/` directory tree to ensure no other module
   defines its own copy.

## Search Results

| Location | Symbol | Visibility | Definition |
|---|---|---|---|
| `modules/fundamental/src/advisory/service/advisory.rs` | `SEVERITY_ORDER` | crate-private (no `pub`) | `const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];` |

No other definitions of `SEVERITY_ORDER` or equivalent severity-ordering constants were
found anywhere in the `modules/` directory tree.

## Reuse Decision

**Decision: Export and reuse the existing constant. Do NOT declare a new one.**

### Rationale

1. **Same crate**: Both `advisory` and `sbom` modules live within the `modules/fundamental`
   crate. No new cross-crate dependency is needed -- only a visibility change.
2. **DRY principle**: The constant encodes domain knowledge (severity ranking). Having two
   copies risks them diverging silently if one is updated and the other is not.
3. **Minimal change**: Adding `pub` to the existing declaration is a one-keyword change
   with zero behavioral impact on the advisory module.
4. **SKILL.md guidance**: The "Reuse over duplication" section (Step 6) directs: "If the
   dependency already exists: make the function public and import it rather than duplicating
   the code."

### Implementation

1. In `modules/fundamental/src/advisory/service/advisory.rs`: change
   `const SEVERITY_ORDER` to `pub const SEVERITY_ORDER` so it is visible to sibling modules
   within the same crate.
2. In `modules/fundamental/src/sbom/service/sbom.rs`: import the constant via
   `use crate::advisory::service::advisory::SEVERITY_ORDER;` (or re-export through the
   advisory module's public API if the module structure requires it).
3. Verify with `find_referencing_symbols` that no existing callers are broken by the
   visibility change (widening visibility from private to public is always backward-compatible).

### Rejected Alternative

Declaring a new `SEVERITY_ORDER` in `sbom/service/sbom.rs` was rejected because:
- It violates the task's acceptance criterion: "The severity ordering uses the existing
  SEVERITY_ORDER constant from the advisory module -- no duplicate definition."
- It introduces a maintenance burden: two constants encoding the same domain rule.
- It conflicts with the skill's symbol deduplication guidance.
