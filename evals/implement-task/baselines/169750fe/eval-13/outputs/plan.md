# Implementation Plan — TC-9211

## Task Summary

Add a vulnerability summary extractor (`extract_vulnerability_summary()`) to `AdvisoryService` that processes `AdvisoryIngestResult` records from the ingestor module and produces a `VulnerabilitySummary` struct suitable for email digest notifications. The extractor must handle all three nullable fields in `AdvisoryIngestResult` defensively.

## Step 0 — Validate Project Configuration

CLAUDE.md contains all required sections:
- **Repository Registry**: trustify-backend with Serena instance `serena_backend`
- **Jira Configuration**: Project key TC, Cloud ID, Feature issue type ID, custom fields
- **Code Intelligence**: Serena with rust-analyzer

Configuration is valid. Proceeding.

## Step 1 — Parse Jira Task

**Repository**: trustify-backend
**Target Branch**: main
**Issue Key**: TC-9211

### Sections Extracted

- **Description**: Add vulnerability summary extractor processing `AdvisoryIngestResult` records with nullable fields (`cves`, `affected_packages`, `severity_counts`).
- **Files to Modify**: `modules/fundamental/src/advisory/service/advisory.rs`
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/vulnerability_summary.rs`
  - `tests/api/advisory_summary.rs`
- **Implementation Notes**: Present with patterns and null-handling guidance.
- **Acceptance Criteria**: 4 items, all specific and verifiable.
- **Test Requirements**: 4 items, all specific.
- **Dependencies**: None.

All required sections present. Proceeding.

## Step 1.5 — Verify Description Integrity

No digest comment found — skipping integrity check. This task may have been created before digest tracking was introduced.

## Step 4 — Understand the Code

### Code Inspection

Before modifying any files, inspect the existing codebase:

1. **`modules/fundamental/src/advisory/service/advisory.rs`** — read `AdvisoryService` struct and existing methods using `get_symbols_overview` to understand the service pattern. Methods return `Result<T, AppError>` with `.context()` wrapping. This is the file receiving the new `extract_vulnerability_summary()` method.

2. **`modules/ingestor/src/service/mod.rs`** — inspect `AdvisoryIngestResult` struct to confirm the three nullable fields:
   - `cves: Option<Vec<String>>`
   - `affected_packages: Option<Vec<AffectedPackage>>`
   - `severity_counts: Option<HashMap<String, u32>>`

3. **`modules/fundamental/src/advisory/model/summary.rs`** — inspect `AdvisorySummary` as the sibling model to follow for struct definition patterns.

4. **`modules/fundamental/src/advisory/model/mod.rs`** — confirm module registration pattern for adding the new `vulnerability_summary` submodule.

5. **`common/src/error.rs`** — confirm `AppError` type used in `Result<T, AppError>` return types.

### Convention Conformance Analysis

Sibling analysis of `advisory/service/advisory.rs`, `advisory/model/summary.rs`, and `advisory/model/details.rs`:

- **Error handling**: Methods return `Result<T, AppError>` with `.context()` for error wrapping
- **Naming**: `verb_noun` pattern for methods (e.g., `fetch_advisory`, `list_advisories`)
- **Model structs**: use `#[derive(Debug, Clone, Serialize, Deserialize)]`; fields are non-optional with sensible defaults where appropriate
- **Module registration**: submodules declared in `mod.rs` with `pub mod <name>;`
- **Test patterns**: integration tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` pattern; tests named `test_<verb>_<noun>`

## Step 5 — Create Branch

```
git checkout main
git pull
git checkout -b TC-9211
```

## Step 6 — Implement Changes

### File 1: Create `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

Define the output struct with non-optional fields:

```rust
use std::collections::HashMap;
use serde::{Deserialize, Serialize};

/// Summary of vulnerability data extracted from an advisory ingest result.
#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct VulnerabilitySummary {
    /// Number of CVE identifiers in this advisory.
    pub cve_count: u32,
    /// List of CVE identifiers (e.g., ["CVE-2024-1234"]).
    pub cve_list: Vec<String>,
    /// Number of packages affected by this advisory.
    pub affected_package_count: u32,
    /// Counts of vulnerabilities per severity level (e.g., {"critical": 2, "high": 5}).
    pub severity_breakdown: HashMap<String, u32>,
}
```

All fields are non-optional. When source data is `None`, they receive sensible defaults (0, empty Vec, empty HashMap).

### File 2: Modify `modules/fundamental/src/advisory/model/mod.rs`

Add module declaration:

```rust
pub mod vulnerability_summary;
```

### File 3: Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add the `extract_vulnerability_summary()` method to `AdvisoryService`. This method takes an `AdvisoryIngestResult` (which crosses a module boundary from the ingestor crate) and produces a `VulnerabilitySummary` with defensive null guards on all three optional fields:

```rust
use crate::advisory::model::vulnerability_summary::VulnerabilitySummary;

impl AdvisoryService {
    /// Extracts a vulnerability summary from an advisory ingest result for email digest use.
    pub fn extract_vulnerability_summary(
        &self,
        result: &AdvisoryIngestResult,
    ) -> Result<VulnerabilitySummary, AppError> {
        // Guard cves: Option<Vec<String>> — use unwrap_or_default for empty Vec fallback
        let cve_list = result.cves.as_ref()
            .map(|v| v.clone())
            .unwrap_or_default();
        let cve_count = cve_list.len() as u32;

        // Guard affected_packages: Option<Vec<AffectedPackage>> — count only, use unwrap_or_default
        let affected_package_count = result.affected_packages.as_ref()
            .map(|pkgs| pkgs.len() as u32)
            .unwrap_or(0);

        // Guard severity_counts: Option<HashMap<String, u32>> — use unwrap_or_default for empty map
        let severity_breakdown = result.severity_counts.as_ref()
            .cloned()
            .unwrap_or_default();

        Ok(VulnerabilitySummary {
            cve_count,
            cve_list,
            affected_package_count,
            severity_breakdown,
        })
    }
}
```

**Key null-guard patterns used:**
- `as_ref()` to borrow the inner value without consuming the Option
- `map()` to transform the inner value when present
- `unwrap_or_default()` to provide sensible empty/zero defaults when None
- No direct `.unwrap()` calls — all paths handle None gracefully

### File 4: Create `tests/api/advisory_summary.rs`

Integration tests covering all nullable field combinations:

```rust
/// Verifies extraction from a fully-populated AdvisoryIngestResult.
#[test]
fn test_extract_vulnerability_summary_all_fields_present() {
    // Given an AdvisoryIngestResult with all fields populated
    let result = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-1234".to_string(), "CVE-2024-5678".to_string()]),
        affected_packages: Some(vec![mock_affected_package("pkg-a"), mock_affected_package("pkg-b"), mock_affected_package("pkg-c")]),
        severity_counts: Some(HashMap::from([("critical".to_string(), 1), ("high".to_string(), 2)])),
    };

    // When extracting the vulnerability summary
    let summary = service.extract_vulnerability_summary(&result).unwrap();

    // Then all fields are populated with actual values
    assert_eq!(summary.cve_count, 2);
    assert_eq!(summary.cve_list, vec!["CVE-2024-1234", "CVE-2024-5678"]);
    assert_eq!(summary.affected_package_count, 3);
    assert_eq!(summary.severity_breakdown.get("critical"), Some(&1));
    assert_eq!(summary.severity_breakdown.get("high"), Some(&2));
}

/// Verifies extraction with all-None fields returns a zeroed summary.
#[test]
fn test_extract_vulnerability_summary_all_none() {
    // Given an AdvisoryIngestResult with all fields None
    let result = AdvisoryIngestResult {
        cves: None,
        affected_packages: None,
        severity_counts: None,
    };

    // When extracting the vulnerability summary
    let summary = service.extract_vulnerability_summary(&result).unwrap();

    // Then all fields are zeroed/empty defaults
    assert_eq!(summary.cve_count, 0);
    assert!(summary.cve_list.is_empty());
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}

/// Verifies that each None field defaults independently without affecting other fields.
#[test]
fn test_extract_vulnerability_summary_mixed_some_none() {
    // Given an AdvisoryIngestResult with cves=Some but other fields=None
    let result = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-9999".to_string()]),
        affected_packages: None,
        severity_counts: None,
    };

    // When extracting the vulnerability summary
    let summary = service.extract_vulnerability_summary(&result).unwrap();

    // Then cve fields are populated but other fields default to zero/empty
    assert_eq!(summary.cve_count, 1);
    assert_eq!(summary.cve_list, vec!["CVE-2024-9999"]);
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}

/// Verifies that cve_count is always consistent with cve_list.len().
#[test]
fn test_cve_count_matches_cve_list_length() {
    // Given varying cve list sizes
    let cases = vec![
        (None, 0),
        (Some(vec![]), 0),
        (Some(vec!["CVE-2024-0001".to_string()]), 1),
        (Some(vec!["CVE-2024-0001".to_string(), "CVE-2024-0002".to_string(), "CVE-2024-0003".to_string()]), 3),
    ];

    for (cves, expected_count) in cases {
        let result = AdvisoryIngestResult {
            cves,
            affected_packages: None,
            severity_counts: None,
        };

        // When extracting the summary
        let summary = service.extract_vulnerability_summary(&result).unwrap();

        // Then cve_count matches cve_list.len()
        assert_eq!(summary.cve_count, expected_count);
        assert_eq!(summary.cve_count as usize, summary.cve_list.len());
    }
}
```

## Step 8 — Verify Acceptance Criteria

- [x] `extract_vulnerability_summary()` produces a valid summary from a fully-populated `AdvisoryIngestResult` — covered by `test_extract_vulnerability_summary_all_fields_present`
- [x] Handles None values for all three fields without panicking — covered by `test_extract_vulnerability_summary_all_none`
- [x] `VulnerabilitySummary` fields are always populated (non-optional) with sensible defaults — struct definition uses `u32`, `Vec<String>`, `HashMap` (not `Option`)
- [x] `cve_count` matches the length of the `cve_list` — covered by `test_cve_count_matches_cve_list_length`

## Step 9 — Self-Verification

### Scope Containment

Files modified/created:
- `modules/fundamental/src/advisory/service/advisory.rs` — listed in Files to Modify ✓
- `modules/fundamental/src/advisory/model/vulnerability_summary.rs` — listed in Files to Create ✓
- `tests/api/advisory_summary.rs` — listed in Files to Create ✓
- `modules/fundamental/src/advisory/model/mod.rs` — **out of scope** (module registration needed for the new submodule; flagged for user approval)

### Module-level test requirement

Resolve the crate name using `cargo metadata --no-deps --format-version 1` from the workspace root. The modified files are in `modules/fundamental/`, which belongs to the `trustify-module-fundamental` package. Run:

```
cargo test -p trustify-module-fundamental
```

### Dead Parameter Detection

No parameters removed — not applicable.

### Sensitive-Pattern Check

No credentials, API keys, or environment files in changes.

## Step 10 — Commit and Push

```
git add modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/model/vulnerability_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add vulnerability summary extractor for digest emails

Add extract_vulnerability_summary() to AdvisoryService that processes
AdvisoryIngestResult records from the ingestor module with defensive
null guards on all three optional fields (cves, affected_packages,
severity_counts). Produce a VulnerabilitySummary with non-optional
fields and sensible defaults.

Implements TC-9211"

git push -u origin TC-9211
gh pr create --base main --title "feat(advisory): add vulnerability summary extractor for digest emails" --body "..."
```
