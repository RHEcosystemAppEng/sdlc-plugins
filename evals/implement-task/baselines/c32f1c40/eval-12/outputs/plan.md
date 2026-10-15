# Implementation Plan for TC-9210

## Task Summary

Add a severity-sorted remediation list to the SBOM risk report endpoint
(`GET /api/v2/sbom/{id}`). Advisories are sorted by severity in descending
order (Critical > High > Medium > Low > None) using the existing
`SEVERITY_ORDER` constant from the advisory module.

## Project Configuration Validation

- Repository Registry: `trustify-backend` with Serena instance `serena_backend` (verified)
- Jira Configuration: Project key TC, Cloud ID, custom fields (verified)
- Code Intelligence: `serena_backend` with rust-analyzer (verified)

## Files to Modify

### 1. `modules/fundamental/src/advisory/service/advisory.rs`

**Change**: Ensure `SEVERITY_ORDER` is exported with at least `pub(crate)` visibility.

**Details**:
- Inspect the current visibility of `SEVERITY_ORDER` using `find_symbol` on `serena_backend`.
- If the constant is private (no `pub` modifier), change it to `pub(crate)`:
  ```rust
  pub(crate) const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
  ```
- If already `pub` or `pub(crate)`, no change needed.
- This is a minimal, non-breaking change -- `pub(crate)` does not affect the
  crate's external API surface.

**Note**: This file is not listed in the task's "Files to Modify" section.
If visibility needs changing, this would be flagged as an out-of-scope file
in Step 9's scope containment check, and user approval would be requested
before proceeding.

### 2. `modules/fundamental/src/sbom/service/sbom.rs`

**Change**: Add a severity-sorted remediation list builder method to `SbomService`.

**Details**:

- **Import the constant**:
  ```rust
  use crate::advisory::service::advisory::SEVERITY_ORDER;
  ```

- **Define the `RemediationItem` struct** (in this file or in the sbom model):
  ```rust
  /// A single remediation entry linking an advisory to its severity and fix.
  #[derive(Debug, Clone, Serialize, Deserialize)]
  pub struct RemediationItem {
      /// The unique identifier of the advisory.
      pub advisory_id: String,
      /// The severity level (e.g., "critical", "high", "medium", "low", "none").
      pub severity: String,
      /// The human-readable title of the advisory.
      pub title: String,
      /// The version that fixes the vulnerability, if available.
      pub fix_version: Option<String>,
  }
  ```

  The struct location decision depends on convention conformance analysis.
  Looking at the sibling pattern: `SbomSummary` is in `sbom/model/summary.rs`
  and `SbomDetails` is in `sbom/model/details.rs`. Following this pattern,
  `RemediationItem` could go in `sbom/model/details.rs` (since it is part of
  the details response) or in a new `sbom/model/remediation.rs`. The simpler
  choice is `details.rs` to avoid creating a new file not listed in
  "Files to Create."

- **Add the builder method** to `SbomService` impl block:
  ```rust
  /// Builds a severity-sorted list of remediation items for the given SBOM.
  ///
  /// Fetches advisories associated with the SBOM, maps each to a
  /// `RemediationItem`, and sorts them by severity in descending order
  /// (Critical > High > Medium > Low > None) using `SEVERITY_ORDER`.
  pub async fn build_remediation_list(
      &self,
      sbom_id: &str,
      db: &impl ConnectionTrait,
  ) -> Result<Vec<RemediationItem>, AppError> {
      // Fetch advisories related to this SBOM (follow existing pattern)
      let advisories = self.fetch_related_advisories(sbom_id, db).await?;

      // Map to RemediationItem
      let mut remediations: Vec<RemediationItem> = advisories
          .iter()
          .map(|adv| RemediationItem {
              advisory_id: adv.id.clone(),
              severity: adv.severity.clone().unwrap_or_default(),
              title: adv.title.clone().unwrap_or_default(),
              fix_version: adv.fix_version.clone(),
          })
          .collect();

      // Sort by severity using SEVERITY_ORDER position (lower index = higher priority)
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

  Key design decisions:
  - **Case-insensitive comparison** via `eq_ignore_ascii_case` for robustness.
  - **Unknown severities sort last** via `unwrap_or(SEVERITY_ORDER.len())`.
  - **Stable sort**: Rust's `sort_by` is stable, so advisories with the same
    severity maintain their original order (satisfying the acceptance criterion
    for stable ordering within the same severity).
  - **Defensive access**: `unwrap_or_default()` guards against null severity
    and title fields from the advisory data.

### 3. `modules/fundamental/src/sbom/endpoints/get.rs`

**Change**: Include the remediation list in the SBOM details response.

**Details**:

- **Update the `SbomDetails` struct** (or its response construction) to include
  a `remediations` field:
  ```rust
  /// Complete SBOM details including severity-sorted remediation list.
  pub struct SbomDetails {
      // ... existing fields ...
      /// Severity-sorted list of remediation items (Critical first, None last).
      pub remediations: Vec<RemediationItem>,
  }
  ```

  If `SbomDetails` is defined in `sbom/model/details.rs`, the struct change
  goes there instead, and the endpoint handler in `get.rs` populates it.

- **Update the GET handler** to call the new builder method:
  ```rust
  // In the GET /api/v2/sbom/{id} handler
  let remediations = sbom_service
      .build_remediation_list(&id, &db)
      .await
      .context("building remediation list")?;
  ```

  Then include `remediations` in the response struct construction.

- **Error handling**: Follow the existing pattern of `.context()` wrapping
  with `Result<T, AppError>` return type.

## Files to Create

### 4. `tests/api/sbom_remediation.rs`

**Change**: Integration tests for the severity-sorted remediation list.

**Details**:

Three test functions, each with documentation comments and given-when-then
structure per skill guidance:

```rust
/// Verifies that the remediation list is sorted by severity (Critical first, None last).
#[tokio::test]
async fn test_remediation_list_sorted_by_severity() {
    // Given an SBOM with advisories of varying severities
    // When fetching SBOM details via GET /api/v2/sbom/{id}
    // Then the remediations field is sorted Critical > High > Medium > Low > None
}

/// Verifies that an SBOM with no advisories returns an empty remediation list.
#[tokio::test]
async fn test_sbom_no_advisories_returns_empty_remediations() {
    // Given an SBOM with no linked advisories
    // When fetching SBOM details
    // Then the remediations field is an empty array
}

/// Verifies that advisories with the same severity maintain stable insertion order.
#[tokio::test]
async fn test_same_severity_maintains_stable_order() {
    // Given an SBOM with multiple advisories all at "high" severity
    // When fetching SBOM details
    // Then the remediations are in the same relative order as inserted
}
```

**Test conventions** (from sibling analysis of `tests/api/sbom.rs` and
`tests/api/advisory.rs`):
- Use `assert_eq!(resp.status(), StatusCode::OK)` for status validation.
- Use value-based assertions on the `remediations` array -- assert on specific
  `severity` field values at specific positions, not just `len()`.
- Follow the existing test DB setup pattern from sibling test files.
- Register the test module in `tests/api/mod.rs` or `tests/Cargo.toml` if
  needed.

## How SEVERITY_ORDER Is Handled

### Symbol Deduplication Decision

The `SEVERITY_ORDER` constant is **reused from the advisory module**, not
redeclared. See `outputs/symbol-search.md` for the full analysis.

### Import Path

```rust
use crate::advisory::service::advisory::SEVERITY_ORDER;
```

Both `sbom` and `advisory` are submodules of the `fundamental` crate, so
this is a crate-internal import requiring no new dependency in `Cargo.toml`.

### Visibility Adjustment

If `SEVERITY_ORDER` is currently private, it must be changed to `pub(crate)`.
This would be flagged as an out-of-scope change in Step 9's scope containment
check and requires user approval.

### Sorting Mechanism

The constant is used as a lookup table for sort keys:

```rust
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
```

Position 0 (`"critical"`) sorts first; position 4 (`"none"`) sorts last.
Unknown severity values get position 5 (beyond the array), sorting after
all known severities.

## Data-Flow Trace

| Stage | Description | Location |
|---|---|---|
| Input | `GET /api/v2/sbom/{id}` request | `sbom/endpoints/get.rs` |
| Processing | Handler calls `SbomService::build_remediation_list()` | `sbom/service/sbom.rs` |
| Data fetch | Service queries advisories linked to the SBOM via `sbom_advisory` join | `sbom/service/sbom.rs` |
| Transform | Advisories mapped to `RemediationItem` structs | `sbom/service/sbom.rs` |
| Sort | Items sorted by `SEVERITY_ORDER` position | `sbom/service/sbom.rs` (using `advisory` constant) |
| Output | `SbomDetails` response includes `remediations: Vec<RemediationItem>` | `sbom/endpoints/get.rs` |

All stages are connected. The data flows from the database through the
service layer to the API response without gaps.

## Acceptance Criteria Mapping

| Criterion | How satisfied |
|---|---|
| GET /api/v2/sbom/{id} includes `remediations` field | `SbomDetails` struct updated; handler populates it |
| Sorted Critical > High > Medium > Low > None | `sort_by` using `SEVERITY_ORDER` position |
| Uses existing `SEVERITY_ORDER` -- no duplicate | Imported from `crate::advisory::service::advisory` |
| `RemediationItem` has advisory_id, severity, title, fix_version | Struct definition includes all four fields |

## Scope Containment Notes

- If `advisory.rs` needs a visibility change for `SEVERITY_ORDER`, this is an
  out-of-scope modification (not in "Files to Modify") and requires user
  approval per Step 9.
- If `SbomDetails` is defined in `sbom/model/details.rs` rather than in
  `get.rs`, that file may also need modification and would similarly need
  approval as out-of-scope.
- The test file `tests/api/sbom_remediation.rs` is a new file listed in
  "Files to Create" and is in-scope.
