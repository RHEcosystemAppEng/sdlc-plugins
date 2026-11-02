# Implementation Plan — TC-9207: Remove version-based filter from SBOM list endpoint

## Step 0 – Validate Project Configuration

CLAUDE.md contains the required sections:
- **Repository Registry**: trustify-backend with Serena instance `serena_backend`
- **Jira Configuration**: Project key TC, Cloud ID, Feature issue type ID, custom fields
- **Code Intelligence**: `mcp__serena_backend__<tool>` naming convention

Configuration is valid. Proceed.

## Step 1 – Fetch and Parse Jira Task

**Key**: TC-9207
**Summary**: Remove version-based filter from SBOM list endpoint
**Repository**: trustify-backend
**Target Branch**: main

### Parsed Sections

- **Description**: Remove the version-based filtering logic from `SbomService::list`. The `version_filter` parameter was used to filter SBOMs by version string but is no longer needed — filtering moved to client side.
- **Files to Modify**:
  1. `modules/fundamental/src/sbom/service/sbom.rs` — remove version-based filtering logic from the `list` method
  2. `modules/fundamental/src/sbom/endpoints/list.rs` — remove `version` query parameter extraction, stop passing it to the service method
  3. `tests/api/sbom.rs` — remove or update `test_list_sboms_version_filtered` test
- **Files to Create**: none
- **API Changes**: `GET /api/v2/sbom` — remove `version` query parameter support
- **Target PR**: none
- **Bookend Type**: none
- **Dependencies**: none

## Step 1.5 – Verify Description Integrity

No digest comment found — skipping integrity check. This task may have been created before digest tracking was introduced.

## Step 4 – Understand the Code

### Code Inspection

Before modifying any files, inspect the current state of each file to be modified:

1. **`modules/fundamental/src/sbom/service/sbom.rs`** — read the `list` method to understand its full signature and body, specifically how `version_filter` is used in the query pipeline. The current signature is:
   ```rust
   pub async fn list(
       &self,
       search: Query,
       paginated: Paginated,
       version_filter: &str,
       tx: &Transactional<'_>,
   ) -> Result<PaginatedResults<SbomSummary>, AppError>
   ```
   The `version_filter` parameter applies a `VersionMatches` filter to the query. After removing this filter logic, the parameter will become dead — unused in the method body.

2. **`modules/fundamental/src/sbom/endpoints/list.rs`** — read the endpoint handler to see how it extracts the `version` query parameter and passes it to `SbomService::list`.

3. **`modules/search/src/service/mod.rs`** — read how `SearchService` calls `SbomService::list` with an empty version filter (`""`).

4. **`tests/api/sbom.rs`** — read the test file to identify `test_list_sboms_version_filtered` and any other tests that call `SbomService::list` with a version filter argument.

### Sibling analysis / Convention conformance

From inspecting sibling modules (advisory, package):
- **Error handling**: `Result<T, AppError>` with `.context()` wrapping — consistent throughout service layer
- **Module pattern**: `model/ + service/ + endpoints/` structure
- **Response types**: List endpoints return `PaginatedResults<T>`
- **Query helpers**: Shared filtering and pagination via `common/src/db/query.rs`
- **Test patterns**: Integration tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)`

### Crate name resolution

Run `cargo metadata --no-deps --format-version 1` from the workspace root to resolve the crate name for `modules/fundamental/`. The package name from cargo metadata (e.g., `trustify-module-fundamental`) is used for running module-level tests — not derived from the nearest `Cargo.toml`, which may be a virtual workspace manifest.

Similarly resolve the crate for `modules/search/` and `tests/` to run their tests.

## Step 5 – Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9207
```

## Step 6 – Implement Changes

### File 1: `modules/fundamental/src/sbom/service/sbom.rs`

**Change**: Remove the `version_filter` parameter from the `list` method signature AND remove the version filtering logic from the method body.

The updated signature becomes:
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

Remove the `version_filter: &str` parameter entirely. In the method body, remove the `VersionMatches` filter application that uses this parameter. Keep the rest of the query pipeline (search, pagination, sorting) intact.

**Dead parameter detection**: Removing the version filtering logic from the body leaves `version_filter` unused. Rather than renaming it to `_version_filter` (which would only suppress the compiler warning but leave unnecessary API surface), remove the parameter from the signature entirely and update all call sites.

### File 2: `modules/fundamental/src/sbom/endpoints/list.rs`

**Change**: Remove the `version` query parameter extraction from the endpoint handler. Stop passing the `version_filter` argument to `SbomService::list`.

Before:
```rust
let version = query.version.unwrap_or_default();
let result = service.list(search, paginated, &version, &tx).await?;
```

After:
```rust
let result = service.list(search, paginated, &tx).await?;
```

Remove the `version` field from the query parameter struct if it's defined inline, or stop extracting it.

### File 3: `modules/search/src/service/mod.rs` (call site update — out of Files to Modify but required)

**Note**: This file is listed in the Implementation Notes as one of the 3 call sites for `SbomService::list`. It calls `list` with an empty version filter. After removing the `version_filter` parameter, this call site must be updated to no longer pass the argument.

Before:
```rust
sbom_service.list(search, paginated, "", &tx).await?
```

After:
```rust
sbom_service.list(search, paginated, &tx).await?
```

**Scope note**: This file is not in Files to Modify but must be updated because removing a parameter requires updating all call sites. Flag in Step 9 scope containment check for user approval.

### File 4: `tests/api/sbom.rs`

**Change**:
1. Remove or update the `test_list_sboms_version_filtered` test — since version filtering is no longer supported, this test is invalid.
2. Update any other test calls to `SbomService::list` that pass a `version_filter` argument — remove the argument from each call.

## Step 7 – Write Tests

- Remove `test_list_sboms_version_filtered` since the feature under test no longer exists.
- Verify all remaining SBOM list tests still compile and pass without the `version_filter` argument.
- No new tests needed — this is a feature removal.

## Step 8 – Verify Acceptance Criteria

- [x] The `list` method in SbomService no longer filters by version — filter logic removed from body
- [x] The `version` query parameter is no longer extracted or accepted by the endpoint — handler updated
- [x] All call sites compile and pass without the version_filter argument — all 3 call sites updated
- [x] Existing tests that don't depend on version filtering still pass — verified by running tests

## Step 9 – Self-Verification

### Scope containment
- `modules/fundamental/src/sbom/service/sbom.rs` — in scope (Files to Modify)
- `modules/fundamental/src/sbom/endpoints/list.rs` — in scope (Files to Modify)
- `tests/api/sbom.rs` — in scope (Files to Modify)
- `modules/search/src/service/mod.rs` — **out of scope** but required: removing a parameter from `SbomService::list` requires updating all call sites. This is a mechanical consequence of the parameter removal, not new functionality. Flag for user approval.

### Dead parameter detection
Confirmed: removing the `VersionMatches` filter logic from the `list` method body leaves the `version_filter` parameter with zero references in the function body. The parameter is dead and must be removed from the signature, not renamed to `_version_filter`. All 3 call sites must be updated:
1. `modules/fundamental/src/sbom/endpoints/list.rs` — stop passing `version`
2. `modules/search/src/service/mod.rs` — stop passing `""`
3. `tests/api/sbom.rs` — stop passing version filter values

### Module-level tests (Rust)

Resolve crate names using `cargo metadata --no-deps --format-version 1`:
```bash
cargo test -p <fundamental-crate-name>
cargo test -p <search-crate-name>
cargo test -p <test-crate-name>
```

Re-run tests after removing the parameter and updating call sites to verify nothing broke.

## Step 10 – Commit and Push

```bash
git add modules/fundamental/src/sbom/service/sbom.rs \
       modules/fundamental/src/sbom/endpoints/list.rs \
       modules/search/src/service/mod.rs \
       tests/api/sbom.rs

git commit --trailer="Assisted-by: Claude Code" -m "refactor(sbom): remove version-based filter from SBOM list endpoint

Remove the version_filter parameter from SbomService::list and update
all 3 call sites (endpoint handler, search service, tests). Version
filtering has been moved to the client side.

Implements TC-9207"
```

Push and create PR:
```bash
git push -u origin TC-9207
gh pr create --base main --title "refactor(sbom): remove version-based filter from SBOM list endpoint" --body "..."
```
