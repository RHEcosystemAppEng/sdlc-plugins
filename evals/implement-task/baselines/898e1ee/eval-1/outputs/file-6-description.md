# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering correct severity counts, 404 handling, empty SBOM, and deduplication.

## Sibling test files inspected

- `tests/api/advisory.rs` -- Advisory endpoint integration tests. Uses real PostgreSQL test database, `assert_eq!(resp.status(), StatusCode::OK)` for status checks, deserializes response body for field assertions. Test names follow `test_<endpoint>_<scenario>` pattern.
- `tests/api/sbom.rs` -- SBOM endpoint integration tests. Same patterns: status code assertions, body deserialization, fixture setup in the database.
- `tests/api/search.rs` -- Search endpoint tests. Same assertion style.

## Test conventions applied

- Tests hit a real PostgreSQL test database (no mocks)
- Status code assertions: `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Response body deserialized via `resp.json::<SeveritySummary>().await`
- Test naming: `test_advisory_summary_<scenario>`
- Each test function has a `///` documentation comment
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments
- Value-based assertions on specific fields (not just length checks)

## Detailed changes

```rust
use axum::http::StatusCode;
use crate::advisory::model::severity_summary::SeveritySummary;

/// Verifies that the advisory summary endpoint returns correct severity counts
/// for an SBOM with known advisories at different severity levels.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories at known severity levels:
    //   2 Critical, 1 High, 3 Medium, 0 Low
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    create_test_advisory(&app, sbom_id, "critical").await;
    create_test_advisory(&app, sbom_id, "critical").await;
    create_test_advisory(&app, sbom_id, "high").await;
    create_test_advisory(&app, sbom_id, "medium").await;
    create_test_advisory(&app, sbom_id, "medium").await;
    create_test_advisory(&app, sbom_id, "medium").await;

    // When requesting the advisory summary for this SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response contains correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2, "expected 2 critical advisories");
    assert_eq!(summary.high, 1, "expected 1 high advisory");
    assert_eq!(summary.medium, 3, "expected 3 medium advisories");
    assert_eq!(summary.low, 0, "expected 0 low advisories");
    assert_eq!(summary.total, 6, "expected 6 total advisories");
}

/// Verifies that the advisory summary endpoint returns 404 for a non-existent SBOM ID,
/// consistent with existing SBOM endpoint behavior.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let app = setup_test_app().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary for this SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all severity counts as zero.
#[tokio::test]
async fn test_advisory_summary_empty_sbom() {
    // Given an SBOM with no advisories linked
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;

    // When requesting the advisory summary for this SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0, "expected 0 critical advisories");
    assert_eq!(summary.high, 0, "expected 0 high advisories");
    assert_eq!(summary.medium, 0, "expected 0 medium advisories");
    assert_eq!(summary.low, 0, "expected 0 low advisories");
    assert_eq!(summary.total, 0, "expected 0 total advisories");
}

/// Verifies that duplicate advisory links (same advisory linked to the same SBOM
/// multiple times) are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    let advisory_id = create_test_advisory(&app, sbom_id, "high").await;
    // Link the same advisory again (simulating duplicate join table entries)
    link_advisory_to_sbom(&app, sbom_id, advisory_id).await;

    // When requesting the advisory summary for this SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the duplicate is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.high, 1, "expected 1 high advisory (deduplicated)");
    assert_eq!(summary.total, 1, "expected 1 total advisory (deduplicated)");
}
```

## Rationale

- Four tests covering all four Test Requirements from the task description.
- Each test has a documentation comment (required by SKILL.md Step 7 for all AI-generated tests).
- Given-when-then section comments for all tests (all are non-trivial with distinct setup, action, and assertion phases).
- Value-based assertions with descriptive messages on all severity fields (not just total).
- Status code assertions use `assert_eq!` with `StatusCode::OK` / `StatusCode::NOT_FOUND` matching sibling test patterns.
- Test names follow `test_advisory_summary_<scenario>` pattern consistent with sibling naming.
- Helper functions (`setup_test_app`, `create_test_sbom`, `create_test_advisory`, `link_advisory_to_sbom`) would be confirmed by inspecting existing test helpers in `tests/api/advisory.rs` and `tests/api/sbom.rs` via Serena before writing final test code.
