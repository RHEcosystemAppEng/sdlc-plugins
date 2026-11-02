# File 6 — Create: `tests/api/advisory_summary.rs`

## What changes

Integration tests for the new severity summary endpoint.

## Code inspection

Before creating, inspect sibling test files `tests/api/advisory.rs` and `tests/api/sbom.rs` with `mcp__serena_backend__get_symbols_overview` to understand test patterns: setup, assertion style, response validation, test naming.

## Detailed changes

```rust
use actix_http::StatusCode;
use test_context::test_context;
use trustify_test_context::TrustifyContext;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[test_context(TrustifyContext)]
#[tokio::test]
async fn test_severity_summary_with_advisories(ctx: &TrustifyContext) {
    // Given an SBOM with advisories at known severity levels ingested into the database
    let sbom_id = ctx.ingest_test_sbom_with_advisories().await;

    // When requesting the severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response is OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 1);
    assert_eq!(body["high"], 2);
    assert_eq!(body["medium"], 3);
    assert_eq!(body["low"], 1);
    assert_eq!(body["total"], 7);
}

/// Verifies that requesting a non-existent SBOM ID returns 404.
#[test_context(TrustifyContext)]
#[tokio::test]
async fn test_severity_summary_sbom_not_found(ctx: &TrustifyContext) {
    // Given a non-existent SBOM ID
    let fake_id = "urn:uuid:00000000-0000-0000-0000-000000000000";

    // When requesting the severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zeros.
#[test_context(TrustifyContext)]
#[tokio::test]
async fn test_severity_summary_no_advisories(ctx: &TrustifyContext) {
    // Given an SBOM with no linked advisories
    let sbom_id = ctx.ingest_test_sbom().await;

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
async fn test_severity_summary_deduplicates_advisories(ctx: &TrustifyContext) {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let sbom_id = ctx.ingest_test_sbom_with_duplicate_advisories().await;

    // When requesting the severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then duplicates are not double-counted
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 1);
    assert_eq!(body["total"], 1);
}
```

## Patterns followed

- Test file location: `tests/api/` alongside `advisory.rs` and `sbom.rs`
- Uses `test_context` and `TrustifyContext` (matches sibling test files)
- Uses `tokio::test` for async tests
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` then deserialize and check values
- Each test function has a `///` documentation comment explaining what it verifies
- Given-When-Then section comments for non-trivial tests
- Test naming: `test_<feature>_<scenario>` pattern
- Value-based assertions (checking specific counts, not just `.len() > 0`)
