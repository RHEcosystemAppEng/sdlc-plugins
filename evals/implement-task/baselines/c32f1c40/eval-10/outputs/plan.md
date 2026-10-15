# Implementation Plan for TC-9208

## Task Summary

Add a REST endpoint `GET /api/v2/sbom/{id}/license-summary` that returns a summary of license types for packages within an SBOM, categorized as permissive, copyleft, or unknown, with counts and deduplicated license identifier lists.

## Project Configuration Validation

The mock CLAUDE.md contains:
- Repository Registry with `trustify-backend` mapped to Serena instance `serena_backend`
- Jira Configuration with project key TC, Cloud ID, and custom field IDs
- Code Intelligence section with `serena_backend` using rust-analyzer

All required sections are present. Proceed.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/mod.rs`

**Current state:** Registers existing package routes (e.g., `GET /api/v2/package` via `list.rs`).

**Changes:**
- Add `pub mod license_summary;` to import the new endpoint module.
- Register the new route in the router builder: add `.route("/api/v2/sbom/:id/license-summary", get(license_summary::get_license_summary))` (or equivalent Axum route registration following the existing pattern in `sbom/endpoints/mod.rs` and `advisory/endpoints/mod.rs`).
- The route may alternatively be registered in `modules/fundamental/src/sbom/endpoints/mod.rs` since the path is under `/api/v2/sbom/{id}/...`. Would need to inspect the actual route-mounting logic in `server/main.rs` to determine which module owns the `/api/v2/sbom` prefix. Based on the task description placing the files under `package/endpoints/`, the route registration goes in `package/endpoints/mod.rs`.

### 2. `modules/fundamental/src/package/model/mod.rs`

**Current state:** Contains `pub mod summary;` for `PackageSummary`.

**Changes:**
- Add `pub mod license_summary;` to register the new model module.

## Files to Create

### 3. `modules/fundamental/src/package/model/license_summary.rs`

**Purpose:** Define the `LicenseSummary` response struct.

**Contents:**
```rust
use serde::Serialize;
use utoipa::ToSchema;

/// Summary of package licenses within an SBOM, categorized by license type.
#[derive(Debug, Serialize, ToSchema)]
pub struct LicenseSummary {
    /// Permissive licenses (e.g., MIT, Apache-2.0, BSD).
    pub permissive: LicenseCategory,
    /// Copyleft licenses (e.g., GPL, LGPL, AGPL).
    pub copyleft: LicenseCategory,
    /// Licenses that could not be categorized.
    pub unknown: LicenseCategory,
}

/// A single license category with its count and the list of deduplicated license identifiers.
#[derive(Debug, Serialize, ToSchema)]
pub struct LicenseCategory {
    /// Number of distinct licenses in this category.
    pub count: usize,
    /// Deduplicated list of SPDX license identifiers.
    pub licenses: Vec<String>,
}
```

**Design decisions:**
- Derive `Serialize` and `ToSchema` (for OpenAPI) following sibling model patterns (`SbomSummary`, `PackageSummary`).
- Use `usize` for count to match Rust idioms; alternatively `u32` if sibling models use it.
- Add doc comments on every public struct and field per skill quality guidance.

### 4. `modules/fundamental/src/package/endpoints/license_summary.rs`

**Purpose:** GET handler for `/api/v2/sbom/{id}/license-summary`.

**Contents (outline):**
```rust
use axum::extract::Path;
use axum::Json;
use sea_orm::*;

use crate::package::model::license_summary::{LicenseCategory, LicenseSummary};
use common::error::AppError;
use entity::{package, sbom_package, package_license};

/// Returns a categorized summary of package licenses for the given SBOM.
pub async fn get_license_summary(
    db: /* extracted database connection, following sibling pattern from list.rs */,
    Path(sbom_id): Path</* Uuid or i32, matching existing SBOM ID type */>,
) -> Result<Json<LicenseSummary>, AppError> {
    // 1. Verify SBOM exists; return 404 if not found
    //    Use sbom entity or SbomService::fetch() following get.rs pattern
    //    Return AppError::NotFound with .context() wrapping

    // 2. Query package_license via JOIN:
    //    sbom_package (filter by sbom_id) -> package -> package_license
    //    Collect all license identifiers

    // 3. Categorize licenses into permissive/copyleft/unknown
    //    Use a classification function (could be a match on known SPDX IDs)
    //    Known permissive: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, etc.
    //    Known copyleft: GPL-2.0, GPL-3.0, LGPL-2.1, LGPL-3.0, AGPL-3.0, MPL-2.0, etc.
    //    Everything else: unknown

    // 4. Deduplicate licenses within each category (use HashSet or .dedup())

    // 5. Build and return LicenseSummary with counts and sorted license lists

    Ok(Json(summary))
}
```

**Design decisions:**
- Follow the `Result<T, AppError>` pattern with `.context()` wrapping per Implementation Notes and sibling conventions.
- Use the `package_license` entity for the JOIN query as specified in Implementation Notes.
- SBOM existence check returns 404 using the same pattern as `sbom/endpoints/get.rs`.
- License classification logic should be a separate helper function for testability, but kept in the same file unless sibling patterns suggest otherwise.
- Defensive access: guard against null/empty license fields from the database using `.unwrap_or_default()`.

### 5. `tests/api/package_license.rs`

**Purpose:** Integration tests for the license summary endpoint.

**Contents:** See `outputs/test-plan.md` for detailed test plan.

**Changes also needed in `tests/`:**
- The test file must be declared in `tests/api/mod.rs` or the test crate's `Cargo.toml` depending on how the test harness is structured. Would need to inspect the actual test configuration. If `tests/api/` files are individual integration test binaries (common in Rust), no `mod.rs` is needed. If they share a binary, add `mod package_license;` to the appropriate module file.

## Data Flow Trace

1. **Input:** HTTP GET request to `/api/v2/sbom/{id}/license-summary` with SBOM ID path parameter.
2. **Validation:** Extract and validate SBOM ID from path. Query database to verify SBOM exists (404 if not).
3. **Processing:** JOIN query across `sbom_package` and `package_license` tables, filtered by SBOM ID. Classify each license identifier into permissive/copyleft/unknown. Deduplicate within each category.
4. **Output:** JSON response with `LicenseSummary` containing three `LicenseCategory` objects, each with `count` and `licenses` fields.

All stages are connected. No incomplete paths.

## Scope Containment Notes

The task specifies exactly 5 files (2 modify, 3 create). Any modifications to files outside this list (e.g., `server/main.rs` for route mounting, `tests/Cargo.toml` for test dependencies) would need to be flagged in Step 9's scope containment check for user approval.

Potential out-of-scope files that might need changes:
- `server/main.rs` if the route mounting doesn't automatically pick up new routes from the package module
- `tests/Cargo.toml` if the test crate needs new dependencies
- `modules/fundamental/Cargo.toml` if new dependencies are needed (e.g., for license classification)

These would be flagged for user approval per the skill's Step 9 scope containment rules.
