# Implementation Plan: TC-9210

## Task Summary

Add a severity-sorted remediation list to the SBOM risk report endpoint. The GET
`/api/v2/sbom/{id}` response must include a `remediations` field containing advisories
sorted by severity (Critical > High > Medium > Low > None), using the existing
`SEVERITY_ORDER` constant from the advisory module.

## Target Branch

main

## Files to Modify

### 1. `modules/fundamental/src/advisory/service/advisory.rs`

**Change:** Export the existing `SEVERITY_ORDER` constant.

- Locate the existing declaration:
  ```rust
  const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
  ```
- Change visibility to `pub`:
  ```rust
  pub const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
  ```
- This is the only change to this file. No logic modifications.
- Verify with `find_referencing_symbols` that existing advisory module code still compiles
  (widening from private to pub is always safe).

**Rationale:** The SBOM service needs this constant for sorting. Rather than duplicating it,
we export the canonical definition. See `symbol-search.md` for the full deduplication analysis.

### 2. `modules/fundamental/src/advisory/service/mod.rs`

**Change:** Re-export `SEVERITY_ORDER` so it is accessible via the advisory service's public API.

- Add a `pub use` statement if the module structure requires it:
  ```rust
  pub use advisory::SEVERITY_ORDER;
  ```
- If `advisory.rs` symbols are already re-exported via glob (`pub use advisory::*;`), this
  step is unnecessary -- verify the existing `mod.rs` contents first.

### 3. `modules/fundamental/src/sbom/model/details.rs`

**Change:** Add `RemediationItem` struct and include a `remediations` field in `SbomDetails`.

- Define the new struct:
  ```rust
  /// A single remediation action derived from an advisory affecting this SBOM.
  #[derive(Debug, Clone, Serialize, Deserialize, utoipa::ToSchema)]
  pub struct RemediationItem {
      /// The unique identifier of the source advisory.
      pub advisory_id: String,
      /// The severity level (e.g., "critical", "high", "medium", "low", "none").
      pub severity: String,
      /// The advisory title describing the vulnerability.
      pub title: String,
      /// The version that contains the fix, if available.
      pub fix_version: Option<String>,
  }
  ```
- Add a `remediations` field to the existing `SbomDetails` struct:
  ```rust
  /// Severity-sorted list of remediation actions from related advisories.
  pub remediations: Vec<RemediationItem>,
  ```
- Follow the existing struct patterns in `details.rs` (derive macros, doc comments,
  field ordering, serde attributes).

### 4. `modules/fundamental/src/sbom/service/sbom.rs`

**Change:** Add a method to build the severity-sorted remediation list.

- Import the `SEVERITY_ORDER` constant:
  ```rust
  use crate::advisory::service::advisory::SEVERITY_ORDER;
  ```
- Import `RemediationItem` from the SBOM model.
- Add a new method to `SbomService`:
  ```rust
  /// Builds a severity-sorted list of remediation items from advisories linked to the given SBOM.
  ///
  /// Advisories are sorted by severity using the canonical `SEVERITY_ORDER` constant
  /// (Critical > High > Medium > Low > None). Advisories with the same severity
  /// maintain their original database ordering (stable sort).
  async fn build_remediation_list(
      &self,
      sbom_id: &str,
      db: &DatabaseConnection,
  ) -> Result<Vec<RemediationItem>, AppError> {
      // 1. Fetch advisories linked to this SBOM via the sbom_advisory join table
      // 2. Map each advisory to a RemediationItem
      // 3. Sort by severity using SEVERITY_ORDER position as the sort key
      //    - Use .position() lookup for each severity string
      //    - Unknown severities sort after "none" (defensive handling)
      // 4. Return the sorted list
  }
  ```
- Sorting logic:
  ```rust
  items.sort_by_key(|item| {
      SEVERITY_ORDER
          .iter()
          .position(|&s| s == item.severity.to_lowercase())
          .unwrap_or(SEVERITY_ORDER.len())
  });
  ```
- Use `sort_by_key` (stable sort) to preserve ordering within the same severity level.
- The existing SBOM service pattern for fetching related advisories (via SeaORM join on
  `sbom_advisory` entity) should be followed -- inspect current methods in `sbom.rs` for
  the query pattern.
- Defensive handling: use `unwrap_or_default()` on optional fields from advisory records
  (e.g., `fix_version` may be absent).

### 5. `modules/fundamental/src/sbom/endpoints/get.rs`

**Change:** Include the remediation list in the SBOM details response.

- In the handler for GET `/api/v2/sbom/{id}`:
  - After fetching the SBOM details, call `sbom_service.build_remediation_list(id, &db)` to
    get the sorted remediations.
  - Populate the `remediations` field on the `SbomDetails` response struct.
  - Follow the existing error handling pattern: `Result<T, AppError>` with `.context()`.
- Ensure the `remediations` field appears in the OpenAPI schema via the `utoipa::ToSchema`
  derive on `RemediationItem` and `SbomDetails`.

## Files to Create

### 6. `tests/api/sbom_remediation.rs`

**Change:** Integration tests for the severity-sorted remediation list.

Tests to implement (following existing patterns in `tests/api/sbom.rs`):

```rust
/// Verifies that the remediation list is sorted by severity with Critical first and None last.
#[tokio::test]
async fn test_remediation_list_sorted_by_severity() {
    // Given an SBOM linked to advisories of varying severities
    // When fetching SBOM details via GET /api/v2/sbom/{id}
    // Then the remediations field contains items sorted Critical > High > Medium > Low > None
    // Assert on specific severity values in order, not just count
}

/// Verifies that an SBOM with no linked advisories returns an empty remediation list.
#[tokio::test]
async fn test_sbom_no_advisories_empty_remediation_list() {
    // Given an SBOM with no linked advisories
    // When fetching SBOM details via GET /api/v2/sbom/{id}
    // Then the remediations field is an empty array
    assert!(remediations.is_empty());
}

/// Verifies that advisories with the same severity maintain stable ordering.
#[tokio::test]
async fn test_remediation_same_severity_stable_order() {
    // Given an SBOM linked to multiple advisories with the same severity
    // When fetching SBOM details via GET /api/v2/sbom/{id}
    // Then advisories of the same severity appear in their original database order
    // Assert on specific advisory_id values to verify stability
}
```

- Follow the assertion style from `tests/api/sbom.rs`:
  `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Use value-based assertions (assert on specific severity strings and advisory IDs),
  not just length checks.
- Each test function has a doc comment and given-when-then section comments.
- Register the new test module in `tests/api/mod.rs` if it uses a module structure
  (check existing test organization first).

## SEVERITY_ORDER Handling

**The existing constant is reused -- no new constant is declared.**

| Step | Action |
|---|---|
| Search | Searched `modules/fundamental/` for `SEVERITY_ORDER` and variations |
| Found | `modules/fundamental/src/advisory/service/advisory.rs` -- crate-private const |
| Decision | Export (`pub const`) and import in SBOM service |
| Import path | `use crate::advisory::service::advisory::SEVERITY_ORDER;` |
| Rejected | Declaring a duplicate `SEVERITY_ORDER` in `sbom/service/sbom.rs` |

See `symbol-search.md` for the complete deduplication analysis.

## Data-Flow Trace

1. **Input**: HTTP GET `/api/v2/sbom/{id}` request arrives at `sbom/endpoints/get.rs` handler.
2. **Processing**:
   a. Handler fetches SBOM record from database.
   b. Handler calls `SbomService::build_remediation_list(id, db)`.
   c. `build_remediation_list` queries `sbom_advisory` join table for linked advisories.
   d. Maps advisory records to `RemediationItem` structs.
   e. Sorts items by severity using `SEVERITY_ORDER` position.
3. **Output**: `SbomDetails` response includes populated `remediations: Vec<RemediationItem>`
   field, serialized as JSON.

All stages connect. No incomplete paths.

## Acceptance Criteria Verification

| Criterion | How verified |
|---|---|
| GET `/api/v2/sbom/{id}` includes `remediations` field | Field added to `SbomDetails`, populated in endpoint handler |
| Sorted Critical > High > Medium > Low > None | `sort_by_key` using `SEVERITY_ORDER.position()` |
| Uses existing `SEVERITY_ORDER` -- no duplicate | Import from `crate::advisory::service::advisory::SEVERITY_ORDER` |
| `RemediationItem` has advisory_id, severity, title, fix_version | Struct definition in `sbom/model/details.rs` |

## Out-of-Scope Considerations

- No changes to the advisory module logic (only visibility change on one constant).
- No changes to the SBOM list endpoint (`list.rs`) -- only the detail endpoint (`get.rs`).
- No database migration needed -- using existing `sbom_advisory` join table.
- No changes to `server/main.rs` -- no new routes, only modifying an existing response shape.

## CI Verification Plan

1. Check for `CONVENTIONS.md` at repository root and extract CI commands.
2. Run `cargo check` to verify compilation.
3. Run `cargo fmt --check` to verify formatting.
4. Run `cargo clippy` to verify no new warnings.
5. Run `cargo test -p trustify-fundamental` (or the crate name from `cargo metadata`) to
   verify all tests pass, including the new remediation tests.
6. Run integration test suite in `tests/api/` to confirm endpoint behavior.
