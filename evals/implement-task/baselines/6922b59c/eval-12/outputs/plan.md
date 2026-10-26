# Implementation Plan for TC-9210

**Task:** Add severity-sorted remediation list to SBOM risk report
**Repository:** trustify-backend
**Target Branch:** main
**Branch name:** TC-9210

---

## Step 0 -- Validate Project Configuration

CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend with serena_backend instance
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: serena_backend with rust-analyzer

Configuration is valid. Proceed.

## Step 1 -- Parse Task Description

Parsed sections:
- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add severity-sorted remediation list to SBOM risk report endpoint
- **Files to Modify:** `modules/fundamental/src/sbom/service/sbom.rs`, `modules/fundamental/src/sbom/endpoints/get.rs`
- **Files to Create:** `tests/api/sbom_remediation.rs`
- **Dependencies:** None
- **Bookend Type:** None
- **Target PR:** None

## Step 2 -- Verify Dependencies

No dependencies to verify.

## Step 4 -- Understand the Code

### Serena inspection plan

Use `mcp__serena_backend__get_symbols_overview` on:
- `modules/fundamental/src/sbom/service/sbom.rs` -- understand SbomService structure
- `modules/fundamental/src/sbom/endpoints/get.rs` -- understand GET handler
- `modules/fundamental/src/sbom/model/details.rs` -- understand SbomDetails struct
- `modules/fundamental/src/advisory/service/advisory.rs` -- locate SEVERITY_ORDER

Use `mcp__serena_backend__find_symbol` with `include_body=true` on:
- `SEVERITY_ORDER` in advisory.rs -- confirm constant definition and visibility
- The handler function in `get.rs` -- understand current response construction
- `SbomDetails` struct -- understand current fields

### Symbol deduplication (critical)

Search the entire `modules/fundamental/src/` for `SEVERITY_ORDER` before declaring
any new constant. See `outputs/symbol-search.md` for the full analysis.

**Result:** `SEVERITY_ORDER` exists as `pub const` in
`modules/fundamental/src/advisory/service/advisory.rs`. Import and reuse it --
do not redeclare.

### Convention conformance analysis

Examine 2-3 sibling files:
- `modules/fundamental/src/sbom/service/sbom.rs` (existing service patterns)
- `modules/fundamental/src/advisory/service/advisory.rs` (sibling service patterns)
- `tests/api/sbom.rs` and `tests/api/advisory.rs` (test patterns)

Expected conventions:
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Naming: `verb_noun` pattern for service methods
- Test assertions: `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Response types: list endpoints use `PaginatedResults<T>`

### Documentation file identification

- `CONVENTIONS.md` at repository root
- `docs/api.md` -- API reference (may need update for new response field)

---

## Files to Modify

### 1. `modules/fundamental/src/sbom/model/details.rs`

**Note:** This file is not listed in Files to Modify but will be flagged during
Step 9 scope containment for user approval. The `SbomDetails` struct lives here
and needs a new field. Alternatively, if `SbomDetails` is defined inline in
`sbom.rs`, the change stays in scope.

**Changes:**
- Add `remediations: Vec<RemediationItem>` field to `SbomDetails` struct
- Add `#[serde(default)]` to ensure backward compatibility

### 2. `modules/fundamental/src/sbom/service/sbom.rs`

**Changes:**

a) **Add import for SEVERITY_ORDER:**
```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;
```

b) **Define `RemediationItem` struct:**
```rust
/// A single remediation entry linking an advisory to its severity and fix version.
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq, Eq)]
pub struct RemediationItem {
    /// The unique identifier of the advisory.
    pub advisory_id: String,
    /// The severity level (e.g., "critical", "high", "medium", "low", "none").
    pub severity: String,
    /// The title of the advisory.
    pub title: String,
    /// The version that fixes the vulnerability, if available.
    pub fix_version: Option<String>,
}
```

c) **Add `build_remediation_list` method to `SbomService`:**
```rust
/// Builds a severity-sorted list of remediation items for the given SBOM.
///
/// Fetches all advisories linked to the SBOM, maps each to a RemediationItem,
/// and sorts by severity using SEVERITY_ORDER (Critical > High > Medium > Low > None).
pub async fn build_remediation_list(
    &self,
    sbom_id: &str,
    connection: &impl ConnectionTrait,
) -> Result<Vec<RemediationItem>, AppError> {
    // Fetch advisories related to this SBOM (follow existing pattern)
    let advisories = self.fetch_related_advisories(sbom_id, connection)
        .await
        .context("fetching advisories for remediation list")?;

    // Map to RemediationItem
    let mut remediations: Vec<RemediationItem> = advisories
        .into_iter()
        .map(|adv| RemediationItem {
            advisory_id: adv.advisory_id.clone(),
            severity: adv.severity.clone().unwrap_or_default(),
            title: adv.title.clone().unwrap_or_default(),
            fix_version: adv.fix_version.clone(),
        })
        .collect();

    // Sort by severity using SEVERITY_ORDER -- position in the array determines priority
    // Lower index = higher severity = appears first
    remediations.sort_by(|a, b| {
        let a_pos = SEVERITY_ORDER
            .iter()
            .position(|s| s.eq_ignore_ascii_case(&a.severity))
            .unwrap_or(SEVERITY_ORDER.len());
        let b_pos = SEVERITY_ORDER
            .iter()
            .position(|s| s.eq_ignore_ascii_case(&b.severity))
            .unwrap_or(SEVERITY_ORDER.len());
        a_pos.cmp(&b_pos)
    });

    Ok(remediations)
}
```

**SEVERITY_ORDER handling:** The constant is imported from
`crate::advisory::service::advisory::SEVERITY_ORDER`. It is already `pub` and in
the same crate, so no visibility changes or new dependencies are needed. The sort
uses `.position()` on the array -- items at index 0 ("critical") sort first, items
not found in the array sort last. Case-insensitive comparison with
`eq_ignore_ascii_case` for defensive matching.

### 3. `modules/fundamental/src/sbom/endpoints/get.rs`

**Changes:**

a) **Modify the GET `/api/v2/sbom/{id}` handler** to call
`build_remediation_list` and include the result in the response:

```rust
// After fetching SBOM details (existing code)
let remediations = sbom_service
    .build_remediation_list(&id, &connection)
    .await
    .context("building remediation list")?;

// Include in response
// Set details.remediations = remediations before returning
```

b) **Ensure RemediationItem is imported:**
```rust
use crate::sbom::service::sbom::RemediationItem;
```

---

## Files to Create

### 4. `tests/api/sbom_remediation.rs`

**Integration tests for severity-sorted remediation list.**

Register the new test module in the test crate (e.g., add `mod sbom_remediation;`
in `tests/api/mod.rs` or the test crate root).

**Test functions:**

a) **`test_remediation_list_sorted_by_severity`**
```rust
/// Verifies that the remediation list is sorted by severity: Critical first, None last.
#[tokio::test]
async fn test_remediation_list_sorted_by_severity() {
    // Given an SBOM with advisories of different severities
    // (set up test SBOM with critical, low, high, medium, none advisories)

    // When fetching the SBOM details
    // GET /api/v2/sbom/{id}

    // Then the remediations field should be sorted Critical > High > Medium > Low > None
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SbomDetailsResponse = resp.json().await.unwrap();
    let severities: Vec<&str> = body.remediations.iter().map(|r| r.severity.as_str()).collect();
    assert_eq!(severities, vec!["critical", "high", "medium", "low", "none"]);
}
```

b) **`test_empty_sbom_returns_empty_remediation_list`**
```rust
/// Verifies that an SBOM with no linked advisories returns an empty remediation list.
#[tokio::test]
async fn test_empty_sbom_returns_empty_remediation_list() {
    // Given an SBOM with no linked advisories

    // When fetching the SBOM details
    // GET /api/v2/sbom/{id}

    // Then the remediations field should be an empty list
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SbomDetailsResponse = resp.json().await.unwrap();
    assert!(body.remediations.is_empty());
}
```

c) **`test_same_severity_maintains_stable_order`**
```rust
/// Verifies that multiple advisories with the same severity maintain stable ordering.
#[tokio::test]
async fn test_same_severity_maintains_stable_order() {
    // Given an SBOM with multiple advisories all at "high" severity

    // When fetching the SBOM details
    // GET /api/v2/sbom/{id}

    // Then all items should have severity "high" and maintain insertion order
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SbomDetailsResponse = resp.json().await.unwrap();
    for item in &body.remediations {
        assert_eq!(item.severity, "high");
    }
    // Verify stable ordering by checking advisory_id order matches insertion order
}
```

All tests use:
- Doc comments on every test function
- Given/When/Then section comments
- Value-based assertions (not just length checks)
- `assert_eq!(resp.status(), StatusCode::OK)` pattern matching sibling tests

---

## Data-Flow Trace

1. **Input:** HTTP GET request to `/api/v2/sbom/{id}`
2. **Processing:**
   - Handler in `get.rs` receives the request and extracts the SBOM ID
   - Calls `SbomService::build_remediation_list` with the SBOM ID
   - Service fetches related advisories from the database (via existing advisory query pattern)
   - Maps advisories to `RemediationItem` structs
   - Sorts by severity using imported `SEVERITY_ORDER` constant
3. **Output:** `SbomDetails` response includes `remediations: Vec<RemediationItem>` field,
   serialized as JSON in the HTTP response

All stages are connected. No incomplete paths.

---

## Scope Containment Notes

The task lists two files to modify and one to create. The model file
`sbom/model/details.rs` may also need a field addition for the `SbomDetails`
struct. If that struct is defined in `details.rs` (not in `sbom.rs`), this
out-of-scope file would be flagged in Step 9 for user approval before proceeding.

---

## SEVERITY_ORDER Handling Summary

| Aspect | Decision |
|--------|----------|
| **Location** | `modules/fundamental/src/advisory/service/advisory.rs` |
| **Visibility** | Already `pub` -- no changes needed |
| **Same crate?** | Yes -- both sbom and advisory are in `modules/fundamental` |
| **Import path** | `use crate::advisory::service::advisory::SEVERITY_ORDER;` |
| **Redeclare?** | No -- import and reuse the existing constant |
| **Rationale** | Same crate, already exported, task explicitly requires reuse, DRY principle |
