# Implementation Plan: TC-9208 -- Add Package License Summary Endpoint with Tests

## Step 0 -- Validate Project Configuration

Verified CLAUDE.md contains all required sections:
- Repository Registry: present (trustify-backend with Serena instance serena_backend at path ./)
- Jira Configuration: present (Project key TC, Cloud ID, Feature issue type ID, custom fields)
- Code Intelligence: present (serena_backend using rust-analyzer)

All configuration sections are valid. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Parsed task TC-9208 structured description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a REST endpoint that returns a summary of license types for packages within an SBOM. The endpoint aggregates package licenses by type (permissive, copyleft, unknown) and returns counts plus the list of specific license identifiers in each category.
- **Files to Modify**:
  - `modules/fundamental/src/package/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/package/model/mod.rs` -- add `pub mod license_summary;`
- **Files to Create**:
  - `modules/fundamental/src/package/model/license_summary.rs` -- LicenseSummary response struct
  - `modules/fundamental/src/package/endpoints/license_summary.rs` -- GET handler for /api/v2/sbom/{id}/license-summary
  - `tests/api/package_license.rs` -- integration tests for the new endpoint
- **API Changes**: GET /api/v2/sbom/{id}/license-summary (NEW)
- **Dependencies**: None

### Target Branch extraction
Target Branch is **main**. This will be used as the base branch for the PR.

## Step 1.5 -- Verify Description Integrity

Would retrieve comments for TC-9208 using `jira.get_issue_comments(TC-9208)` and search for the marker string `[sdlc-workflow] Description digest:`. If no digest comment is found, log a warning and proceed normally (backward compatibility -- tasks created before digest tracking was introduced have no digest comment):

> "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user account ID via `jira.user_info()`
2. Assign TC-9208 to current user via `jira.edit_issue(TC-9208, assignee=<accountId>)`
3. Transition TC-9208 to In Progress via `jira.transition_issue`

## Step 4 -- Understand the Code

### Code inspection plan

Before making any changes, inspect the following files using the serena_backend Serena instance:

1. **`modules/fundamental/src/package/endpoints/mod.rs`** -- Use `get_symbols_overview` to understand the current route registration pattern and how existing endpoints are mounted.

2. **`modules/fundamental/src/package/endpoints/list.rs`** -- Use `get_symbols_overview` and `find_symbol` to read the existing list endpoint handler. This is the sibling endpoint pattern referenced in Implementation Notes that the new handler should follow.

3. **`modules/fundamental/src/package/model/mod.rs`** -- Use `get_symbols_overview` to see current model module registrations (how `summary.rs` is declared) so the new `license_summary` module follows the same pattern.

4. **`modules/fundamental/src/package/model/summary.rs`** -- Use `find_symbol` on `PackageSummary` to understand existing model struct patterns (derives, serde attributes, field types).

5. **`entity/src/package_license.rs`** -- Use `find_symbol` to read the `package_license` entity and understand the SeaORM columns available for JOIN queries.

6. **`common/src/error.rs`** -- Use `find_symbol` on `AppError` to understand the error type and `.context()` wrapping pattern.

7. **`tests/api/advisory.rs`** and **`tests/api/sbom.rs`** -- Use `get_symbols_overview` to understand test structure, setup/teardown, naming conventions, and assertion patterns used in sibling test files.

### CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). If present, read and extract CI check commands and code generation commands.

### Convention conformance analysis

See `outputs/conventions.md` for the full convention analysis, including conflicts with skill guidance.

### Documentation file identification

Identified documentation files:
- `docs/api.md` -- API reference, will need updating for the new endpoint
- `docs/architecture.md` -- Architecture overview, unlikely to need changes
- `README.md` -- Project readme

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9208
```

## Step 6 -- Implement Changes

### File 1: `modules/fundamental/src/package/model/license_summary.rs` (CREATE)

Create the LicenseSummary response struct following the pattern from `summary.rs`:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Summary of package licenses categorized by type for an SBOM.
#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct LicenseSummary {
    /// Licenses in the permissive category (e.g., MIT, Apache-2.0).
    pub permissive: LicenseCategory,
    /// Licenses in the copyleft category (e.g., GPL-3.0, AGPL-3.0).
    pub copyleft: LicenseCategory,
    /// Licenses that could not be categorized.
    pub unknown: LicenseCategory,
}

/// A single category of licenses with a count and the list of identifiers.
#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct LicenseCategory {
    /// Number of distinct licenses in this category.
    pub count: usize,
    /// Deduplicated list of license identifiers (e.g., ["MIT", "Apache-2.0"]).
    pub licenses: Vec<String>,
}
```

Follows existing model patterns: derives `Debug, Clone, Serialize, Deserialize, ToSchema`, uses doc comments on all public structs and fields.

### File 2: `modules/fundamental/src/package/model/mod.rs` (MODIFY)

Add the module declaration for the new model:

```rust
pub mod license_summary;
```

Following the existing pattern where `pub mod summary;` is already declared.

### File 3: `modules/fundamental/src/package/endpoints/license_summary.rs` (CREATE)

Create the GET handler following the pattern from `modules/fundamental/src/package/endpoints/list.rs`:

```rust
use crate::package::model::license_summary::{LicenseSummary, LicenseCategory};
use common::error::AppError;
use axum::extract::Path;
use anyhow::Context;

/// Handler for GET /api/v2/sbom/{id}/license-summary.
///
/// Returns a categorized summary of package licenses for the specified SBOM.
pub async fn get_license_summary(
    Path(sbom_id): Path<i64>,
    // ... service/state dependencies following list.rs pattern
) -> Result<LicenseSummary, AppError> {
    // Query package_license entity via SeaORM JOIN
    // Use entity/src/package_license.rs for the JOIN
    // Group licenses by category (permissive, copyleft, unknown)
    // Deduplicate within each category
    // Return LicenseSummary with counts and lists
    
    let licenses = /* query using package_license entity */
        .context("Failed to fetch package licenses for SBOM")?;
    
    // Categorize and deduplicate...
    // Return 404 if SBOM not found using AppError
}
```

Error handling uses `Result<T, AppError>` with `.context()` wrapping, consistent with the codebase convention.

### File 4: `modules/fundamental/src/package/endpoints/mod.rs` (MODIFY)

Register the new route in the existing endpoint registration:

```rust
pub mod license_summary;

// In route registration function, add:
.route("/api/v2/sbom/:id/license-summary", get(license_summary::get_license_summary))
```

Following the existing route registration pattern in the module's `mod.rs`.

### File 5: `tests/api/package_license.rs` (CREATE)

See `outputs/test-plan.md` for the detailed test assertion approach. Tests follow sibling conventions for naming, setup, teardown, and organization, but use value-based assertions per skill guidance (overriding sibling `.filter().any()` and `.filter().count() > 0` patterns).

## Step 7 -- Write Tests

See `outputs/test-plan.md` for full test implementation details.

After writing tests, run:
```
cargo test
```
Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

- [x] GET /api/v2/sbom/{id}/license-summary returns categorized license counts -- implemented in endpoint handler
- [x] Returns 404 when SBOM ID does not exist -- handler returns AppError for missing SBOM
- [x] Each category includes both a count and a list of license identifiers -- LicenseSummary struct has both fields
- [x] Licenses are deduplicated within each category -- deduplication logic in handler

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and verify all changed files are within the Files to Modify and Files to Create sections:
- `modules/fundamental/src/package/endpoints/mod.rs` -- in Files to Modify
- `modules/fundamental/src/package/model/mod.rs` -- in Files to Modify
- `modules/fundamental/src/package/model/license_summary.rs` -- in Files to Create
- `modules/fundamental/src/package/endpoints/license_summary.rs` -- in Files to Create
- `tests/api/package_license.rs` -- in Files to Create

No out-of-scope files modified.

### Dead parameter detection
No parameters removed from existing functions. No dead parameters detected.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`
No sensitive patterns found.

### Documentation currency
The new endpoint should be documented in `docs/api.md`. Will add an entry for `GET /api/v2/sbom/{id}/license-summary`.

## Step 10 -- Commit and Push

### Commit message

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(package): add license summary endpoint

Add GET /api/v2/sbom/{id}/license-summary endpoint that returns
package licenses categorized by type (permissive, copyleft, unknown)
with counts and deduplicated license identifier lists.

Implements TC-9208"
```

### Branch and PR

```
git push -u origin TC-9208
gh pr create --base main --title "feat(package): add license summary endpoint" --body "..."
```

The PR description will include:
- Implements [TC-9208](<jira-web-url>)
- Summary of changes

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (customfield_10875) with the PR URL using ADF format
2. Add comment to TC-9208 with PR link and summary of changes
3. Transition TC-9208 to In Review
