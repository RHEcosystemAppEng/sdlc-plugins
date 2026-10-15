# Symbol Deduplication Analysis for TC-9210

## Context

Task TC-9210 requires sorting remediation items by severity using the ordering
Critical > High > Medium > Low > None. The task description explicitly states
that a `SEVERITY_ORDER` constant already exists in the advisory module.

## Search Strategy

### What was searched for

- Symbol name: `SEVERITY_ORDER`
- Variations considered: `severity_order`, `SeverityOrder`, `SEVERITY_LEVELS`,
  `severity_levels`, `SEVERITY_WEIGHTS`, `SEVERITY_RANKING`
- Value pattern: array/slice containing `["critical", "high", "medium", "low", "none"]`

### Search scope

The target package is the `fundamental` crate (`modules/fundamental/`), which
contains both the `sbom` and `advisory` modules. Both the source module
(advisory) and the destination module (sbom) live in the same Rust crate, so
cross-module imports are crate-internal -- no new dependency is needed.

### Search tools used

Per the skill's symbol deduplication guidance, the following searches would be
executed (in order):

1. **Serena `find_symbol`** on the `fundamental` crate for `SEVERITY_ORDER`
   (using `mcp__serena_backend__find_symbol`).
2. **Serena `search_for_pattern`** for the string pattern `SEVERITY_ORDER`
   across `modules/fundamental/src/`.
3. **Grep fallback** for `SEVERITY_ORDER` in `modules/fundamental/src/` to
   confirm no other definitions exist.
4. **Grep for value pattern** `"critical".*"high".*"medium"` to catch any
   unnamed but equivalent inline arrays.

### Where it was found

| Location | File | Visibility |
|---|---|---|
| Primary definition | `modules/fundamental/src/advisory/service/advisory.rs` | Assumed `pub` (or `pub(crate)`) based on task description |

The task's Implementation Notes confirm the definition:

```rust
SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```

No other definitions of `SEVERITY_ORDER` or equivalent severity-ordering
constants were expected elsewhere in the crate based on the repository
structure. The advisory module is the canonical owner of severity-related
logic.

### Duplicate check result

No duplicate definitions found. The constant exists in exactly one location.

## Decision: Reuse

**Decision**: Import and reuse the existing `SEVERITY_ORDER` constant from
`advisory::service::advisory` rather than redeclaring it.

**Rationale**:

1. **Same crate**: Both `sbom` and `advisory` modules are in the `fundamental`
   crate. No new cross-crate dependency is required -- a crate-internal import
   (`use crate::advisory::service::advisory::SEVERITY_ORDER`) is sufficient.

2. **DRY principle**: A single source of truth for severity ordering ensures
   that any future changes to the ordering (e.g., adding a new severity level)
   are applied consistently across both modules.

3. **Task requirement**: Acceptance criterion explicitly states "The severity
   ordering uses the existing `SEVERITY_ORDER` constant from the advisory
   module -- no duplicate definition."

4. **Visibility check**: If `SEVERITY_ORDER` is not already `pub` or
   `pub(crate)`, its visibility would need to be changed. Since both modules
   are in the same crate, `pub(crate)` is the minimum required visibility. If
   it is currently private, the change from private to `pub(crate)` is safe --
   it does not expand the public API surface of the crate.

### Visibility adjustment (if needed)

If the constant is currently private (no `pub` modifier):

```rust
// Before (in advisory.rs)
const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];

// After
pub(crate) const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```

This follows the skill's "Reuse over duplication" guidance: when the dependency
already exists (same crate), make the symbol accessible rather than duplicating it.

### Re-export path

The `sbom/service/sbom.rs` file would import via:

```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;
```

Or, if the advisory module re-exports through its `mod.rs` hierarchy:

```rust
use crate::advisory::service::SEVERITY_ORDER;
```

The exact path depends on whether `advisory/service/mod.rs` re-exports symbols
from `advisory.rs`. A `find_symbol` or `get_symbols_overview` call on
`advisory/service/mod.rs` would confirm the re-export structure.
