# Parameter Cleanup: Removing the Dead `version_filter` Parameter

## Context

Task TC-9207 removes the version-based filtering logic from `SbomService::list`.
After that logic is removed, the `version_filter: &str` parameter is no longer
referenced in the method body. This document details the systematic approach to
detecting and removing this dead parameter and updating all call sites.

## Why the Parameter Becomes Dead

The `version_filter` parameter exists solely to pass a version string into the
method body, where it is used to construct a `VersionMatches` filter applied to
the database query. Once the filter logic is removed (the primary objective of
TC-9207), no line in the method body references `version_filter`. The parameter
becomes dead code.

## Approach: Removal, Not Renaming

The implement-task skill's dead parameter detection rule (Step 9) is explicit:

> "The correct fix is removal, not renaming."

Renaming to `_version_filter` would suppress the compiler warning but leave a
vestigial parameter in the public API. This creates:

- **API confusion**: callers must still pass a value that has no effect
- **Maintenance burden**: future developers may think the parameter is needed
- **Test noise**: tests must still construct and pass meaningless arguments

The correct approach is to remove the parameter from the signature entirely and
update all callers.

## Detection Method

### Step 1: Identify the dead parameter from the diff

After removing the `VersionMatches` filter logic, run `git diff` on
`modules/fundamental/src/sbom/service/sbom.rs`. Inspect the modified `list`
function: the removed lines contained the only references to `version_filter`.
The parameter now has zero references in the function body.

### Step 2: Confirm with compiler diagnostics

Running `cargo check` after removing only the filter logic (but keeping the
parameter) would produce:

```
warning: unused variable: `version_filter`
  --> modules/fundamental/src/sbom/service/sbom.rs:NN:MM
   |
NN |     version_filter: &str,
   |     ^^^^^^^^^^^^^^ help: if this is intentional, prefix it with an underscore: `_version_filter`
```

This confirms the parameter is dead. The compiler's suggestion to prefix with
underscore is a suppression mechanism, not the correct fix for a public API
parameter that should be removed.

### Step 3: Verify no trait/interface constraint

Before removing the parameter, check whether `list` is part of a trait
implementation. Use `find_referencing_symbols` on `SbomService` or inspect the
method definition for `impl SomeTrait for SbomService`.

- If `list` is a standalone method (not a trait implementation): remove the
  parameter directly.
- If `list` implements a trait method: check whether any other implementation
  of the trait uses the parameter. If no implementation uses it, remove from
  the trait definition and all implementations. If another implementation
  still uses it, the parameter cannot be removed -- flag this to the user.

Based on the task description, `list` appears to be a direct method on
`SbomService` (not a trait impl), so removal is straightforward.

## Call Site Updates (3 sites)

### Call Site 1: `modules/fundamental/src/sbom/endpoints/list.rs`

**Role**: REST endpoint handler for `GET /api/v2/sbom`

**Current code** (approximate):
```rust
let version = query.version.unwrap_or_default();
let result = service.list(search, paginated, &version, &tx).await?;
```

**Updated code**:
```rust
let result = service.list(search, paginated, &tx).await?;
```

**Additional cleanup**:
- Remove the `version` field from the query parameter struct (e.g.,
  `ListSbomsQuery` or similar)
- Remove the `version` variable binding
- Remove any imports related to version query extraction if no longer used

**Why**: The endpoint extracted the `version` query parameter solely to pass it
to `SbomService::list`. With the parameter removed, there is no reason to
extract the query parameter at all.

### Call Site 2: `modules/search/src/service/mod.rs`

**Role**: Search service that calls `SbomService::list` with an empty version filter

**Current code** (approximate):
```rust
let sboms = sbom_service.list(search, paginated, "", &tx).await?;
```

**Updated code**:
```rust
let sboms = sbom_service.list(search, paginated, &tx).await?;
```

**Additional cleanup**: None expected. The empty string `""` was a no-op
placeholder, and removing it simplifies the call.

### Call Site 3: `tests/api/sbom.rs`

**Role**: Integration tests for the SBOM endpoint

**Changes**:

1. **Delete `test_list_sboms_version_filtered`**: this test specifically exercises
   version filtering, which is being removed. The test has no value after the
   feature is gone.

2. **Update other `list` calls in tests**: any test that calls `SbomService::list`
   directly (e.g., for setup or verification) must remove the version filter
   argument:

   ```rust
   // Before
   let result = service.list(query, paginated, "", &tx).await.unwrap();
   // After
   let result = service.list(query, paginated, &tx).await.unwrap();
   ```

3. **Update HTTP test requests** (if applicable): if tests send HTTP requests
   with `?version=...` query parameters, remove those parameters. Tests that
   send requests without the version parameter need no changes.

## Execution Order

1. Remove the `VersionMatches` filter logic from the `list` method body
   (`sbom.rs`)
2. Remove `version_filter: &str` from the `list` method signature (`sbom.rs`)
3. Clean up unused imports in `sbom.rs` (e.g., `VersionMatches`)
4. Update call site 1: endpoint handler (`list.rs`) -- remove query param
   extraction and argument
5. Update call site 2: search service (`mod.rs`) -- remove empty string argument
6. Update call site 3: tests (`sbom.rs`) -- remove/update test function and
   arguments
7. Run `cargo check` to verify compilation
8. Run `cargo test` to verify all tests pass

This order ensures that the service layer change is made first, then all
consumers are updated. Running the compiler after each group of changes can
catch missed call sites early, but since all 3 sites are known, updating them
all before compiling is also acceptable.

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Missed call site | Use `find_referencing_symbols` or `grep -rn '\.list('` to find all callers. The task identifies 3; verify no others exist. |
| Trait constraint | Verify `list` is not a trait method before removing the parameter. If it is, check all implementations. |
| Downstream crates | If `SbomService::list` is part of a public API consumed by other crates in the workspace, those crates also need updating. `cargo check --workspace` catches these. |
| Version param in HTTP tests | Integration tests making HTTP requests with `?version=...` will still work (param is ignored) but should be cleaned up for clarity. |

## Summary

The cleanup follows a deterministic process: remove the logic that uses the
parameter, detect the parameter is dead (zero references in function body,
compiler warning confirms), remove the parameter from the signature (not rename
with underscore prefix), find all 3 call sites, update each to remove the
corresponding argument, and verify with compilation and tests.
