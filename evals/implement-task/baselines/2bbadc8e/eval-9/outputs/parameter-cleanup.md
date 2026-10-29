# Dead Parameter Cleanup: version_filter removal from SbomService::list

## Detection

Per Step 9 of the implement-task skill ("Dead parameter detection"), after removing the
version-based filtering logic from the `list` method body in
`modules/fundamental/src/sbom/service/sbom.rs`, the `version_filter: &str` parameter is
no longer referenced anywhere in the function body. This makes it a dead parameter.

### Detection method

1. **Identify candidates**: The `git diff` shows removed lines that contained the only
   references to `version_filter` in the method body (the `VersionMatches` filter
   construction and application).
2. **Confirm dead**: After the removal, zero lines in the `list` method body reference
   `version_filter`. The parameter exists only in the signature.
3. **Decision**: The correct fix is **removal**, not renaming to `_version_filter`. The
   skill explicitly states: "The correct fix is removal, not renaming."

## Parameter removal plan

### 1. Remove from function signature

**File**: `modules/fundamental/src/sbom/service/sbom.rs`

Change the `list` method signature from:

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

The `version_filter: &str` parameter is removed entirely from the signature.

### 2. Update all call sites

There are 3 call sites that must be updated. Each one currently passes a `version_filter`
argument that must be removed.

#### Call site 1: Endpoint handler

**File**: `modules/fundamental/src/sbom/endpoints/list.rs`

This is the REST endpoint handler for `GET /api/v2/sbom`. It extracts the `version` query
parameter and passes it to `SbomService::list`.

Changes:
- Remove the `version` field from the query parameters struct (e.g., `ListQuery` or
  equivalent).
- Update the call from:
  ```rust
  service.list(search, paginated, &query.version, &tx).await
  ```
  To:
  ```rust
  service.list(search, paginated, &tx).await
  ```
- Remove any imports related to version filtering if they become unused.

#### Call site 2: Search service

**File**: `modules/search/src/service/mod.rs`

The search service calls `SbomService::list` with an empty version filter string (`""`).

Changes:
- Update the call from:
  ```rust
  sbom_service.list(search, paginated, "", &tx).await
  ```
  To:
  ```rust
  sbom_service.list(search, paginated, &tx).await
  ```

**Note**: This file is NOT listed in the task's "Files to Modify" section. It is
discovered as a necessary change during dead parameter detection in Step 9. Per the
skill's scope containment check, this out-of-scope modification would be flagged to
the user for approval before proceeding. The justification is that removing a parameter
from a public method signature requires updating all callers to maintain compilation.

#### Call site 3: Integration tests

**File**: `tests/api/sbom.rs`

Integration tests pass various version filter values when calling `SbomService::list`
or when hitting the endpoint with `?version=...`.

Changes:
- Remove the `test_list_sboms_version_filtered` test function entirely (the feature
  under test no longer exists).
- For any remaining tests that call `SbomService::list` directly, update calls from:
  ```rust
  service.list(search, paginated, "", &tx).await
  ```
  To:
  ```rust
  service.list(search, paginated, &tx).await
  ```
- For tests that hit the HTTP endpoint with `?version=...` query parameters, remove
  the `version` parameter from the request URL.

### 3. Trait/interface check

Before removing the parameter, verify whether `list` is defined in a trait or interface
that `SbomService` implements. Use `mcp__serena_backend__find_symbol` or Grep to search
for trait definitions containing a `list` method with the same signature.

- If `list` is a trait method: check all implementations of the trait. Only remove the
  parameter if NO implementation references it in the method body.
- If `list` is not a trait method (standalone `impl SbomService` method): safe to remove
  directly since there is only one definition.

Based on the repository structure and conventions (each service has its own `list` method
without a shared trait), `list` is most likely a standalone method on `SbomService`, not
a trait method. Removal is safe.

### 4. Verification

After all changes:

1. Run `cargo check` to verify compilation succeeds across all crates.
2. Run `cargo test -p trustify-fundamental` to verify fundamental module tests pass.
3. Run `cargo test -p trustify-search` to verify search module tests pass (since the
   search service call site was updated).
4. Run integration tests (`cargo test --test api` or equivalent) to verify end-to-end
   tests pass.
5. Run `cargo clippy -- -D warnings` to confirm no new warnings.

## Summary

| Location | Change | Argument removed |
|---|---|---|
| `modules/fundamental/src/sbom/service/sbom.rs` | Remove `version_filter: &str` from `list` signature | (definition) |
| `modules/fundamental/src/sbom/endpoints/list.rs` | Remove `&query.version` argument from `list` call | `&query.version` |
| `modules/search/src/service/mod.rs` | Remove `""` argument from `list` call | `""` |
| `tests/api/sbom.rs` | Remove version filter argument from `list` calls; delete `test_list_sboms_version_filtered` | `""` or test-specific values |

Total call sites updated: **3**
Parameter renamed to underscore: **No** (removal is the correct fix, not renaming)
