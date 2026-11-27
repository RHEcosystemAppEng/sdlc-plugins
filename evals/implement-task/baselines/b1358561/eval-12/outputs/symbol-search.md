# Symbol Deduplication Analysis — TC-9210

Skill step: implement-task Step 4 (search for existing utilities/constants), Step 6 **Reuse**, and Step 9 check 5 (Duplication).

## 1. What needed checking

The feature needs severity ordering (Critical > High > Medium > Low > None) to sort the SBOM remediation list. Before writing any sorting key, the Reuse rules say to look for an existing definition of the same constant, enum, type alias, or config map, including naming variants.

## 2. Searches (Serena instance `serena_backend`, from the Repository Registry in CLAUDE.md)

| # | Tool call (planned) | Purpose |
|---|---|---|
| 1 | `mcp__serena_backend__find_symbol(name_path_pattern="SEVERITY_ORDER", include_body=true)` | Find the constant named in the Implementation Notes, its body and its visibility |
| 2 | `mcp__serena_backend__search_for_pattern(substring_pattern="(?i)severity_?order")` | Naming variants: `SEVERITY_ORDER`, `severity_order`, `SeverityOrder`, `severityOrder` |
| 3 | `mcp__serena_backend__search_for_pattern(substring_pattern="\"critical\",\\s*\"high\"")` | Literal copies of the ordering array under a different name |
| 4 | `mcp__serena_backend__search_for_pattern(substring_pattern="(?i)enum\\s+Severity\|fn\\s+severity_(rank\|weight\|order)")` | Any `Severity` enum or rank/weight helper (with `Ord`) that also encodes the ordering |
| 5 | `mcp__serena_backend__get_symbols_overview(relative_path="modules/fundamental/src/advisory/service/advisory.rs")` | See what the advisory service file holds and whether the constant is `pub`, `pub(crate)`, or private |
| 6 | `mcp__serena_backend__find_referencing_symbols(name_path="SEVERITY_ORDER", relative_path="modules/fundamental/src/advisory/service/advisory.rs")` | Find current users, so a visibility change won't break anything |
| 7 | `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/mod.rs` and `modules/fundamental/src/advisory/mod.rs` | Check whether `service::advisory` is a `pub mod` or re-exported, so the import path resolves |
| 8 | `mcp__serena_backend__search_for_pattern(substring_pattern="(?i)severity", relative_path="common/src")` | Make sure no shared copy already exists in `common`, which would be the better place to import from |

## 3. Findings

- **Location**: `modules/fundamental/src/advisory/service/advisory.rs`, which holds `AdvisoryService`.
- **Definition** (per the task's Implementation Notes): `SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]`. The array index is the sort weight, so a lower index means higher priority.
- **Crate**: `fundamental`, the same crate as the consumer `modules/fundamental/src/sbom/service/sbom.rs`. Importing it adds no new cross-package dependency and no `Cargo.toml` change.
- **No other definitions expected**: searches 2–4 and 8 are there to confirm that no second copy (`severity_order`, a `Severity` enum with `Ord`, or a literal array) exists in `sbom/`, `common/`, `search/` or `ingestor/`. If one turns up, I would report it rather than add a third copy.
- **Visibility**: the task text gives the declaration without a `pub`/`const`/`static` qualifier, so whether it is exported has to be confirmed with search 5. The decision below covers both cases.

## 4. Decision: REUSE. Do not redeclare.

Applying the Step 6 Reuse rules:

| Case (from search 5) | Rule | Action |
|---|---|---|
| Already `pub` / `pub(crate)` and the module path is reachable | Rule 1, exists and is exported | `use crate::advisory::service::advisory::SEVERITY_ORDER;` in `sbom/service/sbom.rs`. No change to `advisory.rs`. |
| Private (`const SEVERITY_ORDER` / `static SEVERITY_ORDER` with no `pub`) | Rule 2, exists but not exported, and its package is already a dependency (same crate) | Change it to `pub(crate) const SEVERITY_ORDER` (smallest visibility that works) and import it as above. **Do not** inline a local copy: inlining is only allowed when exporting would add a new cross-package dependency, and here it would not. |
| `service::advisory` submodule is private | Rule 2 | Add `pub(crate) use advisory::SEVERITY_ORDER;` in `advisory/service/mod.rs`, or make the submodule `pub(crate)`, whichever matches how sibling modules expose their items. |

**Rejected: redeclaring `SEVERITY_ORDER` in `sbom.rs`.** That would create two sources of truth for severity ranking. The two lists could drift apart (for example, if an "unknown" or "moderate" severity were added to only one), and the SBOM report and advisory endpoints would then sort differently. It would also break the acceptance criterion: "The severity ordering uses the existing `SEVERITY_ORDER` constant from the advisory module — no duplicate definition".

## 5. Scope implication (Step 6 / Step 9 check 1)

`advisory.rs` (and possibly `advisory/service/mod.rs`) is **not** in Files to Modify. If the constant is already exported, nothing outside scope is touched. If a visibility change is needed, the one-word `pub(crate)` edit is reported as a **Step 9 scope-containment flag** for user approval before commit. The PR description will record it, as Reuse rule 4 requires: "Exported `SEVERITY_ORDER` as `pub(crate)` from the advisory service so the SBOM remediation list reuses it instead of duplicating it."

## 6. How the constant is used

```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;

/// Returns the sort rank of a severity string: lower means more severe.
/// Unknown or missing severities rank after every entry in SEVERITY_ORDER.
fn severity_rank(severity: Option<&str>) -> usize {
    severity
        .map(|s| s.to_ascii_lowercase())
        .and_then(|s| SEVERITY_ORDER.iter().position(|o| *o == s))
        .unwrap_or(SEVERITY_ORDER.len())
}

// Stable sort, so advisories with the same severity keep their fetch order.
items.sort_by_key(|i| severity_rank(i.severity.as_deref()));
```

`severity_rank` is a small private helper that derives from the shared constant and does not copy it. Before adding it, search 4 confirms that no equivalent `position`-based helper already exists in the advisory module. If one exists (for example `severity_weight`), I reuse it under the same rules.

## 7. Step 9 check 5 (Duplication) re-check

After implementing, re-run searches 2 and 3 across the repo. Expected result: exactly one definition of `SEVERITY_ORDER` (in `advisory.rs`) and one new reference to it (in `sbom.rs`). Any second definition means the check is FLAGGED and must be fixed before commit.
