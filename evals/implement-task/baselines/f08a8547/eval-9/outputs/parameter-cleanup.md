# Parameter Cleanup: Dead Parameter Removal for TC-9207

## Overview

This document details the approach to removing the dead `version_filter` parameter
from `SbomService::list` and propagating that removal through all call sites, following
the SKILL.md Step 9 "Dead parameter detection" protocol.

## Why This Is a Dead Parameter

The task (TC-9207) instructs us to remove the version-based filtering **logic** from the
`list` method body. The task description says to "remove the filter logic from the
service method body." After this removal, the `version_filter: &str` parameter is
referenced nowhere in the function body -- it is dead.

The SKILL.md is explicit about what to do:

> **Detect dead parameters**: look for underscore-prefixed parameters (`_version`,
> `_ctx`), compiler/linter warnings about unused parameters, or parameters with
> zero references in the function body. **The correct fix is removal, not renaming.**

The naive approach -- prefixing with underscore (`_version_filter`) to silence the
Rust compiler warning -- is explicitly rejected by the skill guidance. Dead parameters
pollute the API surface, force callers to construct and pass meaningless arguments, and
obscure the actual contract of the function.

## Step-by-Step Removal Process

### Step 1: Remove the filtering logic from the method body

In `modules/fundamental/src/sbom/service/sbom.rs`, locate the `list` method and remove
the block that uses `version_filter` to apply a `VersionMatches` filter. This typically
looks like:

```rust
// REMOVE this block:
if !version_filter.is_empty() {
    query = query.filter(VersionMatches::new(version_filter));
}
```

After this removal, `version_filter` has zero references in the function body.

### Step 2: Confirm the parameter is dead

Verify that `version_filter` is not used anywhere else in the function body:
- Search the method body for any remaining reference to `version_filter`
- Check for indirect uses (passed to other functions, used in closures, etc.)
- Confirm: the parameter is dead -- it is not read, not passed, not referenced

### Step 3: Remove the parameter from the signature

Change the method signature from:

```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    version_filter: &str,       // <-- REMOVE
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

### Step 4: Find and update all call sites

Use `find_referencing_symbols` on `SbomService::list` (via serena_backend) or Grep to
locate every caller. The task description identifies 3 call sites:

#### Call site 1: Endpoint handler (`modules/fundamental/src/sbom/endpoints/list.rs`)

This is the primary consumer. Changes required:
- Remove the `version` field from the query parameter struct (e.g., `ListParams`)
- Remove the line extracting the version value (e.g., `let version = params.version.unwrap_or_default()`)
- Remove the `version_filter` argument from the `service.list(...)` call

**Before**:
```rust
let version = params.version.unwrap_or_default();
let results = service.list(search, paginated, &version, &tx).await?;
```

**After**:
```rust
let results = service.list(search, paginated, &tx).await?;
```

This also constitutes the API change: `GET /api/v2/sbom` no longer accepts a `version`
query parameter. Clients sending `?version=X` will have the parameter silently ignored
by Axum (it is simply no longer deserialized).

#### Call site 2: Search service (`modules/search/src/service/mod.rs`)

This caller passes an empty string for the version filter, confirming it never actually
filtered by version.

**Before**:
```rust
let sbom_results = sbom_service.list(search, paginated, "", &tx).await?;
```

**After**:
```rust
let sbom_results = sbom_service.list(search, paginated, &tx).await?;
```

**Scope note**: This file is not listed in the task's "Files to Modify" section.
Per SKILL.md Step 9 scope containment, this must be flagged as an out-of-scope
modification requiring user approval. The justification is mechanical necessity --
without this change, the code does not compile. The change is trivially correct
(removing an empty-string argument that was already a no-op).

#### Call site 3: Integration tests (`tests/api/sbom.rs`)

Two types of changes needed:

1. **Remove `test_list_sboms_version_filtered`**: This test exists solely to exercise
   the version filtering feature being removed. It should be deleted entirely.

2. **Update remaining test calls**: Any other tests that call `SbomService::list`
   directly (as opposed to via HTTP) need the `version_filter` argument removed.
   Tests that call via HTTP (`GET /api/v2/sbom?version=...`) need the `version`
   query parameter removed from the request URL.

### Step 5: Clean up unused imports

After removing the `VersionMatches` filter usage, check whether the `VersionMatches`
type is still imported in `sbom.rs`. If the removed filter logic was the only use,
remove the import statement. Similarly, if the `version` field removal from `ListParams`
makes any serde attributes or types unused, remove those as well.

### Step 6: Re-run tests

Run the test suite for all affected crates:

```bash
# Resolve crate names via cargo metadata, then test each
cargo test -p <fundamental-crate-name>
cargo test -p <search-crate-name>
cargo test -p <integration-test-crate-name>
```

Verify:
- No compilation errors across the workspace
- No test failures in remaining SBOM list tests
- No new compiler warnings about unused variables or imports

## Why Removal Instead of Renaming

The SKILL.md explicitly states: "The correct fix is removal, not renaming."

Renaming to `_version_filter` would:
- Silence the compiler warning but leave a dead parameter in the public API
- Force all 3 callers to continue constructing and passing a meaningless argument
- Mislead future developers into thinking the parameter might be used
- Accumulate API debt: dead parameters rarely get cleaned up later

Removal is the clean approach because:
- It accurately reflects the function's actual contract
- It simplifies every call site
- It eliminates the `version` query parameter from the REST API cleanly
- The Rust compiler will catch any missed call sites as compilation errors,
  making the refactoring safe and verifiable

## Verification Checklist

- [ ] `version_filter` parameter removed from `SbomService::list` signature
- [ ] All filtering logic referencing `version_filter` removed from method body
- [ ] `VersionMatches` import removed if no longer used
- [ ] Endpoint handler no longer extracts `version` query parameter
- [ ] `version` field removed from `ListParams` struct
- [ ] Search service call site updated (empty string argument removed)
- [ ] `test_list_sboms_version_filtered` test removed
- [ ] Remaining test call sites updated
- [ ] All crates compile without errors or new warnings
- [ ] All remaining tests pass
- [ ] `docs/api.md` updated if it documents the `version` query parameter
- [ ] Out-of-scope file (`modules/search/src/service/mod.rs`) flagged for user approval
