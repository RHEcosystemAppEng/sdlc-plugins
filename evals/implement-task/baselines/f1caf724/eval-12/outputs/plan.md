# Implementation Plan: TC-9210 -- Add severity-sorted remediation list to SBOM risk report

## Task Summary

Add a severity-sorted remediation list to the SBOM risk report endpoint. Advisories
associated with an SBOM are sorted by severity (Critical > High > Medium > Low > None)
and returned in descending severity order. The existing `SEVERITY_ORDER` constant from
the advisory module is reused for sorting.

## Target Branch

`main` (extracted from the Target Branch section of the task description)

## Branch Operations

```
git checkout main
git pull
git checkout -b TC-9210
```

## Step 4 -- Code Inspection (Pre-Implementation)

Before making any changes, inspect the existing code to understand current patterns
and confirm the referenced symbols exist:

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Use
   `mcp__serena_backend__get_symbols_overview` to examine the advisory service structure.
   Use `mcp__serena_backend__find_symbol` with `include_body=true` to read the
   `SEVERITY_ORDER` constant definition and verify its type and values. This confirms
   the constant exists and has the expected shape: `&[&str] = &["critical", "high", "medium", "low", "none"]`.

2. **`modules/fundamental/src/sbom/service/sbom.rs`** -- Use
   `mcp__serena_backend__get_symbols_overview` to understand the SbomService structure,
   existing methods, and patterns for fetching related data (advisories, packages). This
   informs how to add the remediation list builder method.

3. **`modules/fundamental/src/sbom/endpoints/get.rs`** -- Use
   `mcp__serena_backend__get_symbols_overview` to understand the GET endpoint handler
   pattern, response construction, and how SbomDetails is assembled.

4. **`modules/fundamental/src/sbom/model/details.rs`** -- Read the SbomDetails struct
   to understand its fields and how to add the `remediations` field.

5. **Symbol deduplication search for `SEVERITY_ORDER`** -- Before declaring any new
   constant, search the target package (`modules/fundamental/src/`) for existing
   definitions using `search_for_pattern` and `find_symbol`. See `symbol-search.md`
   for the full analysis. Result: found in `advisory/service/advisory.rs`, will import
   rather than redeclare.

### Convention Conformance Analysis

Inspect sibling files to identify established patterns:

- **Sibling services**: `advisory/service/advisory.rs`, `package/service/mod.rs` --
  all use `Result<T, AppError>` with `.context()` for error handling
- **Sibling endpoints**: `advisory/endpoints/get.rs`, `sbom/endpoints/list.rs` --
  follow standard Axum handler pattern with response type extraction
- **Module structure**: Each domain module follows `model/ + service/ + endpoints/`
- **Naming**: `verb_noun` pattern for service methods (e.g., `fetch_sbom`, `list_advisories`)
- **Tests**: Integration tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)`

## Files to Modify

### 1. `modules/fundamental/src/advisory/service/advisory.rs`

**Change**: Make `SEVERITY_ORDER` constant public.

- Change `const SEVERITY_ORDER: &[&str]` to `pub const SEVERITY_ORDER: &[&str]`
- No other changes to this file -- the constant definition, value, and all existing
  usages remain untouched.

**Rationale**: The symbol deduplication analysis (see `symbol-search.md`) found that
`SEVERITY_ORDER` already exists in this file with the exact semantics needed. Rather
than declaring a duplicate constant in the sbom service, we make the existing one
public so it can be imported. This follows the DRY principle and the skill's "Reuse
over duplication" guidance. Since both modules are in the same crate
(`trustify-module-fundamental`), no new dependency is needed.

### 2. `modules/fundamental/src/sbom/service/sbom.rs`

**Change**: Add a `get_remediation_list` method to `SbomService`.

- Add import: `use crate::advisory::service::advisory::SEVERITY_ORDER;`
- Add a new method `get_remediation_list(&self, sbom_id: &str) -> Result<Vec<RemediationItem>, AppError>`
  that:
  1. Fetches all advisories associated with the given SBOM ID
  2. Maps each advisory to a `RemediationItem` struct with fields:
     `advisory_id`, `severity`, `title`, `fix_version`
  3. Sorts the list using `SEVERITY_ORDER` as the sort key -- the position of
     each advisory's severity string in the `SEVERITY_ORDER` array determines
     its sort priority (lower index = higher severity = earlier in results)
  4. Returns the sorted list wrapped in `Result`
- Follow existing patterns in the same file for fetching related data and error handling
  (use `.context()` for error wrapping)

**Important**: The `SEVERITY_ORDER` constant is NOT declared in this file. It is
imported from `crate::advisory::service::advisory::SEVERITY_ORDER`. This avoids
symbol duplication -- the task's Acceptance Criteria explicitly states "no duplicate
definition".

### 3. `modules/fundamental/src/sbom/endpoints/get.rs`

**Change**: Include the remediation list in the SBOM details response.

- Call `sbom_service.get_remediation_list(&sbom_id)` in the GET handler
- Add the `remediations` field to the response body
- Follow the existing pattern for composing the SbomDetails response

### 4. `modules/fundamental/src/sbom/model/details.rs` (within Files to Modify scope via `get.rs` dependency)

**Note**: The task's Files to Modify does not explicitly list `details.rs`, but the
`SbomDetails` struct needs a new `remediations` field. Since this is a model file
tightly coupled to `get.rs`, it falls within the scope of the endpoint modification.
If strict scope adherence is required, this would be flagged in Step 9's scope
containment check for user approval.

- Add `RemediationItem` struct definition:
  ```rust
  /// A single remediation entry linking an advisory to an SBOM, used for
  /// severity-sorted display in the risk report.
  #[derive(Debug, Clone, Serialize, Deserialize)]
  pub struct RemediationItem {
      /// The unique identifier of the advisory
      pub advisory_id: String,
      /// The severity level (critical, high, medium, low, none)
      pub severity: String,
      /// The advisory title or summary
      pub title: String,
      /// The version that fixes the vulnerability, if available
      pub fix_version: Option<String>,
  }
  ```
- Add `remediations: Vec<RemediationItem>` field to `SbomDetails`

## Files to Create

### 5. `tests/api/sbom_remediation.rs`

**New file**: Integration tests for the severity-sorted remediation list.

Tests to implement (per Test Requirements):

```rust
/// Verifies that the remediation list is sorted by severity in descending order
/// (Critical first, None last).
#[test]
fn test_remediation_list_sorted_by_severity() {
    // Given an SBOM with advisories of varying severity levels
    // When fetching the SBOM details via GET /api/v2/sbom/{id}
    // Then the remediations list is ordered: critical, high, medium, low, none
    // Assert on specific severity values at known positions, not just count
}

/// Verifies that an SBOM with no associated advisories returns an empty
/// remediation list.
#[test]
fn test_sbom_no_advisories_returns_empty_remediation_list() {
    // Given an SBOM with no linked advisories
    // When fetching the SBOM details
    // Then remediations is an empty array
    assert_eq!(resp.remediations.len(), 0);
}

/// Verifies that multiple advisories of the same severity level maintain
/// stable ordering within the severity group.
#[test]
fn test_same_severity_maintains_stable_order() {
    // Given an SBOM with multiple high-severity advisories
    // When fetching the SBOM details
    // Then all high-severity advisories appear in a stable, deterministic order
    // Assert on specific advisory_id values to verify stability
}
```

Follow sibling test patterns from `tests/api/sbom.rs` and `tests/api/advisory.rs`
for setup, teardown, and test database configuration.

## Commit Message

```
feat(sbom): add severity-sorted remediation list to risk report

Add a RemediationItem struct and get_remediation_list method to SbomService
that returns advisories sorted by severity (Critical > High > Medium > Low > None).
Reuses the existing SEVERITY_ORDER constant from the advisory module rather than
redeclaring it, following the DRY principle.

Implements TC-9210
```

With flag: `--trailer='Assisted-by: Claude Code'`

## Self-Verification Checklist

- [ ] **Scope containment**: All changes are within Files to Modify and Files to Create
  - `advisory/service/advisory.rs` -- listed in Files to Modify (visibility change only)
    Note: This file is not in Files to Modify per the task. The symbol search determined
    it needs a `pub` visibility change. Flag in scope containment for user approval.
  - `sbom/service/sbom.rs` -- listed in Files to Modify
  - `sbom/endpoints/get.rs` -- listed in Files to Modify
  - `tests/api/sbom_remediation.rs` -- listed in Files to Create
- [ ] **Symbol deduplication**: `SEVERITY_ORDER` is imported, not redeclared
- [ ] **No duplicate logic**: severity sorting uses the imported constant, no inline ordering
- [ ] **Dead parameter detection**: check for unused parameters after changes
- [ ] **Tests pass**: `cargo test` confirms all new and existing tests pass
- [ ] **Documentation**: `RemediationItem` struct and `get_remediation_list` method have doc comments
