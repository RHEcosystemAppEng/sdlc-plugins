# File 3: `tests/api/advisory_summary.rs` (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Covers all four test requirements from the task description.

## Pre-implementation inspection

Before creating this file, inspect these sibling test files to understand the test patterns:

- **`tests/api/advisory.rs`** -- Read via `mcp__serena_backend__get_symbols_overview` to see test function naming, assertion patterns, setup/teardown, and how the test database is used.
- **`tests/api/sbom.rs`** -- Read to confirm cross-module test pattern consistency, especially the 404 test case pattern and response validation approach.
- **`tests/api/search.rs`** -- Read to verify additional test conventions.

## Detailed changes

Create the file with the following test functions:

```rust
use reqwest::StatusCode;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_get_advisory_summary_valid_sbom() {
    // Given an SBOM linked to advisories with known severity levels
    // (seed test data: 2 Critical, 3 High, 1 Medium, 0 Low advisories)
    let app = TestApp::spawn().await;
    let sbom_id = app.seed_sbom_with_advisories(vec![
        ("ADV-001", "Critical"),
        ("ADV-002", "Critical"),
        ("ADV-003", "High"),
        ("ADV-004", "High"),
        ("ADV-005", "High"),
        ("ADV-006", "Medium"),
    ]).await;

    // When requesting the advisory summary
    let resp = app
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("Failed to send request");

    // Then the response should contain correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 3);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that a non-existent SBOM ID returns a 404 status code.
#[tokio::test]
async fn test_get_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let app = TestApp::spawn().await;
    let non_existent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = app
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", non_existent_id))
        .send()
        .await
        .expect("Failed to send request");

    // Then the response should be 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_get_advisory_summary_empty() {
    // Given an SBOM with no linked advisories
    let app = TestApp::spawn().await;
    let sbom_id = app.seed_sbom_without_advisories().await;

    // When requesting the advisory summary
    let resp = app
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("Failed to send request");

    // Then all severity counts should be zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links to the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_get_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let app = TestApp::spawn().await;
    let sbom_id = app.seed_sbom_with_duplicate_advisories(vec![
        ("ADV-001", "High"),
        ("ADV-001", "High"),  // duplicate
        ("ADV-002", "Critical"),
    ]).await;

    // When requesting the advisory summary
    let resp = app
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("Failed to send request");

    // Then duplicates should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.high, 1);      // ADV-001 counted once
    assert_eq!(summary.critical, 1);  // ADV-002
    assert_eq!(summary.total, 2);     // 2 unique advisories
}
```

## Conventions followed

- Uses `assert_eq!(resp.status(), StatusCode::OK)` pattern (matches sibling tests)
- Includes 404 test case (matches sibling test coverage pattern)
- Follows `test_<endpoint>_<scenario>` naming convention
- Uses real PostgreSQL test database (integration test pattern)
- Asserts on specific field values, not just collection lengths
- Every test function has a `///` documentation comment explaining what it verifies
- Non-trivial tests use given-when-then section comments (`// Given`, `// When`, `// Then`)
