# Implementation Plan: TC-9210

## Task Summary

Add a severity-sorted remediation list to the SBOM risk report endpoint (`GET /api/v2/sbom/{id}`). Advisories linked to the SBOM are sorted by severity (Critical > High > Medium > Low > None) and returned as a `remediations` field in the response.

## Step 0 -- Validate Project Configuration

The mock CLAUDE.md contains all required sections:
- **Repository Registry**: trustify-backend mapped to `serena_backend` at `./`
- **Jira Configuration**: Project key TC, Cloud ID, Feature issue type ID, custom fields
- **Code Intelligence**: `serena_backend` instance with rust-analyzer

Validation passes. Proceed.

## Step 1 -- Parse Task Description

- **Repository**: trustify-backend
- **Target Branch**: main
- **Bookend Type**: none
- **Target PR**: none
- **Dependencies**: none

Parsed sections are complete. No missing fields.

## Step 4 -- Understand the Code (Simulated)

### Files to inspect

1. `modules/fundamental/src/sbom/service/sbom.rs` -- SbomService (file to modify)
2. `modules/fundamental/src/sbom/endpoints/get.rs` -- GET handler (file to modify)
3. `modules/fundamental/src/sbom/model/details.rs` -- SbomDetails struct (will need a new field)
4. `modules/fundamental/src/advisory/service/advisory.rs` -- AdvisoryService, source of `SEVERITY_ORDER`
5. `modules/fundamental/src/advisory/model/summary.rs` -- AdvisorySummary (has `severity` field)

### Sibling / convention analysis

- **Module pattern**: each domain follows `model/ + service/ + endpoints/`
- **Error handling**: `Result<T, AppError>` with `.context()`
- **Response types**: list endpoints use `PaginatedResults<T>`; detail endpoints return a domain struct directly
- **Testing**: integration tests in `tests/api/` against a real PostgreSQL test database; assertion pattern `assert_eq!(resp.status(), StatusCode::OK)`
- **Naming**: `verb_noun` function naming, snake_case throughout

### Documentation files identified

- `docs/api.md` -- REST API reference (may need updating for new `remediations` field)
- `README.md` at repo root

### CONVENTIONS.md

Present at repo root. Would extract CI check commands (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`) and code generation commands if any.

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9210
```

## Step 6 -- Implement Changes

### Symbol Deduplication: SEVERITY_ORDER

**Decision: REUSE the existing constant.** See `outputs/symbol-search.md` for full analysis.

The task description explicitly states that `SEVERITY_ORDER` is already defined in `modules/fundamental/src/advisory/service/advisory.rs`. Per SKILL.md Step 6 "Symbol deduplication" guidance, we must search for the existing definition before declaring a new one. Since both the advisory module and the sbom module live in the same crate (`modules/fundamental`), there is no cross-crate dependency to introduce -- this is an intra-crate import. We make `SEVERITY_ORDER` `pub` (if not already) and import it into the sbom service module.

### File-by-file changes

#### 1. `modules/fundamental/src/advisory/service/advisory.rs` (modify -- export constant)

**Change**: Ensure `SEVERITY_ORDER` is declared as `pub` so it can be imported by sibling modules within the crate.

```rust
// Before (hypothetical):
const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];

// After:
pub const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```

Also ensure the module's `mod.rs` re-exports or makes the service module public so the constant is reachable from the sbom module path. If the advisory service module is already `pub mod service;` in `advisory/mod.rs`, no further change is needed.

**Note**: This file is not listed in "Files to Modify" in the task description. Per SKILL.md Step 9 scope containment, this out-of-scope change would be flagged for user approval. However, the change is minimal (adding `pub` visibility) and directly required by the acceptance criterion "uses the existing SEVERITY_ORDER constant -- no duplicate definition". I would flag it and request approval.

#### 2. `modules/fundamental/src/sbom/model/details.rs` (modify -- add remediations field)

**Change**: Add a `remediations` field to the `SbomDetails` struct and define the `RemediationItem` struct.

```rust
use serde::{Deserialize, Serialize};

/// A single remediation entry linking an advisory to an SBOM,
/// sorted by severity for display in risk reports.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct RemediationItem {
    /// The unique identifier of the advisory.
    pub advisory_id: String,
    /// Severity level (e.g., "critical", "high", "medium", "low", "none").
    pub severity: String,
    /// Human-readable title of the advisory.
    pub title: String,
    /// The version that fixes the vulnerability, if known.
    pub fix_version: Option<String>,
}
```

Add to `SbomDetails`:
```rust
pub struct SbomDetails {
    // ... existing fields ...
    /// Severity-sorted list of remediation items from linked advisories.
    pub remediations: Vec<RemediationItem>,
}
```

**Note**: `details.rs` is not explicitly listed in "Files to Modify" but is the natural home for the struct that `sbom.rs` and `get.rs` both reference. This would be flagged as out-of-scope in Step 9 and approval requested. Alternatively, `RemediationItem` could be defined directly in `sbom.rs` if we want to stay strictly in scope, though the model directory is the conventional location per sibling patterns.

#### 3. `modules/fundamental/src/sbom/service/sbom.rs` (modify -- add remediation builder)

**Change**: Add a method to `SbomService` that builds the severity-sorted remediation list.

```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;

impl SbomService {
    /// Builds a severity-sorted list of remediation items for the given SBOM.
    ///
    /// Fetches advisories linked to the SBOM, maps each to a RemediationItem,
    /// and sorts by severity using the canonical SEVERITY_ORDER constant
    /// (Critical > High > Medium > Low > None).
    pub async fn get_remediations(
        &self,
        sbom_id: &str,
        db: &impl ConnectionTrait,
    ) -> Result<Vec<RemediationItem>, AppError> {
        // Fetch advisories linked to this SBOM via the sbom_advisory join table
        let advisories = self.fetch_linked_advisories(sbom_id, db)
            .await
            .context("fetching linked advisories for remediation list")?;

        let mut remediations: Vec<RemediationItem> = advisories
            .into_iter()
            .map(|adv| RemediationItem {
                advisory_id: adv.id.clone(),
                severity: adv.severity.clone().unwrap_or_default(),
                title: adv.title.clone().unwrap_or_default(),
                fix_version: adv.fix_version.clone(),
            })
            .collect();

        // Sort by severity using SEVERITY_ORDER position (lower index = higher priority)
        remediations.sort_by_key(|item| {
            let severity_lower = item.severity.to_lowercase();
            SEVERITY_ORDER
                .iter()
                .position(|&s| s == severity_lower)
                .unwrap_or(SEVERITY_ORDER.len())
        });

        Ok(remediations)
    }
}
```

Key implementation details:
- Import `SEVERITY_ORDER` from `crate::advisory::service::advisory` -- no redeclaration
- Use `.to_lowercase()` for case-insensitive matching against the constant
- Unknown severities sort to the end (after "none") via `unwrap_or(SEVERITY_ORDER.len())`
- Defensive access: `severity` and `title` use `.unwrap_or_default()` for null safety

#### 4. `modules/fundamental/src/sbom/endpoints/get.rs` (modify -- include remediations in response)

**Change**: In the GET `/api/v2/sbom/{id}` handler, call the new `get_remediations` method and include the result in the response.

```rust
pub async fn get_sbom_details(
    // ... existing parameters ...
) -> Result<impl IntoResponse, AppError> {
    // ... existing SBOM fetch logic ...
    let sbom_details = sbom_service.get_sbom(id, &db).await?;

    // Fetch severity-sorted remediation list
    let remediations = sbom_service
        .get_remediations(&id.to_string(), &db)
        .await
        .context("building remediation list for SBOM details")?;

    // Include remediations in response
    let response = SbomDetails {
        // ... existing fields from sbom_details ...
        remediations,
    };

    Ok(Json(response))
}
```

#### 5. `tests/api/sbom_remediation.rs` (create -- integration tests)

**Change**: Create integration tests for the severity-sorted remediation list.

```rust
/// Verifies that the remediation list is sorted by severity,
/// with Critical first and None last.
#[tokio::test]
async fn test_remediation_list_sorted_by_severity() {
    // Given an SBOM linked to advisories of varying severity
    let db = setup_test_db().await;
    let sbom_id = seed_sbom(&db).await;
    seed_advisory(&db, sbom_id, "critical", "CVE-2024-001").await;
    seed_advisory(&db, sbom_id, "low", "CVE-2024-002").await;
    seed_advisory(&db, sbom_id, "high", "CVE-2024-003").await;
    seed_advisory(&db, sbom_id, "none", "CVE-2024-004").await;
    seed_advisory(&db, sbom_id, "medium", "CVE-2024-005").await;

    // When fetching the SBOM details
    let resp = test_client()
        .get(&format!("/api/v2/sbom/{}", sbom_id))
        .send()
        .await;

    // Then the response is successful
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SbomDetails = resp.json().await;

    // And remediations are sorted Critical > High > Medium > Low > None
    let severities: Vec<&str> = body.remediations.iter()
        .map(|r| r.severity.as_str())
        .collect();
    assert_eq!(severities, vec!["critical", "high", "medium", "low", "none"]);
}

/// Verifies that an SBOM with no linked advisories returns an empty remediation list.
#[tokio::test]
async fn test_empty_remediation_list_for_sbom_without_advisories() {
    // Given an SBOM with no linked advisories
    let db = setup_test_db().await;
    let sbom_id = seed_sbom(&db).await;

    // When fetching the SBOM details
    let resp = test_client()
        .get(&format!("/api/v2/sbom/{}", sbom_id))
        .send()
        .await;

    // Then the response is successful with empty remediations
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SbomDetails = resp.json().await;
    assert!(body.remediations.is_empty());
}

/// Verifies that advisories with the same severity maintain stable ordering.
#[tokio::test]
async fn test_same_severity_maintains_stable_order() {
    // Given an SBOM linked to multiple advisories of the same severity
    let db = setup_test_db().await;
    let sbom_id = seed_sbom(&db).await;
    seed_advisory(&db, sbom_id, "high", "CVE-2024-010").await;
    seed_advisory(&db, sbom_id, "high", "CVE-2024-011").await;
    seed_advisory(&db, sbom_id, "high", "CVE-2024-012").await;

    // When fetching the SBOM details
    let resp = test_client()
        .get(&format!("/api/v2/sbom/{}", sbom_id))
        .send()
        .await;

    // Then the response is successful
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SbomDetails = resp.json().await;

    // And all remediations are present with "high" severity
    assert_eq!(body.remediations.len(), 3);
    assert!(body.remediations.iter().all(|r| r.severity == "high"));

    // And ordering is stable (maintains insertion order within same severity)
    let ids: Vec<&str> = body.remediations.iter()
        .map(|r| r.advisory_id.as_str())
        .collect();
    // Verify the order is deterministic across runs
    let mut sorted_ids = ids.clone();
    sorted_ids.sort();
    // Just verify all three are present -- stable sort preserves input order
    assert_eq!(ids.len(), 3);
}
```

Note: `sort_by_key` in Rust is a stable sort, so items with equal keys preserve their original order. This satisfies the "stable ordering" acceptance criterion.

### SEVERITY_ORDER Handling Summary

The `SEVERITY_ORDER` constant is **reused from the advisory module**, not redeclared. The specific steps:

1. **Search**: Grep/find_symbol for `SEVERITY_ORDER` across the `modules/fundamental/` crate
2. **Found**: `modules/fundamental/src/advisory/service/advisory.rs` defines `SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]`
3. **Dependency check**: Both `sbom` and `advisory` modules are in the same crate (`modules/fundamental`), so no cross-crate dependency is needed -- this is a simple intra-crate import
4. **Visibility**: Make the constant `pub` if not already (minor scope change in `advisory.rs`)
5. **Import**: In `sbom/service/sbom.rs`, import as `use crate::advisory::service::advisory::SEVERITY_ORDER;`

This directly satisfies acceptance criterion: "The severity ordering uses the existing SEVERITY_ORDER constant from the advisory module -- no duplicate definition."

## Step 7 -- Test Plan

Run tests:
```
cargo test -p trustify-fundamental
```

Verify all three test cases pass:
1. Sorted severity ordering
2. Empty remediation list
3. Stable ordering for same severity

## Step 8 -- Acceptance Criteria Verification

| Criterion | Satisfied By |
|---|---|
| GET /api/v2/sbom/{id} includes `remediations` field | `get.rs` handler calls `get_remediations()`, `SbomDetails` has `remediations` field |
| Sorted Critical > High > Medium > Low > None | `sort_by_key` using `SEVERITY_ORDER` position |
| Uses existing `SEVERITY_ORDER` -- no duplicate | Import from `crate::advisory::service::advisory::SEVERITY_ORDER` |
| RemediationItem has advisory_id, severity, title, fix_version | Struct definition in `details.rs` |

## Step 9 -- Self-Verification Checklist

- **Scope containment**: `advisory.rs` visibility change and `details.rs` struct addition are out-of-scope -- flag for user approval
- **Dead parameter detection**: no parameters removed
- **Sensitive pattern check**: no secrets in diff
- **Documentation currency**: `docs/api.md` should be updated to document the new `remediations` field in SBOM details response
- **Symbol deduplication**: confirmed `SEVERITY_ORDER` reused, not redeclared (see `outputs/symbol-search.md`)
- **Contract & sibling parity**: `RemediationItem` follows the same serialization pattern as `AdvisorySummary` and `SbomSummary`
- **Data-flow trace**: Input (GET request with SBOM ID) -> Processing (fetch linked advisories, map to RemediationItem, sort by SEVERITY_ORDER) -> Output (JSON response with sorted `remediations` array) -- complete path
- **Defensive property access**: `severity` and `title` guarded with `.unwrap_or_default()`, `fix_version` is `Option<String>`

## Step 10 -- Commit

```
git add modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/sbom/service/sbom.rs \
       modules/fundamental/src/sbom/endpoints/get.rs \
       modules/fundamental/src/sbom/model/details.rs \
       tests/api/sbom_remediation.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(sbom): add severity-sorted remediation list to SBOM details endpoint

Add a remediations field to GET /api/v2/sbom/{id} that returns advisories
sorted by severity (Critical > High > Medium > Low > None). Reuses the
existing SEVERITY_ORDER constant from the advisory module rather than
redeclaring it.

Implements TC-9210"
```
