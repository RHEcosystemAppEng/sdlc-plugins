# Symbol Deduplication Analysis for TC-9210

## Search Objective

Before implementing the severity-sorted remediation list, search the target package
for an existing `SEVERITY_ORDER` constant to avoid declaring a duplicate.

## Search Process

### 1. Task Description Analysis

The task description explicitly states:

> The advisory module's `advisory.rs` service file defines
> `SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]`
> -- reuse this constant for sorting instead of redefining it

This is a strong hint, but the implement-task skill requires independent verification
via symbol search before relying on task description claims.

### 2. Broad Package Search

**Search scope:** The entire `modules/fundamental/` directory tree -- not just the
file being edited (`sbom/service/sbom.rs`), but all sibling modules and shared code.

**Search strategy:** Multiple queries to cover naming variations:

| Query | Tool | Scope |
|-------|------|-------|
| `SEVERITY_ORDER` | Grep / `search_for_pattern` | `modules/fundamental/src/` |
| `severity_order` | Grep / `search_for_pattern` | `modules/fundamental/src/` |
| `SeverityOrder` | Grep / `search_for_pattern` | `modules/fundamental/src/` |
| `severityOrder` | Grep / `search_for_pattern` | `modules/fundamental/src/` |

**Also searched:** `common/src/` to check if severity ordering is defined in shared
utilities.

### 3. Search Results

**Found:** `SEVERITY_ORDER` in `modules/fundamental/src/advisory/service/advisory.rs`

```rust
pub const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```

This is a `pub const` -- it is already publicly exported from the advisory service
module. No other definitions of `SEVERITY_ORDER` or equivalent severity ordering
constants were found elsewhere in the codebase.

### 4. Dependency Relationship Check

Checked `modules/fundamental/Cargo.toml` -- since both the `sbom` and `advisory`
modules live within the same crate (`modules/fundamental`), there is no cross-crate
dependency issue. The constant is accessible via a module-internal import path:

```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;
```

### 5. Decision

**Reuse the existing constant.** Rationale:

- The constant already exists and is `pub` (publicly visible).
- Both the consumer (`sbom/service/sbom.rs`) and the provider
  (`advisory/service/advisory.rs`) are in the same crate (`modules/fundamental`),
  so no new dependency is needed.
- Duplicating the constant would violate DRY and create a maintenance risk -- if
  the severity ordering ever changes, both copies would need to be updated.
- The task's acceptance criteria explicitly require: "The severity ordering uses the
  existing `SEVERITY_ORDER` constant from the advisory module -- no duplicate
  definition."

### 6. Alternative Considered

If `SEVERITY_ORDER` were not already `pub`, the correct action per the skill's
"Reuse over duplication" guidance would be to make it public rather than duplicating,
since no new cross-crate dependency is required. In this case, the constant is
already public, so no visibility change is needed.
