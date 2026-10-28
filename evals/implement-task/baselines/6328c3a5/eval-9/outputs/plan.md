# Implementation Plan for TC-9207: Remove version-based filter from SBOM list endpoint

## Overview

Remove the version-based filtering logic from `SbomService::list` and then clean up
the now-dead `version_filter` parameter from the function signature and all call sites.
The task spans three files listed in the task description plus one additional call site
discovered in the implementation notes (`modules/search/src/service/mod.rs`).

## Phase 1 -- Remove Filtering Logic (Primary Task)

### File 1: `modules/fundamental/src/sbom/service/sbom.rs`

**What changes:** Remove the `VersionMatches` filter application from the `list` method
body. The method currently builds a query pipeline and applies a version filter using the
`version_filter` parameter. Remove only the filter step; keep the rest of the query
pipeline (search, pagination, transaction handling) intact.

**Before (conceptual):**
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    version_filter: &str,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError> {
    let query = ...;
    // ... search and pagination setup ...
    let query = query.filter(VersionMatches(version_filter)); // REMOVE THIS
    // ... execute and return ...
}
```

**After (conceptual):**
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    version_filter: &str,   // <-- now dead; handled in Phase 2
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError> {
    let query = ...;
    // ... search and pagination setup ...
    // (version filter line removed)
    // ... execute and return ...
}
```

At this point the `version_filter` parameter is still in the signature but is no longer
referenced in the body. This is the dead parameter that Phase 2 addresses.

### File 2: `modules/fundamental/src/sbom/endpoints/list.rs`

**What changes:** Remove the extraction of the `version` query parameter from the HTTP
request. The handler currently reads `version` from the query string (e.g., via an Axum
`Query` extractor or manual extraction) and passes it to `SbomService::list`. After
Phase 2 removes the parameter from the service signature, the handler will no longer
need to extract or pass it.

In Phase 1, we note this file needs updating but defer the call-site change to Phase 2,
since it depends on the signature change.

### File 3: `tests/api/sbom.rs`

**What changes:** Remove or gut the `test_list_sboms_version_filtered` test. This test
exercises the version filtering feature being removed, so it will either fail or become
meaningless. Other SBOM list tests that do not depend on version filtering remain
unchanged.

## Phase 2 -- Dead Parameter Cleanup

After removing the filtering logic in Phase 1, the `version_filter: &str` parameter in
`SbomService::list` is dead -- it is present in the signature but never referenced in
the function body. The implement-task skill's dead parameter detection (Step 9) requires
that dead parameters be removed from the signature, not underscore-prefixed.

### Step 2a: Remove `version_filter` from the `list` signature

Change:
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

### Step 2b: Update all 3 call sites

1. **`modules/fundamental/src/sbom/endpoints/list.rs`** (REST endpoint handler)
   - Remove the `version` query parameter extraction from the request.
   - Change the `SbomService::list` call from
     `service.list(search, paginated, &version, &tx)` to
     `service.list(search, paginated, &tx)`.
   - Remove any struct field, variable, or import related to the version query param.

2. **`modules/search/src/service/mod.rs`** (search service)
   - The search service calls `list` with an empty version filter string (e.g., `""`).
   - Change from `sbom_service.list(search, paginated, "", &tx)` to
     `sbom_service.list(search, paginated, &tx)`.
   - No other changes needed -- the search service was already not using version filtering.

3. **`tests/api/sbom.rs`** (integration tests)
   - Update any remaining test calls to `SbomService::list` to drop the `version_filter`
     argument.
   - Remove the `test_list_sboms_version_filtered` test entirely (the feature no longer
     exists).
   - Verify other SBOM list tests compile and pass without changes beyond removing the
     argument.

### Step 2c: Re-run tests

After all call sites are updated, run the test suite to confirm nothing is broken:

```bash
cargo test -p trustify-fundamental
cargo test -p trustify-search
cargo test --test api
```

(Exact crate names would be resolved via `cargo metadata --no-deps --format-version 1`.)

## Why Remove the Parameter, Not Underscore-Prefix It

See `outputs/parameter-cleanup.md` for the full rationale.

## Scope Summary

| File | Action |
|------|--------|
| `modules/fundamental/src/sbom/service/sbom.rs` | Remove version filter logic from `list` body; remove `version_filter` parameter from signature |
| `modules/fundamental/src/sbom/endpoints/list.rs` | Remove `version` query param extraction; update `list` call to drop argument |
| `modules/search/src/service/mod.rs` | Update `list` call to drop the version filter argument |
| `tests/api/sbom.rs` | Remove `test_list_sboms_version_filtered`; update other `list` calls to drop argument |

Note: `modules/search/src/service/mod.rs` is not in the task's "Files to Modify" section
but is a call site for `SbomService::list`. The skill's dead parameter detection step
(Step 9) requires updating all call sites when removing a parameter. This file would be
flagged as an out-of-scope modification during scope containment review and presented to
the user for approval before committing.

## Verification Checklist

- [ ] `list` method body no longer references `version_filter` or `VersionMatches`
- [ ] `version_filter` parameter removed from `list` signature (not underscore-prefixed)
- [ ] Endpoint handler no longer extracts or accepts `version` query parameter
- [ ] Search service call site updated (empty string argument removed)
- [ ] Test call sites updated (version filter arguments removed)
- [ ] `test_list_sboms_version_filtered` test removed
- [ ] `cargo test` passes for all affected crates
- [ ] No compiler warnings about unused parameters
