# Parameter Cleanup: Dead Parameter Detection and Removal for TC-9207

## Context

The task TC-9207 removes version-based filtering logic from `SbomService::list` in `modules/fundamental/src/sbom/service/sbom.rs`. The method currently accepts a `version_filter: &str` parameter that is used solely by the version filtering logic being removed. Once that logic is removed, the `version_filter` parameter becomes dead -- it is declared in the function signature but never referenced in the function body.

## Dead Parameter Detection Reasoning

After removing the `VersionMatches` filter logic from the `list` method body, the implementation performs a dead parameter scan as required by the skill's Step 9 (Dead parameter detection):

1. **Identify candidates**: The `git diff` shows removed lines that contained the only references to `version_filter` in the method body. Specifically, the removed code used `version_filter` to construct a `VersionMatches` filter and apply it to the query. No other line in the method body references `version_filter`.

2. **Confirm the parameter is dead**: After the removal, scanning the entire `list` method body reveals zero references to `version_filter`. The parameter is declared in the signature but never read, passed, or otherwise used. The Rust compiler would emit an "unused variable" warning for this parameter.

3. **Decision: Remove, do not rename**: The correct fix is to **remove the `version_filter` parameter entirely from the function signature**. The alternative -- prefixing with an underscore (`_version_filter`) -- is explicitly rejected for the following reasons:

   - **Underscore prefixes suppress compiler warnings but leave unnecessary API surface.** Every caller of `SbomService::list` would still be required to pass a `version_filter` value, even though the function ignores it completely. This creates confusion for developers who read the API signature and assume the parameter does something.
   
   - **Dead parameters accumulate technical debt.** If left in the signature, future developers may not realize the parameter is unused and may add new logic that depends on it incorrectly, or they may waste time investigating what it does.
   
   - **The Rust compiler warning exists for a reason.** The warning signals that the parameter serves no purpose. Suppressing it with `_` hides the signal without addressing the root cause. The parameter should be removed so the compiler can verify the function's actual interface.
   
   - **Clean API surface matters.** Function signatures are contracts. A parameter in the signature communicates "this value affects behavior." A dead parameter violates that contract and misleads callers.

## Call Site Updates

Removing the parameter from the function signature requires updating every call site that passes the `version_filter` argument. There are exactly 3 call sites, as documented in the task's Implementation Notes:

### Call site 1: Endpoint handler (`modules/fundamental/src/sbom/endpoints/list.rs`)

The REST endpoint handler extracts the `version` query parameter from the HTTP request and passes it to `SbomService::list`. After removing `version_filter` from the signature:

- Remove the `version` field from the query parameter struct or remove its extraction
- Remove the `version_filter` argument from the call to `service.list()`

```rust
// Before:
let results = service.list(search, paginated, &params.version, &tx).await?;
// After:
let results = service.list(search, paginated, &tx).await?;
```

### Call site 2: Search service (`modules/search/src/service/mod.rs`)

The search service calls `SbomService::list` with an empty version filter string (`""`). This was a passthrough -- the search service never used version filtering. After removing `version_filter`:

- Remove the empty string argument from the call

```rust
// Before:
let results = sbom_service.list(search, paginated, "", &tx).await?;
// After:
let results = sbom_service.list(search, paginated, &tx).await?;
```

### Call site 3: Integration tests (`tests/api/sbom.rs`)

The integration tests call `SbomService::list` with various version filter values. After removing `version_filter`:

- Remove the `test_list_sboms_version_filtered` test entirely (the feature is gone)
- Update all remaining test calls to remove the `version_filter` argument

```rust
// Before:
let results = service.list(search, paginated, "1.0", &tx).await.unwrap();
// After:
let results = service.list(search, paginated, &tx).await.unwrap();
```

## Verification: Re-running Tests

After removing the parameter and updating all 3 call sites, re-run the full test suite to verify nothing broke:

```
cargo test
```

This confirms:
- All 3 call sites compile correctly without the removed argument
- Existing SBOM list tests that do not depend on version filtering still pass
- The search service continues to function correctly
- No other hidden callers were missed by the call site analysis

If any tests fail, investigate whether additional call sites exist that were not identified in the initial analysis (use `grep -r "\.list("` across the codebase as a safety net).

## Summary

| Aspect | Approach |
|--------|----------|
| Dead parameter detected | `version_filter: &str` in `SbomService::list` |
| Root cause | Removed filtering logic was the only consumer of this parameter |
| Fix | Remove parameter from signature, not rename to `_version_filter` |
| Rationale | Underscore prefixes suppress compiler warnings but leave unnecessary API surface and mislead callers |
| Call sites updated | 3 -- endpoint handler, search service, integration tests |
| Verification | Re-run `cargo test` after all updates to confirm compilation and test passage |
