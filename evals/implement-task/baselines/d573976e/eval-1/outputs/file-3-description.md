# File 3: `tests/api/advisory_summary.rs` (CREATE)

## Purpose

Integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all test requirements from the task description.

## Detailed Changes

Create a new file with the following tests:

```rust
use reqwest::StatusCode;

/// Verifies that a valid SBOM with known advisories returns correct severity counts
/// for each severity level (critical, high, medium, low) and the total.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (setup: create test SBOM, link advisories with Critical=2, High=1, Medium=3, Low=0)
    let sbom_id = create_test_sbom_with_advisories(vec![
        ("ADV-001", "Critical"),
        ("ADV-002", "Critical"),
        ("ADV-003", "High"),
        ("ADV-004", "Medium"),
        ("ADV-005", "Medium"),
        ("ADV-006", "Medium"),
    ]);

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response should be 200 with correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 3);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that a non-existent SBOM ID returns a 404 Not Found response,
/// consistent with other SBOM endpoint behavior.
#[tokio::test]
async fn test_advisory_summary_sbom_not_found() {
    // Given a non-existent SBOM ID
    let non_existent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", non_existent_id))
        .send()
        .await
        .unwrap();

    // Then the response should be 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all severity counts
/// as zero and total as zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no advisories linked
    let sbom_id = create_test_sbom_with_advisories(vec![]);

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response should be 200 with all zeros
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links (same advisory linked to the SBOM
/// multiple times) are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links
    let sbom_id = create_test_sbom_with_advisories(vec![
        ("ADV-001", "Critical"),
        ("ADV-001", "Critical"),  // duplicate
        ("ADV-002", "High"),
    ]);

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response should count each advisory only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 1);  // ADV-001 counted once
    assert_eq!(summary.high, 1);      // ADV-002 counted once
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 2);     // 2 unique advisories
}
```

## Conventions Followed

- **Assertion style**: uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching the pattern in `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- **Response validation**: validates specific field values (not just presence or count), asserting on `critical`, `high`, `medium`, `low`, and `total` individually.
- **Error cases**: includes a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`, consistent with all sibling test files.
- **Test naming**: follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_with_known_advisories`).
- **Documentation**: every test function has a `///` doc comment explaining what it verifies.
- **Given-when-then**: all tests use `// Given`, `// When`, `// Then` section comments for structure, since each test has distinct setup, action, and assertion phases.
- **Value-based assertions**: asserts on actual severity count values, not just collection lengths, so test failures reveal what changed.
- **Test file location**: placed in `tests/api/` following the existing pattern of one file per domain area.
