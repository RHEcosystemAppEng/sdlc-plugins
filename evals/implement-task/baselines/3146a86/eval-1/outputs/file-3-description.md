# File 3: CREATE — `tests/api/advisory_summary.rs`

## Purpose
Integration tests for the new severity summary endpoint.

## Changes

Create a new test file with 4 test functions following the Test Requirements:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_advisories() {
    // Given an SBOM with known advisories at different severity levels
    // When GET /api/v2/sbom/{id}/advisory-summary is called
    // Then the response contains correct counts per severity level and total
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.critical, expected_critical);
    assert_eq!(body.high, expected_high);
    assert_eq!(body.medium, expected_medium);
    assert_eq!(body.low, expected_low);
    assert_eq!(body.total, expected_total);
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_severity_summary_not_found() {
    // Given a non-existent SBOM ID
    // When GET /api/v2/sbom/{id}/advisory-summary is called
    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_severity_summary_empty() {
    // Given an SBOM with no linked advisories
    // When GET /api/v2/sbom/{id}/advisory-summary is called
    // Then all severity counts are 0 and total is 0
    assert_eq!(body.critical, 0);
    assert_eq!(body.high, 0);
    assert_eq!(body.medium, 0);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_severity_summary_deduplication() {
    // Given an SBOM with duplicate advisory links
    // When GET /api/v2/sbom/{id}/advisory-summary is called
    // Then each advisory is counted only once
    assert_eq!(body.total, expected_unique_count);
}
```

## Conventions Applied

- Test file in `tests/api/` matching sibling test files (`sbom.rs`, `advisory.rs`, `search.rs`)
- Uses `assert_eq!(resp.status(), StatusCode::OK)` pattern from sibling tests
- Tests named `test_<endpoint>_<scenario>` following naming convention
- Includes 404 test case matching advisory endpoint test patterns
- Doc comments on every test function
- Given-when-then section comments for non-trivial tests
