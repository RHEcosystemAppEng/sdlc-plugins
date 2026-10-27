# Implementation Plan — TC-9208: Add Package License Summary Endpoint

## Step 0 — Project Configuration Validation

Verified Project Configuration in CLAUDE.md:
- **Repository Registry**: present — trustify-backend mapped to `serena_backend` at `./`
- **Jira Configuration**: present — Project key TC, Cloud ID, Feature issue type ID, custom fields
- **Code Intelligence**: present — serena_backend instance with rust-analyzer

## Step 1 — Task Parsing

| Field | Value |
|-------|-------|
| Key | TC-9208 |
| Summary | Add package license summary endpoint with tests |
| Repository | trustify-backend |
| Target Branch | main |
| Bookend Type | (none) |
| Target PR | (none) |
| Dependencies | None |

### Files to Modify
1. `modules/fundamental/src/package/endpoints/mod.rs` — register the new route
2. `modules/fundamental/src/package/model/mod.rs` — add `pub mod license_summary;`

### Files to Create
1. `modules/fundamental/src/package/model/license_summary.rs` — LicenseSummary response struct
2. `modules/fundamental/src/package/endpoints/license_summary.rs` — GET handler
3. `tests/api/package_license.rs` — integration tests

## Step 4 — Code Inspection

### Files inspected before modification

1. **`modules/fundamental/src/package/endpoints/mod.rs`** — understand current route registration pattern; see how `list.rs` is registered to follow the same pattern for `license_summary.rs`
2. **`modules/fundamental/src/package/endpoints/list.rs`** — reference endpoint implementation pattern: handler function signature, `Result<T, AppError>` return type, query parameter extraction, `.context()` error wrapping
3. **`modules/fundamental/src/package/model/mod.rs`** — see existing module re-exports (`pub mod summary;`) to follow the same pattern for `pub mod license_summary;`
4. **`modules/fundamental/src/package/model/summary.rs`** — reference response struct pattern: derive macros, serde attributes, field types
5. **`entity/src/package_license.rs`** — understand the Package-License entity structure for the JOIN query
6. **`common/src/error.rs`** — confirm `AppError` enum and `IntoResponse` implementation
7. **`tests/api/advisory.rs`** — sibling test file for convention analysis (naming, setup, assertion patterns)
8. **`tests/api/sbom.rs`** — sibling test file for convention analysis (naming, setup, assertion patterns)

### Convention conformance analysis

See `conventions.md` for the full analysis, including:
- Production conventions (module structure, error handling, response types, naming)
- Test conventions (naming, setup, status assertions, response parsing)
- **Conflict identified**: sibling assertion style (`.filter().any()`, `.count() > 0`) conflicts with skill's "prefer value-based assertions" guidance — **skill guidance takes precedence**

### CONVENTIONS.md lookup

`CONVENTIONS.md` exists at the repository root. Would read it for CI check commands and code conventions. Verification commands extracted for use in Step 9.

## Step 5 — Branch Creation

```bash
git checkout main
git pull
git checkout -b TC-9208
```

## Step 6 — Implementation

### 6.1 Create `modules/fundamental/src/package/model/license_summary.rs`

New response struct for the license summary endpoint:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Summary of licenses within an SBOM, categorized by license type.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct LicenseSummary {
    /// Permissive licenses (e.g., MIT, Apache-2.0, BSD-2-Clause).
    pub permissive: LicenseCategory,
    /// Copyleft licenses (e.g., GPL-3.0-only, AGPL-3.0-or-later).
    pub copyleft: LicenseCategory,
    /// Licenses that could not be categorized.
    pub unknown: LicenseCategory,
}

/// A single license category with a count and list of license identifiers.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct LicenseCategory {
    /// Number of unique license identifiers in this category.
    pub count: usize,
    /// Deduplicated list of SPDX license identifiers.
    pub licenses: Vec<String>,
}
```

### 6.2 Modify `modules/fundamental/src/package/model/mod.rs`

Add module re-export:

```rust
pub mod license_summary;
```

### 6.3 Create `modules/fundamental/src/package/endpoints/license_summary.rs`

GET handler for `/api/v2/sbom/{id}/license-summary`:

- Extract SBOM ID from path parameter
- Query `package_license` entity (from `entity/src/package_license.rs`) via JOIN with `sbom_package` to find all licenses for packages in the given SBOM
- Return 404 if SBOM does not exist (using `AppError` with `.context()`)
- Categorize each license identifier as permissive, copyleft, or unknown
- Deduplicate licenses within each category using `HashSet`
- Build `LicenseSummary` response with counts and license lists
- Return `Result<Json<LicenseSummary>, AppError>`

Follows the handler pattern from `modules/fundamental/src/package/endpoints/list.rs`.

### 6.4 Modify `modules/fundamental/src/package/endpoints/mod.rs`

Register the new route:

```rust
mod license_summary;

// In the router configuration:
.route("/api/v2/sbom/{id}/license-summary", get(license_summary::get_license_summary))
```

### 6.5 Create `tests/api/package_license.rs`

Integration tests following the test plan in `test-plan.md`. Four test functions with value-based assertions (see `test-plan.md` for full details):

1. `test_get_license_summary_with_known_packages` — verifies exact counts and specific license identifiers per category
2. `test_get_license_summary_nonexistent_sbom` — verifies 404 response
3. `test_get_license_summary_empty_sbom` — verifies all-zero counts and empty lists
4. `test_get_license_summary_deduplicates_licenses` — verifies deduplication (count reflects unique licenses, not total)

## Step 7 — Test Implementation

Tests follow the plan in `test-plan.md`:
- **Value-based assertions** per skill guidance (overriding sibling `.any()`/`.count() > 0` patterns)
- **Sibling conventions** for non-conflicting aspects: test naming (`test_<verb>_<noun>_<scenario>`), shared test DB setup, `assert_eq!(resp.status(), ...)` status checks, `.json::<T>()` response parsing
- **Doc comments** on every test function (`///` convention)
- **Given/When/Then** section comments in non-trivial tests

## Step 9 — Self-Verification

### Scope containment
All modified and created files are within the task's Files to Modify and Files to Create sections:
- **Modified**: `modules/fundamental/src/package/endpoints/mod.rs`, `modules/fundamental/src/package/model/mod.rs`
- **Created**: `modules/fundamental/src/package/model/license_summary.rs`, `modules/fundamental/src/package/endpoints/license_summary.rs`, `tests/api/package_license.rs`

### CI checks
Run all verification commands extracted from `CONVENTIONS.md` (formatting, linting, compilation).

### Module-level test (Rust)
Resolve the crate name using `cargo metadata --no-deps --format-version 1` from the workspace root. The modified files belong to the `trustify-module-fundamental` crate (or equivalent package name from metadata). Run:

```bash
cargo test -p <crate-name>
```

### Duplication check
Search for existing license categorization or summary logic in the repository to avoid duplication.

### Query-scope verification
The endpoint queries licenses for a specific SBOM by ID — query scope matches task target (single SBOM, not all SBOMs).

## Step 10 — Commit and Push

```bash
git add modules/fundamental/src/package/model/license_summary.rs \
      modules/fundamental/src/package/model/mod.rs \
      modules/fundamental/src/package/endpoints/license_summary.rs \
      modules/fundamental/src/package/endpoints/mod.rs \
      tests/api/package_license.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(package): add license summary endpoint with categorized counts

Add GET /api/v2/sbom/{id}/license-summary endpoint that returns
package licenses categorized as permissive, copyleft, or unknown
with deduplicated counts and identifier lists.

Implements TC-9208"
```

Then push and create PR:

```bash
git push -u origin TC-9208
gh pr create --base main --title "feat(package): add license summary endpoint" --body "..."
```

## Step 11 — Update Jira

- Set `customfield_10875` (Git Pull Request) to the PR URL using ADF format
- Add comment with PR link and summary of changes
- Transition TC-9208 to **In Review**
