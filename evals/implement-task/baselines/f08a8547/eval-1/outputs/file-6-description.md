# File 6: Integration Tests for Advisory Summary Endpoint

**File**: `tests/api/advisory_summary.rs`
**Action**: CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.
Tests cover the four scenarios specified in the task's Test Requirements.

## Full File Content

```rust
use reqwest::StatusCode;
use serde_json::Value;
use test_context::test_context;

use crate::common::TestContext;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[test_context(TestContext)]
#[tokio::test]
async fn test_valid_sbom_severity_counts(ctx: &TestContext) {
    // Given an SBOM ingested with advisories at known severity levels:
    //   - 2 Critical advisories
    //   - 3 High advisories
    //   - 1 Medium advisory
    //   - 0 Low advisories
    let sbom_id = ctx.ingest_test_sbom("test-sbom-with-advisories.json").await;
    ctx.link_advisory(sbom_id, "ADV-001", "critical").await;
    ctx.link_advisory(sbom_id, "ADV-002", "critical").await;
    ctx.link_advisory(sbom_id, "ADV-003", "high").await;
    ctx.link_advisory(sbom_id, "ADV-004", "high").await;
    ctx.link_advisory(sbom_id, "ADV-005", "high").await;
    ctx.link_advisory(sbom_id, "ADV-006", "medium").await;

    // When requesting the advisory severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // And the severity counts match the expected values
    let body: Value = resp.json().await.expect("invalid JSON");
    assert_eq!(body["critical"], 2, "expected 2 critical advisories");
    assert_eq!(body["high"], 3, "expected 3 high advisories");
    assert_eq!(body["medium"], 1, "expected 1 medium advisory");
    assert_eq!(body["low"], 0, "expected 0 low advisories");
    assert_eq!(body["total"], 6, "expected 6 total advisories");
}

/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[test_context(TestContext)]
#[tokio::test]
async fn test_nonexistent_sbom_returns_404(ctx: &TestContext) {
    // Given a SBOM ID that does not exist in the database
    let bogus_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", bogus_id))
        .send()
        .await
        .expect("request failed");

    // Then the response status is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all severity counts as zero.
#[test_context(TestContext)]
#[tokio::test]
async fn test_sbom_with_no_advisories_returns_zeros(ctx: &TestContext) {
    // Given an SBOM with no linked advisories
    let sbom_id = ctx.ingest_test_sbom("test-sbom-empty.json").await;

    // When requesting the advisory severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // And all severity counts are zero
    let body: Value = resp.json().await.expect("invalid JSON");
    assert_eq!(body["critical"], 0, "critical should be 0");
    assert_eq!(body["high"], 0, "high should be 0");
    assert_eq!(body["medium"], 0, "medium should be 0");
    assert_eq!(body["low"], 0, "low should be 0");
    assert_eq!(body["total"], 0, "total should be 0");
}

/// Verifies that duplicate advisory links for the same SBOM are deduplicated in the count.
#[test_context(TestContext)]
#[tokio::test]
async fn test_duplicate_advisories_are_deduplicated(ctx: &TestContext) {
    // Given an SBOM linked to the same advisory multiple times
    let sbom_id = ctx.ingest_test_sbom("test-sbom-duplicates.json").await;
    ctx.link_advisory(sbom_id, "ADV-DUP-001", "high").await;
    ctx.link_advisory(sbom_id, "ADV-DUP-001", "high").await; // duplicate link
    ctx.link_advisory(sbom_id, "ADV-DUP-001", "high").await; // another duplicate
    ctx.link_advisory(sbom_id, "ADV-DUP-002", "critical").await;

    // When requesting the advisory severity summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // And the counts reflect unique advisories only (not duplicated links)
    let body: Value = resp.json().await.expect("invalid JSON");
    assert_eq!(body["high"], 1, "ADV-DUP-001 should be counted once despite 3 links");
    assert_eq!(body["critical"], 1, "ADV-DUP-002 should be counted once");
    assert_eq!(body["medium"], 0, "no medium advisories");
    assert_eq!(body["low"], 0, "no low advisories");
    assert_eq!(body["total"], 2, "total should be 2 unique advisories");
}
```

## Design Decisions

1. **Value-based assertions**: every test asserts on the specific count values for
   each severity level, not just the total count or response length. This follows
   the skill's guidance to prefer value-based assertions over length-only checks.

2. **Given-when-then structure**: all tests are non-trivial (setup, action,
   assertion phases) so they use `// Given`, `// When`, `// Then` section comments.

3. **Documentation comments**: every test function has a `///` doc comment
   explaining what it verifies, following the skill's test documentation mandate.

4. **No parameterized tests**: the four test cases exercise different scenarios
   with different setups and assertions, so individual test functions are
   appropriate. The project does not appear to use `rstest` or parameterized
   tests, and the Meszaros heuristic does not apply here since each test has
   distinct setup logic.

5. **Test data setup**: uses helper methods like `ctx.ingest_test_sbom()` and
   `ctx.link_advisory()` -- these would need to exist or be created in the test
   infrastructure. The actual helper implementation depends on the project's
   existing test utilities.

## Convention Adherence

- File placed in `tests/api/` matching sibling test files (`sbom.rs`, `advisory.rs`, `search.rs`).
- Uses `#[test_context(TestContext)]` for database setup/teardown (following project test infra).
- Uses `#[tokio::test]` for async test execution.
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` matches documented project convention.
- Response body deserialization via `serde_json::Value` for flexible field access.

## Test Registration

The test file also needs to be registered in `tests/api/mod.rs` (or whatever module
file aggregates the API tests). Add:

```rust
mod advisory_summary;
```

This is an out-of-scope file modification that would be flagged during Step 9
scope containment and requires user approval.
