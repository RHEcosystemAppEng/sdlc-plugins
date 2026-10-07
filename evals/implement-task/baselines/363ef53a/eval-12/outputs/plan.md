# Implementation Plan -- TC-9210

## Task Summary

Add a severity-sorted remediation list to the SBOM risk report endpoint. The response for `GET /api/v2/sbom/{id}` should include a `remediations` field containing advisories sorted by severity in descending order (Critical > High > Medium > Low > None).

## SEVERITY_ORDER Constant Handling

**Decision: Reuse existing constant -- do NOT declare a new one.**

The `SEVERITY_ORDER` constant already exists in `modules/fundamental/src/advisory/service/advisory.rs`. It defines the exact ordering needed: `&["critical", "high", "medium", "low", "none"]`. Both the advisory and sbom modules reside in the same crate (`modules/fundamental`), so importing across sibling modules requires no new dependency -- only a visibility change if the constant is currently private.

See `outputs/symbol-search.md` for the full search and decision process.

## Files to Modify

### 1. `modules/fundamental/src/advisory/service/advisory.rs`

**Change:** Ensure `SEVERITY_ORDER` has `pub(crate)` visibility so the sbom service can import it.

```rust
// Before (if private):
const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];

// After:
pub(crate) const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```

This is the minimal change needed to enable reuse. `pub(crate)` keeps the constant internal to the `fundamental` crate while making it accessible to sibling modules.

### 2. `modules/fundamental/src/sbom/service/sbom.rs`

**Changes:**

a) **Import `SEVERITY_ORDER`** from the advisory module:
```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;
```

b) **Define `RemediationItem` struct** with documentation:
```rust
/// A single remediation entry linking an advisory to an SBOM, sorted by severity.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RemediationItem {
    /// The unique identifier of the advisory.
    pub advisory_id: String,
    /// The severity level (e.g., "critical", "high", "medium", "low", "none").
    pub severity: String,
    /// The advisory title or summary.
    pub title: String,
    /// The version that fixes the vulnerability, if available.
    pub fix_version: Option<String>,
}
```

c) **Add `build_remediation_list` method** to `SbomService`:
```rust
/// Builds a severity-sorted list of remediation items for a given SBOM.
///
/// Fetches all advisories associated with the SBOM, maps them to
/// `RemediationItem` structs, and sorts by severity using the canonical
/// `SEVERITY_ORDER` constant from the advisory module.
pub async fn build_remediation_list(
    &self,
    sbom_id: &str,
    db: &impl ConnectionTrait,
) -> Result<Vec<RemediationItem>, AppError> {
    // Fetch related advisories using existing SbomService patterns
    // Map each advisory to RemediationItem
    // Sort using SEVERITY_ORDER: position in array = sort priority (lower index = higher severity)
    // Return sorted list
}
```

The sort logic uses `SEVERITY_ORDER.iter().position()` to determine each advisory's sort weight. Advisories with severity values not found in `SEVERITY_ORDER` are sorted to the end.

### 3. `modules/fundamental/src/sbom/endpoints/get.rs`

**Changes:**

a) **Include remediation list in SBOM details response.** In the handler for `GET /api/v2/sbom/{id}`, call `sbom_service.build_remediation_list()` and include the result in the response body under a `remediations` field.

b) **Update the `SbomDetails` struct** (or the response struct used by this endpoint) to include:
```rust
/// Severity-sorted list of remediation items for this SBOM.
pub remediations: Vec<RemediationItem>,
```

If `SbomDetails` is defined in `modules/fundamental/src/sbom/model/details.rs`, that file also needs the field addition. (This is an out-of-scope file -- flag in Step 9 scope containment check for user approval.)

## Files to Create

### 1. `tests/api/sbom_remediation.rs`

**Purpose:** Integration tests for the severity-sorted remediation list.

**Tests to implement:**

a) **`test_remediation_list_sorted_by_severity`** -- Verify that the remediation list returned by `GET /api/v2/sbom/{id}` is sorted Critical > High > Medium > Low > None. Create test advisories with different severities, associate them with a test SBOM, and assert the response order matches the expected severity ordering.

b) **`test_empty_remediation_list`** -- Verify that an SBOM with no associated advisories returns an empty `remediations` array (not null, not absent).

c) **`test_same_severity_stable_ordering`** -- Verify that multiple advisories with the same severity level maintain stable ordering (e.g., by advisory_id or insertion order).

All tests follow the existing integration test pattern: hit a real PostgreSQL test database, use `assert_eq!(resp.status(), StatusCode::OK)`, and include doc comments and given-when-then structure.

## Data Flow Trace

1. **Input:** `GET /api/v2/sbom/{id}` request arrives at `endpoints/get.rs` handler
2. **Processing:** Handler calls `SbomService::build_remediation_list()` which:
   - Queries the `sbom_advisory` join table for associated advisories
   - Fetches advisory details (id, severity, title)
   - Looks up fix versions from advisory data
   - Maps to `RemediationItem` structs
   - Sorts using `SEVERITY_ORDER` from advisory module (imported, not redeclared)
3. **Output:** `SbomDetails` response includes populated `remediations` field with sorted list

## Key Design Decisions

1. **Reuse `SEVERITY_ORDER` from advisory module** rather than declaring a duplicate. Both modules are in the same crate; `pub(crate)` visibility is sufficient. See symbol-search.md for full rationale.
2. **`RemediationItem` as a flat struct** matching the task specification: advisory_id, severity, title, fix_version.
3. **`fix_version` is `Option<String>`** because not all advisories may specify a fix version -- defensive handling of external data per skill guidance.
4. **Sort stability** for same-severity items via secondary sort key (advisory_id) to ensure deterministic ordering.
