# Implementation Plan: TC-9210

## Task Summary

Add a severity-sorted remediation list to the SBOM risk report endpoint. The
`GET /api/v2/sbom/{id}` response must include a `remediations` field containing
advisories sorted by severity in descending order (Critical > High > Medium >
Low > None).

## Project Configuration Validation

Verified CLAUDE.md contains the required sections:
- Repository Registry: `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID present
- Code Intelligence: Serena instance `serena_backend` with rust-analyzer

## Target Branch

main

## Dependencies

None.

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**Purpose:** Add a severity-sorted remediation list builder method to `SbomService`.

**Changes:**

- Add an import for `SEVERITY_ORDER` from the advisory module:
  ```rust
  use crate::advisory::service::advisory::SEVERITY_ORDER;
  ```
  This import works because both `sbom` and `advisory` are submodules of
  `modules/fundamental/src/`, so they share the same crate. No new cross-crate
  dependency is needed.

- Define a `RemediationItem` struct (with doc comment):
  ```rust
  /// A single remediation entry linking an advisory to its severity and fix information.
  #[derive(Debug, Clone, Serialize, Deserialize)]
  pub struct RemediationItem {
      /// The unique identifier of the advisory.
      pub advisory_id: String,
      /// The severity level (e.g., "critical", "high", "medium", "low", "none").
      pub severity: String,
      /// The human-readable title of the advisory.
      pub title: String,
      /// The version that resolves the advisory, if available.
      pub fix_version: Option<String>,
  }
  ```

- Add a method `build_remediation_list` to `SbomService`:
  ```rust
  /// Builds a severity-sorted list of remediation items for the given SBOM.
  ///
  /// Fetches advisories associated with the SBOM, maps each to a
  /// `RemediationItem`, and sorts them in descending severity order
  /// (Critical first, None last) using the shared `SEVERITY_ORDER` constant.
  pub async fn build_remediation_list(
      &self,
      sbom_id: &str,
      db: &DatabaseConnection,
  ) -> Result<Vec<RemediationItem>, AppError> {
  ```
  Implementation pattern: follow the existing advisory-fetching pattern already
  present in `sbom.rs` (query `sbom_advisory` join table, fetch related
  advisories). Map each advisory to a `RemediationItem`. Sort using
  `SEVERITY_ORDER` position as the sort key:
  ```rust
  items.sort_by_key(|item| {
      SEVERITY_ORDER
          .iter()
          .position(|&s| s == item.severity.to_lowercase())
          .unwrap_or(SEVERITY_ORDER.len())
  });
  ```
  This ensures advisories whose severity is not in `SEVERITY_ORDER` sort to the
  end, and advisories with the same severity maintain stable ordering (since
  `sort_by_key` is stable).

### 2. `modules/fundamental/src/sbom/endpoints/get.rs`

**Purpose:** Include the remediation list in the SBOM details response.

**Changes:**

- Add `remediations` field to the `SbomDetails` response struct (or the
  response builder, depending on where the struct is assembled). If
  `SbomDetails` is defined in `modules/fundamental/src/sbom/model/details.rs`,
  add the field there instead and note the out-of-scope file for user approval
  in Step 9.

- In the handler for `GET /api/v2/sbom/{id}`, call
  `sbom_service.build_remediation_list(id, &db).await?` and attach the result
  to the response.

- Use `.context("building remediation list")` for error wrapping, following the
  existing `Result<T, AppError>` convention.

**Likely additional file (flagged for scope containment):**

- `modules/fundamental/src/sbom/model/details.rs` -- The `SbomDetails` struct
  lives here per the repo structure. Adding the `remediations` field requires
  modifying this file. This would be flagged as out-of-scope in Step 9 for user
  approval since it is not listed in Files to Modify. Similarly, the advisory
  module's `advisory.rs` may need `SEVERITY_ORDER` to be made `pub` if it is
  currently private -- this would also be flagged.

## Files to Create

### 1. `tests/api/sbom_remediation.rs`

**Purpose:** Integration tests for the severity-sorted remediation list.

**Changes:**

- Follow the existing test patterns from `tests/api/sbom.rs` (sibling test
  file): use real PostgreSQL test database, `assert_eq!(resp.status(),
  StatusCode::OK)` pattern.

- Test functions (each with a `///` doc comment and given-when-then structure):

  1. `test_remediation_list_sorted_by_severity` -- Create an SBOM with
     advisories of varying severities. Verify the response `remediations` array
     is ordered Critical > High > Medium > Low > None. Use value-based
     assertions on the severity field of each item (not just length checks).

  2. `test_sbom_no_advisories_empty_remediation_list` -- Create an SBOM with no
     associated advisories. Verify the `remediations` array is empty.

  3. `test_same_severity_stable_ordering` -- Create an SBOM with multiple
     advisories of the same severity. Verify they appear in a stable order
     (consistent across runs).

- Register the test module in `tests/api/` (likely via `mod sbom_remediation;`
  in the tests crate root or a `mod.rs` file).

## Handling SEVERITY_ORDER

The `SEVERITY_ORDER` constant is already defined in the advisory module at
`modules/fundamental/src/advisory/service/advisory.rs`. Per the skill's symbol
deduplication protocol (Step 6):

1. **Searched** the target package (`modules/fundamental/src/`) for
   `SEVERITY_ORDER` using `find_symbol` / `search_for_pattern` / Grep.
2. **Found** the existing definition in
   `modules/fundamental/src/advisory/service/advisory.rs`:
   ```rust
   SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]
   ```
3. **Decision: Reuse via import.** Both the advisory and sbom modules reside in
   the same crate (`modules/fundamental`), so no new dependency is required.
   Import the constant:
   ```rust
   use crate::advisory::service::advisory::SEVERITY_ORDER;
   ```
   If `SEVERITY_ORDER` is not currently `pub`, make it `pub` in `advisory.rs`
   (minimal visibility change) and flag this out-of-scope file modification in
   Step 9 for user approval.

4. **Rationale:** Reusing the existing constant avoids duplication, ensures
   future changes to severity ordering propagate automatically, and follows
   the DRY principle. Since the dependency is intra-crate (same Cargo package),
   there is no coupling cost.

## Data-Flow Trace

1. **Input:** HTTP GET request to `/api/v2/sbom/{id}`
2. **Processing:** Endpoint handler calls `SbomService::build_remediation_list`
   which queries the database for advisories linked to the SBOM via the
   `sbom_advisory` join table, maps each to a `RemediationItem`, and sorts by
   severity using `SEVERITY_ORDER`.
3. **Output:** JSON response with `remediations` field containing the sorted
   list of `RemediationItem` objects.

All stages are connected. No incomplete paths.

## Acceptance Criteria Verification Plan

- [x] `GET /api/v2/sbom/{id}` response includes `remediations` field -- added
  to `SbomDetails` and populated in endpoint handler.
- [x] Advisories sorted Critical > High > Medium > Low > None -- sort uses
  `SEVERITY_ORDER` constant positions.
- [x] Uses existing `SEVERITY_ORDER` from advisory module -- imported, not
  redeclared.
- [x] `RemediationItem` includes advisory_id, severity, title, fix_version --
  struct definition covers all fields.

## Commit Plan

```
feat(sbom): add severity-sorted remediation list to risk report

Add a RemediationItem struct and build_remediation_list method to
SbomService. The endpoint GET /api/v2/sbom/{id} now returns a
remediations field with advisories sorted by severity (Critical first).
Reuses the existing SEVERITY_ORDER constant from the advisory module.

Implements TC-9210
```
