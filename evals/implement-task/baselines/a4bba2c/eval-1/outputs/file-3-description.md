# File 3: `tests/api/advisory_summary.rs` (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests verify correct severity counting, proper 404 handling for non-existent SBOMs, zero-count behavior when an SBOM has no linked advisories, and deduplication of advisory links.

## Sibling Reference

- `tests/api/advisory.rs` — existing advisory integration tests for test harness setup, assertion patterns, data seeding conventions, and test context usage
- `tests/api/sbom.rs` — SBOM integration tests for SBOM creation and ID handling patterns

## Content

```rust
use reqwest::StatusCode;
use serde::Deserialize;

// Import the test harness/context from the project's test utilities
// (exact import path derived from sibling test files)
use crate::common::TestContext;

/// Response struct for deserializing the endpoint response in tests.
#[derive(Debug, Deserialize)]
struct SeveritySummaryResponse {
    critical: i64,
    high: i64,
    medium: i64,
    low: i64,
    total: i64,
}

/// Test that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_known_advisories() {
    let ctx = TestContext::new().await;

    // Seed an SBOM
    let sbom_id = ctx.create_sbom("test-sbom-1").await;

    // Seed advisories with known severities and link them to the SBOM
    ctx.create_advisory_for_sbom(sbom_id, "ADV-001", "Critical").await;
    ctx.create_advisory_for_sbom(sbom_id, "ADV-002", "Critical").await;
    ctx.create_advisory_for_sbom(sbom_id, "ADV-003", "High").await;
    ctx.create_advisory_for_sbom(sbom_id, "ADV-004", "Medium").await;
    ctx.create_advisory_for_sbom(sbom_id, "ADV-005", "Low").await;
    ctx.create_advisory_for_sbom(sbom_id, "ADV-006", "Low").await;

    // Make request
    let resp = ctx
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    assert_eq!(resp.status(), StatusCode::OK);

    let body: SeveritySummaryResponse = resp.json().await.expect("invalid JSON");
    assert_eq!(body.critical, 2);
    assert_eq!(body.high, 1);
    assert_eq!(body.medium, 1);
    assert_eq!(body.low, 2);
    assert_eq!(body.total, 6);
}

/// Test that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_severity_summary_nonexistent_sbom() {
    let ctx = TestContext::new().await;

    let fake_id = "00000000-0000-0000-0000-000000000000";

    let resp = ctx
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await
        .expect("request failed");

    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Test that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    let ctx = TestContext::new().await;

    // Seed an SBOM with no linked advisories
    let sbom_id = ctx.create_sbom("test-sbom-empty").await;

    let resp = ctx
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    assert_eq!(resp.status(), StatusCode::OK);

    let body: SeveritySummaryResponse = resp.json().await.expect("invalid JSON");
    assert_eq!(body.critical, 0);
    assert_eq!(body.high, 0);
    assert_eq!(body.medium, 0);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 0);
}

/// Test that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_severity_summary_deduplication() {
    let ctx = TestContext::new().await;

    let sbom_id = ctx.create_sbom("test-sbom-dedup").await;

    // Create one advisory and link it to the SBOM multiple times
    // (simulating duplicate entries in sbom_advisory join table)
    let advisory_id = ctx.create_advisory("ADV-DUP-001", "High").await;
    ctx.link_advisory_to_sbom(advisory_id, sbom_id).await;
    ctx.link_advisory_to_sbom(advisory_id, sbom_id).await; // duplicate link

    let resp = ctx
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    assert_eq!(resp.status(), StatusCode::OK);

    let body: SeveritySummaryResponse = resp.json().await.expect("invalid JSON");
    // Despite two links, only one unique advisory should be counted
    assert_eq!(body.high, 1);
    assert_eq!(body.total, 1);
}
```

## Conventions Followed

- Test file placed in `tests/api/` — matches existing integration test location
- File named `advisory_summary.rs` — descriptive, avoids collision with existing `advisory.rs`
- Uses `#[tokio::test]` — matches async test pattern (Axum + Tokio runtime)
- Test function names use `test_` prefix with descriptive snake_case — matches sibling tests
- Assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern — matches existing tests
- Response body deserialized into a typed struct — matches existing test patterns
- Each test is independent (creates its own context/data) — matches test isolation convention
- Four test cases cover the core scenarios: valid data with counts, missing resource (404), empty results, and deduplication

## Notes

- The test harness API (`TestContext`, `create_sbom`, `create_advisory_for_sbom`, etc.) is illustrative; actual helper method names would be derived from inspecting `tests/api/advisory.rs` and `tests/api/sbom.rs` during pre-implementation analysis
- The deduplication test assumes the test harness can insert duplicate rows into the `sbom_advisory` join table; if the table has a unique constraint, the test would verify deduplication through a different mechanism
- `tests/Cargo.toml` may need the new test file registered in `[[test]]` if tests are not auto-discovered
