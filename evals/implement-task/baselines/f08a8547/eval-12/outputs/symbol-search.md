# Symbol Deduplication Analysis: TC-9210

## Context

The task requires sorting remediation items by severity using a defined ordering
(Critical > High > Medium > Low > None). The implementation needs a constant that
maps severity strings to sort weights. The task description references an existing
`SEVERITY_ORDER` constant in the advisory module.

Per SKILL.md Step 6 "Symbol deduplication" guidance: before declaring any new constant,
search the target package for an existing definition of the same symbol.

## Search Performed

### 1. Primary search: exact symbol name

**Query**: Search for `SEVERITY_ORDER` across the `modules/fundamental/` crate (the
package containing both the sbom and advisory modules).

**Method**: `find_symbol("SEVERITY_ORDER")` via Serena, plus `grep -r "SEVERITY_ORDER" modules/fundamental/src/`

**Result**: Found in `modules/fundamental/src/advisory/service/advisory.rs`

```rust
const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```

### 2. Variation search: alternate naming conventions

**Queries searched**:
- `severityOrder` (camelCase) -- no results
- `SeverityOrder` (PascalCase) -- no results
- `severity_order` (snake_case, non-const) -- no results outside the constant
- `SEVERITY_LEVELS` -- no results
- `SEVERITY_WEIGHTS` -- no results
- `SEVERITY_PRIORITY` -- no results

**Method**: `search_for_pattern` / Grep across `modules/fundamental/`

**Result**: No alternate definitions found. The only severity ordering definition is the
`SEVERITY_ORDER` constant in the advisory module.

### 3. Value search: check for inline severity arrays

**Query**: Search for the literal array value pattern `"critical", "high", "medium"` to catch
any unnamed inline definitions of the same ordering.

**Method**: `grep -r '"critical".*"high".*"medium"' modules/fundamental/src/`

**Result**: Only match is the `SEVERITY_ORDER` constant declaration itself. No inline
duplicates exist anywhere in the crate.

## Dependency Analysis

**Source package**: `modules/fundamental` (crate: `trustify-fundamental`)
**Target package**: `modules/fundamental` (same crate)

Both the advisory module (where `SEVERITY_ORDER` lives) and the sbom module (where it
needs to be used) are in the **same crate** (`modules/fundamental`). This means:

- No new cross-crate dependency needs to be added
- The constant can be accessed via a simple intra-crate path: `crate::advisory::service::advisory::SEVERITY_ORDER`
- The only requirement is that the constant has `pub` visibility

## Visibility Assessment

The constant is currently declared as:
```rust
const SEVERITY_ORDER: &[&str] = ...;
```

Without the `pub` keyword, it is private to the `advisory.rs` module. To reuse it from
the sbom module, it must be made public:

```rust
pub const SEVERITY_ORDER: &[&str] = ...;
```

Additionally, the module path must be public. Checking the module hierarchy:
- `advisory/mod.rs` must have `pub mod service;`
- `advisory/service/mod.rs` must have `pub mod advisory;` (or equivalent re-export)

These are likely already public since `AdvisoryService` is used from endpoints and other
modules, but this needs verification.

## Decision

**REUSE the existing definition.** Do NOT redeclare `SEVERITY_ORDER`.

### Rationale

1. **Same crate**: No dependency cost -- both modules are in `modules/fundamental`
2. **Identical semantics**: The existing constant defines exactly the ordering needed
   (Critical > High > Medium > Low > None, represented as lowercase strings)
3. **DRY principle**: A duplicate definition would create a maintenance risk -- if the
   severity ordering ever changes, both copies would need updating
4. **Acceptance criterion**: The task explicitly requires "uses the existing SEVERITY_ORDER
   constant from the advisory module -- no duplicate definition"
5. **SKILL.md guidance**: Step 6 states "If found: import and reuse the existing definition.
   If it is not exported, follow the 'Reuse over duplication' guidance to decide whether
   to export it or inline it." Since it is in the same crate, exporting (adding `pub`)
   is the correct approach.

### Implementation

```rust
// In modules/fundamental/src/sbom/service/sbom.rs:
use crate::advisory::service::advisory::SEVERITY_ORDER;
```

If the `pub` visibility change to `advisory.rs` is considered out-of-scope (it is not
listed in "Files to Modify"), this will be flagged during Step 9 scope containment
for user approval. The change is minimal (adding `pub` to one line) and directly
required by the acceptance criteria.
