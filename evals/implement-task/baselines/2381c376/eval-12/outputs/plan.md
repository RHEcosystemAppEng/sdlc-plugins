# Implementation Plan for TC-9210

## Task Summary

Add a severity-sorted remediation list to the SBOM risk report endpoint. The list sorts advisories by severity (Critical > High > Medium > Low > None) and returns them in descending severity order, reusing the existing `SEVERITY_ORDER` constant from the advisory module.

## Project Configuration Validation (Step 0)

Verified CLAUDE.md contains:
- Repository Registry: trustify-backend with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID
- Code Intelligence: Serena tool naming convention documented

## Task Parsing (Step 1)

- **Repository**: trustify-backend
- **Target Branch**: main
- **Files to Modify**: `modules/fundamental/src/sbom/service/sbom.rs`, `modules/fundamental/src/sbom/endpoints/get.rs`
- **Files to Create**: `tests/api/sbom_remediation.rs`
- **Bookend Type**: None
- **Target PR**: None
- **Dependencies**: None

## SEVERITY_ORDER Handling (Symbol Deduplication)

See `symbol-search.md` for the full analysis. Summary:

- **Searched** the entire `modules/fundamental/` package for `SEVERITY_ORDER` and variations
- **Found** the existing definition in `modules/fundamental/src/advisory/service/advisory.rs`
- **Decision**: Import and reuse via `use crate::advisory::service::advisory::SEVERITY_ORDER`
- **Visibility change needed**: If not already `pub`, make `SEVERITY_ORDER` public in `advisory.rs`
- **No new dependency**: Both modules are in the same crate (`modules/fundamental`)

## Files to Modify

### 1. `modules/fundamental/src/advisory/service/advisory.rs` (out-of-scope, requires user approval)

**What**: Make `SEVERITY_ORDER` public if it is not already.

**Change**:
```rust
// Change from:
const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
// To:
pub const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```

**Why**: Required so the sbom module can import and reuse this constant instead of redeclaring it. This file is not listed in "Files to Modify" so it will be flagged in Step 9's scope containment check for user approval.

Additionally, verify that the module hierarchy (`advisory/service/mod.rs`, `advisory/mod.rs`) exports this submodule publicly so the path `crate::advisory::service::advisory::SEVERITY_ORDER` is reachable.

### 2. `modules/fundamental/src/sbom/service/sbom.rs`

**What**: Add a severity-sorted remediation list builder method to `SbomService`.

**Changes**:

a) **Add import** for the `SEVERITY_ORDER` constant:
```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;
```

b) **Define `RemediationItem` struct** (or add it in the model directory -- see below):
```rust
/// A single remediation entry linking an advisory to its severity and fix information.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RemediationItem {
    /// The unique identifier of the advisory.
    pub advisory_id: String,
    /// The severity level (e.g., "critical", "high", "medium", "low", "none").
    pub severity: String,
    /// The advisory title or summary.
    pub title: String,
    /// The version that contains the fix, if available.
    pub fix_version: Option<String>,
}
```

c) **Add method `get_remediation_list`** to `SbomService`:
```rust
/// Builds a severity-sorted list of remediation items for the given SBOM.
///
/// Fetches advisories linked to the SBOM, maps each to a RemediationItem,
/// and sorts by severity using SEVERITY_ORDER (Critical first, None last).
/// Advisories with the same severity maintain stable ordering.
pub async fn get_remediation_list(
    &self,
    sbom_id: &str,
    db: &DatabaseConnection,
) -> Result<Vec<RemediationItem>, AppError> {
    // Fetch advisories linked to this SBOM (follow existing pattern for
    // fetching related advisories in sbom.rs)
    let advisories = /* query sbom_advisory join table */;

    // Map to RemediationItem structs
    let mut remediations: Vec<RemediationItem> = advisories
        .iter()
        .map(|adv| RemediationItem {
            advisory_id: adv.id.clone(),
            severity: adv.severity.clone().unwrap_or_default(),
            title: adv.title.clone().unwrap_or_default(),
            fix_version: adv.fix_version.clone(),
        })
        .collect();

    // Sort by SEVERITY_ORDER position (stable sort preserves order within same severity)
    remediations.sort_by_key(|item| {
        SEVERITY_ORDER
            .iter()
            .position(|&s| s == item.severity.to_lowercase())
            .unwrap_or(SEVERITY_ORDER.len())
    });

    Ok(remediations)
}
```

**Patterns followed**: The method follows the existing pattern in `sbom.rs` for fetching related advisories, uses `Result<T, AppError>` with `.context()` error wrapping per the repository's conventions, and uses stable sorting to maintain order within equal severity levels.

### 3. `modules/fundamental/src/sbom/endpoints/get.rs`

**What**: Include the remediation list in the SBOM details response.

**Changes**:

a) **Call the new service method** in the `get_sbom` handler function to fetch the remediation list:
```rust
let remediations = sbom_service
    .get_remediation_list(&id, &db)
    .await
    .context("fetching remediation list")?;
```

b) **Add the `remediations` field** to the response struct or inline response construction. This depends on how SbomDetails is structured:
- If `SbomDetails` is in `modules/fundamental/src/sbom/model/details.rs`, add a `remediations: Vec<RemediationItem>` field there
- If the response is constructed inline in the handler, add the field to the response builder

c) **Update response construction** to include the remediations list in the JSON response body under the `remediations` key.

### 4. `modules/fundamental/src/sbom/model/details.rs` (potential out-of-scope change)

**What**: Add the `remediations` field to the `SbomDetails` struct.

**Change**:
```rust
/// Severity-sorted list of advisory remediations for this SBOM.
pub remediations: Vec<RemediationItem>,
```

**Note**: This file is not listed in "Files to Modify" but may be necessary depending on how the response is structured. Would flag in Step 9's scope containment check. Alternatively, `RemediationItem` could be defined in a new file under `sbom/model/` and the struct could be placed there, but that would also be out of scope.

**Preferred approach**: Define `RemediationItem` in `sbom/model/details.rs` alongside `SbomDetails` since they are closely related, or in a new file `sbom/model/remediation.rs` if convention conformance analysis shows each model type gets its own file.

## Files to Create

### 5. `tests/api/sbom_remediation.rs`

**What**: Integration tests for the severity-sorted remediation list.

**Tests to implement** (following the existing test patterns in `tests/api/sbom.rs`):

a) **`test_remediation_list_sorted_by_severity`**:
```rust
/// Verifies that the remediation list sorts advisories by severity,
/// with Critical first and None last.
#[tokio::test]
async fn test_remediation_list_sorted_by_severity() {
    // Given an SBOM with advisories of varying severity
    // (create test SBOM, link advisories with critical, low, high, medium, none severities)

    // When fetching the SBOM details
    // GET /api/v2/sbom/{id}

    // Then the remediations field contains advisories in severity order:
    // Critical, High, Medium, Low, None
    // Assert on actual severity values, not just count
}
```

b) **`test_remediation_list_empty_when_no_advisories`**:
```rust
/// Verifies that an SBOM with no linked advisories returns an empty remediation list.
#[tokio::test]
async fn test_remediation_list_empty_when_no_advisories() {
    // Given an SBOM with no linked advisories

    // When fetching the SBOM details

    // Then the remediations field is an empty array
}
```

c) **`test_remediation_list_stable_order_same_severity`**:
```rust
/// Verifies that multiple advisories with the same severity maintain stable ordering.
#[tokio::test]
async fn test_remediation_list_stable_order_same_severity() {
    // Given an SBOM with multiple advisories all having "high" severity

    // When fetching the SBOM details

    // Then the remediations field contains all advisories
    // and their relative order is stable (consistent across runs)
    // Assert on specific advisory_id values to verify order
}
```

**Test conventions followed**:
- Uses `assert_eq!(resp.status(), StatusCode::OK)` pattern per repository convention
- Uses `#[tokio::test]` async test attribute
- Each test has a `///` doc comment explaining what it verifies
- Non-trivial tests use given-when-then section comments
- Assertions check actual values (severity strings, advisory IDs), not just collection length

**Module registration**: Add `mod sbom_remediation;` to `tests/api/mod.rs` (if it exists) or ensure the test file is picked up by the test harness.

## Data-Flow Trace

1. **Input**: HTTP GET request to `/api/v2/sbom/{id}`
2. **Processing (endpoint)**: `get.rs` handler receives request, extracts SBOM ID, calls `SbomService::get_remediation_list`
3. **Processing (service)**: `sbom.rs` queries the `sbom_advisory` join table for linked advisories, maps them to `RemediationItem` structs, sorts by `SEVERITY_ORDER` position
4. **Output**: JSON response with `remediations` field containing sorted `RemediationItem` array

All stages are connected. No missing or disconnected stages.

## Scope Containment Notes

The following files would be flagged as out-of-scope modifications requiring user approval in Step 9:

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Making `SEVERITY_ORDER` public. Rationale: required to import the constant from the sbom module per the task's acceptance criteria ("no duplicate definition").

2. **`modules/fundamental/src/sbom/model/details.rs`** (potentially) -- Adding `remediations` field to `SbomDetails`. Rationale: the response struct must include the new field to satisfy the acceptance criterion that `GET /api/v2/sbom/{id}` includes a `remediations` field.

3. **`tests/api/mod.rs`** (potentially) -- Adding `mod sbom_remediation;` to register the new test module.

## CI Verification

Would check for `CONVENTIONS.md` at the repository root and extract CI commands. Regardless, for a Rust repository, would run:

```bash
cargo test -p trustify-fundamental
```

to verify all tests pass in the modified crate before committing.

## Commit Plan

```
feat(sbom): add severity-sorted remediation list to SBOM details

Add a remediation list to the GET /api/v2/sbom/{id} response that sorts
linked advisories by severity (Critical > High > Medium > Low > None).
Reuses the existing SEVERITY_ORDER constant from the advisory module
rather than redeclaring it.

Implements TC-9210
```
