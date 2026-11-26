# Symbol Deduplication Analysis — TC-9210

Per implement-task SKILL.md Step 6 "Symbol deduplication": before declaring any new
constant, enum, type alias, or config map, search the **target package** (not just the
file being edited) for an existing definition, including naming variations.

## Target package

`modules/fundamental` (crate `trustify-module-fundamental`, manifest
`modules/fundamental/Cargo.toml`). Both files to modify
(`sbom/service/sbom.rs`, `sbom/endpoints/get.rs`) and the sibling module that owns the
constant (`advisory/service/advisory.rs`) live in this same crate.

## Symbol needed

A severity ordering used as the sort key for the remediation list
(Critical > High > Medium > Low > None).

## Searches performed (planned — Serena instance `serena_backend`, Grep fallback)

| # | Tool call | Purpose |
|---|---|---|
| 1 | `mcp__serena_backend__find_symbol(name_path_pattern="SEVERITY_ORDER", relative_path="modules/fundamental", include_body=true)` | Exact symbol name from the task |
| 2 | `mcp__serena_backend__search_for_pattern(substring_pattern="(?i)severity_?order", relative_path="modules/fundamental")` | Variations: `SEVERITY_ORDER`, `severity_order`, `SeverityOrder`, `severityOrder` |
| 3 | `mcp__serena_backend__search_for_pattern(substring_pattern="\"critical\",\\s*\"high\",\\s*\"medium\"", relative_path=".")` | Search by **value** — catches an identical array declared under a different name anywhere in the workspace (e.g. `common/`) |
| 4 | `mcp__serena_backend__search_for_pattern(substring_pattern="enum\\s+Severity|fn\\s+severity_(rank|weight)", relative_path=".")` | Check for an existing `Severity` enum / rank helper that would be an even better reuse target |
| 5 | `mcp__serena_backend__get_symbols_overview(relative_path="modules/fundamental/src/advisory/service/advisory.rs")` | Confirm declaration and visibility (`const` vs `pub const` vs `pub(crate) const`) |
| 6 | `mcp__serena_backend__find_referencing_symbols(name_path="SEVERITY_ORDER", relative_path="modules/fundamental/src/advisory/service/advisory.rs")` | Existing callers, to ensure a visibility change has no side effects |
| 7 | `mcp__serena_backend__get_symbols_overview(relative_path="modules/fundamental/src/advisory/service/mod.rs")` and `.../advisory/mod.rs` | Confirm the `service::advisory` submodule path is reachable (`pub mod`) from `crate::sbom` |

## Where it was found

- **Location**: `modules/fundamental/src/advisory/service/advisory.rs`
- **Definition** (per task Implementation Notes):
  `SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]`
- Ordering semantics: the index in the slice is the sort weight (0 = highest priority).
  The Description phrases this as "maps severity strings to numeric sort weights" —
  that is consistent with index-as-weight; no separate map exists and none should be created.
- Expected result of searches 2–4: no other definition (no duplicate under another name,
  no `Severity` enum). If search 3 or 4 had surfaced a second definition, I would stop
  and flag it to the user rather than pick one silently.

## Decision: REUSE (do not redeclare)

The constant already exists in the same crate, so it is imported, not redeclared:

```rust
// modules/fundamental/src/sbom/service/sbom.rs
use crate::advisory::service::advisory::SEVERITY_ORDER;
```

Rationale:
1. Acceptance criterion explicitly requires "uses the existing `SEVERITY_ORDER` constant
   from the advisory module — no duplicate definition".
2. Skill rule "If found: import and reuse the existing definition."
3. "Reuse over duplication" dependency check: source (`advisory`) and target (`sbom`) are
   modules of the **same crate** — no new Cargo dependency is needed at all, so
   duplication is never justified here. A single definition guarantees that any future
   change to the ordering (e.g. adding `"unknown"`) applies to both advisory listing and
   SBOM remediation sorting.

## Visibility handling

- **If already `pub` / `pub(crate)`** (and the `service::advisory` module path is
  reachable): import directly; no change to `advisory.rs`.
- **If private (`const SEVERITY_ORDER`)**: widen it to `pub(crate) const SEVERITY_ORDER`
  (crate-local visibility is sufficient, since the consumer is in the same crate; avoids
  enlarging the public API). Similarly, change `mod advisory;` to `pub(crate) mod advisory;`
  in `advisory/service/mod.rs` only if the module is not already reachable.
  - This touches `advisory/service/advisory.rs` (and possibly `advisory/service/mod.rs`),
    which are **not** in Files to Modify. Per Step 9 scope containment, this would be
    surfaced to the user as an out-of-scope change requiring explicit approval, with the
    justification that it is a one-word visibility change mandated by the "no duplicate
    definition" acceptance criterion. It would NOT be worked around by copying the constant.
  - The decision and rationale would be recorded in the commit body / PR description.

## Rejected alternatives

| Alternative | Why rejected |
|---|---|
| Redeclare `const SEVERITY_ORDER` in `sbom.rs` | Violates acceptance criterion and skill dedup rule; creates drift risk |
| Hard-coded `match` on severity strings in sbom.rs | Same duplication of the ordering, just in another form |
| Move constant to `common/` | Unnecessary refactor outside scope; both consumers are already in the same crate |
| Introduce a new `Severity` enum | Out of scope; the task specifies reuse of the existing slice |

## Post-implementation duplication check (Step 9)

After implementing, re-run search 2 and 3 across the workspace and confirm exactly one
definition of the severity ordering exists (in `advisory.rs`) and that `sbom.rs` only
references it via `use`.
