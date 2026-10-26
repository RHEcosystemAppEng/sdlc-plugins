# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the GET /api/v2/sbom/{id}/advisory-summary endpoint, covering all four test requirements.

## Pre-Implementation Inspection

Before creating, would:
1. `mcp__serena_backend__get_symbols_overview` on `tests/api/advisory.rs` to understand test structure, imports, test setup pattern, assertion style
2. `mcp__serena_backend__get_symbols_overview` on `tests/api/sbom.rs` to see SBOM-related test patterns and how test SBOMs are created
3. `mcp__serena_backend__find_symbol` with `include_body=true` on a representative test function from `tests/api/advisory.rs` to see the full test body (setup, HTTP call, assertions)
4. Check how the test database is bootstrapped -- look for test utilities, fixtures, or setup functions
5. Verify `tests/Cargo.toml` to ensure the test crate has the necessary dependencies

Also need to check if `tests/api/mod.rs` (or equivalent) exists and whether new test files need to be registered there.

## File Content

```rust
use axum::http::StatusCode;
use serde_json::Value;

// Import test utilities following the pattern from sibling test files
// (exact imports depend on the project's test infrastructure)
use crate::common::setup_test_app; // or whatever the test setup pattern is

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_valid_sbom_severity_counts() {
    // Given an SBOM linked to advisories with known severity levels
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    create_test_advisory(&app, sbom_id, "Critical").await;
    create_test_advisory(&app, sbom_id, "Critical").await;
    create_test_advisory(&app, sbom_id, "High").await;
    create_test_advisory(&app, sbom_id, "Medium").await;
    create_test_advisory(&app, sbom_id, "Low").await;
    create_test_advisory(&app, sbom_id, "Low").await;

    // When requesting the advisory summary for the SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response contains correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = serde_json::from_slice(resp.body()).unwrap();
    assert_eq!(body["critical"], 2, "expected 2 critical advisories");
    assert_eq!(body["high"], 1, "expected 1 high advisory");
    assert_eq!(body["medium"], 1, "expected 1 medium advisory");
    assert_eq!(body["low"], 2, "expected 2 low advisories");
    assert_eq!(body["total"], 6, "expected 6 total advisories");
}

/// Verifies that a non-existent SBOM ID returns a 404 status code.
#[tokio::test]
async fn test_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID
    let app = setup_test_app().await;
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
async fn test_sbom_with_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = serde_json::from_slice(resp.body()).unwrap();
    assert_eq!(body["critical"], 0, "critical should be 0 with no advisories");
    assert_eq!(body["high"], 0, "high should be 0 with no advisories");
    assert_eq!(body["medium"], 0, "medium should be 0 with no advisories");
    assert_eq!(body["low"], 0, "low should be 0 with no advisories");
    assert_eq!(body["total"], 0, "total should be 0 with no advisories");
}

/// Verifies that duplicate advisory links to the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_duplicate_advisories_are_deduplicated() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    let advisory_id = create_test_advisory(&app, sbom_id, "High").await;
    // Link the same advisory again to simulate duplicate links
    link_advisory_to_sbom(&app, advisory_id, sbom_id).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the duplicate is counted only once
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = serde_json::from_slice(resp.body()).unwrap();
    assert_eq!(body["high"], 1, "duplicate advisory should be counted once");
    assert_eq!(body["total"], 1, "total should reflect deduplicated count");
}
```

## Notes

- **Test infrastructure:** The exact setup functions (`setup_test_app`, `create_test_sbom`, `create_test_advisory`, `link_advisory_to_sbom`) would be determined by reading sibling test files. The code above uses placeholder names -- actual implementation would match the project's test helper patterns.
- **Assertion style:** Uses `assert_eq!` with specific values rather than length-only checks, following the skill's "prefer value-based assertions" guidance.
- **Doc comments:** Every test function has a `///` doc comment explaining what it verifies, as required by the skill.
- **Given-When-Then:** All tests include `// Given`, `// When`, `// Then` section comments as they are non-trivial (each has distinct setup, action, and assertion phases).
- **Test naming:** Uses `test_<descriptive_name>` pattern consistent with sibling test files.
- **No parameterized tests:** The four test cases exercise different behaviors (valid counts, 404 error, empty result, deduplication) with different setup and assertion logic. Per the Meszaros heuristic, they should be individual tests, not parameterized. Additionally, would verify from sibling analysis whether the project uses parameterized tests at all.
- **Test registration:** Would check if `tests/api/mod.rs` requires a `mod advisory_summary;` line. If so, would add it (and flag it as an out-of-scope modification in Step 9's scope containment check, requesting user approval).
- **Database setup:** Tests assume a test database is bootstrapped automatically by the test harness (common in Rust integration test suites). Would verify by reading sibling test files.
- **Response body parsing:** Uses `serde_json::Value` for flexible assertion. Could alternatively deserialize into `SeveritySummary` struct directly if the test crate has access to the model types -- would match sibling pattern.
- **Cargo metadata for test execution:** Would run `cargo metadata --no-deps --format-version 1` to resolve the test crate name. Then execute `cargo test -p <test-crate-name>` (or `cargo test --test advisory_summary` if integration tests are in the workspace root's `tests/` directory) to run these specific tests.
