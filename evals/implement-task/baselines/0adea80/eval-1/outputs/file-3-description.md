# File 3: `tests/api/advisory_summary.rs` (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests cover correct severity counts, 404 for missing SBOMs, zero counts for SBOMs with no advisories, and deduplication of advisory links.

## Detailed Changes

### Test module

```rust
use reqwest::StatusCode;
use serde_json::Value;

// Test helpers would be imported from a shared test utilities module,
// following the pattern established by tests/api/sbom.rs and tests/api/advisory.rs.

/// Test that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_advisories() {
    // Setup: create test SBOM, link advisories with known severities
    // (e.g., 2 Critical, 1 High, 3 Medium, 0 Low)
    let app = test_app().await;
    let sbom_id = seed_sbom(&app).await;
    seed_advisory(&app, &sbom_id, "critical").await;
    seed_advisory(&app, &sbom_id, "critical").await;
    seed_advisory(&app, &sbom_id, "high").await;
    seed_advisory(&app, &sbom_id, "medium").await;
    seed_advisory(&app, &sbom_id, "medium").await;
    seed_advisory(&app, &sbom_id, "medium").await;

    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 3);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Test that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_severity_summary_sbom_not_found() {
    let app = test_app().await;

    let resp = app
        .get("/api/v2/sbom/nonexistent-id/advisory-summary")
        .await;

    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Test that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    let app = test_app().await;
    let sbom_id = seed_sbom(&app).await;

    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Test that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    let app = test_app().await;
    let sbom_id = seed_sbom(&app).await;
    let advisory_id = seed_advisory(&app, &sbom_id, "critical").await;
    // Link the same advisory again (duplicate join table entry)
    link_advisory_to_sbom(&app, &sbom_id, &advisory_id).await;

    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    // Despite being linked twice, should count as 1
    assert_eq!(body["critical"], 1);
    assert_eq!(body["total"], 1);
}
```

## Conventions Followed

- **Test framework**: Uses `#[tokio::test]` for async tests, matching the existing integration test files.
- **Status assertions**: Uses `assert_eq!(resp.status(), StatusCode::OK)` pattern from `tests/api/sbom.rs` and `tests/api/advisory.rs`.
- **Test database**: Tests hit a real PostgreSQL test database (set up via test helpers), following the project convention.
- **Test isolation**: Each test seeds its own data, ensuring independence.
- **File placement**: Located in `tests/api/` alongside `sbom.rs` and `advisory.rs`, following the integration test directory convention.
- **Naming**: File named `advisory_summary.rs` using snake_case, matching sibling test file naming.
- **Helper functions**: Uses seeding helpers (`seed_sbom`, `seed_advisory`, `link_advisory_to_sbom`) that would follow patterns from existing test setup code. The exact helper implementations depend on the test infrastructure already present in the codebase.

## Notes

- The test helper functions (`test_app`, `seed_sbom`, `seed_advisory`, `link_advisory_to_sbom`) are shown as abstractions. The actual implementation would follow the existing test setup patterns used in `tests/api/sbom.rs` and `tests/api/advisory.rs`.
- The `tests/Cargo.toml` may need to include the new test file in its test targets, depending on how test discovery is configured (Rust auto-discovers by default in the `tests/` directory, but if using a `[[test]]` manifest table, the new file would need an entry).
