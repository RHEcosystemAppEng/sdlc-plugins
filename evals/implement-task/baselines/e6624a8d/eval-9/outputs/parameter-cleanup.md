# Parameter Cleanup Approach for TC-9207

## Overview

This document details the approach for removing the dead `version_filter` parameter from
`SbomService::list` and updating all call sites, following the skill's dead parameter
detection protocol (Step 9).

## Dead Parameter Detection

### How the dead parameter arises

The task asks to remove the version-based filtering logic from the `list` method body in
`modules/fundamental/src/sbom/service/sbom.rs`. After removing the `VersionMatches` filter
application, the `version_filter: &str` parameter is no longer referenced anywhere in the
method body. It becomes a dead parameter.

### Detection method

1. After removing the `VersionMatches` filter logic from the method body, examine the
   remaining code for any references to `version_filter`.
2. The Rust compiler will emit a warning: `unused variable: version_filter`. This confirms
   the parameter is dead.
3. Per the skill's guidance: "The correct fix is removal, not renaming." Do NOT prefix
   the parameter with an underscore (`_version_filter`). Remove it entirely from the
   function signature.

## Removal Strategy

### Step 1: Remove filter logic from method body

In `modules/fundamental/src/sbom/service/sbom.rs`, locate the `list` method and remove
the lines that apply the `VersionMatches` filter using `version_filter`. This typically
looks like:

```rust
// REMOVE this block:
if !version_filter.is_empty() {
    query = query.filter(VersionMatches(version_filter));
}
```

Or it may be unconditionally applied in the query pipeline:

```rust
// REMOVE the .filter(VersionMatches(version_filter)) from the chain:
let results = entity::sbom::Entity::find()
    .apply_search(search)
    .filter(VersionMatches(version_filter))  // <-- REMOVE THIS LINE
    .apply_pagination(paginated)
    .all(tx)
    .await?;
```

Keep all other query pipeline stages (search application, pagination, transaction usage)
intact.

### Step 2: Remove the parameter from the signature

Change the method signature from:

```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    version_filter: &str,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

To:

```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

### Step 3: Find and update all call sites

Use `find_referencing_symbols` on `SbomService::list` (via the `serena_backend` Serena
instance) or Grep for `\.list(` in relevant directories to find all callers. The task
identifies three call sites:

#### Call site 1: `modules/fundamental/src/sbom/endpoints/list.rs`

This is the REST endpoint handler. Changes:

1. Remove the `version` field from the query parameter struct (if one exists), or remove
   the manual query parameter extraction for `version`.
2. Remove the `version_filter` argument from the `service.list(...)` call.

Before:
```rust
let results = service.list(search, paginated, &params.version, &tx).await?;
```

After:
```rust
let results = service.list(search, paginated, &tx).await?;
```

Also remove any deserialization or default value logic for the `version` query parameter
(e.g., `#[serde(default)]` on a struct field, or `unwrap_or_default()` on an extraction).

#### Call site 2: `modules/search/src/service/mod.rs`

This is the search service. It passes an empty string as the version filter, confirming
it never used the filtering feature.

Before:
```rust
let sbom_results = sbom_service.list(search.clone(), paginated.clone(), "", &tx).await?;
```

After:
```rust
let sbom_results = sbom_service.list(search.clone(), paginated.clone(), &tx).await?;
```

This is a straightforward argument removal with no other changes needed.

#### Call site 3: `tests/api/sbom.rs`

Integration tests. Two changes:

1. **Remove `test_list_sboms_version_filtered`**: this test exercises the removed feature.
   Delete the entire test function. If the test calls the service method directly, it
   would fail to compile after the parameter removal. If it calls the HTTP endpoint with
   `?version=X`, it would still compile but test removed behavior.

2. **Update other test call sites**: if any remaining tests call `SbomService::list`
   directly (e.g., for setup or assertion purposes), remove the `version_filter` argument
   from those calls. Tests that go through the HTTP layer and do not pass a `version`
   query parameter need no changes.

### Step 4: Check for trait/interface constraints

Before removing the parameter, verify whether `list` is defined as part of a trait or
interface:

- Use `find_symbol` to check if `SbomService` implements a trait that declares `list`.
- If `list` is a trait method, check whether any other implementation of the trait uses
  the `version_filter` parameter. Only remove the parameter from the trait definition if
  no implementation references it.
- Based on the task description and repository structure, `list` appears to be an inherent
  method on `SbomService` (not a trait method), so trait constraints are unlikely to apply.

### Step 5: Check for unused imports

After removing the `VersionMatches` filter usage, check whether the `VersionMatches` type
import is still needed in `sbom.rs`. If it was only used in the removed filter line,
remove the import to avoid a compiler warning:

```rust
// REMOVE if no longer used:
use crate::sbom::model::VersionMatches;
```

Similarly, check `list.rs` for any imports related to the `version` query parameter
extraction that are no longer needed.

### Step 6: Re-run tests

After all call sites are updated:

1. `cargo check` -- verify compilation succeeds with zero errors and no "unused variable"
   warnings related to these changes.
2. `cargo test` -- verify all remaining tests pass. The removed test
   (`test_list_sboms_version_filtered`) should no longer appear in test output.
3. Specifically verify that SBOM list tests that do NOT depend on version filtering still
   pass unchanged.

## Summary of Changes by File

| File | Change Type | Description |
|---|---|---|
| `modules/fundamental/src/sbom/service/sbom.rs` | Modify | Remove `VersionMatches` filter logic; remove `version_filter` parameter from `list` signature; remove unused import |
| `modules/fundamental/src/sbom/endpoints/list.rs` | Modify | Remove `version` query parameter extraction; remove `version_filter` argument from `service.list()` call |
| `modules/search/src/service/mod.rs` | Modify | Remove empty-string `version_filter` argument from `sbom_service.list()` call |
| `tests/api/sbom.rs` | Modify | Remove `test_list_sboms_version_filtered` test; update any remaining direct `list()` calls |

## Risks and Mitigations

- **API breaking change**: Clients currently passing `?version=X` will have the parameter
  ignored. This is expected and documented in the task. Mitigation: version filtering has
  already been moved to the client side.
- **Search service behavior**: The search service was passing `""` (empty string), so the
  filter was never applied there. Removing the parameter has no functional impact on search
  results.
- **Missed call sites**: Use both Serena's `find_referencing_symbols` and Grep as a belt-
  and-suspenders approach to ensure no call site is missed. The Rust compiler will catch
  any remaining call sites as compilation errors.
