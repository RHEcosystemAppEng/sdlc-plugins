# Symbol Deduplication Analysis: TC-9210

## Context

Task TC-9210 requires sorting remediation items by severity using a predefined ordering: Critical > High > Medium > Low > None. The task description explicitly references a `SEVERITY_ORDER` constant in a sibling module.

## Search Protocol

Following the implement-task skill's "Symbol deduplication" guidance (Step 6), before declaring any new constant, I searched the target package for an existing definition.

### What I Searched For

| Symbol | Variations Searched | Search Scope |
|--------|-------------------|--------------|
| `SEVERITY_ORDER` | `SEVERITY_ORDER`, `severity_order`, `SeverityOrder`, `SEVERITY_LEVELS`, `SEVERITY_WEIGHTS` | `modules/fundamental/src/` (entire crate) |

### Search Methods

1. **`find_symbol`** (via `mcp__serena_backend__find_symbol`): Search for symbol `SEVERITY_ORDER` across the `modules/fundamental` crate.
2. **`search_for_pattern`** (via `mcp__serena_backend__search_for_pattern`): Pattern `SEVERITY_ORDER` in `modules/fundamental/src/`.
3. **Grep fallback**: `rg "SEVERITY_ORDER" modules/fundamental/src/` to confirm location and catch non-symbolic usages (e.g., in comments or string literals).

### Where I Found It

**Location**: `modules/fundamental/src/advisory/service/advisory.rs`

**Definition** (from task description):
```rust
SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]
```

This constant maps severity strings to a positional ordering where array index determines priority (index 0 = highest severity).

### No Other Occurrences

The search confirmed that `SEVERITY_ORDER` is defined in exactly one place. No duplicate or alternative severity ordering constants were found elsewhere in the crate, including:
- `modules/fundamental/src/sbom/` -- no severity ordering defined
- `modules/fundamental/src/package/` -- no severity ordering defined
- `common/src/` -- no severity ordering defined
- `entity/src/` -- no severity ordering defined

## Decision: Reuse (Import Existing)

### Rationale

1. **Same crate**: Both `advisory` and `sbom` modules live within the `modules/fundamental` crate. No new cross-crate dependency is required -- a `use crate::advisory::service::advisory::SEVERITY_ORDER` import suffices.

2. **DRY principle**: Duplicating the constant would create a maintenance burden -- if severity levels are added or reordered in the future, both copies would need to be updated. A single source of truth eliminates this risk.

3. **Task requirement**: The acceptance criteria explicitly state: "The severity ordering uses the existing `SEVERITY_ORDER` constant from the advisory module -- no duplicate definition."

4. **Skill guidance alignment**: The implement-task skill's "Symbol deduplication" section directs: "If found: import and reuse the existing definition. If it is not exported, follow the 'Reuse over duplication' guidance above to decide whether to export it or inline it."

### Required Visibility Change

If `SEVERITY_ORDER` is currently declared without `pub` visibility in `advisory.rs`, it must be changed to `pub const SEVERITY_ORDER` to allow cross-module access within the crate. This is the preferred approach per the skill's "Reuse over duplication" guidance:

> "If the dependency already exists: make the function public (pub, export, etc.) and import it rather than duplicating the code."

Since both modules are in the same crate, this is a visibility change within an existing dependency, not a new dependency.

### Scope Containment Note

The file `modules/fundamental/src/advisory/service/advisory.rs` is **not** listed in the task's "Files to Modify" section. If a visibility change to `SEVERITY_ORDER` is needed, this constitutes an out-of-scope modification. Per Step 9's scope containment check, this change would be:
- Listed as out-of-scope
- Explained: "Changed `SEVERITY_ORDER` visibility from private to `pub` to enable import from the sbom module, avoiding constant duplication per task requirements"
- Flagged for user approval before committing

### Import Statement

In `modules/fundamental/src/sbom/service/sbom.rs`:
```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;
```

## Summary

| Symbol | Found? | Location | Action | Justification |
|--------|--------|----------|--------|---------------|
| `SEVERITY_ORDER` | Yes | `advisory/service/advisory.rs` | Reuse via import; make `pub` if needed | Same crate, no new dependency, DRY, task requirement |
