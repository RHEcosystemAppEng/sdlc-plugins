# Symbol Deduplication Analysis: SEVERITY_ORDER

## Search Process

### What was searched for

The task requires sorting advisories by severity (Critical > High > Medium > Low > None). The Implementation Notes reference an existing constant `SEVERITY_ORDER` in the advisory module. Before declaring any new constant, the implement-task skill's symbol deduplication guidance requires searching the target package for an existing definition.

### Search scope

Searched the entire `modules/fundamental/` package (not just the sbom service file being edited) for:
- `SEVERITY_ORDER`
- `severity_order`
- `SeverityOrder`

Search method: `find_symbol(name_path_pattern="SEVERITY_ORDER")` across the `modules/fundamental` crate, supplemented by `search_for_pattern(pattern="SEVERITY_ORDER")` to catch string literals and non-symbolic references.

### Where it was found

**Existing definition found in:** `modules/fundamental/src/advisory/service/advisory.rs`

```rust
pub(crate) const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```

The constant is defined in the advisory service module within the same `modules/fundamental` crate. It maps severity strings to sort weights by position in the array (index 0 = highest priority).

### Dependency relationship check

The SBOM service (`modules/fundamental/src/sbom/service/sbom.rs`) and the advisory service (`modules/fundamental/src/advisory/service/advisory.rs`) are both within the same crate (`trustify-module-fundamental`). No cross-crate dependency is needed — this is an intra-crate import.

### Decision: Reuse, not redeclare

**Decision:** Import and reuse the existing `SEVERITY_ORDER` constant from the advisory module. Do not declare a duplicate.

**Rationale:**
1. The constant already exists in a sibling module within the same crate — no new dependency is required.
2. The current visibility is `pub(crate)`, which means it is already accessible from the sbom service within the same crate.
3. Reusing ensures the DRY principle is maintained: if the severity ordering ever changes (e.g., adding a new severity level), the fix applies in one place.
4. Declaring a new `SEVERITY_ORDER` in the sbom service would create a duplication that could silently diverge, causing inconsistent sorting behavior between the advisory and sbom modules.

**Import path:**
```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;
```

No visibility change is needed since `pub(crate)` already grants access within `modules/fundamental`.
