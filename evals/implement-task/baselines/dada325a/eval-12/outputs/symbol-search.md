# Symbol Deduplication Analysis — TC-9210

Per implement-task Step 6 "Symbol deduplication": before declaring any new constant, enum,
type alias, or configuration map, search the **target package** (not just the file being
edited) for an existing definition, including naming variations.

## 1. Symbols the task needs

| Symbol | Kind | Needed for |
|---|---|---|
| `SEVERITY_ORDER` | constant (`&[&str]`) | Sort key for remediation list |
| `RemediationItem` | struct | Element type of the `remediations` list |

## 2. Searches performed (simulated, using the `serena_backend` instance)

Target package: `modules/fundamental` (crate `trustify-module-fundamental`, containing
both `sbom/` and `advisory/`).

### 2a. `SEVERITY_ORDER`

| # | Tool call | Scope | Purpose |
|---|---|---|---|
| 1 | `mcp__serena_backend__find_symbol(name_path_pattern="SEVERITY_ORDER", include_body=true)` | whole repo | Exact name |
| 2 | `mcp__serena_backend__search_for_pattern(substring_pattern="(?i)severity_?order", relative_path="modules/fundamental")` | target crate | Variations: `SEVERITY_ORDER`, `severity_order`, `SeverityOrder`, `severityOrder` |
| 3 | `mcp__serena_backend__search_for_pattern(substring_pattern="\"critical\",\\s*\"high\"", relative_path=".")` | whole repo | Same **value** declared under a different name (e.g. `SEVERITY_RANK`, `SEVERITY_LEVELS`) |
| 4 | `mcp__serena_backend__search_for_pattern(substring_pattern="enum\\s+Severity", relative_path=".")` | whole repo | An existing `Severity` enum with `Ord` that might supersede a string array |
| 5 | `mcp__serena_backend__get_symbols_overview(relative_path="modules/fundamental/src/advisory/service/advisory.rs")` | sibling file | Confirm declaration and its visibility (`pub` / `pub(crate)` / private) |
| 6 | `mcp__serena_backend__find_referencing_symbols(name_path="SEVERITY_ORDER", relative_path="modules/fundamental/src/advisory/service/advisory.rs")` | crate | Existing consumers (to ensure a visibility change breaks nothing) |
| 7 | `mcp__serena_backend__get_symbols_overview(relative_path="modules/fundamental/src/advisory/service/mod.rs")` and `.../advisory/mod.rs` | module tree | Confirm `service` / `advisory` modules are reachable from `crate::sbom` |

### Finding

- **Found:** `SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]`
  in `modules/fundamental/src/advisory/service/advisory.rs` (stated in the task
  Description and Implementation Notes; the repo layout confirms the file exists in the
  same crate as `sbom/service/sbom.rs`).
- No other definition (no `SeverityOrder`/`severity_order` variant, no duplicate array
  literal elsewhere) is expected; any hit from search #3 outside `advisory.rs` would be an
  existing duplicate, which I'd report rather than add to.
- Note: the Description says the constant "maps severity strings to numeric sort weights",
  but its actual shape is an ordered slice. The "weight" is the **index** in the slice
  (Implementation Notes: "position in the array determines priority"). I go with the
  declared shape (`&[&str]`) and treat the index as the weight.

## 3. Decision: REUSE, do not redeclare

**Reason:**
1. The symbol already exists, with exactly the semantics required (Critical > High >
   Medium > Low > None).
2. Acceptance Criterion: "The severity ordering uses the existing `SEVERITY_ORDER`
   constant from the advisory module — no duplicate definition."
3. "Reuse over duplication" dependency check: the source (`advisory`) and the target
   (`sbom`) are in the **same crate** (`modules/fundamental`). No new Cargo dependency is
   needed, so reuse is always the right choice and inlining is not justified.

**Import used in `modules/fundamental/src/sbom/service/sbom.rs`:**

```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;
```

(If `advisory/service/mod.rs` re-exports it, e.g. `pub use advisory::*;`, use the
shorter `crate::advisory::service::SEVERITY_ORDER` to match how sibling code imports from
that module.)

### Visibility handling

| Visibility found by search #5 | Action |
|---|---|
| `pub const` or `pub(crate) const` | Import directly. No change to `advisory.rs`. |
| private `const` (no `pub`) | Make it `pub(crate)` (smallest visibility that works within the crate; it doesn't need to be part of the crate's public API). This is a one-word edit to `advisory.rs`, which is **not** in Files to Modify, so I'd flag it in Step 9 scope containment and ask the user to approve it before committing. I would **not** fall back to redeclaring the constant in `sbom.rs`, because that breaks the AC. |
| `advisory::service` module is private in `advisory/mod.rs` | Same approach: widen to `pub(crate) mod service;` and flag as out of scope for approval. |

The decision and why will go in the commit body and PR description ("Reuses
`SEVERITY_ORDER` from the advisory module instead of redeclaring it").

## 4. `RemediationItem`

| # | Tool call | Purpose |
|---|---|---|
| 1 | `mcp__serena_backend__find_symbol(name_path_pattern="RemediationItem")` | Exact name |
| 2 | `mcp__serena_backend__search_for_pattern(substring_pattern="(?i)struct\\s+Remediation", relative_path=".")` | Variants: `Remediation`, `RemediationEntry`, `RemediationSummary` |

**Expected finding:** not found. The task asks for a new struct, and the repo layout has
no remediation module.

**Decision: declare new.** By module convention (`model/ + service/ + endpoints/`) the
best home would be `sbom/model/details.rs`, but that file is not in Files to Modify.
So I declare `RemediationItem` in `sbom/service/sbom.rs` (in scope) and note in Step 9
that moving it to `sbom/model/` would match convention better, if the user approves
touching that file.

## 5. Post-implementation duplication check (Step 9)

After writing the code, re-run:

- `search_for_pattern("\"critical\"", relative_path="modules/fundamental")`: expected to
  return only `advisory/service/advisory.rs`. A hit in `sbom/` would mean a literal
  duplicate slipped in.
- `search_for_pattern("SEVERITY_ORDER")`: expected hits are the definition in
  `advisory.rs`, its existing consumers, and the new `use` and usage in `sbom/service/sbom.rs`.
