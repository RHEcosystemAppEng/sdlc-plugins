# File 3: `tests/api/advisory_summary.rs` (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the acceptance criteria.

## Detailed Changes

Create a new file with the following test cases. The exact test harness setup (database initialization, HTTP client creation, fixture insertion) will mirror the patterns found in `tests/api/advisory.rs` and `tests/api/sbom.rs`.

### Test Module Structure

```rust
use serde_json::Value;
// Import shared test harness (exact path confirmed from sibling test files)
use crate::common::TestContext;  // or similar shared setup

/// Test 1: Valid SBOM with known advisories returns correct severity counts
#[tokio::test]
async fn test_severity_summary_with_advisories() {
    let ctx = TestContext::new().await;

    // Setup: create an SBOM
    let sbom_id = ctx.create_sbom("test-sbom").await;

    // Setup: create advisories with known severities and link to SBOM
    ctx.create_advisory_for_sbom(sbom_id, "CVE-2024-001", "Critical").await;
    ctx.create_advisory_for_sbom(sbom_id, "CVE-2024-002", "Critical").await;
    ctx.create_advisory_for_sbom(sbom_id, "CVE-2024-003", "High").await;
    ctx.create_advisory_for_sbom(sbom_id, "CVE-2024-004", "Medium").await;
    ctx.create_advisory_for_sbom(sbom_id, "CVE-2024-005", "Low").await;

    // Act
    let response = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Assert
    assert_eq!(response.status(), 200);

    let body: Value = response.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 1);
    assert_eq!(body["total"], 5);
}

/// Test 2: Non-existent SBOM ID returns 404
#[tokio::test]
async fn test_severity_summary_sbom_not_found() {
    let ctx = TestContext::new().await;

    let response = ctx
        .client
        .get("/api/v2/sbom/nonexistent-id/advisory-summary")
        .send()
        .await;

    assert_eq!(response.status(), 404);
}

/// Test 3: SBOM with no advisories returns all zeros
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    let ctx = TestContext::new().await;

    // Setup: create an SBOM with no linked advisories
    let sbom_id = ctx.create_sbom("empty-sbom").await;

    // Act
    let response = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Assert
    assert_eq!(response.status(), 200);

    let body: Value = response.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Test 4: Duplicate advisory links are deduplicated in the count
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    let ctx = TestContext::new().await;

    // Setup: create an SBOM and one advisory
    let sbom_id = ctx.create_sbom("dedup-sbom").await;
    let advisory_id = ctx.create_advisory("CVE-2024-010", "High").await;

    // Link the same advisory to the SBOM twice (simulating duplicate join entries)
    ctx.link_advisory_to_sbom(advisory_id, sbom_id).await;
    ctx.link_advisory_to_sbom(advisory_id, sbom_id).await;

    // Act
    let response = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Assert: should count as 1, not 2
    assert_eq!(response.status(), 200);

    let body: Value = response.json().await;
    assert_eq!(body["high"], 1);
    assert_eq!(body["total"], 1);
}
```

### Design Decisions

- **`TestContext` pattern:** The exact test context type and helper methods will be adapted from `tests/api/advisory.rs` and `tests/api/sbom.rs`. The pseudocode above shows the intent; actual helper names will match whatever the project provides.
- **Four test cases:** Maps directly to the four test requirements in the acceptance criteria.
- **`serde_json::Value`:** Used for flexible JSON assertion without importing the `SeveritySummary` struct into the test (keeping it a true black-box integration test).
- **Deduplication test:** Explicitly creates duplicate join-table entries to verify the `DISTINCT` / dedup logic in the service method.

### Notes

- The test file may need to be registered in a `tests/api/mod.rs` or via `#[path]` attribute if the test harness uses a module-based test discovery pattern. This will be confirmed by inspecting sibling test organization at implementation time.
- Helper methods like `create_sbom`, `create_advisory_for_sbom`, and `link_advisory_to_sbom` are illustrative. The actual implementation will use whatever test fixture utilities exist in the project (e.g., direct database insertion, or calling existing API endpoints to set up state).
