# File 3: `tests/api/advisory_summary.rs` (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Covers the four test requirements: correct severity counts, 404 for missing SBOMs, zero counts for SBOMs with no advisories, and deduplication of advisory links.

## Detailed Changes

### Test module

```rust
use reqwest::StatusCode;
use serde_json::Value;

// Test helpers would be imported from a shared test utilities module,
// following the pattern established by tests/api/sbom.rs and tests/api/advisory.rs.

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_advisories() {
    // Given an SBOM with advisories at known severity levels
    let app = test_app().await;
    let sbom_id = seed_sbom(&app).await;
    seed_advisory(&app, &sbom_id, "critical").await;
    seed_advisory(&app, &sbom_id, "critical").await;
    seed_advisory(&app, &sbom_id, "high").await;
    seed_advisory(&app, &sbom_id, "medium").await;
    seed_advisory(&app, &sbom_id, "medium").await;
    seed_advisory(&app, &sbom_id, "medium").await;

    // When requesting the advisory summary for that SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response contains correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 3);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_severity_summary_sbom_not_found() {
    // Given a non-existent SBOM ID
    let app = test_app().await;

    // When requesting the advisory summary for that ID
    let resp = app
        .get("/api/v2/sbom/nonexistent-id/advisory-summary")
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all-zero severity counts.
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let app = test_app().await;
    let sbom_id = seed_sbom(&app).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then all severity counts are 0
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links in the join table are deduplicated in the count.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    // Given an SBOM with the same advisory linked twice
    let app = test_app().await;
    let sbom_id = seed_sbom(&app).await;
    let advisory_id = seed_advisory(&app, &sbom_id, "critical").await;
    // Link the same advisory again (duplicate join table entry)
    link_advisory_to_sbom(&app, &sbom_id, &advisory_id).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the advisory is counted only once despite being linked twice
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 1);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 1);
}
```

## Conventions Followed

- **Test framework**: Uses `#[tokio::test]` for async tests, matching the existing integration test files in `tests/api/`.
- **Status code assertions**: Uses `assert_eq!(resp.status(), StatusCode::OK)` pattern from `tests/api/sbom.rs` and `tests/api/advisory.rs`.
- **Value-based assertions**: Asserts on specific field values (not just lengths or `.any()` checks), following the skill's guidance to prefer value-based assertions over length-only checks. Each severity level is checked individually.
- **Test database**: Tests hit a real PostgreSQL test database via test helpers, following the project convention.
- **Test isolation**: Each test seeds its own data, ensuring independence between tests.
- **File placement**: Located in `tests/api/` alongside `sbom.rs`, `advisory.rs`, and `search.rs`, following the integration test directory convention.
- **Naming**: File named `advisory_summary.rs` using snake_case. Test functions follow `test_<endpoint>_<scenario>` pattern.
- **Doc comments**: Every test function has a `///` doc comment explaining what it verifies, as required by the skill's test documentation standard.
- **Given-when-then structure**: Non-trivial tests include `// Given`, `// When`, `// Then` section comments for navigability, following the skill's guidance.
- **Error case coverage**: Includes a 404 test consistent with the pattern in sibling test files.

## Notes

- The test helper functions (`test_app`, `seed_sbom`, `seed_advisory`, `link_advisory_to_sbom`) are shown as abstractions. Their actual implementation would follow the existing test setup patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`.
- The `tests/Cargo.toml` may need to include the new test file in its test targets if using explicit `[[test]]` manifest entries. Rust auto-discovers test files in the `tests/` directory by default.
