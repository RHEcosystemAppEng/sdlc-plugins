# File 6: Create `tests/api/advisory_summary.rs`

## Change Type
Create new file

## Description
Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Covers all four test scenarios from the Test Requirements section plus verifies the acceptance criteria.

## Full File Content

```rust
//! Integration tests for the advisory severity summary endpoint.

use common::model::SeveritySummary;
use reqwest::StatusCode;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM linked to advisories of known severities
    let app = test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    create_test_advisory(&app, sbom_id, "critical").await;
    create_test_advisory(&app, sbom_id, "critical").await;
    create_test_advisory(&app, sbom_id, "high").await;
    create_test_advisory(&app, sbom_id, "medium").await;
    create_test_advisory(&app, sbom_id, "low").await;
    create_test_advisory(&app, sbom_id, "low").await;
    create_test_advisory(&app, sbom_id, "low").await;

    // When requesting the severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response contains correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 3);
    assert_eq!(summary.total, 7);
}

/// Verifies that a non-existent SBOM ID returns a 404 status code.
#[tokio::test]
async fn test_advisory_summary_sbom_not_found() {
    // Given a non-existent SBOM ID
    let app = test_app().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let app = test_app().await;
    let sbom_id = create_test_sbom(&app).await;

    // When requesting the severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let app = test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    let advisory_id = create_test_advisory(&app, sbom_id, "high").await;
    // Link the same advisory a second time via a duplicate sbom_advisory entry
    link_advisory_to_sbom(&app, sbom_id, advisory_id).await;

    // When requesting the severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.high, 1);
    assert_eq!(summary.total, 1);
}
```

## Conventions Followed
- **Test file location:** `tests/api/advisory_summary.rs` follows the pattern of sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`)
- **Assertion style:** Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching sibling test patterns
- **Response validation:** Checks status code first, then deserializes and validates individual fields with value-based assertions (not just length checks)
- **Error cases:** Includes 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` matching sibling test patterns
- **Test naming:** Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_sbom_not_found`)
- **Test setup:** Uses test app and helper functions consistent with integration test infrastructure hitting PostgreSQL
- **Documentation:** Every test function has a `///` doc comment explaining what it verifies
- **Given-When-Then:** All non-trivial tests include `// Given`, `// When`, `// Then` section comments
- **Independent tests:** Each test function creates its own fixtures and does not depend on state from other tests

## Test Registration

The test file would also need to be registered in `tests/api/` -- if there is a `mod.rs` or the tests are auto-discovered by Cargo, this may happen automatically. Would verify by checking how `tests/api/advisory.rs` is included (likely via `#[cfg(test)]` or Cargo auto-discovery in the `tests/` directory).
