# Implementation Plan -- TC-9210

**Task:** Add severity-sorted remediation list to SBOM risk report
**Repository:** trustify-backend
**Target Branch:** main

---

## Overview

Add a `remediations` field to the GET /api/v2/sbom/{id} response containing a
severity-sorted list of remediation items. Each item maps an advisory to a
`RemediationItem` struct with `advisory_id`, `severity`, `title`, and `fix_version`
fields. Sorting uses the existing `SEVERITY_ORDER` constant from the advisory module.

## SEVERITY_ORDER Handling

The `SEVERITY_ORDER` constant already exists in
`modules/fundamental/src/advisory/service/advisory.rs` as:

```rust
pub const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```

**Decision: import and reuse.** Both the sbom and advisory modules live in the same
crate (`modules/fundamental`), so no new dependency is needed. The constant is already
`pub`. A new declaration will NOT be added anywhere.

Import path in `sbom/service/sbom.rs`:

```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;
```

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**Changes:**

- Add import for `SEVERITY_ORDER` from `crate::advisory::service::advisory`.
- Add a new method `build_remediation_list` to `SbomService`:
  - Fetches advisories related to the given SBOM (following the existing pattern for
    advisory lookups already present in this service).
  - Maps each advisory to a `RemediationItem { advisory_id, severity, title, fix_version }`.
  - Sorts the list using `SEVERITY_ORDER` as the sort key: position in the array
    determines priority (index 0 = highest priority). Advisories with the same
    severity maintain stable ordering (use `sort_by` with a stable sort, which is
    Rust's default).
  - Returns `Vec<RemediationItem>`.
- Add defensive guards on advisory fields (severity, title, fix_version) using
  `.unwrap_or_default()` for fields that may be absent.
- Add doc comment on `build_remediation_list` explaining its purpose and sort order.

### 2. `modules/fundamental/src/sbom/endpoints/get.rs`

**Changes:**

- In the handler for GET /api/v2/sbom/{id}, call
  `SbomService::build_remediation_list` to produce the remediation list.
- Include the result as a `remediations` field in the `SbomDetails` response.
- This likely requires adding a `remediations: Vec<RemediationItem>` field to
  `SbomDetails` in `modules/fundamental/src/sbom/model/details.rs` (scope
  containment note: this is a struct referenced by `get.rs` and is a necessary
  supporting change -- flag in Step 9 for user approval if not listed in Files to Modify).

## Files to Create

### 3. `tests/api/sbom_remediation.rs`

**Contents:**

- Integration tests hitting a real PostgreSQL test database (following the pattern in
  `tests/api/sbom.rs`).
- Test functions:

  1. `test_remediation_list_sorted_by_severity` -- creates an SBOM with advisories of
     varying severity, fetches via GET /api/v2/sbom/{id}, asserts the `remediations`
     array is sorted Critical > High > Medium > Low > None. Uses value-based assertions
     on specific severity strings, not just length checks.

  2. `test_sbom_no_advisories_returns_empty_remediations` -- creates an SBOM with no
     linked advisories, asserts `remediations` is an empty array.

  3. `test_same_severity_stable_ordering` -- creates an SBOM with multiple advisories
     of the same severity, asserts they appear in a stable (deterministic) order.

- Each test function has a `///` doc comment explaining what it verifies.
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments.
- Response assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern per
  project convention.

## Structs

### `RemediationItem`

Defined in `sbom/service/sbom.rs` (or a dedicated model file if convention requires):

```rust
/// A single remediation entry linking an advisory to its severity and fix.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RemediationItem {
    /// The advisory identifier.
    pub advisory_id: String,
    /// Severity level (critical, high, medium, low, none).
    pub severity: String,
    /// Human-readable advisory title.
    pub title: String,
    /// Version that resolves the advisory, if known.
    pub fix_version: Option<String>,
}
```

## Data-Flow Trace

1. **Input:** GET /api/v2/sbom/{id} request arrives at `endpoints/get.rs` handler.
2. **Processing:** Handler calls `SbomService::build_remediation_list(sbom_id)`, which
   queries the `sbom_advisory` join table to fetch related advisories, maps each to a
   `RemediationItem`, and sorts using `SEVERITY_ORDER`.
3. **Output:** Sorted `Vec<RemediationItem>` is attached to `SbomDetails` and serialized
   in the JSON response as the `remediations` field.

All stages are connected -- no incomplete paths.

## Out-of-Scope Considerations

- `modules/fundamental/src/sbom/model/details.rs` may need a new field
  (`remediations: Vec<RemediationItem>`) -- not listed in Files to Modify but
  structurally required. Flag in Step 9 scope containment for user approval.
- No changes to `advisory/service/advisory.rs` -- `SEVERITY_ORDER` is already `pub`.
- No new `SEVERITY_ORDER` constant declared anywhere.
