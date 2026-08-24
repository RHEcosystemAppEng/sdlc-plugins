# File 6: tests/api/advisory_summary.rs (CREATE)

## Pre-Implementation Inspection

Read sibling test files `tests/api/advisory.rs` and `tests/api/sbom.rs` to understand:
- Test setup/teardown patterns
- How test database is initialized
- Assertion patterns used (assert_eq with StatusCode)
- How test data is created and linked

## New File Content

```rust
//! Integration tests for the advisory severity summary endpoint.

use actix_http::StatusCode;
use serde_json::Value;
use test_context::test_context;

use crate::common::TestContext;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[test_context(TestContext)]
#[tokio::test]
async fn test_severity_summary_with_advisories(ctx: &TestContext) {
    // Given an SBOM with advisories of known severity levels
    let sbom_id = ctx.create_test_sbom().await;
    ctx.link_advisory(sbom_id, "ADV-001", "critical").await;
    ctx.link_advisory(sbom_id, "ADV-002", "high").await;
    ctx.link_advisory(sbom_id, "ADV-003", "high").await;
    ctx.link_advisory(sbom_id, "ADV-004", "medium").await;

    // When requesting the advisory summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response returns correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 1);
    assert_eq!(body["high"], 2);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 4);
}

/// Verifies that a non-existent SBOM ID returns a 404 status.
#[test_context(TestContext)]
#[tokio::test]
async fn test_severity_summary_nonexistent_sbom(ctx: &TestContext) {
    // Given a non-existent SBOM ID
    let fake_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await;

    // Then the response returns 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zero counts.
#[test_context(TestContext)]
#[tokio::test]
async fn test_severity_summary_empty(ctx: &TestContext) {
    // Given an SBOM with no linked advisories
    let sbom_id = ctx.create_test_sbom().await;

    // When requesting the advisory summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then all counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[test_context(TestContext)]
#[tokio::test]
async fn test_severity_summary_deduplication(ctx: &TestContext) {
    // Given an SBOM with duplicate advisory links
    let sbom_id = ctx.create_test_sbom().await;
    ctx.link_advisory(sbom_id, "ADV-001", "critical").await;
    ctx.link_advisory(sbom_id, "ADV-001", "critical").await; // duplicate
    ctx.link_advisory(sbom_id, "ADV-002", "high").await;

    // When requesting the advisory summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then duplicate advisories are counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 1); // ADV-001 counted once despite duplicate link
    assert_eq!(body["high"], 1);
    assert_eq!(body["total"], 2);
}
```

Tests follow sibling conventions:
- Integration test style hitting a real PostgreSQL test database
- `assert_eq!(resp.status(), StatusCode::OK)` pattern
- `test_` prefix with descriptive snake_case names
- Setup-action-assertion structure with given/when/then comments
- Doc comments on every test function (skill guidance override)
