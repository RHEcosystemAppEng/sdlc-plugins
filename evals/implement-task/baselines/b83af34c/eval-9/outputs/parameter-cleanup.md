# Dead Parameter Cleanup: `version_filter` in `SbomService::list`

## How the Dead Parameter Arises

The task (TC-9207) asks us to remove the version-based filtering logic from the body of `SbomService::list`. After removing that logic, the `version_filter: &str` parameter is no longer referenced anywhere in the method body. It becomes a dead parameter -- accepted by the function signature but never read or used.

## Why Dead Parameters Must Be Removed, Not Underscore-Prefixed

The Rust compiler emits an `unused variable` warning for parameters that are accepted but never read. A common but incorrect response is to rename the parameter to `_version_filter` to silence the warning. This is wrong for several reasons:

1. **It hides a real API design problem.** The parameter is part of the public method signature. Every caller must still construct and pass a value for it. Underscore-prefixing tells the compiler "I know this is unused" but does nothing to fix the fact that callers are doing unnecessary work.

2. **It misleads future developers.** A parameter in a function signature communicates intent: "this function needs this input to do its job." A dead parameter communicates false intent. A future developer reading `list(search, paginated, _version_filter, tx)` may assume the parameter will be used again soon, or that removing it would break something. Neither is true.

3. **It accumulates technical debt.** Dead parameters spread through the codebase. Every call site carries a vestigial argument. Every test constructs a value that is thrown away. Over time, multiple dead parameters accumulate and the function signature becomes a historical record of removed features rather than a description of current behavior.

4. **It violates the principle of least surprise.** Callers expect that every argument they pass affects the function's behavior. Silently ignoring an argument is a form of dishonesty in the API contract.

5. **The skill explicitly requires removal.** Step 9's dead parameter detection states: "The correct fix is removal, not renaming." This is a deliberate design choice -- the skill treats dead parameters as defects to be fixed, not warnings to be silenced.

## Approach to Removing the Dead Parameter

### Step 1: Identify the dead parameter

After removing the `VersionMatches` filter logic from the `list` method body in `modules/fundamental/src/sbom/service/sbom.rs`, scan the remaining method body for any reference to `version_filter`. Finding none, confirm it is dead.

### Step 2: Remove from the method signature

Change the signature from:

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

### Step 3: Find all call sites

Use `find_referencing_symbols` on `SbomService::list` (or Grep for `\.list(` in relevant modules) to locate every caller. The task description identifies 3 call sites:

#### Call site 1: `modules/fundamental/src/sbom/endpoints/list.rs`

This is the REST endpoint handler. It currently:
- Extracts the `version` query parameter from the HTTP request
- Passes it to `SbomService::list` as the `version_filter` argument

**Cleanup actions:**
- Remove the `version` field from the query parameter struct or extractor
- Remove the `version_filter` argument from the `service.list(...)` call
- Remove any imports related to version filtering (e.g., a `VersionQuery` type)
- If the version field was the only field in a dedicated query struct, remove the entire struct

#### Call site 2: `modules/search/src/service/mod.rs`

The search service calls `SbomService::list` with an empty version filter (`""`). This call site exists because the search service needs to list SBOMs without any version constraint.

**Cleanup actions:**
- Remove the empty string argument `""` from the `sbom_service.list(...)` call
- No other changes needed -- the search service was already not using version filtering

#### Call site 3: `tests/api/sbom.rs`

Integration tests that exercise the SBOM list endpoint. Contains:
- `test_list_sboms_version_filtered` -- a test specifically for the version filtering feature
- Other tests that call `list` with various version filter values

**Cleanup actions:**
- Delete `test_list_sboms_version_filtered` entirely -- the feature it tests has been removed
- Update all remaining `SbomService::list` calls in other tests to remove the `version_filter` argument
- Remove any `?version=X` query parameters from test HTTP requests to the list endpoint
- Remove any test fixture setup that was only needed for version filtering scenarios

### Step 4: Re-run tests

After updating all 3 call sites:

```bash
cargo test
```

This confirms:
- The code compiles without the dead parameter
- All remaining tests pass without the version filter argument
- No test was silently depending on the version filtering behavior in a way we missed

If any test fails, investigate whether it was implicitly depending on version filtering and update accordingly.

### Step 5: Verify completeness

Run `cargo clippy` (or the project's CI lint commands from CONVENTIONS.md) to confirm:
- No new `unused variable` or `dead code` warnings were introduced
- No other parameters became dead as a side effect of this change

Run `git diff --name-only` to verify scope containment -- only the 4 expected files should appear:
- `modules/fundamental/src/sbom/service/sbom.rs`
- `modules/fundamental/src/sbom/endpoints/list.rs`
- `modules/search/src/service/mod.rs`
- `tests/api/sbom.rs`

## Trait/Interface Considerations

Before removing a parameter, verify whether `list` is defined as part of a trait or interface. If `SbomService::list` implements a trait method:
- Check whether any other implementation of that trait uses the `version_filter` parameter
- If no implementation uses it, remove it from both the trait definition and all implementations
- If another implementation still uses it, the parameter cannot be removed from the trait -- only from this implementation (which may require a different approach, such as splitting the trait)

In this case, based on the task description and repository structure, `SbomService::list` appears to be a concrete method (not a trait implementation), so the parameter can be removed directly.

## Summary

The complete dead parameter cleanup touches 4 files across 3 call sites plus the definition site. The approach is: remove from definition, let the compiler identify all callers, fix each caller, re-run tests. This is strictly preferable to underscore-prefixing because it eliminates the dead parameter from the entire codebase rather than hiding it at the definition site while leaving vestigial arguments at every call site.
