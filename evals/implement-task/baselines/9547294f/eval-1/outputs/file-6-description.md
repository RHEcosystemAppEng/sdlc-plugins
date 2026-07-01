# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task description.

## Detailed Changes

Create a new test file with the following content:

```rust
//! Integration tests for the advisory severity summary endpoint.
//!
//! Tests the `GET /api/v2/sbom/{id}/advisory-summary` endpoint that returns
//! aggregated severity counts for advisories linked to a given SBOM.

use reqwest::StatusCode;
use crate::common::TestContext;  // hypothetical test helper module

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
///
/// Sets up an SBOM with advisories at each severity level and validates that the
/// response contains the expected count for each severity.
#[tokio::test]
async fn test_severity_summary_valid_sbom_with_advisories() {
    // Given an SBOM linked to advisories of known severities
    let ctx = TestContext::new().await;
    let sbom_id = ctx.create_test_sbom("test-sbom").await;
    ctx.create_advisory_linked_to_sbom(sbom_id, "critical").await;
    ctx.create_advisory_linked_to_sbom(sbom_id, "critical").await;
    ctx.create_advisory_linked_to_sbom(sbom_id, "high").await;
    ctx.create_advisory_linked_to_sbom(sbom_id, "medium").await;
    ctx.create_advisory_linked_to_sbom(sbom_id, "medium").await;
    ctx.create_advisory_linked_to_sbom(sbom_id, "medium").await;
    ctx.create_advisory_linked_to_sbom(sbom_id, "low").await;

    // When requesting the advisory summary for that SBOM
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    // Then the response should contain correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: serde_json::Value = resp.json().await.expect("failed to parse JSON");
    assert_eq!(summary["critical"], 2, "expected 2 critical advisories");
    assert_eq!(summary["high"], 1, "expected 1 high advisory");
    assert_eq!(summary["medium"], 3, "expected 3 medium advisories");
    assert_eq!(summary["low"], 1, "expected 1 low advisory");
    assert_eq!(summary["total"], 7, "expected 7 total advisories");
}

/// Verifies that a non-existent SBOM ID returns a 404 Not Found response.
#[tokio::test]
async fn test_severity_summary_sbom_not_found() {
    // Given a non-existent SBOM ID
    let ctx = TestContext::new().await;
    let non_existent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary for that SBOM
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", non_existent_id))
        .send()
        .await
        .expect("request failed");

    // Then the response should be 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_severity_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    let ctx = TestContext::new().await;
    let sbom_id = ctx.create_test_sbom("empty-sbom").await;

    // When requesting the advisory summary for that SBOM
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    // Then all severity counts should be zero
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: serde_json::Value = resp.json().await.expect("failed to parse JSON");
    assert_eq!(summary["critical"], 0, "critical should be 0");
    assert_eq!(summary["high"], 0, "high should be 0");
    assert_eq!(summary["medium"], 0, "medium should be 0");
    assert_eq!(summary["low"], 0, "low should be 0");
    assert_eq!(summary["total"], 0, "total should be 0");
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
///
/// When the same advisory is linked to an SBOM multiple times (e.g., through different
/// vulnerability paths), it should only be counted once in the severity summary.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links
    let ctx = TestContext::new().await;
    let sbom_id = ctx.create_test_sbom("dedup-sbom").await;
    let advisory_id = ctx.create_advisory("high").await;

    // Link the same advisory to the SBOM multiple times
    ctx.link_advisory_to_sbom(advisory_id, sbom_id).await;
    ctx.link_advisory_to_sbom(advisory_id, sbom_id).await;
    ctx.link_advisory_to_sbom(advisory_id, sbom_id).await;

    // When requesting the advisory summary for that SBOM
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    // Then the advisory should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: serde_json::Value = resp.json().await.expect("failed to parse JSON");
    assert_eq!(summary["high"], 1, "duplicate advisory should be counted once");
    assert_eq!(summary["total"], 1, "total should reflect deduplicated count");
    assert_eq!(summary["critical"], 0, "critical should be 0");
    assert_eq!(summary["medium"], 0, "medium should be 0");
    assert_eq!(summary["low"], 0, "low should be 0");
}
```

## Conventions Applied

- **Assertion style**: uses `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` matching sibling tests in `tests/api/advisory.rs` and `tests/api/sbom.rs`
- **Response validation**: validates specific field values (not just counts/lengths) -- asserts on `critical`, `high`, `medium`, `low`, and `total` individually with descriptive messages
- **Error cases**: includes 404 test for non-existent SBOM, consistent with sibling endpoint tests
- **Test naming**: follows `test_<endpoint>_<scenario>` pattern (e.g., `test_severity_summary_valid_sbom_with_advisories`)
- **Test organization**: happy path first, then error cases, then edge cases (deduplication)
- **Documentation**: every test function has a `///` doc comment describing what it verifies (AI-generated test standard)
- **Given-When-Then**: non-trivial tests include `// Given`, `// When`, `// Then` section comments for navigability
- **Value-based assertions**: asserts on specific severity count values, not just checking that the response is non-empty or has the right number of fields
- **No parameterized tests**: uses individual test functions for each scenario, matching sibling test file conventions (no `#[rstest]` usage observed in siblings)

## Notes

- The actual test setup (TestContext, create_test_sbom, etc.) would be adapted to match whatever test infrastructure exists in the codebase -- the patterns shown are illustrative of the test logic structure
- The exact `use` imports would be confirmed by inspecting sibling test files during Step 4
- Test file would also need to be registered in `tests/` Cargo.toml or test harness mod file if the project uses a centralized test registry
