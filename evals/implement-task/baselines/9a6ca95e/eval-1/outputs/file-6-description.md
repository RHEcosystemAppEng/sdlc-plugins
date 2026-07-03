# File 6: `tests/api/advisory_summary.rs` (CREATE)

## Inspection performed

Used `mcp__serena_backend__get_symbols_overview` on sibling test files to understand test patterns:
- `tests/api/advisory.rs` -- integration tests for advisory endpoints: uses `assert_eq!(resp.status(), StatusCode::OK)`, creates test fixtures via helper functions, tests both success and 404 cases
- `tests/api/sbom.rs` -- integration tests for SBOM endpoints: same assertion pattern, tests list and get operations
- `tests/api/search.rs` -- integration tests for search endpoint

All tests use a real PostgreSQL test database and follow the `test_<action>_<scenario>` naming convention.

No parameterized test patterns (`#[rstest]`) found in sibling tests -- will not introduce them.

## File content

```rust
use axum::http::StatusCode;

mod common;

/// Verifies that a valid SBOM with known advisories of different severity levels
/// returns the correct per-severity counts and total.
#[tokio::test]
async fn test_get_advisory_summary_with_advisories() {
    // Given an SBOM with advisories at different severity levels
    let app = common::setup_test_app().await;
    let sbom_id = common::create_test_sbom(&app).await;
    common::create_test_advisory(&app, sbom_id, "critical").await;
    common::create_test_advisory(&app, sbom_id, "critical").await;
    common::create_test_advisory(&app, sbom_id, "high").await;
    common::create_test_advisory(&app, sbom_id, "medium").await;

    // When requesting the severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response contains correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 4);
}

/// Verifies that requesting a severity summary for a non-existent SBOM ID
/// returns a 404 Not Found response, consistent with other SBOM endpoints.
#[tokio::test]
async fn test_get_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let app = common::setup_test_app().await;
    let non_existent_id = uuid::Uuid::new_v4();

    // When requesting the severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", non_existent_id))
        .await;

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all severity counts
/// as zero and a total of zero.
#[tokio::test]
async fn test_get_advisory_summary_empty() {
    // Given an SBOM with no advisories
    let app = common::setup_test_app().await;
    let sbom_id = common::create_test_sbom(&app).await;

    // When requesting the severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then all counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links (the same advisory linked to the same
/// SBOM multiple times) are deduplicated, counting each advisory only once.
#[tokio::test]
async fn test_get_advisory_summary_deduplicates() {
    // Given an SBOM with the same advisory linked multiple times
    let app = common::setup_test_app().await;
    let sbom_id = common::create_test_sbom(&app).await;
    let advisory_id = common::create_test_advisory(&app, sbom_id, "high").await;
    // Link the same advisory again (duplicate)
    common::link_advisory_to_sbom(&app, advisory_id, sbom_id).await;

    // When requesting the severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["high"], 1);
    assert_eq!(body["total"], 1);
}
```

## Rationale

- **Test naming**: Follows `test_<action>_<scenario>` pattern consistent with `tests/api/advisory.rs` (e.g., `test_get_advisory_summary_with_advisories`)
- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` matching sibling test patterns
- **Response validation**: Deserializes body as `serde_json::Value` and asserts on specific field values (not just count or shape), per skill requirement to "prefer value-based assertions over length-only checks"
- **Doc comments**: Every test function has a `///` doc comment explaining what it verifies, per skill requirements (overrides sibling convention even if siblings lack doc comments)
- **Given-When-Then**: Each non-trivial test includes `// Given`, `// When`, `// Then` section comments for navigability, per skill requirements
- **No parameterized tests**: Sibling tests do not use `#[rstest]` or similar, so individual test functions are used instead
- **Four test cases cover all Test Requirements**:
  1. Valid SBOM with known advisories returns correct severity counts
  2. Non-existent SBOM ID returns 404
  3. SBOM with no advisories returns all zeros
  4. Duplicate advisory links are deduplicated in the count
- **Test setup**: Uses helper functions (`common::setup_test_app`, `common::create_test_sbom`, `common::create_test_advisory`) consistent with the integration test infrastructure pattern seen in sibling tests
