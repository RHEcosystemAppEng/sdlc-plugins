# Symbol Deduplication Analysis for TC-9210

## Context

Task TC-9210 requires sorting advisories by severity using a severity ordering constant. The Implementation Notes reference a `SEVERITY_ORDER` constant defined in the advisory module. Before declaring any new constant, the implement-task skill (Step 6, "Symbol deduplication") requires searching the target package for an existing definition.

## Search Performed

### Target Package

The target package is `modules/fundamental`, which is a single Rust crate containing both the `sbom` and `advisory` modules. Both modules being in the same crate means no cross-crate dependency is needed to share symbols between them.

### Symbol Searched

- **Primary name**: `SEVERITY_ORDER`
- **Variations searched**: `severity_order`, `SeverityOrder`, `SEVERITY_LEVELS`, `severity_levels`, `SeverityLevels`, `SEVERITY_PRIORITY`, `severity_priority`

### Search Strategy

Used a broad search across the entire `modules/fundamental/` directory tree (not just the file being edited) to ensure thorough coverage. Searched using multiple methods:

1. **Grep for `SEVERITY_ORDER`** across `modules/fundamental/src/` -- finds exact constant name in any file
2. **Grep for `severity_order`** (case-insensitive) across `modules/fundamental/src/` -- catches any casing variation
3. **Grep for the value pattern** `"critical", "high", "medium", "low", "none"` across `modules/fundamental/src/` -- catches redefinitions under a different name
4. **Serena `find_symbol`** on `SEVERITY_ORDER` within the `modules/fundamental` crate -- locates the symbol via rust-analyzer

### Search Results

| Search | Location Found | Details |
|--------|---------------|---------|
| `SEVERITY_ORDER` by name | `modules/fundamental/src/advisory/service/advisory.rs` | Constant definition: `SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]` |
| Case-insensitive variations | No additional hits | Only the single definition in advisory.rs |
| Value pattern search | No additional hits | No duplicate definitions with different names |

### Existing Definition Details

- **File**: `modules/fundamental/src/advisory/service/advisory.rs`
- **Symbol**: `SEVERITY_ORDER`
- **Type**: `&[&str]` (static string slice)
- **Value**: `&["critical", "high", "medium", "low", "none"]`
- **Current visibility**: Needs to be checked -- if not already `pub`, it must be made `pub` to be importable from the sbom module

## Decision: Reuse

**Decision**: Import and reuse the existing `SEVERITY_ORDER` constant from the advisory module. Do NOT redeclare it.

**Rationale**:

1. **Same crate**: Both `sbom` and `advisory` are submodules of `modules/fundamental`. They share the same `Cargo.toml` and compile as a single crate. No new dependency is required -- this is a simple intra-crate import.

2. **DRY principle**: The "Reuse over duplication" guidance in the implement-task skill says: "If the dependency already exists: make the function public and import it rather than duplicating the code. This follows the DRY principle and ensures future bug fixes apply in one place."

3. **Single source of truth**: If the severity ordering ever needs to change (e.g., adding a new severity level), having a single definition ensures consistency across both the advisory and sbom modules.

4. **Task description confirms intent**: The task description explicitly states: "reuse this constant for sorting instead of redefining it" and the acceptance criteria include: "The severity ordering uses the existing SEVERITY_ORDER constant from the advisory module -- no duplicate definition."

### Visibility Adjustment

If `SEVERITY_ORDER` is not already `pub`, the following change is needed in `modules/fundamental/src/advisory/service/advisory.rs`:

```rust
// Before (if private):
const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];

// After:
pub const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```

The `advisory/service/mod.rs` module must also re-export or make the `advisory` submodule public so the symbol is accessible from sibling modules. The import path from the sbom module would be:

```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;
```

This is an intra-crate path (using `crate::`) since both modules live in the same crate (`modules/fundamental`).

### Scope Note

Making `SEVERITY_ORDER` public is an out-of-scope file change (the file `modules/fundamental/src/advisory/service/advisory.rs` is not listed in Files to Modify). Per Step 9's scope containment check, this would be flagged to the user for approval with the explanation: "Making SEVERITY_ORDER pub in advisory.rs is required to import it from sbom module, avoiding a duplicate definition per the task's acceptance criteria."
