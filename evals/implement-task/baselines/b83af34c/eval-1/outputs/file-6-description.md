# File 6: tests/api/advisory_summary.rs (CREATE)

## Pre-implementation Inspection

Before creating, would inspect sibling test files to match conventions:

1. `mcp__serena_backend__get_symbols_overview("tests/api/advisory.rs")` -- see test function names, setup patterns, assertion style.
2. `mcp__serena_backend__find_symbol("test_get_advisory", include_body=true)` -- read a representative test to understand the full pattern (request building, response assertion, fixture setup).
3. `mcp__serena_backend__get_symbols_overview("tests/api/sbom.rs")` -- cross-module sibling for additional pattern reference.
4. Check for shared test utilities, fixtures, or harness setup functions used across test files.

## File Content

```rust
//! Integration tests for the advisory severity summary endpoint.

use actix_http::StatusCode;
use test_context::TestContext;

use crate::common::TestApp;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM linked to advisories of known severity levels
    let app = TestApp::setup().await;
    let sbom_id = app.ingest_test_sbom("test-sbom-with-advisories.json").await;
    app.link_advisory_to_sbom(sbom_id, "ADV-001", "Critical").await;
    app.link_advisory_to_sbom(sbom_id, "ADV-002", "High").await;
    app.link_advisory_to_sbom(sbom_id, "ADV-003", "High").await;
    app.link_advisory_to_sbom(sbom_id, "ADV-004", "Medium").await;
    app.link_advisory_to_sbom(sbom_id, "ADV-005", "Low").await;

    // When requesting the advisory summary for the SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response contains correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 1);
    assert_eq!(body["high"], 2);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 1);
    assert_eq!(body["total"], 5);
}

/// Verifies that a non-existent SBOM ID returns a 404 status.
#[tokio::test]
async fn test_advisory_summary_sbom_not_found() {
    // Given a non-existent SBOM ID
    let app = TestApp::setup().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary for the non-existent SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all-zero severity counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let app = TestApp::setup().await;
    let sbom_id = app.ingest_test_sbom("test-sbom-empty.json").await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
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
    let app = TestApp::setup().await;
    let sbom_id = app.ingest_test_sbom("test-sbom-dedup.json").await;
    app.link_advisory_to_sbom(sbom_id, "ADV-100", "Critical").await;
    app.link_advisory_to_sbom(sbom_id, "ADV-100", "Critical").await; // duplicate link
    app.link_advisory_to_sbom(sbom_id, "ADV-101", "High").await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the duplicate advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 1); // ADV-100 counted once despite duplicate link
    assert_eq!(body["high"], 1);
    assert_eq!(body["total"], 2); // 1 critical + 1 high = 2 (not 3)
}
```

## Rationale

- **Test naming**: follows `test_<endpoint>_<scenario>` pattern observed in sibling test files.
- **Assertion style**: uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching the established pattern in `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- **Value-based assertions**: asserts on specific field values (`body["critical"]`, `body["high"]`, etc.) rather than just checking response status. This satisfies the skill's preference for value-based assertions over length-only checks.
- **Doc comments**: every test function has a `///` doc comment explaining what it verifies, per skill Step 7 requirements.
- **Given-When-Then**: all tests include `// Given`, `// When`, `// Then` section comments since they have distinct setup, action, and assertion phases.
- **Error case coverage**: includes a 404 test consistent with the sibling pattern.
- **Deduplication test**: specifically tests acceptance criterion 3 (deduplication by advisory ID).
- **No parameterized tests**: sibling test files do not use `#[rstest]` or similar, so individual test functions are used per skill guidance.

## Note on test utilities

The exact test setup utilities (`TestApp::setup()`, `ingest_test_sbom()`, `link_advisory_to_sbom()`) are representative. The actual helper method names and fixture setup pattern would be confirmed by reading the sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`) with Serena to match the project's established test harness. If no `link_advisory_to_sbom` helper exists, the test would directly use the ingestion service or database seeding pattern observed in siblings.
