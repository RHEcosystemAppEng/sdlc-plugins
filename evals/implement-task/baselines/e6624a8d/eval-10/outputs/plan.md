# Implementation Plan for TC-9208

## Summary

Add a REST endpoint `GET /api/v2/sbom/{id}/license-summary` that returns a summary of license types for packages within an SBOM, categorized as permissive, copyleft, or unknown, with counts and deduplicated license identifier lists.

## Step-by-step plan

### Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections: Repository Registry (trustify-backend with serena_backend), Jira Configuration (Project key: TC, Cloud ID, Feature issue type ID), and Code Intelligence (serena_backend with rust-analyzer). Proceed.

### Step 1 -- Fetch and Parse Jira Task

- **Repository**: trustify-backend
- **Target Branch**: main
- **Bookend Type**: none (standard implementation)
- **Target PR**: none (new PR flow)
- **Dependencies**: none

### Step 4 -- Understand the Code

Use `mcp__serena_backend__get_symbols_overview` on sibling files to understand patterns:

1. Inspect `modules/fundamental/src/package/endpoints/list.rs` -- the sibling endpoint handler. Understand route registration, handler signature, return type, error handling.
2. Inspect `modules/fundamental/src/package/model/summary.rs` -- the sibling model. Understand struct shape, derive macros, serde attributes.
3. Inspect `modules/fundamental/src/package/endpoints/mod.rs` -- understand how routes are registered (Router composition).
4. Inspect `modules/fundamental/src/package/model/mod.rs` -- understand how model modules are declared.
5. Inspect `entity/src/package_license.rs` -- understand the Package-License SeaORM entity for the JOIN query.
6. Inspect `common/src/error.rs` -- understand AppError enum and `.context()` usage.
7. Inspect `tests/api/sbom.rs` and `tests/api/advisory.rs` -- understand test structure, setup, and assertion patterns.
8. Check for `CONVENTIONS.md` at repository root -- present per repo structure. Read it for naming rules, CI commands, and conventions.

### Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9208
```

### Step 6 -- Implement Changes

#### Files to Create

**1. `modules/fundamental/src/package/model/license_summary.rs`**

Create a new response struct for the license summary endpoint.

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Categorized summary of license types found in an SBOM's packages.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct LicenseSummary {
    /// Licenses classified as permissive (e.g., MIT, Apache-2.0, BSD).
    pub permissive: LicenseCategory,
    /// Licenses classified as copyleft (e.g., GPL, LGPL, AGPL).
    pub copyleft: LicenseCategory,
    /// Licenses that could not be classified into permissive or copyleft.
    pub unknown: LicenseCategory,
}

/// A single license category with a count and list of deduplicated identifiers.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct LicenseCategory {
    /// Number of distinct licenses in this category.
    pub count: usize,
    /// Deduplicated list of SPDX license identifiers in this category.
    pub licenses: Vec<String>,
}
```

Follow the same derive macro pattern as `summary.rs` (Serialize, Deserialize, Clone, Debug, ToSchema). Add doc comments on the struct and each field per the skill's code quality requirement.

**2. `modules/fundamental/src/package/endpoints/license_summary.rs`**

Create the GET handler for `/api/v2/sbom/{id}/license-summary`.

- Follow the handler pattern from `list.rs`: use Axum extractor for path parameters, return `Result<Json<LicenseSummary>, AppError>`.
- Extract `id` from the path using `Path(id): Path<Uuid>` (or whatever the SBOM ID type is, confirmed by inspecting `sbom/endpoints/get.rs`).
- Query logic:
  1. Look up the SBOM by ID; return 404 (`AppError::NotFound`) if not found, using `.context("SBOM not found")` wrapping.
  2. JOIN `sbom_package` with `package` and `package_license` to get all licenses for packages in the SBOM.
  3. Classify each license identifier into permissive/copyleft/unknown using a categorization function.
  4. Deduplicate licenses within each category using a `HashSet`.
  5. Build and return the `LicenseSummary` response.
- The categorization function would contain known SPDX identifiers:
  - Permissive: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, Unlicense, etc.
  - Copyleft: GPL-2.0, GPL-3.0, LGPL-2.1, LGPL-3.0, AGPL-3.0, MPL-2.0, etc.
  - Unknown: anything not in the above lists.

**3. `tests/api/package_license.rs`**

Integration tests for the new endpoint (see test-plan.md for detailed test approach).

#### Files to Modify

**4. `modules/fundamental/src/package/endpoints/mod.rs`**

- Add `pub mod license_summary;` declaration.
- In the route registration function, add a new route: `.route("/api/v2/sbom/:id/license-summary", get(license_summary::handler))` (or equivalent using the project's router pattern -- confirm exact syntax by inspecting the existing route registration in this file and `sbom/endpoints/mod.rs`).

**5. `modules/fundamental/src/package/model/mod.rs`**

- Add `pub mod license_summary;` to expose the new model module.

**6. `tests/Cargo.toml`** (potentially out-of-scope -- would flag to user)

- If `package_license.rs` is a new test file, it may need to be registered in `tests/Cargo.toml` or a `mod.rs` depending on how the test harness discovers tests. Inspect sibling test registration to determine if this is needed.

### Step 7 -- Write Tests

See outputs/test-plan.md for detailed test assertions.

### Step 8 -- Verify Acceptance Criteria

1. GET /api/v2/sbom/{id}/license-summary returns categorized license counts -- verified by the handler returning `LicenseSummary` with permissive/copyleft/unknown categories.
2. Returns 404 when SBOM ID does not exist -- verified by the 404 check in the handler and corresponding test.
3. Each category includes both a count and a list of license identifiers -- verified by the `LicenseCategory` struct shape containing both fields.
4. Licenses are deduplicated within each category -- verified by using `HashSet` in the aggregation logic and a dedicated deduplication test.

### Step 9 -- Self-Verification

- **Scope containment**: `git diff --name-only` should show only the 5 files listed above (plus potentially `tests/Cargo.toml`). Any extra files would be flagged.
- **Untracked file check**: New files (`license_summary.rs` in model and endpoints, `package_license.rs` in tests) must be staged.
- **Sensitive-pattern check**: No credentials or secrets expected.
- **Data-flow trace**: `GET request` -> path extraction -> SBOM lookup -> package-license JOIN query -> license classification -> deduplication -> JSON response. All stages connected. **COMPLETE**.
- **Contract & sibling parity**: The handler follows `Result<T, AppError>` contract. Sibling parity with `list.rs` handler: both use Axum extractors, both return Result with AppError, both use `.context()` wrapping.
- **Duplication check**: Search for existing license classification logic in the codebase to avoid duplication.
- **CI checks from CONVENTIONS.md**: Run whatever CI commands are specified (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`).

### Step 10 -- Commit and Push

```
git add modules/fundamental/src/package/model/license_summary.rs
git add modules/fundamental/src/package/endpoints/license_summary.rs
git add modules/fundamental/src/package/model/mod.rs
git add modules/fundamental/src/package/endpoints/mod.rs
git add tests/api/package_license.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add package license summary endpoint

Add GET /api/v2/sbom/{id}/license-summary that returns categorized
license counts (permissive, copyleft, unknown) with deduplicated
license identifier lists for all packages in an SBOM.

Implements TC-9208"
```

Create PR targeting `main` with description referencing the Jira issue.

### Step 11 -- Update Jira

- Set `customfield_10875` (Git Pull Request) to the PR URL in ADF format.
- Add comment summarizing: new endpoint added, tests written, license classification logic implemented.
- Transition TC-9208 to "In Review".
