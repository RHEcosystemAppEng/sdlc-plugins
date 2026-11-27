# File 6 (CREATE): `tests/api/advisory_summary.rs`

Integration tests against the real PostgreSQL test DB, using the same test context /
fixture helpers and HTTP client as `tests/api/advisory.rs` and `tests/api/sbom.rs`.
Siblings use one function per scenario (no `rstest`), so no parameterization. Each test
compares the full `SeveritySummary` (value-based) and has a `///` doc + Given/When/Then.

```rust
use axum::http::StatusCode;
use trustify_module_fundamental::advisory::model::severity_summary::SeveritySummary;
// + sibling test-context / fixture imports (e.g. `use crate::common::*;`)

/// Verifies that an SBOM with known advisories returns correct counts per severity level.
#[tokio::test]
async fn advisory_summary_returns_counts_by_severity() {
    // Given an SBOM linked to 2 critical, 1 high, 3 medium and 1 low advisories
    let ctx = TestContext::new().await;
    let sbom_id = ctx.ingest_sbom("fixture-sbom.json").await;
    ctx.link_advisories(sbom_id, &[
        ("ADV-1", "critical"), ("ADV-2", "critical"), ("ADV-3", "high"),
        ("ADV-4", "medium"), ("ADV-5", "medium"), ("ADV-6", "medium"), ("ADV-7", "low"),
    ]).await;

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary")).await;

    // Then the response contains the exact counts and total
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body, SeveritySummary { critical: 2, high: 1, medium: 3, low: 1, total: 7 });
}

/// Verifies that requesting the summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn advisory_summary_unknown_sbom_returns_404() {
    // Given an SBOM id that does not exist
    let ctx = TestContext::new().await;
    let missing_id = Id::random();

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{missing_id}/advisory-summary")).await;

    // Then the API responds with 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all-zero counts.
#[tokio::test]
async fn advisory_summary_no_advisories_returns_zeros() {
    // Given an SBOM without any linked advisories
    let ctx = TestContext::new().await;
    let sbom_id = ctx.ingest_sbom("fixture-sbom.json").await;

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary")).await;

    // Then every level and the total are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body, SeveritySummary::default());
}

/// Verifies that an advisory linked to the same SBOM more than once is counted once.
#[tokio::test]
async fn advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM where ADV-1 (high) is linked twice and ADV-2 (low) once
    let ctx = TestContext::new().await;
    let sbom_id = ctx.ingest_sbom("fixture-sbom.json").await;
    ctx.link_advisories(sbom_id, &[("ADV-1", "high"), ("ADV-1", "high"), ("ADV-2", "low")]).await;

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary")).await;

    // Then the duplicate link contributes only one high advisory
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body, SeveritySummary { critical: 0, high: 1, medium: 0, low: 0, total: 2 });
}
```

Notes:
- `TestContext`, `ingest_sbom`, `link_advisories`, `get` are placeholders for the actual
  helpers in sibling tests; use those, don't invent new helpers. If inserting duplicate
  `sbom_advisory` rows needs a helper that does not exist, write it locally in this file.
- If the duplicate link is rejected by a unique constraint on `sbom_advisory`, dedup is
  then guaranteed at the schema level; the test should insert the duplicate the way the
  ingestor would (e.g. same advisory via two documents) — confirm during Step 4.
- If `tests/Cargo.toml` requires explicit `[[test]]` entries or a `mod advisory_summary;`
  in a test main file, that edit is outside Files to Create -> Step 9 scope flag for user approval.
