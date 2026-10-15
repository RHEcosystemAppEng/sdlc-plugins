# Dead Parameter Cleanup: `version_filter` in `SbomService::list`

## Context

The task TC-9207 removes the `VersionMatches` filtering logic from `SbomService::list`.
After removing that logic, the `version_filter: &str` parameter has zero references in
the method body -- it is a dead parameter.

Per the implement-task skill (Step 9, "Dead parameter detection"), the correct fix is
**removal, not renaming**. Prefixing with underscore (`_version_filter`) silences the
compiler warning but leaves a misleading parameter in the public API. The parameter
must be removed from the signature, and all call sites must be updated to stop passing
the corresponding argument.

## Detection Method

1. **Identify candidate**: After removing the `VersionMatches` filter block from the
   `list` method body, `git diff` shows that the removed lines contained the only
   reference to `version_filter` in the function body. The parameter is now dead.

2. **Confirm dead status**: Search the method body for any remaining reference to
   `version_filter`. Expect zero matches. The Rust compiler would also emit a warning:
   `unused variable: version_filter` (or the code would need an underscore prefix to
   compile without warning, which is explicitly the wrong approach per skill guidance).

## Removal Approach

### Step 1: Remove the parameter from the function signature

**File**: `modules/fundamental/src/sbom/service/sbom.rs`

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

The `version_filter: &str` parameter is removed entirely. The remaining parameters
(`search`, `paginated`, `tx`) retain their original order and types.

### Step 2: Find all call sites

Use `mcp__serena_backend__find_referencing_symbols` on `SbomService::list` (or Grep
as fallback: `grep -rn "\.list(" modules/ tests/`) to locate every caller. The task
documents 3 call sites:

| # | File | Context | Current argument |
|---|---|---|---|
| 1 | `modules/fundamental/src/sbom/endpoints/list.rs` | REST endpoint handler | `&version_param` (extracted from query string) |
| 2 | `modules/search/src/service/mod.rs` | Search service | `""` (empty string -- no version filter) |
| 3 | `tests/api/sbom.rs` | Integration tests | Various values (`""`, `"1.0"`, etc.) |

### Step 3: Update each call site

#### Call site 1: `modules/fundamental/src/sbom/endpoints/list.rs`

- Remove the `version` query parameter extraction (e.g., remove the `version` field
  from the query params struct, or remove the `Query<VersionFilter>` extractor from the
  handler signature).
- Remove the `version_filter` argument from the `service.list(...)` call.

**Before:**
```rust
let results = service.list(search, paginated, &query.version, &tx).await?;
```

**After:**
```rust
let results = service.list(search, paginated, &tx).await?;
```

If the `version` field was the only field in a dedicated query params struct (beyond
search and pagination), the struct and its extractor can also be removed.

#### Call site 2: `modules/search/src/service/mod.rs`

- Remove the empty-string argument from the `list` call.

**Before:**
```rust
let sboms = sbom_service.list(search, paginated, "", &tx).await?;
```

**After:**
```rust
let sboms = sbom_service.list(search, paginated, &tx).await?;
```

Note: This file is **not** listed in the task's "Files to Modify" section. During
Step 9's scope containment check, this file would appear in `git diff --name-only`
as an out-of-scope modification. However, the change is mechanically required --
the code will not compile without it. I would flag this to the user for approval,
explaining that the call site update is a necessary consequence of the parameter
removal and that omitting it would cause a compilation failure.

#### Call site 3: `tests/api/sbom.rs`

- Remove `test_list_sboms_version_filtered` entirely (this test verifies the removed
  feature).
- Update all other test functions that call `SbomService::list` to remove the
  `version_filter` argument.

**Before (non-version tests):**
```rust
let results = service.list(search, paginated, "", &tx).await.unwrap();
```

**After:**
```rust
let results = service.list(search, paginated, &tx).await.unwrap();
```

### Step 4: Verify compilation and tests

Run:
```bash
cargo check -p trustify-fundamental
cargo check -p trustify-search
cargo test -p trustify-fundamental
cargo test -p trustify-tests
```

All must pass with zero warnings about unused parameters.

## Why Not Underscore-Prefix

The skill explicitly states: "The correct fix is removal, not renaming." Reasons:

1. **API clarity**: A parameter in a public method signature signals to callers that
   the value matters. An unused parameter is misleading.
2. **Caller burden**: Every caller must construct and pass a value that is silently
   ignored. The search service already passes `""` as a dummy -- this is a code smell.
3. **Future maintenance**: An underscore-prefixed parameter invites confusion about
   whether it might be used in the future, creating uncertainty for maintainers.
4. **Compiler enforcement**: Removing the parameter ensures the compiler catches any
   caller that was relying on the old signature, making the migration complete and
   verifiable.

## Trait/Interface Consideration

Before removing the parameter, check whether `list` is defined by a trait or interface.
If `SbomService::list` implements a trait method, the parameter can only be removed if
**no other implementation** of that trait uses the parameter. Use
`mcp__serena_backend__find_symbol` to check whether `list` is a trait method or an
inherent method. Based on the task description (which refers to it as a method on
`SbomService` directly), it appears to be an inherent method, making removal safe.

## Summary of Changes

| File | Change |
|---|---|
| `modules/fundamental/src/sbom/service/sbom.rs` | Remove `version_filter: &str` from signature; remove `VersionMatches` filter logic from body |
| `modules/fundamental/src/sbom/endpoints/list.rs` | Remove `version` query param extraction; remove argument from `list()` call |
| `modules/search/src/service/mod.rs` | Remove `""` argument from `list()` call (out-of-scope, requires user approval) |
| `tests/api/sbom.rs` | Delete `test_list_sboms_version_filtered`; remove argument from remaining `list()` calls |
