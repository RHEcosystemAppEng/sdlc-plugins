# Parameter Cleanup: Removing Dead Parameters and Updating Call Sites

## Why Remove Dead Parameters Instead of Underscore-Prefixing

When code that references a function parameter is removed, the parameter becomes dead --
it exists in the signature but is never used in the body. Languages like Rust will emit
a compiler warning for unused parameters, and a common quick fix is to prefix with an
underscore (`_version_filter`) to silence the warning. **This is the wrong approach.**

The correct fix is to **remove the parameter entirely** from the function signature and
update all call sites. Reasons:

1. **API clarity:** A parameter in a function signature is a promise to the caller that
   the value will be used. A dead parameter misleads callers into thinking the value
   matters, leading to confusion and maintenance burden.

2. **Unnecessary coupling:** Every caller must construct and pass the argument even
   though it has no effect. This adds noise to call sites and makes future refactoring
   harder.

3. **Compiler as safety net:** Removing the parameter causes a compile error at every
   call site. This is a feature, not a bug -- the compiler identifies every location
   that needs updating, guaranteeing no call site is missed.

4. **Underscore-prefixing hides the problem:** `_version_filter` silences the warning
   but leaves the dead parameter in place. Future developers may not realize the
   parameter is unused and may try to "fix" callers that don't pass a meaningful value.

## The Dead Parameter in TC-9207

**Function:** `SbomService::list` in `modules/fundamental/src/sbom/service/sbom.rs`

**Parameter:** `version_filter: &str`

**Why it becomes dead:** The task removes the version-based filtering logic from the
method body. After removal, `version_filter` has zero references in the function body.
The Rust compiler would emit: `warning: unused variable: version_filter`.

## Approach to Removal

### Step 1: Remove the filter logic from the method body

Remove the lines that use `version_filter` to construct and apply a `VersionMatches`
filter to the query. Keep the rest of the query pipeline intact (search parsing,
pagination, transaction handling).

### Step 2: Remove the parameter from the signature

Change the signature from:

```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    version_filter: &str,    // <-- REMOVE this
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

### Step 3: Update all 3 call sites

Use `find_referencing_symbols` (Serena) or Grep to locate every call to
`SbomService::list` and remove the `version_filter` argument from each.

**Call site 1: Endpoint handler** (`modules/fundamental/src/sbom/endpoints/list.rs`)

This is the REST handler for `GET /api/v2/sbom`. It extracts a `version` query
parameter and passes it to the service method.

Changes:
- Remove the `version` query parameter extraction from the handler.
- Remove the `version_filter` argument from the `list()` call.

Before:
```rust
let version = query.version.unwrap_or_default();
let results = sbom_service.list(search, paginated, &version, &tx).await?;
```

After:
```rust
let results = sbom_service.list(search, paginated, &tx).await?;
```

**Call site 2: Search service** (`modules/search/src/service/mod.rs`)

The search service calls `SbomService::list` with an empty string for the version
filter (effectively no filtering).

Changes:
- Remove the empty-string argument from the `list()` call.

Before:
```rust
let results = sbom_service.list(search, paginated, "", &tx).await?;
```

After:
```rust
let results = sbom_service.list(search, paginated, &tx).await?;
```

**Call site 3: Integration tests** (`tests/api/sbom.rs`)

The test file contains tests that call `SbomService::list` with various version
filter values, including a dedicated `test_list_sboms_version_filtered` test.

Changes:
- Remove the `test_list_sboms_version_filtered` test entirely, since the feature
  it tests has been removed.
- Update any remaining test calls to `SbomService::list` to remove the
  `version_filter` argument.

Before:
```rust
let results = sbom_service.list(search, paginated, "1.0", &tx).await.unwrap();
```

After:
```rust
let results = sbom_service.list(search, paginated, &tx).await.unwrap();
```

### Step 4: Compile and verify

Run `cargo check` from the workspace root to confirm all call sites compile. The
compiler will flag any call site that was missed -- this is one of the key benefits
of removing the parameter rather than underscore-prefixing it.

### Step 5: Run tests

Run the test suite for every affected crate to verify nothing is broken:

```bash
cargo test -p <fundamental-crate-name>
cargo test -p <search-crate-name>
cargo test -p <integration-test-crate-name>
```

If any test fails, investigate and fix before proceeding. The removal of
`test_list_sboms_version_filtered` is expected -- it tested the now-removed feature.
Other SBOM list tests should continue to pass because they exercise pagination,
search, and other non-version-filter behavior.

## Summary

| Aspect | Approach |
|--------|----------|
| Dead parameter detection | Identified by removing filter logic; `version_filter` has zero references in body |
| Fix strategy | Remove parameter from signature (NOT underscore-prefix) |
| Call site discovery | Use Serena `find_referencing_symbols` or Grep for `SbomService::list` |
| Call sites found | 3: endpoint handler (list.rs), search service (mod.rs), tests (sbom.rs) |
| Verification | `cargo check` (compile), `cargo test -p <crate>` (runtime) |
| Confidence | High -- Rust compiler guarantees all call sites are caught at compile time |
