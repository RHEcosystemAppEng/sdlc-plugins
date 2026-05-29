# File 6: Create `tests/api/advisory_summary.rs`

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task.

## Pre-Implementation Inspection

Before writing, inspect sibling test files for patterns:
- Read `tests/api/advisory.rs` -- understand assertion style, setup patterns, naming
- Read `tests/api/sbom.rs` -- understand SBOM-related test fixtures and setup

## Detailed Changes

### Test File Content

```rust
//! Integration tests for the advisory severity summary endpoint.

use axum::http::StatusCode;
use serde_json::Value;

// Test infrastructure imports (matching sibling test patterns)
// Exact imports would be confirmed by inspecting sibling test files

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    // (seed test database with SBOM linked to advisories:
    //  2 critical, 1 high, 3 medium, 0 low)
    let sbom_id = setup_sbom_with_advisories(vec![
        ("adv-1", "critical"),
        ("adv-2", "critical"),
        ("adv-3", "high"),
        ("adv-4", "medium"),
        ("adv-5", "medium"),
        ("adv-6", "medium"),
    ])
    .await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response is 200 OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 3);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_advisory_summary_sbom_not_found() {
    // Given a non-existent SBOM ID
    let fake_id = "non-existent-sbom-id";

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_empty_advisories() {
    // Given an SBOM with no linked advisories
    let sbom_id = setup_sbom_with_advisories(vec![]).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response is 200 OK with all zero counts
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM linked to the same advisory multiple times
    // (e.g., advisory "adv-1" appears twice in sbom_advisory join table)
    let sbom_id = setup_sbom_with_advisory_links(vec![
        ("adv-1", "critical"),
        ("adv-1", "critical"),  // duplicate link
        ("adv-2", "high"),
    ])
    .await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response counts each advisory only once
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 1);  // adv-1 counted once despite two links
    assert_eq!(body["high"], 1);      // adv-2 counted once
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 2);     // 2 unique advisories, not 3 links
}
```

### Design Decisions

- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern from sibling tests (e.g., `test_advisory_summary_valid_sbom`, `test_advisory_summary_sbom_not_found`)
- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` matching sibling test patterns exactly
- **Value-based assertions**: Asserts on specific field values (`body["critical"]`, `body["high"]`, etc.) rather than just collection lengths, per skill Step 7 guidance
- **Given-When-Then comments**: Each test has `// Given`, `// When`, `// Then` section comments as required by skill Step 7 for non-trivial tests
- **Doc comments**: Every test function has a `///` doc comment explaining what it verifies, as required by skill Step 7
- **No parameterized tests**: Sibling test analysis showed no `#[rstest]` usage in API tests, so individual test functions are used per convention
- **Deduplication test**: Specifically tests the AC "Counts only unique advisories (deduplicates by advisory ID)" by inserting duplicate links and verifying counts
- **All zeros test**: Specifically tests AC "All severity levels default to 0 when no advisories exist at that level"
- **404 test**: Matches the error case coverage pattern from sibling tests

### Note on Test Infrastructure

The exact test setup functions (`setup_sbom_with_advisories`, `setup_sbom_with_advisory_links`, `client`) would be determined by inspecting the sibling test files' actual setup patterns. The tests above show the logical structure; actual implementation would use the project's test harness (likely involving a test database connection, fixture seeding, and an Axum test client).

### Test Registration

The new test file needs to be registered in `tests/Cargo.toml` or a test module root (e.g., `tests/api/mod.rs` if one exists). This would be verified during implementation by inspecting how sibling test files `sbom.rs` and `advisory.rs` are registered. If using Cargo's default test discovery (each `.rs` file in `tests/` is auto-discovered), no additional registration is needed.
