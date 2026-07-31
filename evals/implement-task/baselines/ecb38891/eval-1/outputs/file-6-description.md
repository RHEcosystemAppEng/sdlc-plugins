# File 6: Create `tests/api/advisory_summary.rs`

## Purpose
Integration tests for the new severity summary endpoint.

## Pattern Reference
Follows the test patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`: set up test data, make HTTP requests, assert on responses using `assert_eq!` with specific values.

## Content

```rust
use actix_http::StatusCode;
use test_context::test_context;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[test_context(TrustifyContext)]
#[tokio::test]
async fn test_severity_summary_with_known_advisories(ctx: &TrustifyContext) {
    // Given an SBOM linked to advisories with known severities
    let sbom_id = ctx.ingest_test_sbom("test-sbom-with-advisories.json").await;
    // (test fixture includes 2 Critical, 1 High, 3 Medium, 0 Low advisories)

    // When requesting the severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response contains correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 3);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Verifies that a non-existent SBOM ID returns 404.
#[test_context(TrustifyContext)]
#[tokio::test]
async fn test_severity_summary_not_found(ctx: &TrustifyContext) {
    // Given a non-existent SBOM ID
    let fake_id = "non-existent-sbom-id";

    // When requesting the severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await;

    // Then a 404 is returned
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zeros.
#[test_context(TrustifyContext)]
#[tokio::test]
async fn test_severity_summary_empty(ctx: &TrustifyContext) {
    // Given an SBOM with no linked advisories
    let sbom_id = ctx.ingest_test_sbom("test-sbom-empty.json").await;

    // When requesting the severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[test_context(TrustifyContext)]
#[tokio::test]
async fn test_severity_summary_deduplication(ctx: &TrustifyContext) {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let sbom_id = ctx.ingest_test_sbom("test-sbom-with-duplicates.json").await;
    // (test fixture has 1 High advisory linked twice via sbom_advisory)

    // When requesting the severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the duplicate is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["high"], 1);  // not 2
    assert_eq!(body["total"], 1); // deduplicated count
}
```

## Notes
- Each test function has a `///` documentation comment explaining what it verifies (per skill guidance)
- Tests use given-when-then section comments for non-trivial test structure
- Uses value-based assertions (`assert_eq!` on specific field values) rather than length-only checks
- Follows sibling test conventions: `test_context`, `tokio::test`, `StatusCode` checks
- Test file location matches project convention: `tests/api/advisory_summary.rs`
