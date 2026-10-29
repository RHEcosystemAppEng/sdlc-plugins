# File 7: tests/api/advisory_summary.rs

**Action**: Create (new file)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all four test requirements from the task description.

## Full File Content

```rust
//! Integration tests for the advisory severity summary endpoint.
//!
//! Tests the GET /api/v2/sbom/{id}/advisory-summary endpoint which returns
//! aggregated advisory severity counts for a given SBOM.

use axum::http::StatusCode;
use serde_json::Value;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
///
/// Seeds an SBOM with advisories of known severities and asserts the response
/// contains the exact expected counts per severity level plus the correct total.
#[tokio::test]
async fn test_severity_summary_with_known_advisories() {
    // Given an SBOM with 2 critical, 1 high, 1 medium, and 0 low advisories
    let app = test_app().await;
    let sbom_id = seed_sbom(&app).await;
    seed_advisory(&app, sbom_id, "critical").await;
    seed_advisory(&app, sbom_id, "critical").await;
    seed_advisory(&app, sbom_id, "high").await;
    seed_advisory(&app, sbom_id, "medium").await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response contains the correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 4);
}

/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_severity_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID
    let app = test_app().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all-zero severity counts.
#[tokio::test]
async fn test_severity_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    let app = test_app().await;
    let sbom_id = seed_sbom(&app).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links for the same advisory are deduplicated
/// in the severity count, so each advisory is counted only once.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisory_links() {
    // Given an SBOM with the same advisory linked twice (duplicate join table entries)
    let app = test_app().await;
    let sbom_id = seed_sbom(&app).await;
    let advisory_id = seed_advisory(&app, sbom_id, "high").await;
    // Link the same advisory again (duplicate)
    link_advisory_to_sbom(&app, sbom_id, advisory_id).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["high"], 1); // Not 2 — deduplicated
    assert_eq!(body["total"], 1);
}
```

## Rationale

- **Test coverage**: All 4 test requirements from the task are covered:
  1. `test_severity_summary_with_known_advisories` -- valid SBOM with known advisories
  2. `test_severity_summary_nonexistent_sbom_returns_404` -- non-existent SBOM
  3. `test_severity_summary_no_advisories_returns_zeros` -- SBOM with no advisories
  4. `test_severity_summary_deduplicates_advisory_links` -- duplicate advisory deduplication

- **Value-based assertions**: Tests assert on specific values (`body["critical"]`, `body["high"]`, etc.) rather than just checking counts or lengths. This follows skill guidance for value-based assertions.

- **Doc comments**: Every test function has a `///` doc comment explaining what it verifies, following skill guidance that overrides sibling patterns for test documentation.

- **Given-when-then**: All tests have `// Given`, `// When`, `// Then` section comments since they have distinct setup, action, and assertion phases (non-trivial tests per skill guidance).

- **Assertion pattern**: Uses `assert_eq!(resp.status(), StatusCode::OK)` matching the sibling test convention in `tests/api/advisory.rs` and `tests/api/sbom.rs`.

- **Parameterized tests**: Not used because sibling tests do not use parameterized test patterns, and the test cases here have different setup requirements (different seed data), making individual functions more appropriate per the Meszaros heuristic.

## Convention Conformance

- File location: `tests/api/` directory matching sibling test files
- File naming: `advisory_summary.rs` follows domain naming (cf. `advisory.rs`, `sbom.rs`)
- Test naming: `test_<action>_<scenario>` pattern (cf. existing tests)
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` matches siblings
- Test database: Uses real PostgreSQL test database via `test_app()` helper (same as sibling tests)
- Async tests: `#[tokio::test]` attribute for async test functions

## Notes

- Helper functions (`test_app`, `seed_sbom`, `seed_advisory`, `link_advisory_to_sbom`) are assumed to exist in the test infrastructure or would be created as test utilities. Their exact signatures would be determined during Step 4 code inspection by examining existing test helpers in `tests/api/sbom.rs` and `tests/api/advisory.rs`.
- The `tests/Cargo.toml` may need to be updated to include the new test file in the test suite, depending on how the project organizes its integration tests (auto-discovery vs. explicit listing).
