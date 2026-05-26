# File 6 — Create: `tests/api/advisory_summary.rs`

## Purpose

Integration tests for `GET /api/v2/sbom/{id}/advisory-summary`. Tests exercise
the full HTTP stack against a real PostgreSQL test database, following the
patterns established in `tests/api/advisory.rs` and `tests/api/sbom.rs`.

## Test Convention Basis (from sibling analysis)

- `assert_eq!(resp.status(), StatusCode::OK)` immediately after the request.
- Body: `let body: SeveritySummary = resp.json().await.unwrap();`
- Field-level assertions on each bucket (not just `total`).
- 404 test uses a valid UUID that was never inserted.
- Naming: `test_<feature>_<scenario>`.
- Setup: shared test helper (e.g., `common::setup_app()`, `TestFixture::new()`).
- Each test is a standalone `#[tokio::test]` (no `#[rstest]` — not used in sibling tests).
- `// Given / // When / // Then` comments for non-trivial tests.
- `///` doc comment on every test function.

## Full File Content

```rust
use reqwest::StatusCode;
use uuid::Uuid;

mod common;

/// Verifies that a valid SBOM with known advisories returns correct per-severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given a bootstrapped app with a seeded SBOM linked to 3 advisories
    // (2 Critical, 1 High, 0 Medium, 0 Low)
    let app = common::setup_app().await;
    let sbom_id = app.seed_sbom_with_advisories(&[
        ("advisory-1", "Critical"),
        ("advisory-2", "Critical"),
        ("advisory-3", "High"),
    ]).await;

    // When requesting the advisory summary for that SBOM
    let resp = app
        .client()
        .get(format!("/api/v2/sbom/{sbom_id}/advisory-summary"))
        .send()
        .await
        .unwrap();

    // Then the response is 200 OK with correct severity bucket counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 3);
}

/// Verifies that requesting a summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a bootstrapped app with no SBOM for the given ID
    let app = common::setup_app().await;
    let nonexistent_id = Uuid::new_v4();

    // When requesting the advisory summary for a non-existent SBOM
    let resp = app
        .client()
        .get(format!("/api/v2/sbom/{nonexistent_id}/advisory-summary"))
        .send()
        .await
        .unwrap();

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all-zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given a seeded SBOM with zero advisory links
    let app = common::setup_app().await;
    let sbom_id = app.seed_sbom_with_advisories(&[]).await;

    // When requesting the advisory summary for that SBOM
    let resp = app
        .client()
        .get(format!("/api/v2/sbom/{sbom_id}/advisory-summary"))
        .send()
        .await
        .unwrap();

    // Then the response is 200 OK with all counts zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links for the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM where the same advisory is linked twice (duplicate rows in sbom_advisory)
    let app = common::setup_app().await;
    let sbom_id = app.seed_sbom_with_duplicate_advisory_link("Critical").await;

    // When requesting the advisory summary for that SBOM
    let resp = app
        .client()
        .get(format!("/api/v2/sbom/{sbom_id}/advisory-summary"))
        .send()
        .await
        .unwrap();

    // Then the response counts each unique advisory only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 1,
        "duplicate advisory links must be deduplicated; expected 1, not 2");
    assert_eq!(body["total"], 1);
}
```

## Notes on Test Helpers

- `common::setup_app()` — returns a test app handle with a dedicated test DB.
  This follows the pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`.
- `app.seed_sbom_with_advisories(&[("id", "severity")])` — seeds the `sbom`, `advisory`,
  and `sbom_advisory` tables. This helper is new; it should be added to the shared `common`
  module in `tests/` following the pattern of existing seed helpers.
- `app.seed_sbom_with_duplicate_advisory_link("severity")` — seeds an SBOM with one
  advisory linked twice in `sbom_advisory` to test deduplication.
- `app.client()` — returns a `reqwest::Client` pre-configured with the test server's base URL.

## Registration in `tests/Cargo.toml`

The new test file must be registered as an integration test target:

```toml
[[test]]
name = "advisory_summary"
path = "api/advisory_summary.rs"
```

This follows the pattern used for `sbom.rs` and `advisory.rs` in the same directory.

## Acceptance Criteria Coverage

| Criterion | Covered By |
|---|---|
| Returns correct severity counts | `test_advisory_summary_valid_sbom` |
| Returns 404 for non-existent SBOM | `test_advisory_summary_not_found` |
| All-zeros for SBOM with no advisories | `test_advisory_summary_no_advisories` |
| Deduplicates duplicate advisory links | `test_advisory_summary_deduplication` |

## Inspection Steps

1. `mcp__serena_backend__get_symbols_overview` on `tests/api/advisory.rs` — confirm setup helper name, test structure, and import style.
2. `mcp__serena_backend__get_symbols_overview` on `tests/api/sbom.rs` — cross-check seed helper patterns.
3. Check `tests/Cargo.toml` for existing `[[test]]` declarations to replicate the registration format.
4. Write the file using the Write tool (new file).
