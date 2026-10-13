# Symbol Deduplication Analysis -- TC-9210

## Trigger

The task description references a `SEVERITY_ORDER` constant needed to sort remediation
items by severity (Critical > High > Medium > Low > None). Before declaring a new
constant, Step 6's "Symbol deduplication" rule requires searching the target package for
an existing definition.

## Search Performed

### Scope

Searched the entire `modules/fundamental/` package -- not just the target file
(`sbom/service/sbom.rs`), but all sibling modules (advisory, package) and shared code.
This broad search scope is required by the skill: "search the target package (not just
the file being edited)."

### Search commands

Using the Serena instance `serena_backend` (from the Repository Registry):

1. `mcp__serena_backend__find_symbol` with query `SEVERITY_ORDER` across
   `modules/fundamental/src/` -- searches for the exact symbol name in all modules.

2. `mcp__serena_backend__search_for_pattern` with pattern `SEVERITY_ORDER` across
   `modules/fundamental/src/` -- catches string-literal and comment references that
   `find_symbol` might miss.

3. As a fallback/confirmation, Grep for common naming variations:
   - `SEVERITY_ORDER` (SCREAMING_SNAKE_CASE -- Rust const convention)
   - `severity_order` (snake_case -- Rust variable convention)
   - `SeverityOrder` (PascalCase -- Rust type/enum convention)

   Pattern used: `(?i)severity.?order` across `modules/fundamental/src/`

## Result

**Found:** `SEVERITY_ORDER` is already defined in
`modules/fundamental/src/advisory/service/advisory.rs`.

Definition:

```rust
pub const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```

The constant is declared as `pub`, meaning it is already exported from the advisory
service module. No visibility change is needed.

## Decision

**Reuse the existing constant.** Import `SEVERITY_ORDER` from the advisory module
rather than redeclaring it in `sbom/service/sbom.rs`.

### Rationale

1. The advisory module (`modules/fundamental`) is the same crate as the sbom module --
   both live under `modules/fundamental/src/`. No new cross-crate dependency is
   required; this is an intra-crate import.
2. The constant is already `pub` -- no visibility change needed.
3. Redeclaring the same constant would violate DRY and create a maintenance risk: if
   the severity ordering changes, two definitions would need updating.
4. The task description itself says "reuse this constant for sorting instead of
   redefining it" (Implementation Notes), and the acceptance criteria explicitly require
   "no duplicate definition."

### Import path

From `sbom/service/sbom.rs`, the import would be:

```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;
```

This follows the intra-crate import convention already used in `modules/fundamental`.
