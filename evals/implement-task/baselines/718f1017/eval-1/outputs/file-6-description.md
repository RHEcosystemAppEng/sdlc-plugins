# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose
Integration tests for the GET /api/v2/sbom/{id}/advisory-summary endpoint covering all four test requirements.

## Detailed Changes

Create a new test file:

```rust
use axum::http::StatusCode;
use crate::advisory::model::severity_summary::SeveritySummary;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with 2 critical, 1 high, 1 medium, 0 low advisories
    let sbom = create_test_sbom().await;
    let adv_critical_1 = create_test_advisory("critical").await;
    let adv_critical_2 = create_test_advisory("critical").await;
    let adv_high = create_test_advisory("high").await;
    let adv_medium = create_test_advisory("medium").await;
    link_advisory_to_sbom(sbom.id, adv_critical_1.id).await;
    link_advisory_to_sbom(sbom.id, adv_critical_2.id).await;
    link_advisory_to_sbom(sbom.id, adv_high.id).await;
    link_advisory_to_sbom(sbom.id, adv_medium.id).await;

    // When requesting the severity summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom.id))
        .send()
        .await;

    // Then the response contains correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 4);
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let fake_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the severity summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await;

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let sbom = create_test_sbom().await;

    // When requesting the severity summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom.id))
        .send()
        .await;

    // Then all counts are zero
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
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with the same advisory linked twice
    let sbom = create_test_sbom().await;
    let adv = create_test_advisory("high").await;
    link_advisory_to_sbom(sbom.id, adv.id).await;
    link_advisory_to_sbom(sbom.id, adv.id).await; // duplicate link

    // When requesting the severity summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom.id))
        .send()
        .await;

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.high, 1);
    assert_eq!(summary.total, 1);
}
```

## Rationale
- Follows test conventions from sibling files `tests/api/advisory.rs` and `tests/api/sbom.rs`
- Each test has a doc comment explaining what it verifies (skill requirement)
- Given/When/Then structure with section comments for non-trivial tests
- Uses `assert_eq!` with `StatusCode` constants (project convention)
- Value-based assertions on specific fields, not just length checks
- Tests all four requirements: valid counts, 404, all zeros, deduplication
- Test naming follows `test_<endpoint>_<scenario>` convention
