# Symbol Deduplication Analysis: TC-9210

## Context

Task TC-9210 requires sorting advisories by severity using the ordering
Critical > High > Medium > Low > None. The implementation needs a constant
that maps severity strings to sort weights. Before declaring any new constant,
the skill's symbol deduplication protocol (Step 6) requires searching the
target package for existing definitions.

## Search Performed

### Search target

Package: `modules/fundamental` (the crate containing both `sbom` and `advisory`
modules).

### Search queries

The following searches were conducted using `find_symbol`, `search_for_pattern`,
and Grep across the `modules/fundamental/src/` directory tree:

1. **`SEVERITY_ORDER`** -- exact match for the constant name referenced in the
   task description and Implementation Notes.
2. **`severityOrder`** / **`SeverityOrder`** -- camelCase and PascalCase
   variations to cover alternative naming conventions.
3. **`severity.*order`** -- pattern search to catch any severity-ordering logic
   under a different name (e.g., `SEVERITY_SORT_ORDER`,
   `severity_priority_order`).

### Search results

| Query | Location Found | Symbol Type |
|-------|---------------|-------------|
| `SEVERITY_ORDER` | `modules/fundamental/src/advisory/service/advisory.rs` | `const` / `static` |
| `severityOrder` | No matches | -- |
| `SeverityOrder` | No matches | -- |
| `severity.*order` | Same hit as `SEVERITY_ORDER` above | -- |

### Existing definition

Found in `modules/fundamental/src/advisory/service/advisory.rs`:

```rust
SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]
```

This constant defines the exact severity ordering needed by the task: position 0
is highest severity (critical), position 4 is lowest (none). The task's
Implementation Notes explicitly reference this constant and its location.

## Decision: Reuse via Import

### Dependency check

The `SEVERITY_ORDER` constant lives in `modules/fundamental/src/advisory/service/advisory.rs`.
The code that needs it is in `modules/fundamental/src/sbom/service/sbom.rs`. Both files
are part of the same Rust crate (`modules/fundamental`), as they share a single
`Cargo.toml` at `modules/fundamental/Cargo.toml`. No new cross-crate dependency
is required.

### Visibility check

If `SEVERITY_ORDER` is already `pub`, it can be imported directly:

```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;
```

If it is not currently `pub`, the constant needs to be made public. This is a
minimal change (adding the `pub` keyword) in a file outside the task's explicit
Files to Modify scope. Per the skill's scope containment protocol (Step 9),
this out-of-scope modification to `advisory.rs` would be flagged for user
approval before committing. Additionally, the module re-exports in
`advisory/service/mod.rs` may need to be checked to ensure the symbol is
accessible through the `crate::advisory::service::advisory` path.

### Why reuse, not redeclare

1. **DRY principle:** The constant already encodes the canonical severity
   ordering. A second copy would create a maintenance risk -- if the ordering
   changes (e.g., adding a "negligible" severity), both copies must be updated.
2. **Intra-crate dependency:** Both modules are in the same crate, so reuse
   adds zero coupling cost. There is no new entry in `Cargo.toml`.
3. **Task requirement:** The acceptance criteria explicitly state "no duplicate
   definition" and the Implementation Notes say "reuse this constant for sorting
   instead of redefining it."

### Alternative considered

Duplicating the constant in `sbom/service/sbom.rs` was considered and rejected.
While it would avoid modifying the advisory module, it violates the task's
acceptance criteria and introduces a maintenance burden. Since the dependency
is intra-crate, there is no architectural reason to prefer duplication.

## Summary

| Symbol | Action | Source | Target |
|--------|--------|--------|--------|
| `SEVERITY_ORDER` | Import (reuse) | `modules/fundamental/src/advisory/service/advisory.rs` | `modules/fundamental/src/sbom/service/sbom.rs` |

No new constant declarations are needed. The existing `SEVERITY_ORDER` constant
from the advisory module will be imported and used directly for sorting
remediation items by severity.
