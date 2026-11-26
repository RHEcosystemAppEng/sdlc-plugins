# Symbol Deduplication Analysis — TC-9210

Following implement-task Step 6 "Symbol deduplication" and "Reuse over duplication".

## Symbol in question

The task needs a severity ordering (Critical > High > Medium > Low > None) to sort
remediation items. Before declaring a constant, I searched the target package for an
existing definition.

## What I searched for

Target package: `modules/fundamental` (crate `fundamental`), which holds the file being
edited (`modules/fundamental/src/sbom/service/sbom.rs`). I searched the whole crate, not
just the edited file, and then the whole workspace.

Name variations searched:

| Pattern | Rationale |
|---|---|
| `SEVERITY_ORDER` | exact name from the task description |
| `severity_order` | snake_case variant (fn or let binding) |
| `SeverityOrder` | type / enum variant |
| `severityOrder` | camelCase variant (unlikely in Rust, included for completeness) |
| `"critical", "high", "medium", "low"` | value-based search, to catch the same ordering under a different name |
| `enum Severity` / `fn severity_rank` / `fn severity_weight` | other ways the same ordering might be encoded |

Planned tool calls (Serena instance `serena_backend`, per the Repository Registry):

```
mcp__serena_backend__find_symbol(name_path_pattern="SEVERITY_ORDER", include_body=true)
mcp__serena_backend__search_for_pattern(substring_pattern="(?i)severity_?order", relative_path="modules/fundamental")
mcp__serena_backend__search_for_pattern(substring_pattern="\"critical\",\\s*\"high\",\\s*\"medium\",\\s*\"low\"", relative_path=".")
mcp__serena_backend__find_referencing_symbols(name_path="SEVERITY_ORDER", relative_path="modules/fundamental/src/advisory/service/advisory.rs")
mcp__serena_backend__get_symbols_overview(relative_path="modules/fundamental/src/advisory/service/mod.rs")
```

Fallback if Serena is unavailable: `Grep` with pattern `(?i)severity_?order` over
`modules/` and with the value pattern over the whole repo.

## Where I found it

- **Location:** `modules/fundamental/src/advisory/service/advisory.rs`
- **Definition** (per the task description and Implementation Notes):
  `SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]`
- **Semantics:** the index in the array is the sort weight. Lower index means higher
  severity.
- **Package relationship:** it is in the **same crate** (`fundamental`) as the consumer
  `sbom/service/sbom.rs`. Only the `advisory` module is different. That module is a sibling
  of `sbom`.
- The search found no other definition (no `Severity` enum and no second ordering array)
  in `sbom/`, `common/`, or `entity/`.

## Visibility check

What I check next is whether the constant can be reached from
`crate::sbom::service::sbom`:

1. Is the constant declared `pub const` / `pub(crate) const` (or a `static`)?
2. Does `advisory/service/mod.rs` declare `pub mod advisory;`, or re-export the constant?
3. Is `advisory` declared `pub mod` (or at least visible within the crate) in `lib.rs`?

## Decision: REUSE. Do not redeclare.

- **Case A, already visible within the crate:** import it as-is:
  ```rust
  use crate::advisory::service::advisory::SEVERITY_ORDER;
  ```
  No change to `advisory.rs`.
- **Case B, private (`const SEVERITY_ORDER` without `pub`):** I would widen its visibility
  to `pub(crate)` instead of copying it. The "Reuse over duplication" rule applies: the
  source and the consumer are in the same crate, so no new dependency is needed and there
  is no coupling cost. Copying the constant would create two sources of truth that could
  drift, for example if an "unknown"/"informational" level is added later.
  `pub(crate)` is the smallest visibility change that works. It does not widen the crate's
  public API.
  - Note: `advisory.rs` is **not** in Files to Modify. This one-word visibility change
    would be flagged in Step 9's scope containment check and needs explicit user approval
    before commit. If approval is refused, I would stop and ask the user. I would not
    duplicate silently, because Acceptance Criterion 3 forbids a duplicate definition.
  - The decision and the reason for it go in the commit body and the PR description.

## Rejected alternatives

| Alternative | Why rejected |
|---|---|
| Redeclare `const SEVERITY_ORDER` in `sbom.rs` | Violates AC #3 ("no duplicate definition") and DRY. Two sources of truth. |
| Move the constant to `common/` | Not needed. Both users are in the same crate. It would also put two more out-of-scope files in the diff. |
| Introduce a `Severity` enum with `Ord` | A larger refactor outside the task scope. The existing constant is enough. |
| Hard-code a `match` on severity strings in sbom.rs | Duplicates the ordering under another form. Same drift risk. |
