# Implementation Plan: TC-9211

## Task Summary

Add a vulnerability summary extractor (`extract_vulnerability_summary()`) to `AdvisoryService` that processes `AdvisoryIngestResult` records with nullable fields and produces a non-optional `VulnerabilitySummary` struct suitable for email digest notifications.

## Step 0 -- Validate Project Configuration

Project CLAUDE.md contains all required sections:
- **Repository Registry**: `trustify-backend` with Serena instance `serena_backend` at path `./`
- **Jira Configuration**: Project key `TC`, Cloud ID, Feature issue type ID `10142`, custom fields configured
- **Code Intelligence**: `mcp__serena_backend__<tool>` convention with rust-analyzer

Validation passes. Proceed.

## Step 1 -- Parse Task Description

- **Repository**: trustify-backend
- **Target Branch**: main
- **Bookend Type**: none
- **Target PR**: none
- **Dependencies**: none
- **GitHub Issue custom field**: customfield_10747 (not populated on this task)

### Parsed Sections

| Section | Content |
|---|---|
| Files to Modify | `modules/fundamental/src/advisory/service/advisory.rs` |
| Files to Create | `modules/fundamental/src/advisory/model/vulnerability_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | None |
| Implementation Notes | AdvisoryIngestResult defined in `modules/ingestor/src/service/mod.rs`; service methods return `Result<T, AppError>`; output struct has non-optional fields with defaults |
| Acceptance Criteria | 4 items (fully-populated, None handling, non-optional output fields, cve_count consistency) |
| Test Requirements | 4 test cases (all-Some, all-None, mixed, count consistency) |

## Step 4 -- Understand the Code

### Files to inspect (via Serena or Read/Grep fallback)

1. **`modules/ingestor/src/service/mod.rs`** -- Read `AdvisoryIngestResult` struct definition; confirm `cves`, `affected_packages`, `severity_counts` are all `Option<T>`. Also inspect `AffectedPackage` struct for its field types.
2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Examine existing `AdvisoryService` methods to understand the pattern (return types, error handling, use of `Result<T, AppError>` with `.context()`).
3. **`modules/fundamental/src/advisory/model/mod.rs`** -- Understand how sibling model modules are registered (likely `pub mod summary;` and `pub mod details;`).
4. **`modules/fundamental/src/advisory/model/summary.rs`** -- Sibling model file; examine struct patterns (derive macros, field documentation, serde attributes).
5. **`modules/fundamental/src/advisory/model/details.rs`** -- Another sibling model file for convention confirmation.
6. **`common/src/error.rs`** -- Confirm `AppError` type and how `.context()` is used.
7. **`tests/api/advisory.rs`** -- Sibling test file; examine test patterns (setup, assertions, naming).

### Convention conformance analysis

Expected conventions from sibling inspection:
- **Naming**: `snake_case` for functions/methods, `PascalCase` for types
- **Error handling**: `Result<T, AppError>` with `anyhow::Context` for `.context()` wrapping
- **Derive macros on models**: `#[derive(Debug, Clone, Serialize, Deserialize)]` expected on output structs
- **Test assertions**: `assert_eq!` with explicit expected values, not `.any()` or length-only
- **Module registration**: `pub mod <module_name>;` in parent `mod.rs`

### Documentation files identified

- `README.md` at repository root
- `CONVENTIONS.md` at repository root (check for CI commands)
- `docs/architecture.md`, `docs/api.md`

### CONVENTIONS.md

Would read this file and extract any CI check commands (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`) for use in Step 9.

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9211
```

No Target PR or Bookend Type -- standard branching flow.

## Step 6 -- Implement Changes

### File 1: Create `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

**Purpose**: Define the `VulnerabilitySummary` output struct with non-optional fields.

```rust
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use utoipa::ToSchema;

/// Summary of vulnerability data extracted from an advisory ingest result.
///
/// All fields are non-optional with sensible defaults, ensuring safe consumption
/// downstream even when the source `AdvisoryIngestResult` has `None` fields.
#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct VulnerabilitySummary {
    /// Number of CVE identifiers found in the advisory.
    pub cve_count: u32,
    /// List of CVE identifier strings (e.g., "CVE-2024-1234").
    pub cve_list: Vec<String>,
    /// Number of packages affected by the advisory.
    pub affected_package_count: u32,
    /// Counts of vulnerabilities grouped by severity level (e.g., "critical" -> 5).
    pub severity_breakdown: HashMap<String, u32>,
}

impl Default for VulnerabilitySummary {
    fn default() -> Self {
        Self {
            cve_count: 0,
            cve_list: Vec::new(),
            affected_package_count: 0,
            severity_breakdown: HashMap::new(),
        }
    }
}
```

**Design decisions**:
- `Default` trait implemented explicitly rather than `#[derive(Default)]` for clarity, though both produce the same result for these types. Either is acceptable; derive would also work here.
- All fields are non-optional to insulate downstream consumers from upstream nullability.
- `ToSchema` derived for potential OpenAPI inclusion (following sibling model patterns).

### File 2: Modify `modules/fundamental/src/advisory/service/advisory.rs`

**Purpose**: Add `extract_vulnerability_summary()` method to `AdvisoryService`.

**Change**: Add a new method to the existing `impl AdvisoryService` block:

```rust
use crate::advisory::model::vulnerability_summary::VulnerabilitySummary;

impl AdvisoryService {
    // ... existing methods ...

    /// Extracts a vulnerability summary from an advisory ingest result.
    ///
    /// Handles nullable fields in `AdvisoryIngestResult` defensively:
    /// `None` values produce zero counts and empty collections rather than panics.
    pub fn extract_vulnerability_summary(
        result: &AdvisoryIngestResult,
    ) -> VulnerabilitySummary {
        // Defensively access cves: Option<Vec<String>>
        let cve_list = result.cves.clone().unwrap_or_default();
        let cve_count = cve_list.len() as u32;

        // Defensively access affected_packages: Option<Vec<AffectedPackage>>
        let affected_package_count = result
            .affected_packages
            .as_ref()
            .map(|pkgs| pkgs.len() as u32)
            .unwrap_or(0);

        // Defensively access severity_counts: Option<HashMap<String, u32>>
        let severity_breakdown = result
            .severity_counts
            .clone()
            .unwrap_or_default();

        VulnerabilitySummary {
            cve_count,
            cve_list,
            affected_package_count,
            severity_breakdown,
        }
    }
}
```

**Key patterns**:
- Method is a pure function (no `&self` needed unless DB access is required; if service convention requires `&self`, add it for consistency).
- Uses `unwrap_or_default()` for `Vec` and `HashMap` (both implement `Default`).
- Uses `as_ref().map().unwrap_or()` for `affected_packages` to avoid cloning when only the count is needed.
- `cve_count` is derived from the resolved `cve_list.len()`, guaranteeing consistency (AC #4).

### File 2 (continued): Module registration

**Modify `modules/fundamental/src/advisory/model/mod.rs`**:

Add module declaration:
```rust
pub mod vulnerability_summary;
```

This ensures the new model struct is accessible as `crate::advisory::model::vulnerability_summary::VulnerabilitySummary`.

### File 3: Create `tests/api/advisory_summary.rs`

**Purpose**: Integration tests for the extractor covering all four test requirements.

```rust
use std::collections::HashMap;
use trustify_module_fundamental::advisory::model::vulnerability_summary::VulnerabilitySummary;
// Import AdvisoryIngestResult and AffectedPackage from ingestor module
use trustify_module_ingestor::service::AdvisoryIngestResult;
use trustify_module_ingestor::service::AffectedPackage;

/// Verifies that a fully-populated AdvisoryIngestResult produces a complete summary.
#[test]
fn test_extract_summary_all_fields_populated() {
    // Given an AdvisoryIngestResult with all fields populated
    let mut severity = HashMap::new();
    severity.insert("critical".to_string(), 2);
    severity.insert("high".to_string(), 5);

    let result = AdvisoryIngestResult {
        cves: Some(vec![
            "CVE-2024-0001".to_string(),
            "CVE-2024-0002".to_string(),
        ]),
        affected_packages: Some(vec![
            make_test_package("pkg-a"),
            make_test_package("pkg-b"),
            make_test_package("pkg-c"),
        ]),
        severity_counts: Some(severity.clone()),
        // ... other non-nullable fields as required by struct definition
    };

    // When extracting the vulnerability summary
    let summary = AdvisoryService::extract_vulnerability_summary(&result);

    // Then all fields reflect the input data
    assert_eq!(summary.cve_count, 2);
    assert_eq!(summary.cve_list, vec!["CVE-2024-0001", "CVE-2024-0002"]);
    assert_eq!(summary.affected_package_count, 3);
    assert_eq!(summary.severity_breakdown, severity);
}

/// Verifies that an AdvisoryIngestResult with all None fields produces a zeroed summary.
#[test]
fn test_extract_summary_all_none_fields() {
    // Given an AdvisoryIngestResult with all nullable fields set to None
    let result = AdvisoryIngestResult {
        cves: None,
        affected_packages: None,
        severity_counts: None,
        // ... other non-nullable fields as required
    };

    // When extracting the vulnerability summary
    let summary = AdvisoryService::extract_vulnerability_summary(&result);

    // Then all fields default to zero/empty
    assert_eq!(summary.cve_count, 0);
    assert!(summary.cve_list.is_empty());
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}

/// Verifies that each None field defaults independently when other fields are Some.
#[test]
fn test_extract_summary_mixed_some_none() {
    // Given an AdvisoryIngestResult with cves populated but other fields None
    let result = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-9999".to_string()]),
        affected_packages: None,
        severity_counts: None,
        // ... other non-nullable fields as required
    };

    // When extracting the vulnerability summary
    let summary = AdvisoryService::extract_vulnerability_summary(&result);

    // Then cves are extracted while other fields default
    assert_eq!(summary.cve_count, 1);
    assert_eq!(summary.cve_list, vec!["CVE-2024-9999"]);
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}

/// Verifies that cve_count always equals cve_list.len() for consistency.
#[test]
fn test_cve_count_matches_cve_list_length() {
    // Given various AdvisoryIngestResult inputs
    let cases: Vec<Option<Vec<String>>> = vec![
        None,
        Some(vec![]),
        Some(vec!["CVE-2024-0001".to_string()]),
        Some(vec![
            "CVE-2024-0001".to_string(),
            "CVE-2024-0002".to_string(),
            "CVE-2024-0003".to_string(),
        ]),
    ];

    for cves in cases {
        let result = AdvisoryIngestResult {
            cves,
            affected_packages: None,
            severity_counts: None,
        };

        // When extracting the summary
        let summary = AdvisoryService::extract_vulnerability_summary(&result);

        // Then cve_count must equal cve_list.len()
        assert_eq!(
            summary.cve_count as usize,
            summary.cve_list.len(),
            "cve_count ({}) != cve_list.len() ({}) for input",
            summary.cve_count,
            summary.cve_list.len()
        );
    }
}

/// Helper to construct a test AffectedPackage with a given name.
fn make_test_package(name: &str) -> AffectedPackage {
    AffectedPackage {
        name: name.to_string(),
        // ... populate other required fields with test defaults
    }
}
```

**Test registration**: Add `mod advisory_summary;` to `tests/api/mod.rs` (or the test harness entry point) to register the new test module.

## Step 7 -- Write Tests

Tests are defined above in File 3. After writing, run:

```
cargo test -p trustify-module-fundamental
```

or if the tests live in the top-level `tests/` crate:

```
cargo test --test api
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | How verified |
|---|---|---|
| 1 | `extract_vulnerability_summary()` produces valid summary from fully-populated input | `test_extract_summary_all_fields_populated` asserts exact values |
| 2 | Handles None for cves, affected_packages, severity_counts without panicking | `test_extract_summary_all_none_fields` passes without panic |
| 3 | VulnerabilitySummary fields are always populated (non-optional) with defaults | Struct definition uses `u32`, `Vec<String>`, `HashMap` -- no `Option<T>` wrappers |
| 4 | cve_count matches cve_list.len() | `test_cve_count_matches_cve_list_length` parameterized over None, empty, 1, 3 cases |

## Step 9 -- Self-Verification

### Scope containment

Expected modified/created files:
- `modules/fundamental/src/advisory/service/advisory.rs` (modified -- in scope)
- `modules/fundamental/src/advisory/model/vulnerability_summary.rs` (created -- in scope)
- `modules/fundamental/src/advisory/model/mod.rs` (modified -- out of scope, but required for module registration; flag for user approval)
- `tests/api/advisory_summary.rs` (created -- in scope)

**Out-of-scope file**: `modules/fundamental/src/advisory/model/mod.rs` requires adding `pub mod vulnerability_summary;` for the new module to be reachable. This is a necessary structural change to register the new file and would be flagged for user approval.

### CI checks

Run commands from CONVENTIONS.md (expected):
```
cargo fmt --check
cargo clippy -- -D warnings
cargo test -p trustify-module-fundamental
```

### Data-flow trace

Input: `AdvisoryIngestResult` (from ingestor module) -> Processing: `extract_vulnerability_summary()` applies null guards, computes counts -> Output: `VulnerabilitySummary` (non-optional struct for email digest consumption). Complete path.

## Step 10 -- Commit and Push

```
git add modules/fundamental/src/advisory/model/vulnerability_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add vulnerability summary extractor for digest emails

Extract CVE identifiers, affected package counts, and severity breakdowns
from AdvisoryIngestResult with defensive handling of nullable fields.
All Option<T> fields are resolved to non-optional defaults using
unwrap_or_default() and as_ref().map().

Implements TC-9211"

git push -u origin TC-9211
gh pr create --base main --title "feat(advisory): add vulnerability summary extractor" --body "..."
```

## Step 11 -- Update Jira

- Set `customfield_10875` (Git Pull Request) to the PR URL in ADF format
- Add comment with PR link, summary of changes, no deviations from plan
- Transition TC-9211 to In Review
