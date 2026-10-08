# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the new GET `/api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task description.

## Pre-Implementation Analysis

Before creating, would analyze sibling test files:
- Read `tests/api/advisory.rs` -- understand test setup, HTTP client usage, assertion patterns
- Read `tests/api/sbom.rs` -- understand SBOM-related test patterns and test data setup
- Read `tests/Cargo.toml` -- verify test dependencies and crate name

### Crate name resolution

Would run `cargo metadata --no-deps --format-version 1` from the workspace root to resolve
the crate name for `tests/api/advisory_summary.rs`. The crate name comes from the `name`
field in the package whose manifest path matches `tests/Cargo.toml` -- it is NOT derived
by reading `Cargo.toml` directly. This resolved name is used for `cargo test -p <crate-name>`.

### Test convention conformance

From sibling analysis:
- Tests use real PostgreSQL test database
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` for status
- Response bodies parsed from JSON and compared with `assert_eq!` on specific values
- Test functions prefixed with `test_`

### Skill overrides applied

- **Value-based assertions** over length-only checks (skill guidance)
- **Doc comments** on every test function (skill guidance, overrides sibling patterns if siblings lack them)
- **given-when-then** section comments for non-trivial tests (skill guidance)

## File Content

```rust
use axum::http::StatusCode;

// Test setup imports would follow sibling patterns from tests/api/advisory.rs

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_known_advisories() {
    // Given an SBOM with known advisories at various severity levels
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    create_test_advisory(&app, sbom_id, "Critical").await;
    create_test_advisory(&app, sbom_id, "Critical").await;
    create_test_advisory(&app, sbom_id, "High").await;
    create_test_advisory(&app, sbom_id, "Medium").await;
    create_test_advisory(&app, sbom_id, "Low").await;
    create_test_advisory(&app, sbom_id, "Low").await;
    create_test_advisory(&app, sbom_id, "Low").await;

    // When requesting the advisory severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response contains correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 3);
    assert_eq!(body["total"], 7);
}

/// Verifies that a non-existent SBOM ID returns a 404 response.
#[tokio::test]
async fn test_severity_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID
    let app = setup_test_app().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .await;

    // Then a 404 status is returned
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all-zero severity counts.
#[tokio::test]
async fn test_severity_summary_empty_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;

    // When requesting the advisory severity summary
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
async fn test_severity_summary_deduplicates_advisory_links() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    let advisory_id = create_test_advisory(&app, sbom_id, "High").await;
    // Link the same advisory a second time to create a duplicate
    link_advisory_to_sbom(&app, sbom_id, advisory_id).await;

    // When requesting the advisory severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["high"], 1); // Not 2, despite being linked twice
    assert_eq!(body["total"], 1);
}
```

## Key Decisions

- **Value-based assertions**: All tests assert on specific field values (`assert_eq!(body["critical"], 2)`) rather than length checks -- per skill guidance
- **Doc comments**: Every test function has a `///` doc comment explaining what it verifies -- per skill guidance (overrides sibling pattern if siblings lack them)
- **given-when-then**: All tests use `// Given`, `// When`, `// Then` section comments since they have distinct setup, action, and assertion phases -- per skill guidance
- **Test names**: Follow `test_` prefix + descriptive snake_case matching sibling convention in `tests/api/advisory.rs`
- **Status assertions**: `assert_eq!(resp.status(), StatusCode::OK)` pattern matches sibling test convention
- **Coverage**: All 4 test requirements from the task are covered:
  1. Valid SBOM with known advisories returns correct counts
  2. Non-existent SBOM returns 404
  3. SBOM with no advisories returns all zeros
  4. Duplicate advisory links are deduplicated

## Test Execution Plan

After writing tests, would run:

1. Resolve crate name: `cargo metadata --no-deps --format-version 1` from workspace root, find package whose manifest or target source contains `tests/api/advisory_summary.rs`
2. Run tests: `cargo test -p <resolved-crate-name>` (or `cargo nextest run -p <resolved-crate-name>` if project uses nextest)
3. Hard stop on failure -- fix and re-run until passing before proceeding to Step 8
