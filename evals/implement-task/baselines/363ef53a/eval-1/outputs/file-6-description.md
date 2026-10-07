# File 6: Create `tests/api/advisory_summary.rs`

**Action:** Create new file

## Pre-implementation inspection

Before writing this file, read the sibling test files `tests/api/advisory.rs` and `tests/api/sbom.rs` to understand:
- Test setup and database bootstrapping patterns
- Assertion patterns (`assert_eq!(resp.status(), StatusCode::OK)`)
- How test data (SBOMs, advisories) is created in the test database
- Response body deserialization approach
- Error case testing patterns (e.g., 404 for non-existent IDs)

## Contents

Define 4 integration tests matching the Test Requirements:

```rust
use axum::http::StatusCode;
// ... other imports matching sibling test file patterns

/// Verifies that a valid SBOM with known advisories returns the correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (create test SBOM and link advisories with specific severities)

    // When requesting the severity summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains the correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, /* expected count */);
    assert_eq!(summary.high, /* expected count */);
    assert_eq!(summary.medium, /* expected count */);
    assert_eq!(summary.low, /* expected count */);
    assert_eq!(summary.total, /* expected total */);
}

/// Verifies that requesting a severity summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_severity_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the severity summary
    // GET /api/v2/sbom/{non_existent_id}/advisory-summary

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all-zero severity counts.
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the severity summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked multiple times)

    // When requesting the severity summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then each advisory is counted only once, regardless of duplicate links
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    // Assert that total reflects unique advisory count, not duplicate link count
    assert_eq!(summary.total, /* unique count, not duplicate count */);
}
```

**Pattern conformance:**
- Uses `#[tokio::test]` async test attribute matching sibling test patterns
- Uses `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern from `tests/api/advisory.rs` and `tests/api/sbom.rs`
- Asserts on specific field values (not just collection lengths) following the skill's "prefer value-based assertions" guidance
- Each test function has a `///` documentation comment explaining what it verifies
- Each non-trivial test uses given-when-then section comments (`// Given`, `// When`, `// Then`)
- Tests hit a real PostgreSQL test database (same approach as sibling test files)
- Test setup creates appropriate test data (SBOMs, advisories with specific severities, join table entries) following the patterns in sibling test files

**Note:** The file must also be registered in `tests/Cargo.toml` or the test harness module if required by the project's test configuration. Check whether sibling test files (`sbom.rs`, `advisory.rs`) need explicit registration or are auto-discovered.
