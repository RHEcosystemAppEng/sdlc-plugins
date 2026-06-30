# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task description.

## Detailed Changes

Create a new file with the following contents:

```rust
use actix_http::StatusCode;
use serde_json::Value;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
///
/// Seeds the test database with an SBOM linked to advisories of known severities,
/// then asserts that the response contains the expected counts per severity level.
#[tokio::test]
async fn test_advisory_summary_valid_sbom_with_advisories() {
    // Given an SBOM linked to advisories with known severities:
    // - 2 Critical advisories
    // - 1 High advisory
    // - 3 Medium advisories
    // - 0 Low advisories
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_with_advisories(&app, vec![
        ("adv-1", "Critical"),
        ("adv-2", "Critical"),
        ("adv-3", "High"),
        ("adv-4", "Medium"),
        ("adv-5", "Medium"),
        ("adv-6", "Medium"),
    ]).await;

    // When requesting the advisory summary for that SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response should be 200 with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 3);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Verifies that a non-existent SBOM ID returns 404, consistent with existing SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID
    let app = setup_test_app().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .await;

    // Then the response should be 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all severity counts as zero.
#[tokio::test]
async fn test_advisory_summary_sbom_with_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_without_advisories(&app).await;

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
///
/// When the same advisory is linked to an SBOM multiple times (e.g., through
/// different vulnerability references), it should only be counted once.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM with duplicate advisory links
    // adv-1 (Critical) is linked twice, adv-2 (High) is linked once
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_with_duplicate_advisories(&app, vec![
        ("adv-1", "Critical"),
        ("adv-1", "Critical"),  // duplicate
        ("adv-2", "High"),
    ]).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the duplicated advisory should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 1);  // adv-1 counted once despite duplicate link
    assert_eq!(body["high"], 1);      // adv-2 counted once
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 2);     // only 2 unique advisories
}
```

## Conventions Applied

- **Test location**: Placed in `tests/api/` directory following the project's integration test organization (sibling files: `sbom.rs`, `advisory.rs`, `search.rs`)
- **File naming**: Named `advisory_summary.rs` following the pattern of `sbom.rs`, `advisory.rs` (domain-based naming)
- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` matching the project's assertion pattern
- **Response validation**: Validates specific field values (`critical`, `high`, `medium`, `low`, `total`) not just counts -- ensuring regressions show what changed
- **Error cases**: Includes 404 test for non-existent SBOM ID, consistent with sibling test files
- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom_with_advisories`)
- **Documentation**: Every test function has a `///` doc comment explaining what it verifies (per skill requirement -- this overrides sibling convention)
- **Given-When-Then**: Non-trivial tests include `// Given`, `// When`, `// Then` section comments for navigability
- **Value-based assertions**: Assert on specific severity count values, not just collection lengths
- **Deduplication test**: Explicitly tests that duplicate advisory links produce correct (deduplicated) counts, satisfying the acceptance criterion
- **Async tests**: Uses `#[tokio::test]` for async integration tests, consistent with the Rust async test ecosystem

## Notes

- The test helper functions (`setup_test_app`, `seed_sbom_with_advisories`, etc.) would be defined in a shared test utilities module or within this file, following the project's existing test setup patterns
- The tests hit a real PostgreSQL test database as noted in the project conventions -- no mocking
- The `tests/Cargo.toml` may need to be updated to register the new test file if the project uses explicit test module registration (this would be verified during actual implementation)
