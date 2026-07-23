# File 6: `tests/api/advisory_summary.rs` (CREATE)

## Purpose
Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task description.

## Full File Content

```rust
//! Integration tests for the advisory severity summary endpoint.
//!
//! Tests the GET /api/v2/sbom/{id}/advisory-summary endpoint, verifying
//! correct severity counting, 404 handling, empty results, and deduplication.

use actix_http::StatusCode;
use serde_json::Value;
use test_context::test_context;

// Import project test utilities -- exact imports depend on the test harness
// used by sibling test files (sbom.rs, advisory.rs).
// use crate::common::TestContext;

/// Verifies that an SBOM with known advisories returns correct severity counts.
#[test_context(TestContext)]
#[tokio::test]
async fn test_advisory_summary_valid_sbom(ctx: &TestContext) {
    // Given an SBOM with advisories at known severity levels:
    //   - 2 Critical advisories
    //   - 1 High advisory
    //   - 0 Medium advisories
    //   - 1 Low advisory
    let sbom_id = ctx.create_test_sbom_with_advisories(vec![
        ("adv-1", "Critical"),
        ("adv-2", "Critical"),
        ("adv-3", "High"),
        ("adv-4", "Low"),
    ]).await;

    // When requesting the severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should be 200 OK with correct counts
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 2, "Expected 2 critical advisories");
    assert_eq!(body["high"], 1, "Expected 1 high advisory");
    assert_eq!(body["medium"], 0, "Expected 0 medium advisories");
    assert_eq!(body["low"], 1, "Expected 1 low advisory");
    assert_eq!(body["total"], 4, "Expected 4 total advisories");
}

/// Verifies that a non-existent SBOM ID returns a 404 response.
#[test_context(TestContext)]
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom(ctx: &TestContext) {
    // Given a non-existent SBOM ID
    let fake_id = "non-existent-sbom-id";

    // When requesting the severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await;

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zeros.
#[test_context(TestContext)]
#[tokio::test]
async fn test_advisory_summary_empty_sbom(ctx: &TestContext) {
    // Given an SBOM with no linked advisories
    let sbom_id = ctx.create_test_sbom_without_advisories().await;

    // When requesting the severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should be 200 OK with all zero counts
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
///
/// When an advisory is linked to an SBOM multiple times (e.g., through different
/// vulnerability paths), it should only be counted once.
#[test_context(TestContext)]
#[tokio::test]
async fn test_advisory_summary_deduplicates(ctx: &TestContext) {
    // Given an SBOM where the same advisory is linked multiple times
    let sbom_id = ctx.create_test_sbom_with_advisories(vec![
        ("adv-1", "Critical"),
        ("adv-1", "Critical"),  // duplicate link
        ("adv-2", "High"),
    ]).await;

    // When requesting the severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should count each advisory only once
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 1, "Duplicate advisory should be counted once");
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 2, "Total should reflect deduplicated count");
}
```

## Design Decisions
- **Test naming** follows `test_<endpoint>_<scenario>` pattern discovered from sibling test files
- **Assertion style** uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching the pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`
- **Value-based assertions** check specific field values (not just response shape or count), per the skill's guidance to prefer value-based assertions over length-only checks
- **Doc comments** on every test function explain what it verifies, per the skill's documentation requirement
- **Given/When/Then comments** structure non-trivial tests for readability
- **Error case** includes a 404 test with `StatusCode::NOT_FOUND`, matching the sibling pattern
- **Test setup** uses helper methods on the test context -- the exact method names (`create_test_sbom_with_advisories`, etc.) should be confirmed against or created to match the test harness used by sibling test files
- **No parameterized tests** used because each test case has distinct setup and assertion logic (valid/not-found/empty/dedup are structurally different scenarios, not same-algorithm-different-data)

## Notes
- The exact test harness imports, context type, and helper method signatures should be confirmed from sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`). The code above uses `TestContext` as a placeholder.
- The test file should also be registered in `tests/Cargo.toml` if the test harness requires explicit test binary registration.
