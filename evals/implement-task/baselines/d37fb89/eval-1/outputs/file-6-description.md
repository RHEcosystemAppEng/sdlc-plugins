# File 6: Create `tests/api/advisory_summary.rs`

## Action: CREATE

## Purpose
Integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task description.

## Conventions Applied
- Integration tests in `tests/api/` hitting a real PostgreSQL test database (project convention)
- Test naming: `test_<endpoint>_<scenario>` pattern (sibling convention from `advisory.rs`, `sbom.rs`)
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization (sibling convention)
- Error case: 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` (sibling convention)
- Value-based assertions on specific field values, not just collection lengths (skill requirement)
- Documentation comment on every test function (skill requirement)
- Given-When-Then section comments for non-trivial tests (skill requirement)

## Detailed Changes

Create a new file with the following content:

```rust
use axum::http::StatusCode;
use serde_json::Value;

// Test helpers and fixtures assumed to be available from the test harness
// (consistent with how sibling test files set up test context)

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories at known severity levels:
    //   2 Critical, 1 High, 3 Medium, 0 Low
    let app = test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    create_test_advisory(&app, sbom_id, "critical").await;
    create_test_advisory(&app, sbom_id, "critical").await;
    create_test_advisory(&app, sbom_id, "high").await;
    create_test_advisory(&app, sbom_id, "medium").await;
    create_test_advisory(&app, sbom_id, "medium").await;
    create_test_advisory(&app, sbom_id, "medium").await;

    // When requesting the advisory summary for that SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response should contain correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 3);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found_for_missing_sbom() {
    // Given a non-existent SBOM ID
    let app = test_app().await;
    let non_existent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", non_existent_id))
        .await;

    // Then the response should be 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_returns_zeros_for_no_advisories() {
    // Given an SBOM with no advisories linked
    let app = test_app().await;
    let sbom_id = create_test_sbom(&app).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then all severity counts should be zero
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
async fn test_advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM with the same advisory linked multiple times
    let app = test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    let advisory_id = create_test_advisory(&app, sbom_id, "high").await;
    // Link the same advisory again (duplicate)
    link_advisory_to_sbom(&app, sbom_id, advisory_id).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the duplicate should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["high"], 1);
    assert_eq!(body["total"], 1);
}
```

## Rationale
- Four test functions map directly to the four test requirements in the task description
- Each test has a documentation comment explaining what it verifies (skill requirement)
- Given-When-Then comments make the test structure navigable (skill requirement)
- Value-based assertions check specific field values (not just that the response is OK)
- The deduplication test explicitly creates a duplicate link and verifies it is counted only once
- The zero-counts test verifies the default behavior with no advisories
- The 404 test is consistent with the error case pattern used in sibling test files
- Test helper functions (`test_app`, `create_test_sbom`, `create_test_advisory`, `link_advisory_to_sbom`) follow the patterns assumed to exist in the test harness based on sibling test file conventions

## Note on `tests/Cargo.toml`
The new test file `advisory_summary.rs` may need to be registered in `tests/Cargo.toml` if the test harness uses explicit test file listing rather than auto-discovery. This would be verified during implementation by inspecting the existing `tests/Cargo.toml` configuration. If registration is needed, a `[[test]]` entry would be added following the pattern of existing test entries.
