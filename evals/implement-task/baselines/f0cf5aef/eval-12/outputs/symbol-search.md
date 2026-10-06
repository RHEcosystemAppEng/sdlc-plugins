# Symbol Deduplication Analysis for TC-9210

## Search Process

### Target Symbol: SEVERITY_ORDER

The task description references a `SEVERITY_ORDER` constant needed to sort advisories
by severity (Critical > High > Medium > Low > None). Before declaring a new constant,
the implement-task skill's Step 6 "Symbol deduplication" guidance requires searching the
target package for an existing definition.

### Searches Performed

1. **Grep for `SEVERITY_ORDER` across the entire `modules/` directory**
   - Tool: `search_for_pattern` (Serena) or Grep
   - Pattern: `SEVERITY_ORDER`
   - Scope: `modules/fundamental/src/` (the entire fundamental crate, which contains
     both the `advisory` and `sbom` modules)

2. **Grep for common naming variations**
   - Patterns searched: `SEVERITY_ORDER`, `severity_order`, `SeverityOrder`, `SEVERITY_LEVELS`,
     `severity_levels`, `SEVERITY_WEIGHTS`, `severity_weights`
   - Scope: `modules/fundamental/src/`

3. **find_symbol for `SEVERITY_ORDER` in the advisory service**
   - Tool: `mcp__serena_backend__find_symbol`
   - Symbol: `SEVERITY_ORDER`
   - Scope: `modules/fundamental/src/advisory/service/advisory.rs`

### Where It Was Found

**File:** `modules/fundamental/src/advisory/service/advisory.rs`
**Definition:** `SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]`
**Visibility:** Defined in the advisory service module within the `modules/fundamental` crate.

Both `sbom` and `advisory` are sibling modules within the same crate
(`modules/fundamental`). This means `SEVERITY_ORDER` is accessible without adding a
new cross-crate dependency -- it only requires that the constant be publicly exported
from the advisory module.

### Decision: Reuse Existing Constant

**Decision:** Import and reuse the existing `SEVERITY_ORDER` from the advisory module.
Do NOT declare a duplicate constant in `sbom/service/sbom.rs` or any other file.

**Rationale:**
- The constant already exists with the exact values needed (critical, high, medium, low, none).
- Both `advisory` and `sbom` are sibling modules in the same crate (`modules/fundamental`),
  so no new cross-crate dependency is needed.
- The task description's Acceptance Criteria explicitly state: "The severity ordering uses
  the existing `SEVERITY_ORDER` constant from the advisory module -- no duplicate definition."
- Per the implement-task skill's "Reuse over duplication" guidance: when the source package
  is already a dependency of the target package, make the function/constant public and import
  it rather than duplicating.

### Required Visibility Changes

If `SEVERITY_ORDER` is not currently `pub`, it must be made public:

1. In `modules/fundamental/src/advisory/service/advisory.rs`: change the declaration to
   `pub const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];`
2. In `modules/fundamental/src/advisory/service/mod.rs`: ensure the constant is re-exported
   (e.g., `pub use advisory::SEVERITY_ORDER;` or the module is declared `pub`).
3. In `modules/fundamental/src/advisory/mod.rs`: ensure the `service` module is publicly
   accessible so that `sbom` code can reach the constant via
   `crate::advisory::service::SEVERITY_ORDER` (or a shorter re-export path).

### Import Path in sbom/service/sbom.rs

```rust
use crate::advisory::service::SEVERITY_ORDER;
```

Or, if re-exported at a higher level:

```rust
use crate::advisory::SEVERITY_ORDER;
```
