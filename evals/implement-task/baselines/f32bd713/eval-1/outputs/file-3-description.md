# File 3: tests/api/advisory_summary.rs

**Action**: Create

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering
the four test requirements from the task description.

## Pre-implementation inspection

Before creating this file, would inspect siblings using Serena:

- `mcp__serena_backend__get_symbols_overview` on `tests/api/advisory.rs` -- understand test setup, assertions, imports, and helper functions
- `mcp__serena_backend__get_symbols_overview` on `tests/api/sbom.rs` -- cross-reference with another domain's test file for consistency
- `mcp__serena_backend__find_symbol` with `include_body=true` on a test function in `tests/api/advisory.rs` -- read full test body to understand setup/teardown, database seeding, HTTP client usage
- `mcp__serena_backend__search_for_pattern` for test helper functions (e.g., test database setup, HTTP client creation, test data seeding)
- Check `tests/Cargo.toml` for test dependencies and the crate name

Also check for parameterized test usage in siblings:
- Grep for `rstest` or `#[case]` in `tests/api/` directory -- if not found, do not introduce parameterized tests

## Detailed changes

```rust
use axum::http::StatusCode;
use serde_json::Value;

// Test helper imports would be confirmed from sibling test inspection
use crate::helpers::{setup_test_app, seed_sbom, seed_advisory, link_advisory_to_sbom};

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    let app = setup_test_app().await;
    let sbom_id = seed_sbom(&app.db).await;
    let adv_critical = seed_advisory(&app.db, "critical").await;
    let adv_high = seed_advisory(&app.db, "high").await;
    let adv_medium = seed_advisory(&app.db, "medium").await;
    link_advisory_to_sbom(&app.db, adv_critical, sbom_id).await;
    link_advisory_to_sbom(&app.db, adv_high, sbom_id).await;
    link_advisory_to_sbom(&app.db, adv_medium, sbom_id).await;

    // When requesting the advisory summary for the SBOM
    let resp = app
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response contains correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 1);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 3);
}

/// Verifies that a non-existent SBOM ID returns 404, consistent with existing SBOM endpoints.
#[tokio::test]
async fn test_severity_summary_not_found() {
    // Given a non-existent SBOM ID
    let app = setup_test_app().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = app
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .send()
        .await;

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all severity counts as zero.
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let app = setup_test_app().await;
    let sbom_id = seed_sbom(&app.db).await;

    // When requesting the advisory summary
    let resp = app
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then all counts are zero
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
async fn test_severity_summary_deduplicates_advisories() {
    // Given an SBOM with the same advisory linked twice
    let app = setup_test_app().await;
    let sbom_id = seed_sbom(&app.db).await;
    let adv_high = seed_advisory(&app.db, "high").await;
    link_advisory_to_sbom(&app.db, adv_high, sbom_id).await;
    link_advisory_to_sbom(&app.db, adv_high, sbom_id).await; // duplicate link

    // When requesting the advisory summary
    let resp = app
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the duplicate is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["high"], 1);
    assert_eq!(body["total"], 1);
}
```

## Conventions applied

- Test file named `advisory_summary.rs` following the domain naming convention in `tests/api/`
- Uses `#[tokio::test]` async tests, matching sibling test patterns
- `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern from sibling analysis
- Value-based assertions on specific severity counts (per SKILL.md -- not just length checks)
- `///` doc comment on every test function (per SKILL.md requirement)
- `// Given`, `// When`, `// Then` section comments on all tests (per SKILL.md -- non-trivial tests)
- No parameterized tests (siblings do not use them)
- Test function names use `test_` prefix with descriptive snake_case names
- Each test is self-contained with its own setup

## Notes

- The exact test helper functions (`setup_test_app`, `seed_sbom`, etc.) would be confirmed by inspecting sibling test files
- If siblings use a different HTTP client pattern (e.g., `reqwest::Client` directly), would match that pattern
- The duplicate link test assumes the join table allows duplicates; if it has a unique constraint, the test setup would need adjustment (would be discovered during Serena inspection of `entity/src/sbom_advisory.rs`)
- The `tests/Cargo.toml` may need updating to include the new test file in its test targets -- would check during scope containment in Step 9
