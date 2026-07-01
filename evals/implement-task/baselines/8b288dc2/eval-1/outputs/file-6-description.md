# File 6: `tests/api/advisory_summary.rs`

**Action**: Create new file

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests cover all four scenarios specified in the task's Test Requirements.

## Conventions Applied

- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern from sibling tests.
- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- **Error case coverage**: Includes 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`, matching sibling test patterns.
- **Test setup**: Uses real PostgreSQL test database with seeded test data, matching existing integration test infrastructure.
- **Documentation**: Every test function has a `///` doc comment explaining what it verifies (AI-generated standard).
- **Given-When-Then**: Non-trivial tests include `// Given`, `// When`, `// Then` section comments.
- **Individual test functions**: No parameterized tests, matching the sibling test pattern (no `rstest` usage observed).

## Detailed Changes

```rust
use axum::http::StatusCode;
use serde_json::Value;

// Test infrastructure imports (matching sibling test files)
use crate::common::TestContext;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories at known severity levels:
    //   2 Critical, 3 High, 1 Medium, 0 Low
    let ctx = TestContext::new().await;
    let sbom_id = ctx.seed_sbom_with_advisories(&[
        ("adv-1", "critical"),
        ("adv-2", "critical"),
        ("adv-3", "high"),
        ("adv-4", "high"),
        ("adv-5", "high"),
        ("adv-6", "medium"),
    ]).await;

    // When requesting the advisory summary
    let resp = ctx
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response contains correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 3);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Verifies that a non-existent SBOM ID returns HTTP 404, consistent with other SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID
    let ctx = TestContext::new().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary for a non-existent SBOM
    let resp = ctx
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .send()
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all severity counts as zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories_returns_all_zeros() {
    // Given an SBOM with no linked advisories
    let ctx = TestContext::new().await;
    let sbom_id = ctx.seed_sbom_without_advisories().await;

    // When requesting the advisory summary
    let resp = ctx
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links (same advisory linked multiple times)
/// are deduplicated so each advisory is counted only once in the summary.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM with duplicate advisory links
    //   adv-1 (critical) linked twice, adv-2 (high) linked three times
    let ctx = TestContext::new().await;
    let sbom_id = ctx.seed_sbom_with_duplicate_advisory_links(&[
        ("adv-1", "critical"),
        ("adv-1", "critical"),  // duplicate
        ("adv-2", "high"),
        ("adv-2", "high"),      // duplicate
        ("adv-2", "high"),      // duplicate
    ]).await;

    // When requesting the advisory summary
    let resp = ctx
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then each advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 1);  // adv-1 counted once
    assert_eq!(body["high"], 1);      // adv-2 counted once
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 2);     // 2 unique advisories
}
```

## Design Decisions

- **Value-based assertions**: Every test asserts on specific field values (e.g., `assert_eq!(body["critical"], 2)`) rather than just checking response length or status code. This follows the SKILL.md guidance to "prefer value-based assertions over length-only checks."
- **Test data seeding**: The test helper methods (`seed_sbom_with_advisories`, `seed_sbom_without_advisories`, `seed_sbom_with_duplicate_advisory_links`) are assumed to exist or would be added to the test context. The actual implementation would match whatever test data seeding pattern is used in `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- **UUID for non-existent ID**: Uses a zeroed UUID as the non-existent SBOM ID, which is a common pattern in test suites to avoid collisions with seeded data.
- **No parameterized tests**: Sibling test files use individual test functions, so we follow the same pattern rather than introducing `rstest`.
- **Async test runtime**: Uses `#[tokio::test]` matching the project's async runtime (Axum is built on tokio).

## Test-to-Requirement Mapping

| Test Requirement | Test Function |
|---|---|
| Test that a valid SBOM with known advisories returns correct severity counts | `test_advisory_summary_returns_correct_counts` |
| Test that a non-existent SBOM ID returns 404 | `test_advisory_summary_nonexistent_sbom_returns_404` |
| Test that an SBOM with no advisories returns all zeros | `test_advisory_summary_no_advisories_returns_all_zeros` |
| Test that duplicate advisory links are deduplicated in the count | `test_advisory_summary_deduplicates_advisory_links` |
