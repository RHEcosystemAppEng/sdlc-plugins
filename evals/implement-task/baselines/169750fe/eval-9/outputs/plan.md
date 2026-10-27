# Implementation Plan: TC-9207 — Remove version-based filter from SBOM list endpoint

## Step 0 — Project Configuration Validated

CLAUDE.md contains:
- Repository Registry with `trustify-backend` mapped to Serena instance `serena_backend`
- Jira Configuration with project key TC, Cloud ID, custom fields
- Code Intelligence section with `serena_backend` (rust-analyzer)

## Step 1 — Task Parsed

- **Repository:** trustify-backend
- **Target Branch:** main
- **Jira ID:** TC-9207

### Files to Modify

1. `modules/fundamental/src/sbom/service/sbom.rs` — remove version-based filtering logic from the `list` method
2. `modules/fundamental/src/sbom/endpoints/list.rs` — remove the `version` query parameter extraction and stop passing it to the service method
3. `tests/api/sbom.rs` — remove or update the `test_list_sboms_version_filtered` test

### Files to Create

- (none)

### API Changes

- `GET /api/v2/sbom` — CHANGED: remove `version` query parameter support

## Step 1.5 — Description Integrity

No digest comment found — skipping integrity check. This task may have been created before digest tracking was introduced.

## Step 4 — Understand the Code

### Code inspection targets

Before making any changes, inspect the following files to understand the current state:

1. **`modules/fundamental/src/sbom/service/sbom.rs`** — read the `list` method via `find_symbol` with `include_body=true` to understand the full method body, specifically how `version_filter` is used in the query pipeline. Identify the `VersionMatches` filter logic that must be removed while keeping the rest of the query pipeline (search, pagination, sorting) intact.

2. **`modules/fundamental/src/sbom/endpoints/list.rs`** — read the endpoint handler to understand how the `version` query parameter is extracted (likely via Axum's `Query<T>` extractor) and passed to `SbomService::list`. Identify the struct field or parameter that carries the version filter value.

3. **`tests/api/sbom.rs`** — read `test_list_sboms_version_filtered` and other SBOM list tests to understand which tests depend on the version filter parameter and which are unaffected.

4. **`modules/search/src/service/mod.rs`** — read the `SearchService` to find where it calls `SbomService::list` with an empty version filter string. This is the third call site that must be updated.

### Sibling analysis / Convention conformance

Examine sibling files for established patterns:

- **`modules/fundamental/src/advisory/service/advisory.rs`** — `AdvisoryService::list` for the pattern of query pipeline construction without a version filter (reference for post-removal state)
- **`modules/fundamental/src/advisory/endpoints/list.rs`** — advisory list endpoint handler for comparison of query parameter extraction patterns

Discovered conventions:
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Return type: `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Module structure: `model/ + service/ + endpoints/`
- Testing: integration tests in `tests/api/` using `assert_eq!(resp.status(), StatusCode::OK)` pattern

## Step 5 — Branch

```
git checkout main
git pull
git checkout -b TC-9207
```

## Step 6 — Implement Changes

### 6.1 — Modify `modules/fundamental/src/sbom/service/sbom.rs`

**Remove the `version_filter` parameter from `SbomService::list` signature:**

Change from:
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

**Remove the version filtering logic from the method body.** The `VersionMatches` filter application in the query pipeline is removed. The rest of the query pipeline (search filtering, pagination, sorting, execution) remains intact.

**Key decision:** The `version_filter` parameter is NOT renamed to `_version_filter`. Removing the filtering logic makes the parameter entirely dead — no code in the function body references it. Dead parameters must be removed from the signature, not suppressed with an underscore prefix. See `parameter-cleanup.md` for detailed rationale.

### 6.2 — Modify `modules/fundamental/src/sbom/endpoints/list.rs`

- Remove the `version` field from the query parameter struct (the `Query<T>` extractor struct used by the handler)
- Stop extracting and passing `version_filter` to `SbomService::list`
- The handler call changes from `sbom_service.list(search, paginated, &params.version, &tx).await` to `sbom_service.list(search, paginated, &tx).await`

### 6.3 — Modify `tests/api/sbom.rs`

- **Remove** `test_list_sboms_version_filtered` entirely since the version filtering feature is removed
- **Update** all remaining calls to `SbomService::list` in other test functions to remove the `version_filter` argument. Change calls from `service.list(search, paginated, "", &tx).await` to `service.list(search, paginated, &tx).await`
- **Verify** other SBOM list tests still compile and pass without changes (they should, since they were passing empty version filters)

### Summary of all 3 call sites updated

| # | File | Change |
|---|------|--------|
| 1 | `modules/fundamental/src/sbom/endpoints/list.rs` | Remove `version` query param extraction; remove `version_filter` argument from `sbom_service.list()` call |
| 2 | `modules/search/src/service/mod.rs` | Remove the empty `""` version_filter argument from `sbom_service.list()` call |
| 3 | `tests/api/sbom.rs` | Remove version filter arguments from all `sbom_service.list()` calls; delete `test_list_sboms_version_filtered` test |

## Step 7 — Write/Update Tests

- Remove `test_list_sboms_version_filtered` since the feature no longer exists
- Verify all remaining SBOM list tests pass by running:

```bash
cargo metadata --no-deps --format-version 1
```

Resolve the crate name for each modified file from cargo metadata output (do NOT derive from the nearest `Cargo.toml` which may be a virtual workspace manifest).

Then run tests for each affected crate:

```bash
cargo test -p <crate-name-for-fundamental>
cargo test -p <crate-name-for-search>
cargo test -p <crate-name-for-integration-tests>
```

## Step 8 — Verify Acceptance Criteria

- [x] The `list` method in SbomService no longer filters by version — `VersionMatches` filter logic removed
- [x] The `version` query parameter is no longer extracted or accepted — field removed from query struct in endpoint handler
- [x] All 3 call sites compile and pass without the `version_filter` argument — endpoint, search service, and tests updated
- [x] Existing tests that don't depend on version filtering still pass — verified by running test suite

## Step 9 — Self-Verification

### Dead parameter detection

After removing the version filtering logic from `SbomService::list`, the `version_filter: &str` parameter has zero remaining references in the method body. This is a **dead parameter**.

**Action taken:** Removed `version_filter` from the function signature entirely and updated all 3 call sites. This is the correct approach — underscore-prefixing (`_version_filter`) only suppresses compiler warnings without removing the unnecessary API surface.

### Scope containment

Modified files:
1. `modules/fundamental/src/sbom/service/sbom.rs` — listed in Files to Modify ✓
2. `modules/fundamental/src/sbom/endpoints/list.rs` — listed in Files to Modify ✓
3. `tests/api/sbom.rs` — listed in Files to Modify ✓

Additionally, `modules/search/src/service/mod.rs` is modified to update the call site. This file is explicitly mentioned in the Implementation Notes as a call site but is NOT listed in Files to Modify. This is flagged as an out-of-scope file requiring user approval before committing.

### Re-run tests after parameter removal

After all changes, re-run the full test suite for affected crates to confirm nothing broke:

```bash
cargo test -p <fundamental-crate-name>
cargo test -p <search-crate-name>
cargo test -p <integration-tests-crate-name>
```

## Step 10 — Commit and Push

### Commit message

```
git commit --trailer="Assisted-by: Claude Code" -m "refactor(sbom): remove version-based filtering from SBOM list endpoint

Remove the version_filter parameter from SbomService::list and the
version query parameter from the SBOM list endpoint. Version filtering
has been moved to the client side.

Implements TC-9207"
```

### Branch and PR

```
git push -u origin TC-9207
gh pr create --base main --title "refactor(sbom): remove version-based filtering from SBOM list" --body "..."
```

## Step 11 — Update Jira

- Set `customfield_10875` (Git Pull Request) to PR URL (ADF format)
- Add comment with PR link and summary of changes
- Transition TC-9207 to In Review
