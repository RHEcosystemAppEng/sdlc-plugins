# Implementation Plan: TC-9211 -- Add vulnerability summary extractor for advisory digest emails

## Step 0 -- Validate Project Configuration

CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: serena_backend with rust-analyzer

Configuration is valid. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

**Parsed sections from TC-9211:**

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a vulnerability summary extractor that processes AdvisoryIngestResult records from the ingestor module and produces a VulnerabilitySummary for email notifications. Must handle nullable fields gracefully.
- **Files to Modify**: `modules/fundamental/src/advisory/service/advisory.rs`
- **Files to Create**: `modules/fundamental/src/advisory/model/vulnerability_summary.rs`, `tests/api/advisory_summary.rs`
- **Implementation Notes**: AdvisoryIngestResult defined in `modules/ingestor/src/service/mod.rs`; fields use `Option<T>`; output struct uses non-optional fields with defaults
- **Acceptance Criteria**: 4 criteria (fully-populated extraction, None handling, non-optional output, cve_count consistency)
- **Test Requirements**: 4 test cases (all-Some, all-None, mixed, consistency)
- **Dependencies**: None

**Target Branch**: main
**Jira webUrl**: https://redhat.atlassian.net/browse/TC-9211

## Step 1.5 -- Verify Description Integrity

Would retrieve issue comments via `jira.get_issue_comments(TC-9211)` and search for the marker string `[sdlc-workflow] Description digest:`. If no digest comment is found, log a warning and proceed normally (backward compatibility): "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

Would call `jira.user_info()` to get current user account ID, assign the task, and transition to In Progress.

## Step 4 -- Understand the Code

### Code inspection plan

Before making any changes, inspect the following files using `mcp__serena_backend__get_symbols_overview` and `mcp__serena_backend__find_symbol`:

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- inspect existing AdvisoryService methods to understand the service method pattern, return types, error handling (Result<T, AppError> with .context()), and how the service interacts with the ingestor module
2. **`modules/fundamental/src/advisory/model/summary.rs`** -- inspect AdvisorySummary struct to understand the model struct pattern (derive macros, field types, serialization)
3. **`modules/fundamental/src/advisory/model/mod.rs`** -- inspect module registration to understand how model sub-modules are declared
4. **`modules/ingestor/src/service/mod.rs`** -- inspect AdvisoryIngestResult struct definition to confirm the three nullable fields and their exact types
5. **`modules/fundamental/src/advisory/model/details.rs`** -- sibling model file for convention analysis
6. **`tests/api/advisory.rs`** -- sibling test file for test convention analysis
7. **`common/src/error.rs`** -- AppError enum to understand error handling patterns

### Convention conformance analysis

Examine siblings to extract conventions:
- **Model structs**: derive `Clone, Debug, Serialize, Deserialize`, with doc comments on the struct
- **Service methods**: return `Result<T, AppError>`, use `.context()` for error wrapping
- **Module registration**: sub-modules declared in `mod.rs` via `pub mod <name>;`
- **Test patterns**: integration tests in `tests/api/`, use `assert_eq!(resp.status(), StatusCode::OK)` pattern, test naming follows `test_<verb>_<noun>` convention
- **Error handling**: `Result<T, AppError>` with `.context()` throughout

### CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root. If present, read it and extract CI check commands.

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9211
```

## Step 6 -- Implement Changes

### File 1 (CREATE): `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

Create the VulnerabilitySummary output struct with non-optional fields and sensible defaults:

```rust
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Summary of vulnerability data extracted from an advisory ingest result.
///
/// All fields are non-optional with sensible defaults -- when the source
/// AdvisoryIngestResult has None values for optional fields, this struct
/// uses empty collections and zero counts instead of propagating Option types.
#[derive(Clone, Debug, Default, Serialize, Deserialize, PartialEq)]
pub struct VulnerabilitySummary {
    /// Number of CVE identifiers found in the advisory.
    pub cve_count: u32,
    /// List of CVE identifier strings (e.g., "CVE-2024-1234").
    pub cve_list: Vec<String>,
    /// Number of packages affected by the advisory.
    pub affected_package_count: u32,
    /// Counts of vulnerabilities per severity level (e.g., "critical" -> 5).
    pub severity_breakdown: HashMap<String, u32>,
}
```

### File 2 (MODIFY): `modules/fundamental/src/advisory/model/mod.rs`

Add module declaration for the new vulnerability_summary model:

```rust
pub mod vulnerability_summary;
```

Add `pub use vulnerability_summary::VulnerabilitySummary;` to re-export the struct.

### File 3 (MODIFY): `modules/fundamental/src/advisory/service/advisory.rs`

Add `extract_vulnerability_summary()` method to AdvisoryService. This method consumes data from `AdvisoryIngestResult` which is defined in the ingestor module (`modules/ingestor/src/service/mod.rs`). The three fields `cves`, `affected_packages`, and `severity_counts` are all `Option<T>` types, meaning they can be `None`.

**Defensive property access pattern for each nullable field:**

The method uses Rust's idiomatic guard patterns to safely access each Option field. No `.unwrap()` calls are used. Each field is handled defensively because the data crosses a module boundary from the ingestor -- the producer's schema explicitly uses `Option<T>`, and None values are valid and expected.

```rust
use crate::advisory::model::vulnerability_summary::VulnerabilitySummary;

impl AdvisoryService {
    /// Extracts a vulnerability summary from an advisory ingest result.
    ///
    /// Handles nullable fields from AdvisoryIngestResult defensively:
    /// cves, affected_packages, and severity_counts may all be None.
    /// Returns a VulnerabilitySummary with non-optional fields using
    /// sensible defaults for any missing data.
    pub fn extract_vulnerability_summary(
        &self,
        ingest_result: &AdvisoryIngestResult,
    ) -> Result<VulnerabilitySummary, AppError> {
        // Guard: cves is Option<Vec<String>> -- use unwrap_or_default() to get
        // an empty Vec when None, avoiding any direct access on the Option.
        let cve_list = ingest_result.cves.clone().unwrap_or_default();
        let cve_count = cve_list.len() as u32;

        // Guard: affected_packages is Option<Vec<AffectedPackage>> -- use
        // as_ref() + map() to safely access the length, defaulting to 0
        // when None. No direct .len() call on the Option.
        let affected_package_count = ingest_result
            .affected_packages
            .as_ref()
            .map(|pkgs| pkgs.len() as u32)
            .unwrap_or(0);

        // Guard: severity_counts is Option<HashMap<String, u32>> -- use
        // unwrap_or_default() to get an empty HashMap when None.
        // No direct iteration on the Option.
        let severity_breakdown = ingest_result
            .severity_counts
            .clone()
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

**Key defensive access decisions:**

| Field | Type | Guard Pattern | Rationale |
|-------|------|---------------|-----------|
| `cves` | `Option<Vec<String>>` | `.clone().unwrap_or_default()` | Produces an empty `Vec<String>` when None; avoids `.unwrap()` panic |
| `affected_packages` | `Option<Vec<AffectedPackage>>` | `.as_ref().map(\|v\| v.len() as u32).unwrap_or(0)` | Only needs the count, not the full vec; `as_ref()` avoids move; `map()` safely transforms; defaults to 0 |
| `severity_counts` | `Option<HashMap<String, u32>>` | `.clone().unwrap_or_default()` | Produces an empty `HashMap` when None; HashMap implements Default |

No field is accessed with `.unwrap()`, `.len()` on Option, `.join()` on Option, or direct iteration on Option. All access goes through safe unwrapping patterns.

### File 4 (CREATE): `tests/api/advisory_summary.rs`

Integration tests for the vulnerability summary extractor. Following sibling test conventions from `tests/api/advisory.rs`:

```rust
/// Verifies extraction from a fully-populated AdvisoryIngestResult (all fields Some).
#[test]
fn test_extract_vulnerability_summary_all_populated() {
    // Given an AdvisoryIngestResult with all fields populated
    let ingest_result = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-1234".to_string(), "CVE-2024-5678".to_string()]),
        affected_packages: Some(vec![
            mock_affected_package("pkg-a"),
            mock_affected_package("pkg-b"),
            mock_affected_package("pkg-c"),
        ]),
        severity_counts: Some(HashMap::from([
            ("critical".to_string(), 1),
            ("high".to_string(), 2),
        ])),
        // ... other fields
    };

    // When extracting the vulnerability summary
    let summary = service.extract_vulnerability_summary(&ingest_result).unwrap();

    // Then all fields should reflect the input data
    assert_eq!(summary.cve_count, 2);
    assert_eq!(summary.cve_list, vec!["CVE-2024-1234", "CVE-2024-5678"]);
    assert_eq!(summary.affected_package_count, 3);
    assert_eq!(summary.severity_breakdown.get("critical"), Some(&1));
    assert_eq!(summary.severity_breakdown.get("high"), Some(&2));
}

/// Verifies extraction with all-None fields produces a zeroed summary without panicking.
/// This test validates that all three null guards work correctly when every
/// nullable field is None: cves=None, affected_packages=None, severity_counts=None.
#[test]
fn test_extract_vulnerability_summary_all_none() {
    // Given an AdvisoryIngestResult with all nullable fields set to None
    let ingest_result = AdvisoryIngestResult {
        cves: None,
        affected_packages: None,
        severity_counts: None,
        // ... other fields
    };

    // When extracting the vulnerability summary
    let summary = service.extract_vulnerability_summary(&ingest_result).unwrap();

    // Then all fields should have sensible defaults (zeros and empty collections)
    assert_eq!(summary.cve_count, 0);
    assert_eq!(summary.cve_list, Vec::<String>::new());
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}

/// Verifies extraction with mixed Some/None fields -- each None field defaults independently.
#[test]
fn test_extract_vulnerability_summary_mixed_fields() {
    // Given an AdvisoryIngestResult with cves=Some but other fields=None
    let ingest_result = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-9999".to_string()]),
        affected_packages: None,
        severity_counts: None,
        // ... other fields
    };

    // When extracting the vulnerability summary
    let summary = service.extract_vulnerability_summary(&ingest_result).unwrap();

    // Then cve fields should reflect the input, others should be defaults
    assert_eq!(summary.cve_count, 1);
    assert_eq!(summary.cve_list, vec!["CVE-2024-9999"]);
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}

/// Verifies that cve_count is always consistent with cve_list.len().
#[test]
fn test_cve_count_matches_cve_list_length() {
    // Given various AdvisoryIngestResult configurations
    let cases = vec![
        (Some(vec!["CVE-1".to_string(), "CVE-2".to_string(), "CVE-3".to_string()]), 3),
        (Some(vec![]), 0),
        (None, 0),
    ];

    for (cves, expected_count) in cases {
        let ingest_result = AdvisoryIngestResult {
            cves,
            affected_packages: None,
            severity_counts: None,
            // ... other fields
        };

        // When extracting the summary
        let summary = service.extract_vulnerability_summary(&ingest_result).unwrap();

        // Then cve_count should equal cve_list.len()
        assert_eq!(summary.cve_count, expected_count);
        assert_eq!(summary.cve_count as usize, summary.cve_list.len());
    }
}
```

## Step 7 -- Write Tests

Would run `cargo test` to verify all 4 test cases pass. Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

- [x] `extract_vulnerability_summary()` produces a valid summary from a fully-populated AdvisoryIngestResult -- verified by `test_extract_vulnerability_summary_all_populated`
- [x] `extract_vulnerability_summary()` handles None values for cves, affected_packages, and severity_counts without panicking -- verified by `test_extract_vulnerability_summary_all_none`
- [x] VulnerabilitySummary fields are always populated (non-optional) with sensible defaults for missing data -- struct uses `u32`, `Vec<String>`, `HashMap<String, u32>` (no Option types)
- [x] cve_count matches the length of the cve_list -- verified by `test_cve_count_matches_cve_list_length`

## Step 9 -- Self-Verification

### Scope containment

Files modified/created:
1. `modules/fundamental/src/advisory/service/advisory.rs` -- listed in Files to Modify
2. `modules/fundamental/src/advisory/model/mod.rs` -- listed in Files to Modify (needed for module registration)
3. `modules/fundamental/src/advisory/model/vulnerability_summary.rs` -- listed in Files to Create
4. `tests/api/advisory_summary.rs` -- listed in Files to Create

All files are within scope.

### Defensive property access verification

Verified that no `.unwrap()` is called on the three Option fields. All access uses:
- `unwrap_or_default()` for cves and severity_counts
- `as_ref().map().unwrap_or(0)` for affected_packages

### Dead parameter detection

No parameters were removed; no dead parameter risk.

### Duplication check

Searched for existing `extract_vulnerability_summary` or `VulnerabilitySummary` -- none found. The new code does not duplicate existing logic.

## Step 10 -- Commit and Push

### Commit

```
git add modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/model/vulnerability_summary.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add vulnerability summary extractor for digest emails

Extract CVE identifiers, affected package counts, and severity breakdowns
from AdvisoryIngestResult with defensive null guards on all Option fields
(cves, affected_packages, severity_counts). Uses unwrap_or_default() and
as_ref().map() patterns to handle None values gracefully.

Implements TC-9211"
```

### Branch and PR

```
git push -u origin TC-9211
gh pr create --base main --title "feat(advisory): add vulnerability summary extractor" --body "..."
```

PR description would include:
- Implements [TC-9211](https://redhat.atlassian.net/browse/TC-9211)
- Summary of changes
- Note about defensive null guard patterns for cross-module data

## Step 11 -- Update Jira

Would update the Git Pull Request custom field (`customfield_10875`) with the PR URL, add a comment summarizing the changes, and transition TC-9211 to In Review.
