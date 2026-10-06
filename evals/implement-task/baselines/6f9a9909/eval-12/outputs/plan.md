# Implementation Plan: TC-9210

## Task Summary

Add a severity-sorted remediation list to the SBOM risk report endpoint (`GET /api/v2/sbom/{id}`). The list sorts advisories by severity (Critical > High > Medium > Low > None) in descending order, returning `RemediationItem` structs.

## Project Configuration Validation (Step 0)

The mock CLAUDE.md (`claude-md-mock.md`) contains all required sections:
- Repository Registry: `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: `serena_backend` with rust-analyzer

Validation passes.

## Parsed Task Fields (Step 1)

- **Repository**: trustify-backend
- **Target Branch**: main
- **Files to Modify**: `modules/fundamental/src/sbom/service/sbom.rs`, `modules/fundamental/src/sbom/endpoints/get.rs`
- **Files to Create**: `tests/api/sbom_remediation.rs`
- **Dependencies**: None
- **Target PR**: None
- **Bookend Type**: None

## Branch (Step 5)

```
git checkout main
git pull
git checkout -b TC-9210
```

## Code Understanding (Step 4)

Before implementing, inspect the following using the `serena_backend` Serena instance:

1. **`modules/fundamental/src/sbom/service/sbom.rs`** -- `get_symbols_overview` to understand SbomService structure (methods like `fetch`, `list`, `ingest`). Then `find_symbol` on specific methods to understand the pattern for fetching related advisories.

2. **`modules/fundamental/src/sbom/endpoints/get.rs`** -- `get_symbols_overview` to see the GET handler structure and how it builds the response from SbomDetails.

3. **`modules/fundamental/src/sbom/model/details.rs`** -- `get_symbols_overview` to see the SbomDetails struct fields, since the remediation list will be added here.

4. **`modules/fundamental/src/advisory/service/advisory.rs`** -- `find_symbol` for `SEVERITY_ORDER` with `include_body=true` to confirm its definition and visibility. This is the key constant for sorting.

5. **`modules/fundamental/src/advisory/model/summary.rs`** -- `get_symbols_overview` to understand the AdvisorySummary struct (has `severity` field per the repo description).

6. **Sibling test analysis**: `tests/api/sbom.rs` and `tests/api/advisory.rs` -- inspect test patterns, assertion style, setup/teardown.

7. **CONVENTIONS.md**: Read and extract CI check commands and conventions.

### Convention Conformance Analysis

Examine sibling files for:
- **Naming**: Rust `snake_case` for functions/variables, `PascalCase` for types, `SCREAMING_SNAKE` for constants
- **Error handling**: `Result<T, AppError>` with `.context()` wrapping
- **Response types**: Detail endpoints return the struct directly; list endpoints return `PaginatedResults<T>`
- **Test patterns**: `assert_eq!(resp.status(), StatusCode::OK)` pattern, real PostgreSQL test database

## Files to Modify

### 1. `modules/fundamental/src/sbom/model/details.rs`

**Changes**: Add a `remediations` field to the `SbomDetails` struct.

```rust
/// Severity-sorted list of remediation items for advisories affecting this SBOM.
pub remediations: Vec<RemediationItem>,
```

Also define the `RemediationItem` struct in this file (or in a new `remediation.rs` model file under `sbom/model/`):

```rust
/// A single remediation action derived from an advisory affecting the SBOM.
#[derive(Debug, Clone, Serialize, Deserialize, utoipa::ToSchema)]
pub struct RemediationItem {
    /// The unique identifier of the advisory.
    pub advisory_id: String,
    /// The severity level of the advisory (e.g., "critical", "high").
    pub severity: String,
    /// The title or summary of the advisory.
    pub title: String,
    /// The version that fixes the vulnerability, if available.
    pub fix_version: Option<String>,
}
```

### 2. `modules/fundamental/src/sbom/service/sbom.rs`

**Changes**: Add a method `build_remediation_list` to `SbomService` that:

1. Fetches advisories related to the SBOM (following existing patterns for advisory fetching in this service).
2. Maps each advisory to a `RemediationItem` struct.
3. Sorts the list using `SEVERITY_ORDER` from the advisory module.
4. Returns the sorted `Vec<RemediationItem>`.

```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;

impl SbomService {
    /// Builds a severity-sorted list of remediation items for the given SBOM.
    ///
    /// Advisories are sorted in descending severity order: Critical > High > Medium > Low > None.
    pub async fn build_remediation_list(
        &self,
        sbom_id: &str,
        connection: &impl ConnectionTrait,
    ) -> Result<Vec<RemediationItem>, AppError> {
        // Fetch advisories related to this SBOM via the sbom_advisory join table
        let advisories = /* query using existing advisory-fetching pattern */;

        let mut remediations: Vec<RemediationItem> = advisories
            .iter()
            .map(|adv| RemediationItem {
                advisory_id: adv.id.clone(),
                severity: adv.severity.clone().unwrap_or_default(),
                title: adv.title.clone().unwrap_or_default(),
                fix_version: adv.fix_version.clone(),
            })
            .collect();

        // Sort by position in SEVERITY_ORDER (lower index = higher severity)
        remediations.sort_by_key(|item| {
            SEVERITY_ORDER
                .iter()
                .position(|s| s.eq_ignore_ascii_case(&item.severity))
                .unwrap_or(SEVERITY_ORDER.len())
        });

        Ok(remediations)
    }
}
```

**SEVERITY_ORDER handling**: The constant `SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]` already exists in `modules/fundamental/src/advisory/service/advisory.rs`. Per the symbol deduplication protocol:

1. **Search**: Use `find_symbol` / `search_for_pattern` / Grep to locate `SEVERITY_ORDER` in the `modules/fundamental` crate.
2. **Found**: It exists in `advisory/service/advisory.rs`.
3. **Dependency check**: Both the advisory and sbom modules are within the same crate (`modules/fundamental`), so no new cross-crate dependency is needed.
4. **Visibility**: If `SEVERITY_ORDER` is not already `pub`, change it to `pub` so it can be imported from `crate::advisory::service::advisory::SEVERITY_ORDER`.
5. **Import**: Add `use crate::advisory::service::advisory::SEVERITY_ORDER;` in `sbom/service/sbom.rs`.

This avoids duplicating the constant and ensures any future changes to severity ordering are applied consistently across both advisory and sbom modules.

### 3. `modules/fundamental/src/advisory/service/advisory.rs`

**Changes (conditional)**: If `SEVERITY_ORDER` is not already `pub`, change its visibility:

```rust
// Before (if private):
const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];

// After:
/// Canonical severity ordering for advisory sorting. Lower index = higher severity.
pub const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```

This file is not listed in "Files to Modify" so if this change is needed, it would be flagged in Step 9's scope containment check for user approval. However, this is the correct approach per the "Reuse over duplication" guidance -- making the existing symbol public rather than duplicating it.

### 4. `modules/fundamental/src/sbom/endpoints/get.rs`

**Changes**: In the GET handler for `/api/v2/sbom/{id}`, call the new `build_remediation_list` method and include the result in the response.

```rust
// Within the existing GET handler:
let remediations = sbom_service
    .build_remediation_list(&id, &connection)
    .await
    .context("building remediation list")?;

// Include in response (add to SbomDetails construction):
// details.remediations = remediations;
```

### 5. `modules/fundamental/src/sbom/model/mod.rs`

**Changes**: If `RemediationItem` is defined in `details.rs`, ensure it is re-exported from the model module. If a separate `remediation.rs` file is created, add `pub mod remediation;` to `mod.rs`.

## Files to Create

### 1. `tests/api/sbom_remediation.rs`

Integration tests for the severity-sorted remediation list:

```rust
/// Verifies that the remediation list is sorted by severity, with Critical first and None last.
#[tokio::test]
async fn test_remediation_list_sorted_by_severity() {
    // Given an SBOM with advisories of different severities
    // (set up test data with Critical, Low, High, None, Medium advisories)

    // When fetching the SBOM details
    // GET /api/v2/sbom/{id}

    // Then the remediations field should be sorted Critical > High > Medium > Low > None
    assert_eq!(remediations[0].severity, "critical");
    assert_eq!(remediations[1].severity, "high");
    assert_eq!(remediations[2].severity, "medium");
    assert_eq!(remediations[3].severity, "low");
    assert_eq!(remediations[4].severity, "none");
}

/// Verifies that an SBOM with no advisories returns an empty remediation list.
#[tokio::test]
async fn test_empty_remediation_list_for_sbom_without_advisories() {
    // Given an SBOM with no linked advisories

    // When fetching the SBOM details
    // GET /api/v2/sbom/{id}

    // Then the remediations field should be an empty array
    assert!(remediations.is_empty());
}

/// Verifies that advisories with the same severity maintain stable ordering.
#[tokio::test]
async fn test_stable_ordering_for_same_severity() {
    // Given an SBOM with multiple High-severity advisories

    // When fetching the SBOM details
    // GET /api/v2/sbom/{id}

    // Then all High advisories should appear together, and their relative order
    // should be deterministic (stable sort preserves insertion order)
    let high_items: Vec<_> = remediations
        .iter()
        .filter(|r| r.severity == "high")
        .collect();
    assert_eq!(high_items.len(), expected_high_count);
    // Assert specific advisory_ids to verify stable ordering
}
```

Tests follow the existing patterns from `tests/api/sbom.rs`: use `assert_eq!` with `StatusCode::OK`, real PostgreSQL test database, value-based assertions (not just length checks).

Also add `mod sbom_remediation;` to `tests/api/mod.rs` or the test harness entry point if one exists.

## Verification (Step 9)

### Scope Containment
- Files in diff should match: `sbom/service/sbom.rs`, `sbom/endpoints/get.rs`, `sbom/model/details.rs`, `tests/api/sbom_remediation.rs`
- Potentially out-of-scope: `advisory/service/advisory.rs` (if visibility change needed), `sbom/model/mod.rs` (module registration) -- flag for user approval

### Data-Flow Trace
- Input: GET request to `/api/v2/sbom/{id}`
- Processing: `SbomService::build_remediation_list` fetches advisories via `sbom_advisory` join, maps to `RemediationItem`, sorts by `SEVERITY_ORDER`
- Output: JSON response with `remediations` array in `SbomDetails`
- Complete path: request -> handler -> service -> DB query -> mapping -> sorting -> response serialization

### Duplication Check
- `SEVERITY_ORDER`: reused from advisory module, not duplicated
- `RemediationItem`: new struct, no existing equivalent found
- Sorting logic: new, specific to remediation list

### CI Checks
- Run commands from `CONVENTIONS.md` (if found)
- `cargo test -p trustify-fundamental` (module-level test for the fundamental crate)
- `cargo fmt --check`, `cargo clippy`

## Commit

```
feat(sbom): add severity-sorted remediation list to SBOM details

Implements TC-9210
```
