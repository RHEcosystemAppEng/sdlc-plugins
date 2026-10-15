# Parameter Cleanup: Removing `version_filter` from `SbomService::list`

## Overview

This document details the approach to removing the dead `version_filter` parameter
from `SbomService::list` and updating all call sites after the version-based
filtering logic is removed from the method body.

## Dead Parameter Detection (Step 9 of implement-task skill)

The implement-task skill's Step 9 includes a **Dead parameter detection** check:

> When the implementation removes code that references function parameters, scan the
> modified functions for parameters that are no longer used in the function body.

In this task, the primary change is removing the `VersionMatches` filter logic from
the `list` method body. After that removal, the `version_filter: &str` parameter
has zero references in the function body -- it becomes a dead parameter.

### Detection method

1. After removing the `VersionMatches` filter logic from the `list` method body,
   the `version_filter` parameter is no longer referenced anywhere in the function.
2. The Rust compiler (`rustc`) would emit a warning: `unused variable: version_filter`.
   The `cargo check` or `cargo build` step would surface this.
3. The skill's dead parameter detection step explicitly checks for this: parameters
   with zero references in the function body after code removal.

### Correct fix: removal, not renaming

The skill explicitly states: "The correct fix is removal, not renaming." This means
we do NOT prefix the parameter with an underscore (`_version_filter`) to silence the
warning. Instead, we remove the parameter entirely from the signature and update all
call sites.

## Parameter Removal Strategy

### Phase 1: Remove the filter logic from the method body

In `modules/fundamental/src/sbom/service/sbom.rs`, locate the `list` method and
remove the code block that uses `version_filter` to apply a `VersionMatches` filter
to the query. The rest of the query pipeline (search, pagination, transaction) remains
unchanged.

**Before (conceptual method body):**
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    version_filter: &str,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError> {
    let mut query = sbom::Entity::find();
    query = query.apply_search(&search);
    
    // Version filter logic (TO BE REMOVED)
    if !version_filter.is_empty() {
        query = query.filter(sbom::Column::Version.matches(version_filter));
    }
    
    let result = query.paginate(paginated).all(tx).await?;
    Ok(result)
}
```

**After removing filter logic (version_filter is now dead):**
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    version_filter: &str,  // <-- DEAD: no longer referenced
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError> {
    let mut query = sbom::Entity::find();
    query = query.apply_search(&search);
    let result = query.paginate(paginated).all(tx).await?;
    Ok(result)
}
```

### Phase 2: Remove the dead parameter from the signature

Remove `version_filter: &str` from the method signature:

```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError> {
    let mut query = sbom::Entity::find();
    query = query.apply_search(&search);
    let result = query.paginate(paginated).all(tx).await?;
    Ok(result)
}
```

### Phase 3: Find and update all call sites

Use `mcp__serena_backend__find_referencing_symbols` on `SbomService::list` (or Grep
as fallback) to locate every call site. The task identifies 3 call sites:

#### Call site 1: `modules/fundamental/src/sbom/endpoints/list.rs`

This is the REST endpoint handler. It currently:
1. Extracts a `version` query parameter from the HTTP request
2. Passes it to `SbomService::list`

**Changes:**
- Remove the `version` field from the query parameter struct (e.g., remove
  `version: Option<String>` or `version: String` from the deserialization struct)
- Update the `SbomService::list` call to remove the `version_filter` argument

**Before:**
```rust
let result = sbom_service
    .list(search, paginated, &query.version.unwrap_or_default(), &tx)
    .await?;
```

**After:**
```rust
let result = sbom_service
    .list(search, paginated, &tx)
    .await?;
```

#### Call site 2: `modules/search/src/service/mod.rs`

The search service calls `list` with an empty version filter. This call site is
NOT in the task's "Files to Modify" section, which makes it an out-of-scope
modification. However, it is a compilation-critical change -- without it, the
project will not build.

Per Step 9's scope containment check, this file would be flagged to the user for
approval with an explanation that it is required for compilation.

**Before:**
```rust
let sboms = sbom_service.list(search, paginated, "", &tx).await?;
```

**After:**
```rust
let sboms = sbom_service.list(search, paginated, &tx).await?;
```

#### Call site 3: `tests/api/sbom.rs`

Integration tests that call `SbomService::list` or hit the `GET /api/v2/sbom`
endpoint with a `version` query parameter.

**Changes:**
- **Remove** `test_list_sboms_version_filtered` entirely -- the feature it tests
  no longer exists
- **Update** any remaining test calls to `SbomService::list` to remove the
  `version_filter` argument
- **Update** any HTTP test calls that pass `?version=...` query parameters to
  the endpoint -- remove the query parameter

### Phase 4: Verify compilation and tests

1. Run `cargo check` to verify all call sites compile without the parameter
2. Run `cargo test -p <crate-name>` for each affected crate:
   - `cargo test -p trustify-fundamental` (or the actual crate name from `cargo metadata`)
   - `cargo test -p trustify-search` (for the search service call site)
   - Run integration tests in `tests/api/sbom.rs`
3. Confirm no unused-parameter warnings remain

## Trait/Interface Consideration

The skill's dead parameter detection step notes: "For trait/interface methods, only
remove if no implementation references the parameter."

For this task, we need to check whether `SbomService::list` is defined as part of a
trait implementation. If it is:
- Check all implementations of the trait to confirm none reference `version_filter`
  after the filter logic removal
- Only then remove the parameter from the trait definition and all implementations

If `list` is a plain method on `SbomService` (not a trait method), this consideration
does not apply and the parameter can be removed directly.

## Summary of All Files Modified

| File | Change | In Scope? |
|---|---|---|
| `modules/fundamental/src/sbom/service/sbom.rs` | Remove filter logic + remove `version_filter` parameter | Yes |
| `modules/fundamental/src/sbom/endpoints/list.rs` | Remove `version` query param extraction, update call site | Yes |
| `tests/api/sbom.rs` | Remove version filter test, update remaining call sites | Yes |
| `modules/search/src/service/mod.rs` | Update call site to remove `version_filter` argument | No -- flagged for user approval |

## Key Principle

The dead parameter detection step ensures that removing code from a function body
does not leave behind orphaned parameters that silently accept arguments no caller
needs to provide. The correct response is always full removal of the parameter and
updating all callers -- never renaming with an underscore prefix, which merely hides
the problem.
