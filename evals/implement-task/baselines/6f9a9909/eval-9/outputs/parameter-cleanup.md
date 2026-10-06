# Dead Parameter Cleanup: version_filter

## Context

Task TC-9207 requires removing the version-based filtering logic from the body of `SbomService::list`. After this removal, the `version_filter: &str` parameter becomes dead -- it is still present in the function signature but has zero references in the function body.

## Dead Parameter Detection (implement-task Skill Step 9)

The implement-task skill's Step 9 includes a "Dead parameter detection" protocol that applies directly to this scenario:

> When the implementation removes code that references function parameters, scan the modified functions for parameters that are no longer used in the function body.

### Detection process

1. **Identify candidate**: After removing the `VersionMatches` filter logic from the `list` method body, run `git diff` to confirm that the removed lines contained the only references to `version_filter` in the function body.

2. **Confirm the parameter is dead**: Verify that `version_filter` has zero remaining references in the method body. The Rust compiler would also flag this as an "unused variable" warning (or error under `-D warnings`), but the skill requires proactive detection rather than waiting for compiler output.

3. **Correct fix is removal, not renaming**: The skill explicitly states: "The correct fix is removal, not renaming." Do not prefix the parameter with `_` (i.e., do not rename to `_version_filter`). Underscore-prefixing silences the compiler warning but leaves dead code in the API surface, burdening all callers with an argument that serves no purpose.

## Parameter Removal Approach

### Step 1: Remove from function signature

Change the `SbomService::list` signature from:

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

### Step 2: Find all call sites

Use `find_referencing_symbols` on `SbomService::list` (via the `serena_backend` Serena instance) or Grep as fallback to find every caller. The task description identifies 3 call sites:

| # | File | Current call | Purpose |
|---|------|-------------|---------|
| 1 | `modules/fundamental/src/sbom/endpoints/list.rs` | `service.list(search, paginated, &version, &tx)` | REST endpoint handler |
| 2 | `modules/search/src/service/mod.rs` | `sbom_service.list(search, paginated, "", &tx)` | Search service (passes empty filter) |
| 3 | `tests/api/sbom.rs` | `service.list(query, paginated, "1.0", &tx)` (and similar) | Integration tests |

### Step 3: Update each call site

**Call site 1 -- Endpoint handler** (`modules/fundamental/src/sbom/endpoints/list.rs`):
- Remove the `version` field from the query parameter deserialization struct
- Remove the extraction of the version value from query params
- Remove the `version_filter` argument from the `service.list(...)` call
- Before: `service.list(search, paginated, &params.version.unwrap_or_default(), &tx)`
- After: `service.list(search, paginated, &tx)`

**Call site 2 -- Search service** (`modules/search/src/service/mod.rs`):
- Remove the empty string argument that was passed as the version filter
- Before: `sbom_service.list(search, paginated, "", &tx)`
- After: `sbom_service.list(search, paginated, &tx)`
- This call site was already passing an empty filter, meaning the search service never used version filtering. The cleanup here is purely mechanical.

**Call site 3 -- Tests** (`tests/api/sbom.rs`):
- Remove the `test_list_sboms_version_filtered` test entirely (tests removed functionality)
- For any other test that calls `SbomService::list` directly, remove the version argument
- For HTTP-level tests that pass `?version=...` as a query parameter, remove the parameter from the request URL. These tests should continue to work since the endpoint still returns SBOM lists -- it just no longer filters by version.

### Step 4: Trait/interface check

Before removing the parameter, verify whether `list` is defined on a trait that `SbomService` implements:

- Use `find_symbol` to check if there is a trait definition for `list`
- If `list` is a trait method: check all implementations of the trait. Only remove the parameter if **no** implementation references it in the body.
- If `list` is an inherent method (not part of a trait): safe to remove without checking other implementations.

Based on the task description, `list` appears to be an inherent method on `SbomService` (no trait is mentioned). Proceed with removal.

### Step 5: Re-run tests

After updating all call sites:

```bash
cargo test -p trustify-fundamental
cargo test -p trustify-search
```

Confirm that:
- All modified code compiles without warnings
- All remaining tests pass
- No test references the removed `version_filter` parameter

### Step 6: Verify with clippy

```bash
cargo clippy -p trustify-fundamental -p trustify-search -- -D warnings
```

Clippy should report no unused parameter warnings since the parameter was removed (not underscore-prefixed).

## Why Removal Over Underscore-Prefix

| Approach | Effect | Problem |
|----------|--------|---------|
| `_version_filter` | Silences warning | All 3 callers still pass a useless argument; the dead parameter persists in the public API |
| Remove parameter | Clean API | All callers are simplified; no dead code remains |

The skill is explicit: "The correct fix is removal, not renaming." Underscore-prefixing is a compiler workaround, not a code quality fix. It leaves callers burdened with constructing and passing an argument that is ignored, and it obscures the fact that the functionality was intentionally removed.

## Out-of-Scope File Handling

The task's "Files to Modify" section lists 3 files, but `modules/search/src/service/mod.rs` is also a call site that must be updated. This file is technically out of scope per the task description. Per Step 9's scope containment check:

1. Flag `modules/search/src/service/mod.rs` as out-of-scope
2. Explain: "This file calls `SbomService::list` with the removed `version_filter` parameter. It must be updated for compilation to succeed."
3. Request user approval before including it in the commit

This is a mechanical, compilation-required change (removing one argument from a function call), so approval is expected.

## Summary

The dead parameter cleanup for `version_filter` is a direct application of the implement-task skill's Step 9 dead parameter detection protocol. The approach is:

1. Remove filter logic from method body (Step 6)
2. Detect that `version_filter` is now dead (Step 9)
3. Remove parameter from signature (Step 9)
4. Update all 3 call sites to remove the argument (Step 9)
5. Re-run tests to confirm nothing broke (Step 9)

Total files modified: 4 (3 in scope + 1 out-of-scope requiring approval).
