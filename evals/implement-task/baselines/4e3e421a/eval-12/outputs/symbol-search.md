# Symbol Deduplication Analysis — TC-9210

Skill reference: implement-task Step 6, "Symbol deduplication" and "Reuse over duplication".

## 1. Symbols the task needs

| Symbol | Kind | Needed for |
|---|---|---|
| `SEVERITY_ORDER` | constant (`&[&str]`) | sorting key for the remediation list |
| `RemediationItem` | struct | element type of the `remediations` field |
| severity rank helper (e.g. `severity_rank`) | function | maps a severity string to its index in `SEVERITY_ORDER` |

## 2. What I would search for, and where

Target package: the `fundamental` crate (`modules/fundamental/`). The task names the sibling
module `advisory`, so I search the whole crate, not just `sbom/service/sbom.rs`. I also check the
workspace crates that `fundamental` already depends on (`common`, `entity`).

### 2a. `SEVERITY_ORDER` and its variants

Serena (instance `serena_backend`, taken from the Repository Registry):

```
mcp__serena_backend__find_symbol(name_path_pattern="SEVERITY_ORDER", include_body=true)
mcp__serena_backend__find_symbol(name_path_pattern="SeverityOrder")
mcp__serena_backend__find_symbol(name_path_pattern="severity_order")
mcp__serena_backend__search_for_pattern(substring_pattern="SEVERITY_ORDER|SeverityOrder|severity_order|severityOrder")
```

Search by value, to catch the same list declared under a different name:

```
mcp__serena_backend__search_for_pattern(substring_pattern="\"critical\",\\s*\"high\",\\s*\"medium\"")
mcp__serena_backend__search_for_pattern(substring_pattern="enum\\s+Severity")
```

Grep fallback, in case rust-analyzer is still indexing (the Code Intelligence section says
indexing can take 30-60s):

```
Grep pattern="SEVERITY_ORDER|SeverityOrder|severity_order" path="modules/" type="rust"
Grep pattern="\"critical\",\s*\"high\"" path="." type="rust"
```

Then I would check who already uses it, so I don't break any callers:

```
mcp__serena_backend__find_referencing_symbols(name_path="SEVERITY_ORDER",
    relative_path="modules/fundamental/src/advisory/service/advisory.rs")
```

### 2b. `RemediationItem`

```
mcp__serena_backend__find_symbol(name_path_pattern="RemediationItem")
mcp__serena_backend__search_for_pattern(substring_pattern="Remediation")
```

### 2c. Existing severity rank or compare helpers

```
mcp__serena_backend__search_for_pattern(substring_pattern="fn .*severity.*\\(")
mcp__serena_backend__get_symbols_overview(relative_path="modules/fundamental/src/advisory/service/advisory.rs")
mcp__serena_backend__get_symbols_overview(relative_path="common/src/db/query.rs")
```

## 3. Findings

| Symbol | Found? | Location |
|---|---|---|
| `SEVERITY_ORDER` | **Yes** | `modules/fundamental/src/advisory/service/advisory.rs`, `SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]` (task Description and Implementation Notes; file is in the repo tree as "AdvisoryService: fetch, list, search") |
| `SeverityOrder` / `severity_order` variants | Expected none | — |
| Duplicate value list elsewhere | Expected none | — |
| `RemediationItem` | Not found | Nothing in the repo tree or the task suggests it exists. It is a new type. |
| Severity rank helper | Not confirmed | If `advisory.rs` already has a helper that ranks severities by `SEVERITY_ORDER`, reuse it as well. |

Note: the Description says the constant "maps severity strings to numeric sort weights", while
the Implementation Notes give it as a plain array. These agree: the array index is the weight
(0 = critical, 4 = none). I would confirm the real shape with `find_symbol(include_body=true)`
before writing the sort code.

## 4. Decision: REUSE `SEVERITY_ORDER`, do not redeclare it

Reasoning, following "Reuse over duplication":

1. **Dependency check.** `sbom` and `advisory` are both modules in the same crate
   (`modules/fundamental`). There is no cross-crate edge to add and nothing to change in
   `Cargo.toml`.
2. **Visibility check.** I would check the declaration in `advisory.rs`:
   - **Already `pub` (or `pub(crate)`) and the module path is reachable**: import it as is:
     `use crate::advisory::service::advisory::SEVERITY_ORDER;`
   - **Private (`const SEVERITY_ORDER`)**: widen it to `pub(crate) const SEVERITY_ORDER`. That
     is the smallest change that lets `sbom` import it while keeping it out of the crate's
     public API. Copying it into `sbom.rs` is **not** acceptable. Acceptance criterion 3
     requires "no duplicate definition", and the same-crate case is exactly where the skill says
     to make the symbol visible instead of duplicating it.
   - Also check that `advisory/service/mod.rs` declares `advisory` as a reachable module
     (`pub mod advisory;` or `pub(crate) mod advisory;`). If it is a private `mod advisory;`,
     the import path needs a re-export or a wider module visibility.
3. **Scope consequence.** `advisory.rs` (and possibly `advisory/service/mod.rs`) is **not**
   listed in Files to Modify. If either needs a visibility change, I would list it under Step 9
   scope containment and ask the user to approve it before committing. I would explain that a
   one-word visibility change is needed to satisfy the "no duplicate definition" criterion.
   I would not silently redeclare the constant to stay inside scope.
4. **Record the decision.** The commit body and PR description will say: "Reuses
   `SEVERITY_ORDER` from `advisory::service::advisory` (same crate). Visibility widened to
   `pub(crate)` if required, and no duplicate definition was added."

## 5. Decision for `RemediationItem`: declare it new

It does not exist, so it gets declared. The task lists no model file, so I would put it in
`modules/fundamental/src/sbom/service/sbom.rs` next to the builder that produces it. That file
is in scope. If the serialized `SbomDetails` struct in `sbom/model/details.rs` must carry the
field, I would flag that file for approval too (see plan.md). It gets a `///` doc comment and
derives `Serialize`, `Clone`, `Debug`, `PartialEq` (plus `utoipa::ToSchema` if sibling models
use it).

## 6. Post-implementation duplication check (Step 9)

After implementing, I would re-run
`search_for_pattern("SEVERITY_ORDER|\"critical\",\\s*\"high\"")` and expect exactly one
declaration (in `advisory.rs`) plus the new `use` in `sbom.rs`. Any second declaration fails
the check.
