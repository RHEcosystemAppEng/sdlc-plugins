# File 6: `tests/api/advisory_summary.rs` (CREATE)

## Purpose
Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all four test requirements specified in the task.

## Full File Content

```rust
//! Integration tests for the advisory severity summary endpoint.
//!
//! Tests the GET /api/v2/sbom/{id}/advisory-summary endpoint against a
//! real PostgreSQL test database, validating severity count aggregation,
//! 404 handling, empty results, and deduplication.

use axum::http::StatusCode;
use crate::advisory::model::severity_summary::SeveritySummary;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with linked advisories at known severity levels
    let app = create_test_app().await;
    let sbom_id = seed_sbom(&app).await;
    seed_advisory(&app, sbom_id, "critical").await;
    seed_advisory(&app, sbom_id, "critical").await;
    seed_advisory(&app, sbom_id, "high").await;
    seed_advisory(&app, sbom_id, "medium").await;
    seed_advisory(&app, sbom_id, "low").await;
    seed_advisory(&app, sbom_id, "low").await;
    seed_advisory(&app, sbom_id, "low").await;

    // When requesting the advisory severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response status is 200 and counts match
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 3);
    assert_eq!(summary.total, 7);
}

/// Verifies that requesting a severity summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let app = create_test_app().await;
    let non_existent_id = uuid::Uuid::new_v4();

    // When requesting the advisory severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", non_existent_id))
        .await;

    // Then the response status is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all-zero severity counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let app = create_test_app().await;
    let sbom_id = seed_sbom(&app).await;

    // When requesting the advisory severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response status is 200 and all counts are zero
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links for the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let app = create_test_app().await;
    let sbom_id = seed_sbom(&app).await;
    let advisory_id = seed_advisory(&app, sbom_id, "high").await;
    // Link the same advisory a second time to create a duplicate
    link_advisory_to_sbom(&app, sbom_id, advisory_id).await;

    // When requesting the advisory severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the duplicate is counted only once
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.high, 1, "duplicate advisory should be counted once");
    assert_eq!(summary.total, 1, "total should reflect deduplicated count");
}
```

## Conventions Applied
- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching existing tests in `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- **Response validation**: Asserts on specific field values (not just counts or lengths).
- **Error cases**: Includes a 404 test matching the pattern in sibling test files.
- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom`).
- **Test documentation**: Every test function has a `///` doc comment explaining what it verifies.
- **Given-When-Then**: All tests use `// Given`, `// When`, `// Then` section comments.
- **No parameterized tests**: Individual test functions are used, consistent with sibling test files that do not use `rstest`.
- **Value-based assertions**: Asserts on actual severity counts, not just collection lengths.

## Notes
- Helper functions (`create_test_app`, `seed_sbom`, `seed_advisory`, `link_advisory_to_sbom`) are placeholders following the pattern likely used in sibling test files. The actual implementation would reuse the project's existing test infrastructure.
- The `resp.json()` deserialization call assumes an Axum test helper or similar utility used by the project's existing integration tests.
- Tests run against a real PostgreSQL test database, consistent with the project's testing conventions.
