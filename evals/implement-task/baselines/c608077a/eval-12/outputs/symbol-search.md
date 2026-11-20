# Symbol Deduplication Analysis — TC-9210

Skill reference: implement-task, Step 6, "Symbol deduplication" and "Reuse over duplication".

The task needs a severity ordering to sort remediations. Before declaring any constant,
enum, type alias or config map, I searched the whole target package for an existing
definition, not only the files I was editing.

## 1. What I needed

- A severity ordering: Critical > High > Medium > Low > None
- A `RemediationItem` struct (`advisory_id`, `severity`, `title`, `fix_version`)
- Possibly a helper that maps a severity string to a sort weight

## 2. Search scope

- **Target package**: `modules/fundamental` (crate `trustify-module-fundamental`). Both
  files to modify are in this crate: `src/sbom/service/sbom.rs` and `src/sbom/endpoints/get.rs`.
- **Wider check**: `common/`, `entity/`, `modules/ingestor/`, `modules/search/`. This
  catches a copy that might live in a shared crate.

## 3. Searches I would run (Serena instance `serena_backend`)

| # | Tool call | Purpose |
|---|---|---|
| 1 | `mcp__serena_backend__find_symbol(name_path_pattern="SEVERITY_ORDER", include_body=true)` | Find the exact constant and its visibility |
| 2 | `mcp__serena_backend__search_for_pattern(substring_pattern="(?i)severity_?order", relative_path="modules/fundamental")` | Catch name variations: `SEVERITY_ORDER`, `severityOrder`, `SeverityOrder`, `severity_order` |
| 3 | `mcp__serena_backend__search_for_pattern(substring_pattern="\"critical\",\\s*\"high\"")` | Find the same value declared under a different name, across the whole repo |
| 4 | `mcp__serena_backend__search_for_pattern(substring_pattern="(?i)(enum|struct)\\s+Severity\|fn\\s+severity_(rank|weight|order)")` | Find an existing Severity enum or a ranking helper |
| 5 | `mcp__serena_backend__get_symbols_overview(relative_path="modules/fundamental/src/advisory/service/advisory.rs")` | Confirm the structure of the file that defines it |
| 6 | `mcp__serena_backend__find_symbol(name_path_pattern="advisory", relative_path="modules/fundamental/src/lib.rs")` and read `advisory/mod.rs` and `advisory/service/mod.rs` | Check the module path is visible from `sbom` (`pub mod` or `pub(crate) mod`, or re-exports) |
| 7 | `mcp__serena_backend__find_referencing_symbols(name_path="SEVERITY_ORDER", relative_path="modules/fundamental/src/advisory/service/advisory.rs")` | See current callers, so a visibility change cannot break anything |
| 8 | `mcp__serena_backend__search_for_pattern(substring_pattern="RemediationItem\|struct\\s+Remediation")` | Check that `RemediationItem` does not exist yet |

## 4. Findings

| Symbol | Found? | Location | Notes |
|---|---|---|---|
| `SEVERITY_ORDER` | **Yes** | `modules/fundamental/src/advisory/service/advisory.rs` | `SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]`. The array index is the sort priority (0 = highest). Same crate as the code that needs it. |
| Variations (`severityOrder`, `SeverityOrder`, `severity_order`) | No other definitions expected | — | Only the one canonical definition. No second copy to merge. |
| Same value under another name | None expected | — | If one turned up, I would flag it as existing duplication and not touch it, because it is out of scope. |
| `Severity` enum / ranking helper | None expected | — | If a helper such as `fn severity_rank(&str) -> usize` existed next to the constant, I would call it instead of writing a new one. |
| `RemediationItem` | No | — | This is a new type, so declaring it is correct. |

The task Description, the Implementation Notes and Acceptance Criterion 3 all say the
constant exists in the advisory module and must be reused ("no duplicate definition").
The repository structure confirms that `advisory/service/advisory.rs` sits in the same
`fundamental` crate as `sbom/`.

## 5. Decision: REUSE `SEVERITY_ORDER`. Do not redeclare it.

**Dependency relationship (Reuse over duplication, step 1):** the source
(`advisory::service::advisory`) and the consumer (`sbom::service::sbom`) are in the
same crate, `modules/fundamental`. No new crate dependency and no `Cargo.toml` change
is needed. Under the skill rules this means I must reuse it. Duplicating it is not
acceptable.

**How it gets imported depends on the visibility found by search #1/#6:**

- **Case A: the constant is already `pub` (or `pub(crate)`) and the module path is visible.**
  Import it directly in `sbom/service/sbom.rs`:
  ```rust
  use crate::advisory::service::advisory::SEVERITY_ORDER;
  ```
  Or use the re-exported path if `advisory/service/mod.rs` re-exports it. No other file changes.

- **Case B: the constant is private (`const SEVERITY_ORDER` with no `pub`).**
  Make the smallest visibility change, `const` to `pub(crate) const`, and import it as
  in Case A. `pub(crate)` is enough because the consumer is in the same crate, and it
  avoids widening the crate's public API. I would not copy the array into `sbom.rs`.
  - **Scope caveat:** `advisory/service/advisory.rs` is not listed in Files to
    Modify. Following the skill's scope rules, I would **not** add it to the plan
    silently. I would flag it in Step 9's scope containment check as a one-line,
    visibility-only change, explain why (AC3 requires reuse, and a private constant
    cannot be imported otherwise), and wait for explicit user approval before committing.
  - If a parent module is private (for example `mod service;` in `advisory/mod.rs`),
    the same applies: make the smallest `pub(crate)` change and flag it.
  - If the user rejects the out-of-scope edit, I would stop and ask how to proceed. I would
    not fall back to redeclaring the constant, because that breaks AC3.

**Rationale recorded for reviewers (commit body / PR description):**
"Reuses `SEVERITY_ORDER` from `advisory::service::advisory` (same crate) instead of
redeclaring it, so one ordering is shared by advisory and SBOM remediation sorting."
If Case B applies, add: "Visibility changed to `pub(crate)` to allow the import."

## 6. How the constant is used (no new ordering data)

```rust
/// Returns the sort rank of a severity string by its index in `SEVERITY_ORDER`
/// (0 = most severe). Comparison ignores case. Unknown or missing severities
/// rank after all known values.
fn severity_rank(severity: Option<&str>) -> usize {
    severity
        .and_then(|s| SEVERITY_ORDER.iter().position(|o| o.eq_ignore_ascii_case(s)))
        .unwrap_or(SEVERITY_ORDER.len())
}
```

This small private helper only looks values up in the shared constant. It does not hold
any ordering data of its own. If search #4 finds an existing equivalent helper, I would
use that instead.

## 7. Self-verification (Step 9 duplication check)

After the implementation, I would re-run
`search_for_pattern("\"critical\",\\s*\"high\"")` and
`search_for_pattern("(?i)severity_?order")` over the repo. The check passes only if
there is still exactly one definition, in `advisory/service/advisory.rs`, and `sbom.rs`
contains only a `use` of it.
