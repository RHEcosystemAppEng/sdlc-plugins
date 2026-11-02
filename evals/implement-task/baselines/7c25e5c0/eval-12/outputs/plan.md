# Implementation Plan: TC-9210 — Severity-Sorted Remediation List

## Step 0 — Project Configuration Validation

Verified CLAUDE.md contains:
- Repository Registry with `trustify-backend` entry and Serena instance `serena_backend`
- Jira Configuration with project key TC, Cloud ID, and custom field IDs
- Code Intelligence section with tool naming convention and rust-analyzer instance

## Step 1 — Task Parsing

- **Repository:** trustify-backend
- **Target Branch:** main
- **Jira Issue:** TC-9210
- **Issue URL:** https://redhat.atlassian.net/browse/TC-9210

### Sections extracted:
- Description: Add severity-sorted remediation list to SBOM risk report endpoint
- Files to Modify: 2 files
- Files to Create: 1 file
- Implementation Notes: reuse SEVERITY_ORDER from advisory module
- Acceptance Criteria: 4 items
- Test Requirements: 3 items
- Dependencies: None

## Step 1.5 — Description Integrity

Would check for `[sdlc-workflow] Description digest:` comment on the Jira issue. No digest comment provided in this simulation — proceed with warning per backward compatibility.

## Step 4 — Code Inspection

### Files to inspect before modifying:

1. **`modules/fundamental/src/advisory/service/advisory.rs`** — inspect to locate the existing `SEVERITY_ORDER` constant definition, understand its visibility (`pub(crate)`), and confirm the value matches the expected severity ordering.

2. **`modules/fundamental/src/sbom/service/sbom.rs`** — inspect to understand the existing SbomService implementation patterns, method signatures, return types, error handling (`Result<T, AppError>` with `.context()`), and how related data (advisories) is currently fetched.

3. **`modules/fundamental/src/sbom/endpoints/get.rs`** — inspect to understand the current SBOM details response structure and how the endpoint handler calls SbomService methods.

4. **`modules/fundamental/src/sbom/model/details.rs`** — inspect to understand the SbomDetails struct and determine where to add the `remediations` field.

5. **`modules/fundamental/src/advisory/model/summary.rs`** — inspect to understand the AdvisorySummary struct and its `severity` field, which will be used in sorting.

### Symbol deduplication search

Before declaring any new `SEVERITY_ORDER` constant, searched the `modules/fundamental` crate using `find_symbol` and `search_for_pattern`. Found the existing definition in `modules/fundamental/src/advisory/service/advisory.rs`. See `symbol-search.md` for full analysis.

**Decision:** Import via `use crate::advisory::service::advisory::SEVERITY_ORDER;` — no duplicate declaration.

### Convention conformance analysis

Discovered conventions from sibling code analysis:
- **Error handling:** `Result<T, AppError>` with `.context()` wrapping throughout service methods
- **Module structure:** model/ + service/ + endpoints/ pattern per domain
- **Service methods:** async methods on service struct, taking `&self` and query parameters
- **Endpoint handlers:** extract path params, call service, map to response type
- **Test patterns:** integration tests in `tests/api/`, using real PostgreSQL test database, `assert_eq!(resp.status(), StatusCode::OK)` validation pattern

## Step 5 — Branch Creation

```bash
git checkout main
git pull
git checkout -b TC-9210
```

## Step 6 — Implementation Changes

### File 1: `modules/fundamental/src/sbom/service/sbom.rs` (MODIFY)

**Changes:**
1. Add import: `use crate::advisory::service::advisory::SEVERITY_ORDER;`
2. Add a new `RemediationItem` struct (or add it in the model layer — see File 3 note):
   ```rust
   /// A single remediation entry linking an advisory to an SBOM, sorted by severity.
   pub struct RemediationItem {
       pub advisory_id: String,
       pub severity: String,
       pub title: String,
       pub fix_version: Option<String>,
   }
   ```
3. Add a new method `get_remediation_list(&self, sbom_id: Id) -> Result<Vec<RemediationItem>, AppError>`:
   - Fetch advisories related to the SBOM (follow existing pattern for fetching related advisories)
   - Map each advisory to a `RemediationItem`
   - Sort using `SEVERITY_ORDER`: for each item, find the index of `item.severity.to_lowercase()` in `SEVERITY_ORDER`, use that as the sort key
   - Return sorted list

**Sorting logic:**
```rust
items.sort_by_key(|item| {
    SEVERITY_ORDER
        .iter()
        .position(|&s| s == item.severity.to_lowercase())
        .unwrap_or(SEVERITY_ORDER.len())
});
```

### File 2: `modules/fundamental/src/sbom/endpoints/get.rs` (MODIFY)

**Changes:**
1. In the SBOM details handler, call `sbom_service.get_remediation_list(id)` after fetching SBOM details
2. Include the remediation list in the response body under a `remediations` field
3. Follow existing error handling pattern: `.context("fetching remediation list")?`

### File 3: `tests/api/sbom_remediation.rs` (CREATE)

**Changes:**
Create integration tests following the existing patterns in `tests/api/sbom.rs`:

```rust
/// Verifies that the remediation list is sorted by severity in descending order.
#[test]
async fn test_remediation_list_sorted_by_severity() {
    // Given an SBOM with advisories of varying severity
    // ... setup with Critical, Low, High, Medium advisories

    // When fetching the SBOM details
    // ... GET /api/v2/sbom/{id}

    // Then the remediations are sorted Critical > High > Medium > Low > None
    assert_eq!(remediations[0].severity, "critical");
    assert_eq!(remediations[1].severity, "high");
    assert_eq!(remediations[2].severity, "medium");
    assert_eq!(remediations[3].severity, "low");
}

/// Verifies that an SBOM with no advisories returns an empty remediation list.
#[test]
async fn test_empty_remediation_list() {
    // Given an SBOM with no linked advisories

    // When fetching the SBOM details

    // Then the remediations field is an empty array
    assert_eq!(remediations.len(), 0);
}

/// Verifies that advisories with the same severity maintain stable ordering.
#[test]
async fn test_same_severity_stable_ordering() {
    // Given an SBOM with multiple High-severity advisories

    // When fetching the SBOM details

    // Then all High-severity items are adjacent and their relative order is stable
    let high_items: Vec<_> = remediations.iter()
        .filter(|r| r.severity == "high")
        .collect();
    assert_eq!(high_items.len(), 2);
    // Verify specific advisory IDs to confirm stable sort
    assert_eq!(high_items[0].advisory_id, expected_first_id);
    assert_eq!(high_items[1].advisory_id, expected_second_id);
}
```

### Module registration

- Add `mod sbom_remediation;` to `tests/api/mod.rs` (if a mod.rs exists) or ensure the test file is picked up by the test harness

## Step 7 — Test Execution

Run module-level tests using `cargo metadata --no-deps --format-version 1` to resolve the crate name for `modules/fundamental` (the package name, e.g., `trustify-module-fundamental`):

```bash
cargo test -p trustify-module-fundamental
```

Also run integration tests:

```bash
cargo test -p trustify-tests  # or whatever the tests/ crate is named
```

Fix any failures before proceeding.

## Step 9 — Self-Verification

### Scope containment
Files modified/created:
- `modules/fundamental/src/sbom/service/sbom.rs` — listed in Files to Modify
- `modules/fundamental/src/sbom/endpoints/get.rs` — listed in Files to Modify
- `tests/api/sbom_remediation.rs` — listed in Files to Create

All files within scope.

### Symbol deduplication check
Confirmed: `SEVERITY_ORDER` is imported from `crate::advisory::service::advisory`, not redeclared. See `symbol-search.md`.

### Dead parameter detection
No parameters removed — not applicable.

### Sensitive-pattern check
No secrets or credentials in the diff.

## Step 10 — Commit and Push

### Commit message:
```
feat(sbom): add severity-sorted remediation list to SBOM risk report

Add a new method to SbomService that fetches advisories related to an
SBOM, maps them to RemediationItem structs, and sorts by severity using
the existing SEVERITY_ORDER constant from the advisory module.

Implements TC-9210
```

```bash
git add modules/fundamental/src/sbom/service/sbom.rs \
       modules/fundamental/src/sbom/endpoints/get.rs \
       tests/api/sbom_remediation.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(sbom): add severity-sorted remediation list to SBOM risk report

Add a new method to SbomService that fetches advisories related to an
SBOM, maps them to RemediationItem structs, and sorts by severity using
the existing SEVERITY_ORDER constant from the advisory module.

Implements TC-9210"
```

### Branch and PR:
```bash
git push -u origin TC-9210
gh pr create --base main --title "feat(sbom): add severity-sorted remediation list" --body "..."
```

PR description would include:
- Implements [TC-9210](https://redhat.atlassian.net/browse/TC-9210)
- Summary of changes
- Note about reusing SEVERITY_ORDER from advisory module (no duplication)
