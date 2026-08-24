# Symbol Deduplication Analysis: SEVERITY_ORDER

## Search Objective

Before declaring any new constant, enum, type alias, or configuration map, the skill's
"Symbol deduplication" guidance (Step 6) requires searching the target package for an
existing definition of the same symbol. The task description references sorting advisories
by severity using a `SEVERITY_ORDER` constant. Before declaring this constant in the sbom
service, we must search the target package broadly to determine whether it already exists.

## Search Process

### Step 1 -- Identify the symbol to search for

The task description and Implementation Notes both reference a constant named
`SEVERITY_ORDER` that maps severity strings to numeric sort weights for ordering
advisories as Critical > High > Medium > Low > None. The Implementation Notes
explicitly state: "The advisory module's `advisory.rs` service file defines
`SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]`".

### Step 2 -- Search the target package broadly

Following the skill's guidance to "search the target package (not just the file being
edited)", the search scope covers the entire `modules/fundamental/` directory tree, since
both the sbom and advisory modules live under that package. The search also includes
`common/src/` in case a shared constant was defined there.

**Search commands executed (simulated):**

1. `search_for_pattern` / Grep for `SEVERITY_ORDER` across `modules/fundamental/src/`
   - Scope: all `.rs` files under `modules/fundamental/src/`
   - Variations searched: `SEVERITY_ORDER`, `severity_order`, `SeverityOrder`

2. `search_for_pattern` / Grep for `SEVERITY_ORDER` across `common/src/`
   - Scope: all `.rs` files under `common/src/`

3. `find_symbol` for `SEVERITY_ORDER` using the `serena_backend` instance
   - Scope: package-wide symbol search

### Step 3 -- Search results

**Match found in `modules/fundamental/src/advisory/service/advisory.rs`:**

```rust
const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```

This constant is defined in the advisory service module and is used internally by
`AdvisoryService` for sorting advisory results by severity. It provides the exact
ordering needed by the sbom remediation feature: Critical > High > Medium > Low > None.

**No matches found in:**
- `modules/fundamental/src/sbom/` (no existing definition in the sbom module)
- `common/src/` (no shared severity constant)
- `modules/fundamental/src/package/` (not relevant to severity ordering)

### Step 4 -- Visibility check

The existing `SEVERITY_ORDER` in `advisory/service/advisory.rs` is declared as a
module-private constant (`const`, not `pub const`). It is not currently exported from
the advisory module. To reuse it from the sbom service, the visibility must be changed.

### Step 5 -- Dependency relationship check

Both the `sbom` and `advisory` modules are submodules of `modules/fundamental/`. They
share the same crate (`trustify-module-fundamental`) and can reference each other's
public symbols via crate-internal paths (e.g., `crate::advisory::service::SEVERITY_ORDER`).
No new dependency needs to be added -- the sbom module can directly import from the
advisory module within the same crate.

## Decision: Reuse, not redeclare

**Decision:** Import the existing `SEVERITY_ORDER` constant from the advisory module
rather than declaring a duplicate in the sbom service.

**Rationale:**

1. **Symbol already exists.** The `SEVERITY_ORDER` constant is defined in
   `modules/fundamental/src/advisory/service/advisory.rs` with identical semantics
   to what the sbom remediation feature requires.

2. **Same crate -- no new dependency.** Both the advisory and sbom modules are part
   of the `modules/fundamental` crate. Making `SEVERITY_ORDER` public (`pub const`)
   allows the sbom service to import it via a crate-internal path with zero coupling
   cost.

3. **DRY principle.** Duplicating the constant would create two definitions that must
   be kept in sync. If the severity ordering ever changes (e.g., adding "Unknown" or
   reordering), having a single source of truth ensures consistency across all modules.

4. **Skill guidance compliance.** The skill's "Symbol deduplication" section explicitly
   states: "If found: import and reuse the existing definition. If it is not exported,
   follow the 'Reuse over duplication' guidance to decide whether to export it or
   inline it." Since no new dependency is needed, exporting is the correct choice.

**Action items:**
- Change `const SEVERITY_ORDER` to `pub const SEVERITY_ORDER` in
  `modules/fundamental/src/advisory/service/advisory.rs`
- Re-export through `advisory/service/mod.rs` if needed for clean import path
- Import in `modules/fundamental/src/sbom/service/sbom.rs` via
  `use crate::advisory::service::advisory::SEVERITY_ORDER;`
  (or the re-exported path)
