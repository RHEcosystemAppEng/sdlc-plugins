# Implementation Plan for TC-9208

## Summary

Add a REST endpoint `GET /api/v2/sbom/{id}/license-summary` that aggregates package licenses by type (permissive, copyleft, unknown) and returns counts plus deduplicated license identifier lists for each category.

## Pre-Implementation Checks

### Step 0 -- Validate Project Configuration

The mock CLAUDE.md contains all required sections:
- Repository Registry: `trustify-backend` with Serena instance `serena_backend` at path `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: `serena_backend` with rust-analyzer

Configuration is valid. Proceed.

### Step 1 -- Parse Task

- **Repository**: trustify-backend
- **Target Branch**: main
- **Bookend Type**: none
- **Target PR**: none
- **Dependencies**: none
- **GitHub Issue custom field**: customfield_10747 (would check for value)
- **Jira webUrl**: https://redhat.atlassian.net/browse/TC-9208

### Step 2 -- Dependencies

No dependencies listed. Proceed.

### Step 3 -- Transition and Assign

Would transition TC-9208 to In Progress and assign to current user.

## Step 4 -- Understand the Code

### Sibling Analysis

Inspect sibling files to understand established patterns before implementing.

**Production code siblings** (same module pattern):
1. `modules/fundamental/src/sbom/endpoints/list.rs` -- reference endpoint implementation
2. `modules/fundamental/src/sbom/endpoints/get.rs` -- single-resource GET handler
3. `modules/fundamental/src/sbom/model/summary.rs` -- response struct pattern
4. `modules/fundamental/src/package/endpoints/list.rs` -- existing package endpoint (same module)
5. `modules/fundamental/src/package/model/summary.rs` -- existing PackageSummary struct

**Test code siblings**:
1. `tests/api/sbom.rs` -- SBOM integration test patterns
2. `tests/api/advisory.rs` -- advisory integration test patterns

### CONVENTIONS.md

The repo has a `CONVENTIONS.md` at root. Would read it and extract:
- CI check commands (formatting, linting, compilation)
- Code generation commands (if any)

### Documentation Files

- `docs/api.md` -- REST API reference, needs updating for new endpoint
- `docs/architecture.md` -- system architecture, unlikely to need changes
- `README.md` -- project readme, unlikely to need changes

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9208
```

## Step 6 -- Implementation Changes

### File 1: `modules/fundamental/src/package/model/license_summary.rs` (CREATE)

Create a new response struct for the license summary endpoint.

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Summary of license categories for packages within an SBOM.
///
/// Groups licenses into permissive, copyleft, and unknown categories,
/// providing both a count and the deduplicated list of license identifiers
/// in each category.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct LicenseSummary {
    /// Permissive license category (e.g., MIT, Apache-2.0, BSD).
    pub permissive: LicenseCategory,
    /// Copyleft license category (e.g., GPL, LGPL, AGPL).
    pub copyleft: LicenseCategory,
    /// Licenses that could not be categorized.
    pub unknown: LicenseCategory,
}

/// A single license category with count and identifier list.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct LicenseCategory {
    /// Number of distinct licenses in this category.
    pub count: usize,
    /// Deduplicated license identifiers (e.g., "MIT", "GPL-3.0-only").
    pub licenses: Vec<String>,
}
```

Key decisions:
- Derive `ToSchema` for OpenAPI spec generation (following sibling model pattern)
- Derive `Default` so empty SBOM case returns zeroed struct naturally
- Use `usize` for count to match Rust conventions for collection sizes
- Add doc comments on all public types and fields per skill quality guidance

### File 2: `modules/fundamental/src/package/model/mod.rs` (MODIFY)

Add module declaration for the new license_summary model.

```rust
// Add this line:
pub mod license_summary;
```

### File 3: `modules/fundamental/src/package/endpoints/license_summary.rs` (CREATE)

Create the GET handler for `/api/v2/sbom/{id}/license-summary`.

Structure (following `list.rs` and `get.rs` sibling patterns):

1. **Import block**: Import `AppError`, SeaORM entities (`package_license`, `sbom_package`, `package`), `LicenseSummary`, `LicenseCategory`, Axum extractors.

2. **License classification function**:
   ```rust
   /// Classifies an SPDX license identifier into permissive, copyleft, or unknown.
   fn classify_license(license_id: &str) -> &'static str {
       // Match against known SPDX identifiers
       // Permissive: MIT, Apache-2.0, BSD-*, ISC, Unlicense, etc.
       // Copyleft: GPL-*, LGPL-*, AGPL-*, MPL-*, EUPL-*, etc.
       // Unknown: anything else
   }
   ```

3. **Handler function**:
   ```rust
   /// Returns a categorized summary of package licenses for a given SBOM.
   ///
   /// Queries all packages linked to the SBOM, aggregates their licenses,
   /// deduplicates within each category, and returns counts with identifier lists.
   pub async fn license_summary(
       State(db): State<DatabaseConnection>,
       Path(sbom_id): Path<Uuid>,
   ) -> Result<Json<LicenseSummary>, AppError> {
       // 1. Verify SBOM exists; return 404 if not
       // 2. JOIN sbom_package -> package -> package_license
       // 3. Collect all license identifiers
       // 4. Classify each license, deduplicate per category using HashSet
       // 5. Build LicenseSummary with counts and sorted license lists
       // 6. Return Json(summary)
   }
   ```

Key implementation details:
- Error handling: `Result<T, AppError>` with `.context()` wrapping (matches sibling convention)
- SBOM existence check: query `sbom` entity first, return `AppError::NotFound` if absent
- Deduplication: use `HashSet<String>` per category, then convert to sorted `Vec<String>`
- Sort license lists alphabetically for deterministic output
- Use `package_license` entity from `entity/src/package_license.rs` for the JOIN query

### File 4: `modules/fundamental/src/package/endpoints/mod.rs` (MODIFY)

Register the new route in the package endpoints module.

```rust
// Add module declaration:
mod license_summary;

// In the router function, add:
.route("/api/v2/sbom/:id/license-summary", get(license_summary::license_summary))
```

Follow the existing registration pattern from sibling `sbom/endpoints/mod.rs`.

### File 5: `tests/api/package_license.rs` (CREATE)

See test-plan.md for detailed test approach.

### Documentation Impact

- `docs/api.md` -- Add documentation for the new `GET /api/v2/sbom/{id}/license-summary` endpoint, including request parameters, response schema, and example response.

## Step 9 -- Self-Verification Checklist

### Scope containment
- Verify `git diff --name-only` only shows the 5 files listed above plus `docs/api.md`
- Flag `docs/api.md` as out-of-scope for user approval (documentation update)

### Sensitive-pattern check
- Scan diff for passwords, API keys, secrets

### Duplication check
- Search for existing license classification logic in the codebase
- Search for existing `LicenseSummary` or similar types

### Symbol deduplication
- Search for `classify_license`, `LicenseSummary`, `LicenseCategory` across the codebase before declaring

### Dead parameter detection
- N/A for new code; check modified files (mod.rs files) for any unused imports after changes

### Contract and sibling parity
- **Contract**: Verify `LicenseSummary` derives all required traits matching sibling models (Serialize, Deserialize, ToSchema, Clone, Debug)
- **Sibling parity**: Compare handler signature with `list.rs` and `get.rs` for consistent extractors, error handling, and response wrapping
- **Cross-module entity**: Check if `package_license` entity is used by other modules; verify compatible query patterns (transaction handling, conflict handling)
- **Caller-site**: N/A (new endpoint, no existing callers)

### Data-flow trace
- Input: HTTP GET request with SBOM UUID path parameter
- Processing: SBOM existence validation -> JOIN query across sbom_package/package/package_license -> license classification -> deduplication via HashSet
- Output: JSON response with LicenseSummary struct
- All stages connected; no incomplete paths

### CI checks from CONVENTIONS.md
- Run extracted CI commands (cargo fmt --check, cargo clippy, cargo check, cargo test)
- Hard stop on any failure

### Module-level test requirement (Rust)
- Run `cargo metadata --no-deps --format-version 1` to resolve crate names for modified files
- Run `cargo test -p <crate-name>` for each affected crate

## Step 10 -- Commit and Push

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(package): add license summary endpoint

Add GET /api/v2/sbom/{id}/license-summary that returns categorized
license counts (permissive, copyleft, unknown) with deduplicated
license identifier lists for all packages within an SBOM.

Implements TC-9208"
```

Then push and create PR targeting `main` with:
- Summary of changes
- `Implements [TC-9208](https://redhat.atlassian.net/browse/TC-9208)` link

## Step 11 -- Update Jira

- Set `customfield_10875` (Git Pull Request) with PR URL in ADF format
- Add comment with PR link and summary of changes
- Transition TC-9208 to In Review
