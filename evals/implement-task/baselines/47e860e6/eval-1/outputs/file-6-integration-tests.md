# File 6 — CREATE `tests/api/advisory_summary.rs`

Integration tests against the real PostgreSQL test DB, following `tests/api/advisory.rs` / `tests/api/sbom.rs` (shared test context, `assert_eq!(resp.status(), StatusCode::...)`). Per skill guidance: `///` doc on every test, Given/When/Then sections, value-based assertions on the whole response struct. Scenarios differ in setup and assertions, so separate tests (no parameterization).

```rust
use axum::http::StatusCode;
use trustify_fundamental::advisory::model::severity_summary::SeveritySummary;

use crate::common::{TestContext, ingest_sbom, ingest_advisory, link_advisory}; // existing helpers used by sibling tests

/// Verifies that an SBOM with known advisories returns the correct count per severity level.
#[tokio::test]
async fn advisory_summary_returns_counts_per_severity() {
    // Given an SBOM linked to 2 critical, 1 high, 3 medium and 1 low advisories
    let ctx = TestContext::new().await;
    let sbom_id = ingest_sbom(&ctx, "sbom-with-advisories").await;
    for (name, severity) in [
        ("ADV-C1", "critical"), ("ADV-C2", "critical"),
        ("ADV-H1", "high"),
        ("ADV-M1", "medium"), ("ADV-M2", "medium"), ("ADV-M3", "medium"),
        ("ADV-L1", "low"),
    ] {
        let adv = ingest_advisory(&ctx, name, severity).await;
        link_advisory(&ctx, sbom_id, adv).await;
    }

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary")).await;

    // Then the counts match each severity level and the total
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(
        body,
        SeveritySummary { critical: 2, high: 1, medium: 3, low: 1, total: 7 }
    );
}

/// Verifies that requesting a summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn advisory_summary_unknown_sbom_returns_404() {
    // Given an SBOM ID that does not exist
    let ctx = TestContext::new().await;
    let missing_id = "urn:uuid:00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{missing_id}/advisory-summary")).await;

    // Then the endpoint responds 404, consistent with GET /api/v2/sbom/{id}
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns zero for every level.
#[tokio::test]
async fn advisory_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no advisories
    let ctx = TestContext::new().await;
    let sbom_id = ingest_sbom(&ctx, "sbom-without-advisories").await;

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary")).await;

    // Then all counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body, SeveritySummary::default());
    assert_eq!(
        body,
        SeveritySummary { critical: 0, high: 0, medium: 0, low: 0, total: 0 }
    );
}

/// Verifies that an advisory linked multiple times to the same SBOM is counted once.
#[tokio::test]
async fn advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM where one high advisory is linked twice and one low advisory once
    let ctx = TestContext::new().await;
    let sbom_id = ingest_sbom(&ctx, "sbom-duplicate-links").await;
    let high = ingest_advisory(&ctx, "ADV-H-DUP", "high").await;
    let low = ingest_advisory(&ctx, "ADV-L1", "low").await;
    link_advisory(&ctx, sbom_id, high).await;
    link_advisory(&ctx, sbom_id, high).await; // duplicate link
    link_advisory(&ctx, sbom_id, low).await;

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary")).await;

    // Then the duplicated advisory contributes exactly one to its level and the total
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(
        body,
        SeveritySummary { critical: 0, high: 1, medium: 0, low: 1, total: 2 }
    );
}
```

Notes:
- Helper names (`TestContext`, ingestion/link helpers, `ctx.get`, `resp.json()`) are taken from whatever `tests/api/advisory.rs` actually uses; if no link helper exists, insert into `sbom_advisory` directly via SeaORM `ActiveModel` in the test setup (if the join table has a unique constraint preventing duplicate rows, the dedup test instead links the same advisory via two distinct paths, e.g. two advisory versions sharing the same advisory ID — confirm against `entity/src/sbom_advisory.rs`).
- If the tests crate requires explicit module registration (e.g. `mod advisory_summary;` in a test `main.rs`/`lib.rs` or a `[[test]]` entry in `tests/Cargo.toml`), that file is outside Files to Modify/Create — flag for user approval in Step 9.
- Run: `cargo test -p <tests-package> advisory_summary` plus `cargo test -p trustify-fundamental` (package names from `cargo metadata`).
