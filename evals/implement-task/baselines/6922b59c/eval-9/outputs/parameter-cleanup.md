# Dead Parameter Cleanup: `version_filter` in `SbomService::list`

## Overview

This document details the approach to detecting and removing the dead `version_filter` parameter that results from removing the version filtering logic in TC-9207. This follows the dead parameter detection protocol defined in SKILL.md Step 9.

## Detection

### How the parameter becomes dead

The task requires removing the `VersionMatches` filter logic from the body of `SbomService::list`. Before the change, the method body references `version_filter` to construct and apply a version filter to the query. After removing that logic, `version_filter` has zero references in the function body -- it is accepted as a parameter but never read.

### Detection method

1. After removing the filter logic, run `git diff` on `modules/fundamental/src/sbom/service/sbom.rs`.
2. Observe that the removed lines contained the only references to `version_filter` in the function body.
3. The Rust compiler will emit a warning: `unused variable: version_filter` (or suggest renaming to `_version_filter`).
4. Confirm by searching the function body for any remaining use of `version_filter` -- there are none.

### Why renaming to `_version_filter` is wrong

The Rust compiler's suggestion to prefix with `_` suppresses the warning but does not fix the problem. A dead parameter in a public API:

- Misleads future developers into thinking the parameter is reserved for future use or needed by trait constraints.
- Forces all callers to construct and pass a value that is never used, adding unnecessary code and cognitive overhead.
- Violates the principle that function signatures should reflect actual behavior.
- Creates maintenance burden: every new call site must pass a meaningless argument.

The correct fix is complete removal of the parameter from the signature and all call sites.

## Call Site Inventory

There are exactly 3 call sites for `SbomService::list` that must be updated:

### Call Site 1: `modules/fundamental/src/sbom/endpoints/list.rs`

**Context:** The REST endpoint handler for `GET /api/v2/sbom`. Extracts a `version` query parameter from the HTTP request and passes it to the service method.

**Current code (approximate):**

```rust
let results = sbom_service
    .list(search, paginated, &query.version, &tx)
    .await?;
```

**Updated code:**

```rust
let results = sbom_service
    .list(search, paginated, &tx)
    .await?;
```

**Additional cleanup at this call site:**
- Remove the `version` field from the query parameters struct (e.g., `ListSbomsQuery` or similar).
- Remove the `version` field's `#[serde]` attribute if present.
- Remove any `use` import related to the version query parameter, if it becomes unused.

### Call Site 2: `modules/search/src/service/mod.rs`

**Context:** The search service calls `SbomService::list` with an empty string for the version filter, since full-text search does not need version filtering.

**Current code (approximate):**

```rust
let sboms = sbom_service
    .list(search_query, paginated, "", &tx)
    .await?;
```

**Updated code:**

```rust
let sboms = sbom_service
    .list(search_query, paginated, &tx)
    .await?;
```

**Additional cleanup at this call site:**
- None beyond removing the argument. The empty string `""` was the only version-filter-related code here.

### Call Site 3: `tests/api/sbom.rs`

**Context:** Integration tests for the SBOM endpoint. Some tests pass specific version filter values; others pass empty strings.

**Changes:**
- Remove the `test_list_sboms_version_filtered` test function entirely (the feature it tests no longer exists).
- For all other test functions that call `SbomService::list`, remove the version filter argument.

**Current code (approximate, in remaining tests):**

```rust
let results = sbom_service.list(query, paginated, "", &tx).await.unwrap();
```

**Updated code:**

```rust
let results = sbom_service.list(query, paginated, &tx).await.unwrap();
```

**Additional cleanup at this call site:**
- Remove any test fixture data or helper functions created solely for version filter testing.
- Remove assertions that validated version-filtered results.
- If any tests send HTTP requests with `?version=...` query parameters, remove those parameters from the test URLs.

## Approach Summary

The parameter removal follows a strict sequence to maintain compilability at each step:

1. **Remove the filter logic** from the `list` method body in `sbom.rs`. At this point the code compiles with a warning about unused `version_filter`.

2. **Remove the `version_filter` parameter** from the `list` method signature. At this point the code fails to compile because callers still pass the argument.

3. **Update all 3 call sites** to remove the corresponding argument. The order of call site updates does not matter since compilation is already broken; update all three before re-checking.

4. **Clean up cascading dead code** at each call site:
   - In `list.rs`: remove the `version` query parameter extraction and its struct field.
   - In `mod.rs` (search service): remove only the empty string argument.
   - In `sbom.rs` (tests): remove the dedicated version filter test and update remaining test calls.

5. **Remove unused imports** in any file where removing the version-related code leaves imports with no remaining references.

6. **Run the compiler** (`cargo check`) to verify zero errors and zero new warnings.

7. **Run tests** (`cargo test -p trustify-fundamental`, `cargo test -p trustify-search`, and integration tests) to confirm nothing broke.

## Verification Checklist

- [ ] `version_filter` parameter removed from `SbomService::list` signature
- [ ] `version_filter` does NOT appear anywhere in `sbom.rs` method body (not even as `_version_filter`)
- [ ] Call site 1 (`endpoints/list.rs`): argument removed, `version` query param extraction removed
- [ ] Call site 2 (`search/service/mod.rs`): empty string argument `""` removed
- [ ] Call site 3 (`tests/api/sbom.rs`): all version filter arguments removed, `test_list_sboms_version_filtered` deleted
- [ ] No unused imports remain in any modified file
- [ ] `cargo check` passes with zero errors and no new warnings
- [ ] `cargo test` passes for all affected crates
- [ ] `GET /api/v2/sbom` no longer accepts a `version` query parameter
