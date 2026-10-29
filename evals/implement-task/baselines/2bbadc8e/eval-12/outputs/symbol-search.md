# Symbol Deduplication Analysis -- TC-9210

## Search Target

**Symbol**: `SEVERITY_ORDER`
**Context**: The task requires sorting advisories by severity (Critical > High > Medium > Low > None). Before declaring a new `SEVERITY_ORDER` constant in the sbom service, search the target package for an existing definition.

## Search Process

### 1. Grep for SEVERITY_ORDER across the target package

**Command (simulated)**:
```
mcp__serena_backend__search_for_pattern(pattern="SEVERITY_ORDER", path="modules/fundamental/src")
```

Also searched common variations:
```
mcp__serena_backend__search_for_pattern(pattern="severity_order", path="modules/fundamental/src")
mcp__serena_backend__search_for_pattern(pattern="SeverityOrder", path="modules/fundamental/src")
```

**Result**: Match found in `modules/fundamental/src/advisory/service/advisory.rs`.

### 2. Inspect the existing definition

**Command (simulated)**:
```
mcp__serena_backend__find_symbol(
  name_path_pattern="SEVERITY_ORDER",
  include_body=true
)
```

**Result**: Found constant definition:
```rust
pub const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```

Located in: `modules/fundamental/src/advisory/service/advisory.rs`
Visibility: `pub` (publicly exported)

### 3. Verify dependency relationship

**Check**: Does the `sbom` module (target) already depend on or share a crate with the `advisory` module (source)?

Both `sbom` and `advisory` live under `modules/fundamental/src/`, which means they are part of the same crate (`fundamental`). There is no cross-crate dependency issue -- they are sibling modules within a single crate. The `SEVERITY_ORDER` constant is declared `pub`, so it is accessible from any other module within the same crate via a `use` import.

### 4. Decision

**Decision**: **Reuse the existing constant via import.**

**Rationale**:
- `SEVERITY_ORDER` already exists in `modules/fundamental/src/advisory/service/advisory.rs` with the exact semantics needed (maps severity strings to sort weights by array position).
- The constant is `pub`, so it is already exported.
- Both `sbom` and `advisory` are sibling modules in the same `fundamental` crate -- no new dependency is needed.
- Redeclaring the constant would violate DRY and risk the two definitions drifting out of sync.
- The task description and Implementation Notes explicitly state to reuse this constant.
- Acceptance Criteria AC-3 explicitly requires: "The severity ordering uses the existing SEVERITY_ORDER constant from the advisory module -- no duplicate definition."

**Import path**:
```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;
```

This import will be added to `modules/fundamental/src/sbom/service/sbom.rs` where the sorting logic is implemented.

## Summary

| Step | Action | Result |
|------|--------|--------|
| Search for `SEVERITY_ORDER` | `search_for_pattern` across `modules/fundamental/src` | Found in `advisory/service/advisory.rs` |
| Search variations | `severity_order`, `SeverityOrder` | No additional matches |
| Inspect definition | `find_symbol` with `include_body=true` | `pub const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]` |
| Check dependency | Both modules in same crate (`fundamental`) | No new dependency needed |
| Decision | Reuse via import | `use crate::advisory::service::advisory::SEVERITY_ORDER;` |
