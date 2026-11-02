# Implementation Plan — TC-9208: Add package license summary endpoint with tests

## Step 0 — Validate Project Configuration

CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID present
- Code Intelligence: Tool naming convention documented, `serena_backend` configured

Configuration valid — proceeding.

## Step 1 — Parse Task Description

- **Repository**: trustify-backend
- **Target Branch**: main
- **Jira Issue**: TC-9208
- **Web URL**: https://redhat.atlassian.net/browse/TC-9208

### Files to Modify
1. `modules/fundamental/src/package/endpoints/mod.rs` — register the new route
2. `modules/fundamental/src/package/model/mod.rs` — add `pub mod license_summary;`

### Files to Create
1. `modules/fundamental/src/package/model/license_summary.rs` — LicenseSummary response struct
2. `modules/fundamental/src/package/endpoints/license_summary.rs` — GET handler
3. `tests/api/package_license.rs` — integration tests

## Step 1.5 — Description Integrity

No description digest comment found — skipping integrity check. This task may have been created before digest tracking was introduced.

## Step 4 — Understand the Code

### Code Inspection

Before making changes, I would inspect the following files using `mcp__serena_backend__get_symbols_overview` and `mcp__serena_backend__find_symbol`:

1. **`modules/fundamental/src/package/endpoints/list.rs`** — understand the existing endpoint pattern (route function signature, handler structure, service calls, response wrapping)
2. **`modules/fundamental/src/package/endpoints/mod.rs`** — understand how routes are currently registered to follow the same pattern
3. **`modules/fundamental/src/package/model/mod.rs`** — see existing model module registration pattern
4. **`modules/fundamental/src/package/model/summary.rs`** — understand PackageSummary struct (includes license field) to see existing data model patterns
5. **`entity/src/package_license.rs`** — understand the Package-License mapping entity for the JOIN query
6. **`common/src/error.rs`** — understand AppError usage and `.context()` wrapping pattern
7. **`common/src/model/paginated.rs`** — understand PaginatedResults<T> pattern

### Sibling Analysis (for conventions — see conventions.md)

Sibling endpoints examined:
- `modules/fundamental/src/advisory/endpoints/list.rs` — list endpoint pattern
- `modules/fundamental/src/advisory/endpoints/get.rs` — single-resource get pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — another list endpoint for comparison

Sibling tests examined:
- `tests/api/advisory.rs` — assertion patterns, test structure
- `tests/api/sbom.rs` — assertion patterns, naming conventions

### CONVENTIONS.md Lookup

Would check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). The repo-backend.md manifest shows CONVENTIONS.md exists — would read it for CI check commands and code conventions.

## Step 5 — Create Branch

```
git checkout main
git pull
git checkout -b TC-9208
```

Branch named after the Jira issue ID (TC-9208), based on the Target Branch (main).

## Step 6 — Implement Changes

### File 1: `modules/fundamental/src/package/model/license_summary.rs` (CREATE)

Create a new `LicenseSummary` response struct following the model pattern from `summary.rs`:

```rust
/// Summary of license types for packages within an SBOM.
#[derive(Debug, Clone, Serialize, Deserialize, utoipa::ToSchema)]
pub struct LicenseSummary {
    /// Permissive licenses category.
    pub permissive: LicenseCategory,
    /// Copyleft licenses category.
    pub copyleft: LicenseCategory,
    /// Unknown/unclassified licenses category.
    pub unknown: LicenseCategory,
}

/// A category of licenses with count and identifiers.
#[derive(Debug, Clone, Serialize, Deserialize, utoipa::ToSchema)]
pub struct LicenseCategory {
    /// Number of deduplicated licenses in this category.
    pub count: usize,
    /// List of deduplicated license identifiers.
    pub licenses: Vec<String>,
}
```

### File 2: `modules/fundamental/src/package/endpoints/license_summary.rs` (CREATE)

Create the GET handler following the pattern from `list.rs`:

- Route: `GET /api/v2/sbom/{id}/license-summary`
- Path parameter: SBOM ID
- Query the `package_license` entity via JOIN
- Categorize licenses as permissive/copyleft/unknown
- Deduplicate licenses within each category
- Return `Result<Json<LicenseSummary>, AppError>` with `.context()` error wrapping
- Return 404 when SBOM ID does not exist

### File 3: `modules/fundamental/src/package/endpoints/mod.rs` (MODIFY)

Add route registration for the new license_summary endpoint, following the existing pattern for registering routes.

### File 4: `modules/fundamental/src/package/model/mod.rs` (MODIFY)

Add `pub mod license_summary;` to expose the new model module.

### File 5: `tests/api/package_license.rs` (CREATE)

Integration tests — see test-plan.md for assertion approach details.

## Step 7 — Write Tests

See test-plan.md for the complete test plan, including the convention conflict resolution.

## Step 9 — Self-Verification

### Scope Containment
All modified/created files match the Files to Modify and Files to Create sections exactly:
- Modified: `package/endpoints/mod.rs`, `package/model/mod.rs`
- Created: `package/model/license_summary.rs`, `package/endpoints/license_summary.rs`, `tests/api/package_license.rs`

No out-of-scope files.

### Module-level test requirement (Rust)
Would run `cargo metadata --no-deps --format-version 1` from the workspace root to resolve the crate name for `modules/fundamental/`, then run:
```
cargo test -p <resolved-crate-name>
```

### CI checks from CONVENTIONS.md
Would execute all CI check commands extracted from CONVENTIONS.md.

## Step 10 — Commit and Push

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(package): add license summary endpoint

Add GET /api/v2/sbom/{id}/license-summary endpoint that returns categorized
license counts (permissive, copyleft, unknown) with deduplicated license
identifiers for packages within an SBOM.

Implements TC-9208"
```

Push and create PR:
```
git push -u origin TC-9208
gh pr create --base main --title "feat(package): add license summary endpoint" --body "..."
```

The PR description would include `Implements [TC-9208](https://redhat.atlassian.net/browse/TC-9208)`.

## Step 11 — Update Jira

- Update `customfield_10875` (Git Pull Request) with the PR URL (ADF format)
- Add comment with PR link and change summary
- Transition TC-9208 to In Review
