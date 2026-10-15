# File 3: tests/api/advisory_summary.rs

## Action: CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering
all test requirements from the task description.

## Detailed Changes

### Test Functions

```rust
use reqwest::StatusCode;
use serde_json::Value;
use test_context::test_context;

// Test setup and helpers imported from the test harness (matching sibling test patterns)

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[test_context(TrustifyContext)]
#[tokio::test]
async fn test_severity_summary_with_advisories(ctx: &TrustifyContext) {
    // Given an SBOM with linked advisories of known severities
    // (setup: ingest test SBOM and link advisories with Critical=2, High=3, Medium=1, Low=0)
    let sbom_id = setup_sbom_with_advisories(ctx, vec![
        ("ADV-001", "Critical"),
        ("ADV-002", "Critical"),
        ("ADV-003", "High"),
        ("ADV-004", "High"),
        ("ADV-005", "High"),
        ("ADV-006", "Medium"),
    ]).await;

    // When requesting the advisory severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response should contain correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 3);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Verifies that a non-existent SBOM ID returns 404, consistent with existing SBOM endpoints.
#[test_context(TrustifyContext)]
#[tokio::test]
async fn test_severity_summary_not_found(ctx: &TrustifyContext) {
    // Given a non-existent SBOM ID
    let fake_id = "non-existent-sbom-id";

    // When requesting the advisory severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await
        .unwrap();

    // Then the response should be 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zeros.
#[test_context(TrustifyContext)]
#[tokio::test]
async fn test_severity_summary_empty(ctx: &TrustifyContext) {
    // Given an SBOM with no linked advisories
    let sbom_id = setup_sbom_without_advisories(ctx).await;

    // When requesting the advisory severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then all severity counts should be zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await.unwrap();
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
    let sbom_id = setup_sbom_with_duplicate_advisories(ctx, vec![
        ("ADV-001", "High"),
        ("ADV-001", "High"),  // duplicate link
        ("ADV-002", "Medium"),
    ]).await;

    // When requesting the advisory severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the counts should reflect unique advisories only
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await.unwrap();
    assert_eq!(body["high"], 1);    // ADV-001 counted once despite duplicate link
    assert_eq!(body["medium"], 1);  // ADV-002
    assert_eq!(body["total"], 2);   // 2 unique advisories, not 3
}
```

### Design Decisions

- **Value-based assertions**: per skill guidance, asserts on specific severity count values
  rather than just checking collection length. This ensures test failures reveal exactly
  which count is wrong.
- **Given-when-then structure**: all tests have non-trivial setup, so given-when-then
  section comments are included per skill guidance.
- **Doc comments on every test**: per skill guidance, even though sibling tests may lack them.
- **No parameterized tests**: sibling test files (`sbom.rs`, `advisory.rs`) do not use
  parameterized test patterns, so following project convention per skill guidance.
- **Test naming**: `test_severity_summary_*` follows the `test_<feature>_<scenario>` pattern.
- **StatusCode assertions**: uses `assert_eq!(resp.status(), StatusCode::OK)` matching the
  established convention from sibling test files.
- **Real database**: tests use the `TrustifyContext` test harness that provides a real
  PostgreSQL test database, matching sibling test patterns.

### Convention Conformance

- Test file location: `tests/api/advisory_summary.rs` follows the pattern of sibling test
  files `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- Assertion style matches sibling: `assert_eq!(resp.status(), StatusCode::OK)`.
- JSON deserialization via `serde_json::Value` for flexible field assertions.
