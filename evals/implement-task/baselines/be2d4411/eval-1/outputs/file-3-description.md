# File 3: tests/api/advisory_summary.rs

**Action**: CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task description.

## Detailed Changes

### Test Functions

```rust
use reqwest::StatusCode;

/// Verifies that a valid SBOM with known advisories returns the correct severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with known advisories at different severity levels
    // (test fixtures: 2 Critical, 3 High, 1 Medium, 0 Low)
    let sbom_id = create_test_sbom_with_advisories(vec![
        ("ADV-001", "Critical"),
        ("ADV-002", "Critical"),
        ("ADV-003", "High"),
        ("ADV-004", "High"),
        ("ADV-005", "High"),
        ("ADV-006", "Medium"),
    ]).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should be OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 3);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that a non-existent SBOM ID returns a 404 Not Found response.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let non_existent_id = "non-existent-sbom-id";

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", non_existent_id))
        .send()
        .await;

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all severity counts as zero.
#[tokio::test]
async fn test_advisory_summary_empty_returns_zeros() {
    // Given an SBOM with no linked advisories
    let sbom_id = create_test_sbom_with_advisories(vec![]).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should be OK with all zero counts
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
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let sbom_id = create_test_sbom_with_advisories(vec![
        ("ADV-001", "Critical"),
        ("ADV-001", "Critical"),  // duplicate
        ("ADV-002", "High"),
    ]).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should count each advisory only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 1);  // ADV-001 counted once despite duplicate link
    assert_eq!(summary.high, 1);      // ADV-002 counted once
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 2);     // 2 unique advisories
}
```

### Design Decisions

- **Individual test functions** (not parameterized): Sibling test files in `tests/api/` use individual test functions, not `#[rstest]`. Following established convention.
- **Value-based assertions**: Each test asserts on specific field values (`assert_eq!(summary.critical, 2)`), not just counts or lengths.
- **Given-When-Then comments**: All tests have non-trivial setup, so given-when-then section comments are included.
- **Doc comments on every test**: Each test function has a `///` documentation comment explaining what it verifies.
- **Status code checks first**: Following the sibling pattern of `assert_eq!(resp.status(), StatusCode::OK)` before body deserialization.

### Test Conventions Followed

- File placed in `tests/api/` directory matching sibling test files.
- Test naming follows `test_<feature>_<scenario>` pattern (e.g., `test_advisory_summary_not_found`).
- Uses `assert_eq!` with `StatusCode` for HTTP status validation.
- Uses real PostgreSQL test database (integration test pattern).
- Fixtures created programmatically with helper functions.
- Tests are independent -- each creates its own test data.
