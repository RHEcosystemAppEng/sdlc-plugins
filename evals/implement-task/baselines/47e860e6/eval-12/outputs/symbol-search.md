# Symbol Deduplication Analysis — TC-9210

Following implement-task Step 6, "Symbol deduplication": search the **target package**
(not only the file being edited) before declaring any new constant, enum, type alias,
or configuration map.

Target package: `modules/fundamental` (crate `fundamental`), repo `trustify-backend`.
Code intelligence: Serena instance `serena_backend` (rust-analyzer), from the
Repository Registry in CLAUDE.md. This is a simulated run, so the searches below are
the ones I would run, checked against the repo structure in `repo-backend.md` and the
task's Implementation Notes.

## 1. Symbols the task would introduce

| Symbol | Kind | Needed for |
|---|---|---|
| `SEVERITY_ORDER` | constant (`&[&str]`) | severity sort key |
| `RemediationItem` | struct | item in the remediation list |
| severity-rank helper (e.g. `severity_rank`) | function | maps a severity string to its sort weight |

## 2. Searches for `SEVERITY_ORDER`

Name variations covered: `SEVERITY_ORDER`, `severity_order`, `SeverityOrder`,
`SEVERITY_RANK`, `SEVERITY_WEIGHTS`, `severity_rank`, `severity_weight`.

1. `mcp__serena_backend__find_symbol(name_path_pattern="SEVERITY_ORDER", relative_path="modules/fundamental", include_body=true)`
2. `mcp__serena_backend__search_for_pattern(substring_pattern="(?i)severity_?(order|rank|weight)", relative_path="modules/fundamental")`
3. Search by value, to catch the same constant under a different name:
   `mcp__serena_backend__search_for_pattern(substring_pattern="\"critical\",\\s*\"high\",\\s*\"medium\"", relative_path=".")`
4. Workspace-wide check of `common/` and the other modules, to see whether a shared
   definition exists anywhere else:
   `mcp__serena_backend__search_for_pattern(substring_pattern="SEVERITY_ORDER", relative_path=".")`
5. Callers of the existing definition:
   `mcp__serena_backend__find_referencing_symbols(name_path="SEVERITY_ORDER", relative_path="modules/fundamental/src/advisory/service/advisory.rs")`

### Result

- **Found** in `modules/fundamental/src/advisory/service/advisory.rs`:
  ```rust
  SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]
  ```
  The task Description and Implementation Notes both name this location, and Acceptance
  Criterion 3 says "no duplicate definition".
- No other definition was expected in `common/`, `sbom/`, `package/`, `ingestor/` or
  `search/`. If a second copy did turn up, I would report it to the user and not add a
  third one.

## 3. Decision for `SEVERITY_ORDER`: REUSE, do not redeclare

Checks from "Reuse over duplication":

1. **Dependency relationship.** The source (`advisory/service/advisory.rs`) and the
   target (`sbom/service/sbom.rs`) are in the **same crate** (`modules/fundamental`).
   No `Cargo.toml` change is needed and no new cross-package coupling is added.
2. **Visibility.** I would check with `find_symbol(..., include_body=true)`, plus
   `get_symbols_overview` on `advisory/service/mod.rs` and `advisory/mod.rs`, that the
   constant and the module path down to it are reachable from `crate::sbom`.
   - **Already `pub` (or `pub(crate)`) and the module path is public:** import it with
     `use crate::advisory::service::advisory::SEVERITY_ORDER;`. Nothing else changes.
   - **Private (`const SEVERITY_ORDER` with no `pub`):** the dependency already exists
     because it is the same crate. The rule then says to widen visibility rather than
     duplicate, so the fix is a one-word change to `pub(crate) const SEVERITY_ORDER`.
     `pub(crate)` is the smallest visibility that works, since nothing outside the crate
     needs it. **However, `advisory.rs` is not in Files to Modify.** Following the scope
     rule, I would not quietly edit it. I would raise it in Step 9's scope check as a
     one-line out-of-scope change, with this rationale: AC 3 forbids a duplicate
     definition, and the constant can only be reached by widening its visibility. I
     would ask the user to approve it. If the user declines, I would stop and ask how
     they want to proceed. I would **not** fall back to redeclaring, because that would
     break AC 3.
3. **Record the decision.** The commit body and PR description would say:
   "Reuses `SEVERITY_ORDER` from `advisory::service::advisory` (same crate) rather than
   redeclaring it", plus the visibility change if one was needed.

## 4. Searches for `RemediationItem`

- `find_symbol(name_path_pattern="RemediationItem", relative_path=".")`
- `search_for_pattern(substring_pattern="(?i)remediation", relative_path=".")`

**Result:** not found. The repo tree shows no remediation model, and the task
introduces the struct. **Decision: declare it**, in `sbom/service/sbom.rs`, which is in
scope and next to the builder that produces it. It is re-exported for the endpoint in
`get.rs`. The natural home would be `sbom/model/` (for example `details.rs`), but that
file is not in Files to Modify. I would mention moving it to `sbom/model/` as an
optional follow-up in the Step 9 scope report and would not do it on my own.

## 5. Searches for a severity-rank helper

- `search_for_pattern(substring_pattern="SEVERITY_ORDER\\s*\\.\\s*iter\\(\\)\\s*\\.\\s*position", relative_path="modules/fundamental")`
- `find_referencing_symbols` on `SEVERITY_ORDER` (search 5 above). If the advisory
  service already has a helper such as `fn severity_rank(s: &str) -> usize` that it uses
  for its own sorting, I would reuse it on the same visibility terms as the constant.

**Decision:** reuse an existing helper if one exists. Otherwise write a small private
helper in `sbom.rs` that derives the rank **from `SEVERITY_ORDER`**
(`SEVERITY_ORDER.iter().position(..)`). It contains no hard-coded severity strings, so
the ordering is still defined in one place only.

## 6. Also checked: `common/src/db/query.rs`

`common/src/db/query.rs` has shared sorting helpers. These are SQL `ORDER BY`
builders, while the remediation list is sorted in memory by a domain-specific
severity rank. They do not do the same job, so there is nothing to reuse there. I
would confirm this with `get_symbols_overview` on `query.rs`.

## Summary

| Symbol | Found? | Location | Decision |
|---|---|---|---|
| `SEVERITY_ORDER` | Yes | `modules/fundamental/src/advisory/service/advisory.rs` | **Reuse** via `use crate::advisory::service::advisory::SEVERITY_ORDER;`. If it is private, widen it to `pub(crate)` (one line, out of scope, flagged for user approval). Never redeclare. |
| `RemediationItem` | No | — | Declare in `sbom/service/sbom.rs` |
| severity-rank helper | Check advisory.rs | — | Reuse if it exists. Otherwise a private helper built on `SEVERITY_ORDER` |
