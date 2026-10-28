# Implementation Plan for TC-9210

## Task Summary

Add a severity-sorted remediation list to the SBOM risk report endpoint. The list
sorts advisories by severity (Critical > High > Medium > Low > None) and returns
them in descending severity order.

## Project Configuration Validation (Step 0)

Verified CLAUDE.md contains:
- Repository Registry: `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID present
- Code Intelligence: Tool naming convention documented, `serena_backend` instance configured

## Task Parsing (Step 1)

- **Repository:** trustify-backend
- **Target Branch:** main
- **Files to Modify:** `modules/fundamental/src/sbom/service/sbom.rs`, `modules/fundamental/src/sbom/endpoints/get.rs`
- **Files to Create:** `tests/api/sbom_remediation.rs`
- **Dependencies:** None
- **Bookend Type:** None
- **Target PR:** None

## Code Understanding (Step 4)

### Symbol Deduplication: SEVERITY_ORDER

Before declaring any new constant, the skill requires searching the target package
for an existing definition (see "Symbol deduplication" in skill Step 6).

**Search performed:** Grepped `modules/fundamental/src/` for `SEVERITY_ORDER`,
`severity_order`, `SeverityOrder`, and `severityOrder`. Also searched `common/src/`.

**Found:** `SEVERITY_ORDER` is already defined as a `pub const` in
`modules/fundamental/src/advisory/service/advisory.rs`:

```rust
pub const SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"];
```

**Decision:** Import and reuse via `use crate::advisory::service::advisory::SEVERITY_ORDER`
in `sbom/service/sbom.rs`. Both modules are in the same crate (`modules/fundamental`),
so no new dependency is needed. Full analysis in `outputs/symbol-search.md`.

### Convention Conformance

Based on repository conventions:
- **Framework:** Axum for HTTP, SeaORM for database
- **Module pattern:** `model/ + service/ + endpoints/`
- **Error handling:** `Result<T, AppError>` with `.context()` wrapping
- **Response types:** List endpoints use `PaginatedResults<T>`
- **Testing:** Integration tests in `tests/api/`, hitting real PostgreSQL

### Documentation Files Identified

- `README.md` (repo root)
- `CONVENTIONS.md` (repo root -- would extract CI check commands)
- `docs/api.md` (API reference -- may need updating for new response field)

## Branch (Step 5)

```
git checkout main
git pull
git checkout -b TC-9210
```

## Files to Modify

### 1. `modules/fundamental/src/sbom/model/details.rs`

**Note:** This file is not listed in Files to Modify, but defining the
`RemediationItem` struct here follows the module's `model/` convention. This would
be flagged as an out-of-scope file in Step 9 and require user approval. Alternatively,
the struct could be defined inline in `sbom.rs` if keeping strict scope.

**Changes:**
- Add `RemediationItem` struct with fields: `advisory_id`, `severity`, `title`, `fix_version`
- Add `remediations: Vec<RemediationItem>` field to `SbomDetails` struct
- Add doc comments on the new struct and field

```rust
/// A single remediation action derived from an advisory affecting this SBOM.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RemediationItem {
    /// The unique identifier of the source advisory.
    pub advisory_id: String,
    /// The severity level (e.g., "critical", "high", "medium", "low", "none").
    pub severity: String,
    /// The advisory title or summary.
    pub title: String,
    /// The version that fixes the vulnerability, if known.
    pub fix_version: Option<String>,
}
```

### 2. `modules/fundamental/src/sbom/service/sbom.rs`

**Changes:**
- Add import: `use crate::advisory::service::advisory::SEVERITY_ORDER;`
- Add import for `RemediationItem` from the model module
- Add a new method `build_remediation_list` to `SbomService` that:
  1. Fetches advisories related to the SBOM (following existing patterns for advisory fetching)
  2. Maps each advisory to a `RemediationItem { advisory_id, severity, title, fix_version }`
  3. Sorts by severity using `SEVERITY_ORDER` -- position in the array determines priority
  4. Returns `Vec<RemediationItem>`

```rust
/// Builds a severity-sorted list of remediation items for the given SBOM.
///
/// Advisories are sorted by severity in descending order: Critical > High >
/// Medium > Low > None. The ordering uses the `SEVERITY_ORDER` constant from
/// the advisory module.
pub async fn build_remediation_list(
    &self,
    sbom_id: &str,
    db: &DatabaseConnection,
) -> Result<Vec<RemediationItem>, AppError> {
    // Fetch related advisories (following existing advisory-fetch pattern)
    let advisories = self.fetch_related_advisories(sbom_id, db)
        .await
        .context("fetching advisories for remediation list")?;

    let mut remediations: Vec<RemediationItem> = advisories
        .into_iter()
        .map(|adv| RemediationItem {
            advisory_id: adv.id.clone(),
            severity: adv.severity.clone().unwrap_or_default(),
            title: adv.title.clone().unwrap_or_default(),
            fix_version: adv.fix_version.clone(),
        })
        .collect();

    // Sort by severity using SEVERITY_ORDER -- lower index = higher priority
    remediations.sort_by_key(|item| {
        let severity_lower = item.severity.to_lowercase();
        SEVERITY_ORDER
            .iter()
            .position(|&s| s == severity_lower)
            .unwrap_or(SEVERITY_ORDER.len())
    });

    Ok(remediations)
}
```

**SEVERITY_ORDER handling:** The constant is imported from
`crate::advisory::service::advisory::SEVERITY_ORDER` -- no duplicate definition.
Position in the array determines sort priority (index 0 = "critical" = highest
priority). Unrecognized severities sort after "none".

### 3. `modules/fundamental/src/sbom/endpoints/get.rs`

**Changes:**
- In the handler for `GET /api/v2/sbom/{id}`, call
  `sbom_service.build_remediation_list(&id, &db).await?` to obtain the sorted list
- Include the `remediations` field in the response by setting it on `SbomDetails`
- Add defensive guard: if no advisories exist, `remediations` is an empty `Vec`

## Files to Create

### 4. `tests/api/sbom_remediation.rs`

**Changes:**
- Create integration tests for the severity-sorted remediation list
- Follow existing test patterns from `tests/api/sbom.rs` (assertion style, setup, DB usage)
- Add doc comments on every test function (skill requirement)
- Use given-when-then structure for non-trivial tests

**Test cases:**

```rust
/// Verifies that the remediation list is sorted by severity, with Critical first and None last.
#[tokio::test]
async fn test_remediation_list_sorted_by_severity() {
    // Given an SBOM with advisories of varying severities
    // (setup: create SBOM, attach advisories with critical, low, high, medium, none severities)

    // When fetching the SBOM details
    // (GET /api/v2/sbom/{id})

    // Then the remediations field contains items sorted Critical > High > Medium > Low > None
    // (assert on actual severity values in order, not just count)
}

/// Verifies that an SBOM with no advisories returns an empty remediation list.
#[tokio::test]
async fn test_sbom_no_advisories_empty_remediation_list() {
    // Given an SBOM with no linked advisories

    // When fetching the SBOM details

    // Then the remediations field is an empty array
}

/// Verifies that multiple advisories of the same severity maintain stable ordering.
#[tokio::test]
async fn test_same_severity_stable_ordering() {
    // Given an SBOM with multiple advisories all at "high" severity

    // When fetching the SBOM details

    // Then all items appear in the remediations list with severity "high"
    // and their relative order is stable (consistent across runs)
}
```

### 5. `tests/api/mod.rs` (if needed)

Register the new test module: `mod sbom_remediation;`
This would be flagged as out-of-scope in Step 9 for user approval.

## Self-Verification Checklist (Step 9)

- **Scope containment:** Flag `sbom/model/details.rs` and `tests/api/mod.rs` as
  potentially out-of-scope for user approval
- **Duplication check:** Confirm no other severity-ordering constant exists (done in
  symbol search)
- **Dead parameter detection:** No parameters removed in this change
- **Sensitive-pattern check:** No secrets or credentials in this change
- **Data-flow trace:** API request -> endpoint handler -> service method ->
  advisory fetch -> map to RemediationItem -> sort by SEVERITY_ORDER -> response
- **CI checks:** Run commands from CONVENTIONS.md; run `cargo test -p fundamental`
- **Contract check:** Ensure `RemediationItem` fields match acceptance criteria
  (advisory_id, severity, title, fix_version)

## Commit Plan (Step 10)

```
feat(sbom): add severity-sorted remediation list to SBOM risk report

Add a remediations field to the SBOM details response that lists
advisories sorted by severity (Critical > High > Medium > Low > None).
Reuses the existing SEVERITY_ORDER constant from the advisory module
to avoid duplication.

Implements TC-9210
```
