# Implementation Plan for TC-9207: Remove version-based filter from SBOM list endpoint

## Overview

Task TC-9207 removes the version-based filtering logic from `SbomService::list`. The
`version_filter` parameter was used to apply a `VersionMatches` filter to the query,
but this filtering has been moved client-side and is no longer needed in the backend.

Removing the filter logic from the method body leaves the `version_filter` parameter
dead (unreferenced in the function body). Per the SKILL.md dead parameter detection
guidance (Step 9), the correct fix is to **remove the parameter entirely** from the
function signature -- not to underscore-prefix it as `_version_filter`. Dead parameters
should be removed, not silenced, because they impose unnecessary coupling on every
caller and obscure the actual interface contract.

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs` -- Service method

**What changes:**
- Remove the version-based filtering logic from the `list` method body. This means
  removing the lines that use `version_filter` to apply a `VersionMatches` filter to
  the query pipeline. The rest of the query pipeline (search, pagination, transaction)
  remains intact.
- Remove the `version_filter: &str` parameter from the `list` method signature.

**Before (signature):**
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    version_filter: &str,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

**After (signature):**
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

**Rationale for parameter removal:** After the filter logic is removed from the method
body, `version_filter` has zero references in the function body. The SKILL.md Step 9
dead parameter detection rule states: "The correct fix is removal, not renaming."
Underscore-prefixing (`_version_filter`) only silences the compiler warning while
leaving a misleading parameter in the public API that every caller must still supply.

### 2. `modules/fundamental/src/sbom/endpoints/list.rs` -- Endpoint handler

**What changes:**
- Remove the extraction of the `version` query parameter from the HTTP request.
- Remove the `version_filter` argument from the call to `SbomService::list`.

**Before (call site):**
```rust
sbom_service.list(search, paginated, &version, &tx).await
```

**After (call site):**
```rust
sbom_service.list(search, paginated, &tx).await
```

This also removes the `version` query parameter from the `GET /api/v2/sbom` endpoint,
which is the intended API change.

### 3. `modules/search/src/service/mod.rs` -- Search service

**What changes:**
- Remove the empty-string `version_filter` argument from the call to `SbomService::list`.

**Before (call site):**
```rust
sbom_service.list(search, paginated, "", &tx).await
```

**After (call site):**
```rust
sbom_service.list(search, paginated, &tx).await
```

This call site was passing an empty string as the version filter (i.e., no filtering),
so removing the parameter has no behavioral impact here.

### 4. `tests/api/sbom.rs` -- Integration tests

**What changes:**
- Remove or update the `test_list_sboms_version_filtered` test, since the feature it
  tests no longer exists.
- Update any other test call sites that invoke `SbomService::list` with a
  `version_filter` argument -- remove the argument from those calls.
- Verify that remaining SBOM list tests still pass without changes.

## Handling the `version_filter` Parameter After Removing Filter Logic

The approach is a two-phase change within a single commit:

1. **Phase 1 -- Remove filter logic from method body:** Delete the lines in
   `SbomService::list` that use `version_filter` to construct and apply a
   `VersionMatches` filter. At this point the parameter is dead.

2. **Phase 2 -- Remove dead parameter and update all call sites:** Remove
   `version_filter: &str` from the signature, then update all 3 call sites:
   - `modules/fundamental/src/sbom/endpoints/list.rs` (endpoint handler)
   - `modules/search/src/service/mod.rs` (search service)
   - `tests/api/sbom.rs` (integration tests)

Both phases happen together before committing, so there is no intermediate state
where code fails to compile.

## Verification Steps

1. **Compile check:** Run `cargo check` to verify all call sites compile without the
   removed parameter.
2. **Run tests:** Run `cargo test -p <crate-name>` for each affected crate:
   - The crate containing `modules/fundamental/` (for the service and endpoint changes)
   - The crate containing `modules/search/` (for the search service change)
   - The integration test crate in `tests/`
3. **Dead parameter scan:** Confirm via `git diff` that no underscore-prefixed version
   of the parameter remains (`_version_filter`, `_version`, etc.).
4. **Scope containment:** Verify that only the 3 files listed in "Files to Modify" were
   changed. No out-of-scope files should be modified.
5. **Sensitive-pattern check:** Scan the staged diff for secrets or credentials.

## Acceptance Criteria Mapping

| Criterion | How Verified |
|-----------|-------------|
| The `list` method no longer filters by version | Filter logic removed from method body |
| The `version` query parameter is no longer extracted or accepted | Endpoint handler no longer reads `version` from query params |
| All call sites compile and pass without `version_filter` | Parameter removed from all 3 call sites; `cargo check` passes |
| Existing tests that don't depend on version filtering still pass | `cargo test` run confirms passing |
