# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all test requirements from the task description.

## Full File Contents

```rust
use axum::http::StatusCode;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
///
/// Seeds an SBOM with advisories at each severity level and validates that the
/// endpoint returns the expected counts per severity and the correct total.
#[tokio::test]
async fn test_advisory_summary_returns_correct_severity_counts() {
    // Given an SBOM linked to advisories with known severity levels:
    // 2 Critical, 3 High, 1 Medium, 0 Low
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_with_advisories(
        &app,
        vec![
            ("ADV-001", "Critical"),
            ("ADV-002", "Critical"),
            ("ADV-003", "High"),
            ("ADV-004", "High"),
            ("ADV-005", "High"),
            ("ADV-006", "Medium"),
        ],
    )
    .await;

    // When requesting the advisory severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response should be 200 OK with correct counts
    assert_eq!(resp.status(), StatusCode::OK);

    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 3);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Verifies that requesting an advisory summary for a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_advisory_summary_returns_404_for_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let app = setup_test_app().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .await;

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_zeros_for_sbom_with_no_advisories() {
    // Given an SBOM with no linked advisories
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_with_advisories(&app, vec![]).await;

    // When requesting the advisory severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response should be 200 OK with all zeros
    assert_eq!(resp.status(), StatusCode::OK);

    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links for the same SBOM are deduplicated in the count.
///
/// When the same advisory is linked to an SBOM multiple times (e.g., through different
/// vulnerability paths), it should only be counted once in the severity summary.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM with duplicate advisory links (same advisory ID linked twice)
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_with_advisories(
        &app,
        vec![
            ("ADV-001", "Critical"),
            ("ADV-001", "Critical"), // duplicate link
            ("ADV-002", "High"),
        ],
    )
    .await;

    // When requesting the advisory severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response should count each advisory only once
    assert_eq!(resp.status(), StatusCode::OK);

    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 1); // ADV-001 counted once despite duplicate link
    assert_eq!(body["high"], 1);     // ADV-002 counted once
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 2);    // 2 unique advisories
}
```

## Conventions Followed

- **Location**: Placed in `tests/api/` directory alongside sibling test files (`sbom.rs`, `advisory.rs`, `search.rs`)
- **Test database**: Uses real PostgreSQL test database via `setup_test_app()` helper (matching sibling pattern)
- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization (matching sibling test files)
- **Response validation**: Asserts on specific field values (not just collection lengths), verifying `critical`, `high`, `medium`, `low`, and `total` individually
- **Error case coverage**: Includes 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` matching sibling pattern
- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_returns_correct_severity_counts`)
- **Documentation**: Every test function has a `///` doc comment explaining what it verifies (AI-generated standard)
- **Structure**: Non-trivial tests use `// Given`, `// When`, `// Then` section comments
- **Value-based assertions**: Asserts on actual count values (e.g., `assert_eq!(body["critical"], 2)`) rather than just checking total length
- **Deduplication test**: Specifically tests that duplicate advisory links produce correct unique counts (acceptance criteria requirement)

## Test-to-Requirement Mapping

| Test | Requirement |
|---|---|
| `test_advisory_summary_returns_correct_severity_counts` | Test that a valid SBOM with known advisories returns correct severity counts |
| `test_advisory_summary_returns_404_for_nonexistent_sbom` | Test that a non-existent SBOM ID returns 404 |
| `test_advisory_summary_returns_zeros_for_sbom_with_no_advisories` | Test that an SBOM with no advisories returns all zeros |
| `test_advisory_summary_deduplicates_advisory_links` | Test that duplicate advisory links are deduplicated in the count |
