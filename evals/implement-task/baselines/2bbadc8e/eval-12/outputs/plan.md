# Implementation Plan -- TC-9210

**Task**: Add severity-sorted remediation list to SBOM risk report
**Repository**: trustify-backend
**Target Branch**: main
**Branch**: TC-9210

---

## Step 0 -- Validate Project Configuration

Project CLAUDE.md contains all required sections:
- Repository Registry: present (trustify-backend, serena_backend, `./`)
- Jira Configuration: present (Project key: TC, Cloud ID, Feature issue type ID)
- Code Intelligence: present (serena_backend with rust-analyzer)

Validation passed.

## Step 1 -- Parse Task Description

Parsed sections:
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add severity-sorted remediation list to SBOM risk report endpoint
- **Files to Modify**: `modules/fundamental/src/sbom/service/sbom.rs`, `modules/fundamental/src/sbom/endpoints/get.rs`
- **Files to Create**: `tests/api/sbom_remediation.rs`
- **Bookend Type**: none
- **Target PR**: none
- **Dependencies**: none

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress

Would call:
- `jira.user_info()` to get current user account ID
- `jira.edit_issue("TC-9210", assignee=<account-id>)` to assign
- `jira.transition_issue("TC-9210", "In Progress")` to update status

## Step 4 -- Understand the Code

### Code inspection plan

1. **`modules/fundamental/src/sbom/service/sbom.rs`** (SbomService)
   - Use `mcp__serena_backend__get_symbols_overview` to see existing methods
   - Use `mcp__serena_backend__find_symbol(name_path_pattern="SbomService")` to understand the service struct and its impl block
   - Identify existing patterns for fetching related advisories

2. **`modules/fundamental/src/sbom/endpoints/get.rs`** (GET endpoint)
   - Use `mcp__serena_backend__get_symbols_overview` to see handler function signature
   - Understand how SbomDetails is constructed and returned

3. **`modules/fundamental/src/sbom/model/details.rs`** (SbomDetails struct)
   - Use `mcp__serena_backend__find_symbol(name_path_pattern="SbomDetails", include_body=true)` to see current fields
   - This struct needs a new `remediations` field

4. **`modules/fundamental/src/advisory/service/advisory.rs`** (AdvisoryService)
   - Search for `SEVERITY_ORDER` constant (see symbol-search.md for full analysis)
   - Confirm it is `pub` and accessible from the sbom module

5. **Sibling analysis**: Inspect `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/get.rs` for convention conformance

### Convention conformance findings

Based on the repository structure and conventions:
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Naming: `verb_noun` pattern for service methods (e.g., `fetch_sbom`, `list_sboms`)
- Endpoint pattern: handler functions receive extractor parameters, call service methods, return JSON
- Module structure: `model/ + service/ + endpoints/`
- Test pattern: `assert_eq!(resp.status(), StatusCode::OK)` style assertions

### Documentation files identified

- `docs/api.md` -- REST API reference (may need update for new `remediations` field)
- `docs/architecture.md` -- system architecture overview

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9210
```

## Step 6 -- Implement Changes

### Symbol Deduplication: SEVERITY_ORDER

Before declaring `SEVERITY_ORDER` in the sbom service, searched the target package (`modules/fundamental/src`) for existing definitions. Found `pub const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]` in `modules/fundamental/src/advisory/service/advisory.rs`. Both modules are in the same `fundamental` crate, so no new dependency is required. Will import via `use crate::advisory::service::advisory::SEVERITY_ORDER;` instead of redeclaring. See `symbol-search.md` for full analysis.

### File 1: `modules/fundamental/src/sbom/model/details.rs` (modify -- out-of-scope, flagged)

**Note**: This file is not listed in Files to Modify but needs a new struct and a new field on `SbomDetails`. This will be flagged in the Step 9 scope containment check for user approval.

Planned changes:
- Define the `RemediationItem` struct:
  ```rust
  /// A single remediation entry associating an advisory with its severity and fix version.
  #[derive(Clone, Debug, Serialize, Deserialize, utoipa::ToSchema)]
  pub struct RemediationItem {
      /// The advisory identifier.
      pub advisory_id: String,
      /// Severity level (e.g., "critical", "high", "medium", "low", "none").
      pub severity: String,
      /// Advisory title or summary.
      pub title: String,
      /// The version that fixes the vulnerability, if available.
      pub fix_version: Option<String>,
  }
  ```
- Add `pub remediations: Vec<RemediationItem>` field to `SbomDetails`

### File 2: `modules/fundamental/src/sbom/service/sbom.rs` (modify)

Planned changes:
- Add import for the existing constant:
  ```rust
  use crate::advisory::service::advisory::SEVERITY_ORDER;
  ```
- Add import for the new model type:
  ```rust
  use crate::sbom::model::details::RemediationItem;
  ```
- Add a new method to `SbomService`:
  ```rust
  /// Builds a severity-sorted list of remediation items for the given SBOM.
  ///
  /// Fetches advisories associated with the SBOM and sorts them by severity
  /// in descending order (Critical > High > Medium > Low > None) using the
  /// `SEVERITY_ORDER` constant from the advisory module.
  pub async fn get_remediations(
      &self,
      sbom_id: &str,
      db: &DatabaseConnection,
  ) -> Result<Vec<RemediationItem>, AppError> {
      // Fetch advisories associated with this SBOM
      let advisories = self.fetch_related_advisories(sbom_id, db)
          .await
          .context("fetching advisories for remediation list")?;

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

      // Sort by severity using SEVERITY_ORDER (imported from advisory module)
      remediations.sort_by_key(|item| {
          SEVERITY_ORDER
              .iter()
              .position(|&s| s == item.severity.to_lowercase())
              .unwrap_or(SEVERITY_ORDER.len())
      });

      Ok(remediations)
  }
  ```

### File 3: `modules/fundamental/src/sbom/endpoints/get.rs` (modify)

Planned changes:
- In the handler for `GET /api/v2/sbom/{id}`, after fetching the SBOM details, call the new `get_remediations` method:
  ```rust
  let remediations = sbom_service
      .get_remediations(&id, &db)
      .await
      .context("building remediation list")?;
  ```
- Set the `remediations` field on the `SbomDetails` response struct before returning.

### File 4: `tests/api/sbom_remediation.rs` (create)

See Step 7 below for test details.

### Documentation impact

The `docs/api.md` file may need updating to document the new `remediations` field on the `GET /api/v2/sbom/{id}` response. This would be evaluated during Step 9.

## Step 7 -- Write Tests

Create `tests/api/sbom_remediation.rs` with the following test cases:

```rust
/// Verifies that the remediation list is sorted by severity in descending order
/// (Critical first, None last).
#[tokio::test]
async fn test_remediation_list_sorted_by_severity() {
    // Given an SBOM with advisories at different severity levels
    // (setup: create test SBOM, attach advisories with severities
    //  "low", "critical", "medium", "high", "none" in random order)

    // When requesting SBOM details via GET /api/v2/sbom/{id}

    // Then the remediations list should be ordered:
    // critical, high, medium, low, none
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SbomDetails = resp.json().await;
    let severities: Vec<&str> = body.remediations.iter()
        .map(|r| r.severity.as_str())
        .collect();
    assert_eq!(severities, vec!["critical", "high", "medium", "low", "none"]);
}

/// Verifies that an SBOM with no associated advisories returns an empty remediation list.
#[tokio::test]
async fn test_empty_sbom_returns_empty_remediations() {
    // Given an SBOM with no advisories

    // When requesting SBOM details via GET /api/v2/sbom/{id}

    // Then the remediations field should be an empty list
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SbomDetails = resp.json().await;
    assert!(body.remediations.is_empty());
}

/// Verifies that multiple advisories with the same severity maintain stable ordering
/// (do not shuffle between requests).
#[tokio::test]
async fn test_same_severity_stable_ordering() {
    // Given an SBOM with three advisories all at "high" severity

    // When requesting SBOM details via GET /api/v2/sbom/{id}

    // Then all three should appear with severity "high" and their relative order
    // should be deterministic
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SbomDetails = resp.json().await;
    assert_eq!(body.remediations.len(), 3);
    assert!(body.remediations.iter().all(|r| r.severity == "high"));
    // Verify each item has expected fields populated
    for item in &body.remediations {
        assert!(!item.advisory_id.is_empty());
        assert!(!item.title.is_empty());
    }
}
```

All test functions include doc comments explaining what they verify and use given-when-then section comments for structure.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Satisfied By |
|---|-----------|-------------|
| AC-1 | GET /api/v2/sbom/{id} response includes `remediations` field | `SbomDetails` struct updated with `remediations: Vec<RemediationItem>`, endpoint handler populates it |
| AC-2 | Advisories sorted Critical > High > Medium > Low > None | `get_remediations` sorts using `SEVERITY_ORDER` position as sort key |
| AC-3 | Uses existing `SEVERITY_ORDER` from advisory module -- no duplicate | Imported via `use crate::advisory::service::advisory::SEVERITY_ORDER;` (see symbol-search.md) |
| AC-4 | RemediationItem includes advisory_id, severity, title, fix_version | Struct defined with all four fields |

## Step 9 -- Self-Verification (planned checks)

### Scope containment
- `modules/fundamental/src/sbom/service/sbom.rs` -- in scope (Files to Modify)
- `modules/fundamental/src/sbom/endpoints/get.rs` -- in scope (Files to Modify)
- `tests/api/sbom_remediation.rs` -- in scope (Files to Create)
- `modules/fundamental/src/sbom/model/details.rs` -- **out of scope** (not in Files to Modify). Would flag to user: "Modified to add `RemediationItem` struct and `remediations` field to `SbomDetails`. This file must be changed to add the new response type; approve?"

### Symbol deduplication check
- Confirmed `SEVERITY_ORDER` is imported from `crate::advisory::service::advisory`, not redeclared. No duplicate definitions.

### Dead parameter detection
- No parameters removed from existing functions.

### Sensitive-pattern check
- No secrets, credentials, or `.env` references in changes.

### CI checks
- Would run commands from `CONVENTIONS.md` (formatting, linting, clippy, cargo check)
- Would run `cargo test -p fundamental` for module-level tests
- Would run `cargo test -p tests` for integration tests

### Data-flow trace
- Input: GET /api/v2/sbom/{id} request with SBOM ID
- Processing: SbomService.get_remediations fetches advisories, maps to RemediationItem, sorts by SEVERITY_ORDER position
- Output: SbomDetails response with populated `remediations` Vec
- All stages connected.

## Step 10 -- Commit and Push

```
git add modules/fundamental/src/sbom/service/sbom.rs \
       modules/fundamental/src/sbom/endpoints/get.rs \
       modules/fundamental/src/sbom/model/details.rs \
       tests/api/sbom_remediation.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(sbom): add severity-sorted remediation list to SBOM details

Add RemediationItem struct and get_remediations method to SbomService.
The remediation list sorts advisories by severity (Critical > High >
Medium > Low > None) using the existing SEVERITY_ORDER constant from
the advisory module -- imported rather than redeclared to avoid
duplication.

Implements TC-9210"
```

Then push and create PR:
```
git push -u origin TC-9210
gh pr create --base main --title "feat(sbom): add severity-sorted remediation list" --body "..."
```

## Step 11 -- Update Jira

Would call:
- `jira.update_issue("TC-9210", fields={"customfield_10875": <ADF with PR URL>})`
- `jira.add_comment("TC-9210", <summary of changes and PR link>)`
- `jira.transition_issue("TC-9210", "In Review")`
