# File 6 (CREATE): `tests/api/advisory_summary.rs`

Integration tests against the real PostgreSQL test DB, following `tests/api/advisory.rs` and
`tests/api/sbom.rs` (test context setup, HTTP client, `assert_eq!(resp.status(), StatusCode::OK)`).
Per skill guidance: every test has a `///` doc comment, Given/When/Then comments, and value-based
assertions on the full response body. The four tests differ in setup and assertions, so they are
individual tests (not parameterized).

```rust
use axum::http::StatusCode;
use trustify_module_fundamental::advisory::model::severity_summary::SeveritySummary;

use crate::common::{TestContext, seed_advisory, seed_sbom, link_sbom_advisory};

/// Verifies that an SBOM with known advisories returns the correct count per severity level.
#[tokio::test]
async fn advisory_summary_returns_counts_per_severity() {
    // Given an SBOM linked to 2 critical, 1 high, 3 medium and 1 low advisories
    let ctx = TestContext::new().await;
    let sbom = seed_sbom(&ctx, "sbom-with-advisories").await;
    for (name, severity) in [
        ("ADV-1", "Critical"), ("ADV-2", "Critical"),
        ("ADV-3", "High"),
        ("ADV-4", "Medium"), ("ADV-5", "Medium"), ("ADV-6", "Medium"),
        ("ADV-7", "Low"),
    ] {
        let advisory = seed_advisory(&ctx, name, severity).await;
        link_sbom_advisory(&ctx, sbom.id, advisory.id).await;
    }

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{}/advisory-summary", sbom.id)).await;

    // Then each severity level and the total match the seeded data
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(
        body,
        SeveritySummary { critical: 2, high: 1, medium: 3, low: 1, total: 7 }
    );
}

/// Verifies that requesting the summary for a non-existent SBOM ID returns 404.
#[tokio::test]
async fn advisory_summary_unknown_sbom_returns_not_found() {
    // Given an SBOM ID that does not exist
    let ctx = TestContext::new().await;
    let missing_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{missing_id}/advisory-summary")).await;

    // Then the response is 404, consistent with GET /api/v2/sbom/{id}
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns zero for every level and the total.
#[tokio::test]
async fn advisory_summary_no_advisories_returns_all_zeros() {
    // Given an SBOM with no linked advisories
    let ctx = TestContext::new().await;
    let sbom = seed_sbom(&ctx, "sbom-without-advisories").await;

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{}/advisory-summary", sbom.id)).await;

    // Then every field is 0
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(
        body,
        SeveritySummary { critical: 0, high: 0, medium: 0, low: 0, total: 0 }
    );
}

/// Verifies that an advisory linked to the same SBOM more than once is counted only once.
#[tokio::test]
async fn advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM linked twice to the same high advisory and once to a low advisory
    let ctx = TestContext::new().await;
    let sbom = seed_sbom(&ctx, "sbom-with-duplicate-links").await;
    let high = seed_advisory(&ctx, "ADV-DUP", "High").await;
    let low = seed_advisory(&ctx, "ADV-LOW", "Low").await;
    link_sbom_advisory(&ctx, sbom.id, high.id).await;
    link_sbom_advisory(&ctx, sbom.id, high.id).await;
    link_sbom_advisory(&ctx, sbom.id, low.id).await;

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{}/advisory-summary", sbom.id)).await;

    // Then the duplicated advisory contributes one to high and to the total
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(
        body,
        SeveritySummary { critical: 0, high: 1, medium: 0, low: 1, total: 2 }
    );
}
```

Notes:
- `TestContext`, seeding helpers, and the HTTP client call (`ctx.get(...)`, `resp.json()`) are replaced by whatever `tests/api/advisory.rs` / `tests/api/sbom.rs` actually use; existing helpers are reused rather than new ones written. If a link-seeding helper does not exist, insert `sbom_advisory::ActiveModel` rows directly in the test.
- Duplicate-link test: if `sbom_advisory` has a unique constraint on `(sbom_id, advisory_id)`, the duplicate cannot be inserted. In that case the test instead links the same advisory through two different paths that both land in the join (or is adjusted with user guidance) — the dedup logic in the query is kept either way.
- If the tests crate compiles `tests/api/*.rs` via a harness root (`mod advisory_summary;`) or `[[test]]` entries in `tests/Cargo.toml`, that registration is outside Files to Modify and is flagged for user approval in Step 9.
- Run: `cargo test -p <tests crate name from cargo metadata>` and `cargo test -p <fundamental crate name>`.
