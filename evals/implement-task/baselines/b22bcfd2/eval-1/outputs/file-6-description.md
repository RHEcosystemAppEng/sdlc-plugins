# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all test requirements.

## Pre-Implementation Inspection

- Read `tests/api/advisory.rs` to understand test setup pattern (database seeding, HTTP client initialization, assertion style)
- Read `tests/api/sbom.rs` to understand SBOM-related test patterns (how SBOMs are created in tests, how SBOM IDs are obtained)
- Check `tests/Cargo.toml` for test dependencies and configuration
- Verify test naming convention: expect `test_<endpoint>_<scenario>` pattern

## Detailed Changes

Create a new integration test file:

```rust
//! Integration tests for the advisory severity summary endpoint.

// Test setup imports (exact imports determined by sibling test inspection)
use axum::http::StatusCode;
// ... additional imports for test utilities, database setup, etc.

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
///
/// Seeds the database with an SBOM linked to advisories at various severity levels
/// and asserts the response contains the expected per-level counts and total.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories at known severity levels:
    //   - 2 Critical advisories
    //   - 3 High advisories
    //   - 1 Medium advisory
    //   - 0 Low advisories
    // (seed test database with SBOM, advisories, and sbom_advisory links)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response should be 200 OK with correct counts
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 3);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let non_existent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", non_existent_id))
        .await;

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty_returns_zeros() {
    // Given an SBOM with no linked advisories
    // (seed test database with SBOM only, no sbom_advisory links)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then all counts should be zero
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links to the same SBOM are deduplicated in the count.
///
/// Seeds the database with an SBOM linked to the same advisory via multiple
/// sbom_advisory rows and asserts the advisory is counted only once.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM linked to the same Critical advisory twice via sbom_advisory
    // (seed test database with duplicate sbom_advisory entries for the same advisory)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the advisory should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 1); // Not 2, despite two links
    assert_eq!(summary.total, 1);
}
```

## Notes

- Each test function has a doc comment explaining what it verifies (SKILL.md requirement)
- Non-trivial tests use given-when-then section comments (SKILL.md requirement)
- Assertion style uses `assert_eq!(resp.status(), StatusCode::OK)` pattern matching sibling tests
- Tests assert on specific field values, not just collection lengths (SKILL.md preference for value-based assertions)
- The exact test setup (database seeding, client initialization) will be determined by inspecting sibling test files `tests/api/advisory.rs` and `tests/api/sbom.rs`
- Test naming follows `test_<endpoint>_<scenario>` convention discovered in sibling analysis
- The `tests/Cargo.toml` may need a new entry if the test file needs to be registered (verify against sibling test configuration)
- Run `cargo test` after creating this file to verify all 4 tests pass
