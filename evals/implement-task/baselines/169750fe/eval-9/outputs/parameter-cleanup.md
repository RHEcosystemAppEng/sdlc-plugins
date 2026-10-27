# Parameter Cleanup: Dead Parameter Removal for `version_filter`

## Dead Parameter Detection

When the version-based filtering logic is removed from `SbomService::list`, the `version_filter: &str` parameter becomes dead — it is no longer referenced anywhere in the function body. The parameter exists in the signature but has zero uses in the implementation.

### Why dead parameters should be removed, not underscore-prefixed

The Rust compiler warns about unused function parameters. A common shortcut is to prefix the parameter name with an underscore (`_version_filter`) to suppress the warning. **This is the wrong approach** for public API parameters. Here's why:

1. **Underscore-prefixing hides the problem, it doesn't fix it.** The parameter still exists in the function signature. Every caller must still pass a value for it. The API surface is unnecessarily larger than it needs to be.

2. **Callers carry dead weight.** Each of the 3 call sites currently constructs or passes a `version_filter` argument. If the parameter is merely underscore-prefixed, all 3 call sites continue passing a value that is silently discarded — wasted computation, confusing code, and a maintenance trap.

3. **Future developers will be misled.** Seeing a `_version_filter` parameter suggests the parameter is temporarily unused or reserved for future use. In reality, the feature has been intentionally removed. Removal makes the intent clear: this parameter is gone, not dormant.

4. **Compiler warnings exist for a reason.** The unused parameter warning is the compiler telling you that code can be simplified. Suppressing the warning instead of acting on it leaves unnecessary complexity in the codebase.

**Correct approach:** Remove the parameter from the function signature and update every call site to stop passing the argument.

## Call Site Identification and Update Plan

Before removing the parameter, identify **all** call sites using `find_referencing_symbols` on `SbomService::list` (or Grep as fallback). The task description identifies 3 call sites:

### Call site 1: Endpoint handler (`modules/fundamental/src/sbom/endpoints/list.rs`)

**Current:** Extracts `version` from the query parameters and passes it to the service:
```rust
let result = sbom_service.list(search, paginated, &params.version, &tx).await?;
```

**After cleanup:**
- Remove the `version` field from the query parameter struct
- Remove the argument from the service call:
```rust
let result = sbom_service.list(search, paginated, &tx).await?;
```

### Call site 2: Search service (`modules/search/src/service/mod.rs`)

**Current:** Calls `list` with an empty version filter:
```rust
let sboms = sbom_service.list(search, paginated, "", &tx).await?;
```

**After cleanup:**
```rust
let sboms = sbom_service.list(search, paginated, &tx).await?;
```

### Call site 3: Integration tests (`tests/api/sbom.rs`)

**Current:** Various test functions pass version filter values to `SbomService::list`, including `test_list_sboms_version_filtered` which exercises the now-removed feature.

**After cleanup:**
- Delete `test_list_sboms_version_filtered` entirely (tests a removed feature)
- Update remaining test calls to remove the version_filter argument

## Verification

After removing the parameter and updating all call sites:

1. **Compile check:** `cargo check` must pass with no errors — confirms all call sites were found and updated
2. **Test run:** Re-run tests for all affected crates:
   - `cargo test -p <fundamental-crate>` — verifies the service and endpoint tests pass
   - `cargo test -p <search-crate>` — verifies the search service integration still works
   - `cargo test -p <integration-tests-crate>` — verifies end-to-end API tests pass
3. **Grep verification:** Search for any remaining references to `version_filter` in the codebase to confirm no call sites were missed

The crate names are resolved via `cargo metadata --no-deps --format-version 1`, not by inspecting the nearest `Cargo.toml` (which may be a virtual workspace manifest).

## Summary

| Decision | Rationale |
|----------|-----------|
| **Remove** `version_filter` from signature | Parameter is dead — zero references in function body after filter logic removal |
| **Do NOT** rename to `_version_filter` | Underscore prefixes suppress compiler warnings but leave unnecessary API surface; callers still pass unused values |
| **Update all 3 call sites** | Endpoint handler, search service, and tests must all stop passing the removed argument |
| **Delete** `test_list_sboms_version_filtered` | Tests a feature that has been intentionally removed |
| **Re-run tests** | Verify that removal doesn't break any remaining functionality |
