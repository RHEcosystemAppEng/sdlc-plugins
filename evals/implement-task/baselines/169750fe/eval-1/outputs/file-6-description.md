# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose
Integration tests for the new severity aggregation endpoint.

## Changes

Create new file with the following test cases:

```rust
use actix_web::test;
use reqwest::StatusCode;
use serde_json::Value;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    create_test_advisory(&app, sbom_id, "critical").await;
    create_test_advisory(&app, sbom_id, "critical").await;
    create_test_advisory(&app, sbom_id, "high").await;
    create_test_advisory(&app, sbom_id, "medium").await;

    // When requesting the severity summary
    let resp = app.get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id)).await;

    // Then the response contains correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 4);
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_severity_summary_sbom_not_found() {
    // Given a non-existent SBOM ID
    let app = setup_test_app().await;
    let fake_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the severity summary
    let resp = app.get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id)).await;

    // Then a 404 is returned
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;

    // When requesting the severity summary
    let resp = app.get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id)).await;

    // Then all counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    let advisory_id = create_test_advisory(&app, sbom_id, "high").await;
    link_advisory_to_sbom(&app, advisory_id, sbom_id).await; // duplicate link

    // When requesting the severity summary
    let resp = app.get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id)).await;

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["high"], 1);
    assert_eq!(body["total"], 1);
}
```

## Rationale
- Follows integration test conventions from sibling `tests/api/advisory.rs`:
  - Tests hit real PostgreSQL test database
  - `assert_eq!(resp.status(), StatusCode::OK)` for status checks
  - Response body deserialization for content verification
  - Test naming: `test_<scenario>`
- Uses value-based assertions (specific counts) rather than length-only checks, per skill guidance
- Each test function has a `///` doc comment explaining what it verifies
- Given-when-then section comments for test structure clarity
- Covers all Test Requirements from the task description:
  1. Valid SBOM with known advisories returns correct counts
  2. Non-existent SBOM ID returns 404
  3. SBOM with no advisories returns all zeros
  4. Duplicate advisory links are deduplicated
