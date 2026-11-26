# Symbol Deduplication Analysis — TC-9210

Per implement-task SKILL.md Step 6 "Symbol deduplication": before declaring any new
constant, enum, type alias, or configuration map, search the **target package** (not just
the file being edited) for an existing definition, including naming variations.

## Symbols the implementation needs

| Symbol | Kind | Needed for |
|---|---|---|
| `SEVERITY_ORDER` | constant (`&[&str]`) | sort key for remediation list |
| `RemediationItem` | struct | element type of the `remediations` list |

## Target package

`modules/fundamental` (crate `trustify-module-fundamental` or equivalent). Both the file
that needs the constant (`modules/fundamental/src/sbom/service/sbom.rs`) and the file the
task says defines it (`modules/fundamental/src/advisory/service/advisory.rs`) live in this
**same crate**.

## 1. `SEVERITY_ORDER`

### Searches (what I would run)

Using Serena instance `serena_backend` (from the Repository Registry):

```
mcp__serena_backend__find_symbol(name_path_pattern="SEVERITY_ORDER", include_body=true)
mcp__serena_backend__find_symbol(name_path_pattern="SeverityOrder")
mcp__serena_backend__find_symbol(name_path_pattern="severity_order")
mcp__serena_backend__search_for_pattern(substring_pattern="SEVERITY_ORDER|SeverityOrder|severity_order", relative_path="modules/fundamental")
mcp__serena_backend__search_for_pattern(substring_pattern="\"critical\",\\s*\"high\",\\s*\"medium\"", relative_path=".")
mcp__serena_backend__find_referencing_symbols(name_path="SEVERITY_ORDER", relative_path="modules/fundamental/src/advisory/service/advisory.rs")
```

Grep fallback if Serena is unavailable:

```
Grep pattern="SEVERITY_ORDER|SeverityOrder|severity_order" path=modules/fundamental
Grep pattern="\"critical\",\s*\"high\"" path=.   # value-based search across whole workspace
```

I searched both by **name** (all case variants) and by **value** (the literal
`["critical", "high", "medium", "low", "none"]` array) so that an equivalent constant
under a different name (e.g. in `common/` or `search/`) would also be caught.

### Where it was found

- **Location:** `modules/fundamental/src/advisory/service/advisory.rs`
- **Definition (per task Description + Implementation Notes):**
  `SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]`
- **Semantics:** array position = priority (index 0 = Critical = highest). This matches
  exactly what the task needs (Critical > High > Medium > Low > None).
- No other definition is expected in `modules/fundamental/src/sbom/` — the sbom module
  does not currently do severity sorting.

### Visibility check

Inspect the declaration with `find_symbol(..., include_body=true)`:

- If declared `pub const SEVERITY_ORDER` (and `advisory::service` exposes it): import directly.
- If declared as a private `const SEVERITY_ORDER` (no `pub`): it is not reachable from
  `sbom::service`.

### Decision: **REUSE — do not redeclare**

Reasoning (SKILL.md "Reuse over duplication"):

1. **Dependency relationship:** source (`advisory::service::advisory`) and target
   (`sbom::service::sbom`) are modules in the **same crate** (`modules/fundamental`). No
   `Cargo.toml` dependency is needed at all — the "dependency already exists" branch applies
   trivially.
2. **Therefore:** reuse via import. If the constant is private, widen visibility to
   `pub(crate)` (minimal visibility sufficient for intra-crate use) rather than duplicating
   it. Duplicating would violate Acceptance Criterion #3 ("no duplicate definition") and
   the DRY principle — a future change to the ordering (e.g. adding `"unknown"`) would have
   to be made in two places.
3. **Import in `sbom.rs`:**
   ```rust
   use crate::advisory::service::advisory::SEVERITY_ORDER;
   ```
   (or `crate::advisory::service::SEVERITY_ORDER` if `advisory/service/mod.rs` re-exports it —
   confirm via `get_symbols_overview` on `advisory/service/mod.rs` and follow whichever path
   existing cross-module imports use).

### Scope caveat

`advisory.rs` is **not** listed in Files to Modify. If the constant is already `pub` /
`pub(crate)`, no change is needed there and the work stays in scope. If it is private, the
one-token visibility change (`const` -> `pub(crate) const`) is out of scope, so per Step 9
"Scope containment" I would stop and ask the user to approve that single-line change to
`modules/fundamental/src/advisory/service/advisory.rs` before committing, explaining it is
required to satisfy AC #3 without duplication. Redeclaring the constant in `sbom.rs` to
avoid touching the file is explicitly rejected — it would fail AC #3.

The decision and rationale will be stated in the commit body and PR description
(SKILL.md "Flag the decision").

## 2. `RemediationItem`

### Searches

```
mcp__serena_backend__find_symbol(name_path_pattern="RemediationItem")
mcp__serena_backend__find_symbol(name_path_pattern="Remediation")
mcp__serena_backend__search_for_pattern(substring_pattern="struct\\s+\\w*Remediation\\w*|fix_version", relative_path=".")
```

### Result

Not found anywhere in the repository structure (no remediation model in `sbom/model/`,
`advisory/model/`, or `common/model/`). The task describes it as a new struct.

### Decision: **DECLARE NEW**

Declare `RemediationItem { advisory_id, severity, title, fix_version }` once, in the sbom
module, with a `///` doc comment and the same derives as sibling response models
(`Serialize`, `Deserialize`, `Debug`, `Clone`, `PartialEq`, `utoipa::ToSchema` — confirm
against `SbomSummary`/`SbomDetails`). See plan.md for location/scope discussion.

## 3. Related helper check (Step 4 "existing utilities")

- `common/src/db/query.rs` provides shared *sorting* helpers, but those are DB-level
  `ORDER BY` helpers on columns. Severity ordering here is a custom rank (string -> array
  index), not an alphabetical column sort, so the in-memory sort keyed on `SEVERITY_ORDER`
  is appropriate. I would check `query.rs` with `get_symbols_overview` to confirm there is
  no existing severity-rank helper; if one exists, reuse it instead.
- `AdvisorySummary` (`advisory/model/summary.rs`) already carries a `severity` field —
  reuse it as the source of `RemediationItem.severity` rather than re-querying.

## Summary

| Symbol | Found? | Location | Decision |
|---|---|---|---|
| `SEVERITY_ORDER` | Yes | `modules/fundamental/src/advisory/service/advisory.rs` (same crate) | **Reuse** via `use crate::advisory::service::advisory::SEVERITY_ORDER;` — widen to `pub(crate)` only if private (with user approval, since file is out of scope). Never redeclare. |
| `RemediationItem` | No | — | Declare new (single definition) |
