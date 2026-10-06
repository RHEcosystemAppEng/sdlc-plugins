# Implementation Plan for TC-9210

## Task Summary

Add a severity-sorted remediation list to the SBOM risk report endpoint. The list sorts
advisories by severity (Critical > High > Medium > Low > None) and returns them in
descending severity order.

## SEVERITY_ORDER Constant Handling

**The `SEVERITY_ORDER` constant already exists** in `modules/fundamental/src/advisory/service/advisory.rs`.
It will be imported and reused -- no new constant will be declared. See `symbol-search.md`
for the full search and decision process.

If the constant is not already `pub`, it will be made public so the `sbom` module can
import it. Both modules are in the same crate (`modules/fundamental`), so no new
dependency is needed.

## Files to Modify

### 1. `modules/fundamental/src/advisory/service/advisory.rs`

**Change:** Make `SEVERITY_ORDER` public if it is not already.

- Change `const SEVERITY_ORDER` to `pub const SEVERITY_ORDER`
- This is the minimum change needed to allow the `sbom` module to import the constant.

**Why:** The sbom service needs access to this constant for severity sorting. Since both
modules live in the same crate, making it `pub` and importing it follows the "Reuse over
duplication" guidance from the implement-task skill.

### 2. `modules/fundamental/src/advisory/service/mod.rs`

**Change:** Ensure `SEVERITY_ORDER` is re-exported from the service module.

- Add `pub use advisory::SEVERITY_ORDER;` if not already present, or verify the module
  structure makes the constant accessible to sibling modules.

### 3. `modules/fundamental/src/sbom/service/sbom.rs`

**Changes:**

#### a. Import SEVERITY_ORDER

Add import at the top of the file:
```rust
use crate::advisory::service::SEVERITY_ORDER;
```

#### b. Define RemediationItem struct

Add a new struct to represent each remediation entry:
```rust
/// A single remediation item linking an advisory to its severity and fix information.
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

**Note:** `fix_version` is `Option<String>` as a defensive measure -- not all advisories
may have a fix version. This follows the skill's "Defensive property access on external
data" guidance.

#### c. Add `build_remediation_list` method to SbomService

Add a method that:
1. Fetches advisories related to the SBOM (following the existing pattern in `sbom.rs`
   for fetching related advisories).
2. Maps each advisory to a `RemediationItem` with advisory_id, severity, title, and
   fix_version.
3. Sorts the list using `SEVERITY_ORDER` -- position in the array determines priority.
   Advisories whose severity is not in `SEVERITY_ORDER` sort to the end.
4. Returns `Vec<RemediationItem>`.

Sorting logic:
```rust
items.sort_by_key(|item| {
    SEVERITY_ORDER
        .iter()
        .position(|&s| s == item.severity.to_lowercase())
        .unwrap_or(SEVERITY_ORDER.len())
});
```

### 4. `modules/fundamental/src/sbom/model/details.rs`

**Change:** Add a `remediations` field to the `SbomDetails` struct.

```rust
/// Severity-sorted list of remediation items for advisories affecting this SBOM.
pub remediations: Vec<RemediationItem>,
```

Import `RemediationItem` from the service module.

### 5. `modules/fundamental/src/sbom/endpoints/get.rs`

**Change:** Include the remediation list in the SBOM details response.

- In the handler for `GET /api/v2/sbom/{id}`, call `SbomService::build_remediation_list`
  to populate the `remediations` field of the `SbomDetails` response.
- Follow the existing pattern in the handler: the handler already fetches SBOM details,
  so the remediation list is added as an additional field populated before returning.
- Error handling uses `Result<T, AppError>` with `.context()` wrapping, matching the
  convention found in sibling endpoint handlers.

## Files to Create

### 6. `tests/api/sbom_remediation.rs`

**Purpose:** Integration tests for the severity-sorted remediation list.

**Tests to write:**

#### a. `test_remediation_list_sorted_by_severity`
- Doc comment: `/// Verifies that the remediation list is sorted by severity (Critical first, None last).`
- Given: An SBOM with advisories at different severity levels (critical, low, high, medium, none).
- When: `GET /api/v2/sbom/{id}` is called.
- Then: The `remediations` array is sorted Critical > High > Medium > Low > None.
- Assert on actual severity values in order, not just array length.

#### b. `test_empty_sbom_returns_empty_remediations`
- Doc comment: `/// Verifies that an SBOM with no advisories returns an empty remediation list.`
- Given: An SBOM with no associated advisories.
- When: `GET /api/v2/sbom/{id}` is called.
- Then: The `remediations` field is an empty array.
- Assert: `assert_eq!(remediations.len(), 0)`.

#### c. `test_same_severity_stable_ordering`
- Doc comment: `/// Verifies that multiple advisories of the same severity maintain stable ordering.`
- Given: An SBOM with multiple advisories all at "high" severity.
- When: `GET /api/v2/sbom/{id}` is called.
- Then: All items have severity "high" and their relative order is deterministic (stable sort).
- Assert on specific advisory_ids to verify ordering is consistent.

**Test conventions to follow:**
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for response validation.
- Tests hit a real PostgreSQL test database (per repository conventions).
- Given-When-Then section comments inside each test body.
- Doc comments on every test function.

### 7. `tests/api/mod.rs` (if needed)

**Change:** Register `sbom_remediation` as a test module if the test directory uses
`mod.rs`-based module registration:
```rust
mod sbom_remediation;
```

## Verification Steps

1. **Scope containment:** `git diff --name-only` must show only the files listed above.
   The advisory module changes (making `SEVERITY_ORDER` public) are flagged as
   out-of-scope per the task's "Files to Modify" section -- user approval will be
   requested since the task only lists `sbom/service/sbom.rs` and `sbom/endpoints/get.rs`.
2. **Duplication check:** Grep for `SEVERITY_ORDER` to confirm no duplicate declaration was
   introduced.
3. **CI checks:** Run any commands from `CONVENTIONS.md` (formatting, linting, compilation).
4. **Rust module-level tests:** `cargo test -p <crate-name>` for the `fundamental` crate.
5. **Data-flow trace:**
   - Input: `GET /api/v2/sbom/{id}` request with SBOM ID.
   - Processing: `SbomService::build_remediation_list` fetches advisories, maps to
     `RemediationItem`, sorts by `SEVERITY_ORDER`.
   - Output: `SbomDetails` response includes `remediations` field with sorted list.
6. **Acceptance criteria verification:** All four criteria checked against implementation.

## Out-of-Scope Considerations

The task's "Files to Modify" section lists only:
- `modules/fundamental/src/sbom/service/sbom.rs`
- `modules/fundamental/src/sbom/endpoints/get.rs`

However, to reuse `SEVERITY_ORDER` without duplication, the advisory module files
(`advisory/service/advisory.rs`, `advisory/service/mod.rs`) may need visibility changes.
Additionally, `sbom/model/details.rs` needs the new `remediations` field. These will be
flagged during Step 9's scope containment check and the user will be asked to approve
each out-of-scope change before committing.
