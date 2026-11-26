# File 3 (CREATE): `tests/api/advisory_summary.rs`

Pattern followed: `tests/api/advisory.rs` and `tests/api/sbom.rs` (real PostgreSQL test DB via the
shared test context, `#[tokio::test]`, `assert_eq!(resp.status(), StatusCode::...)`).
Skill overrides applied: `///` doc comment on every test, Given/When/Then sections, value-based
assertions on the whole `SeveritySummary`. No `rstest` (siblings don't use parameterized tests, and the
four cases differ in setup/assertions anyway).

```rust
use axum::http::StatusCode;
use trustify_module_fundamental::advisory::model::severity_summary::SeveritySummary;

use crate::common::{TestContext, advisory_fixture, sbom_fixture};

/// Verifies that an SBOM linked to advisories of known severities returns the correct counts.
#[tokio::test]
async fn valid_sbom_returns_correct_severity_counts() {
    // Given an SBOM linked to 2 critical, 1 high, 1 medium and 1 low advisory
    let ctx = TestContext::new().await;
    let sbom = sbom_fixture(&ctx, "sbom-with-advisories").await;
    for (name, severity) in [
        ("ADV-1", "Critical"),
        ("ADV-2", "Critical"),
        ("ADV-3", "High"),
        ("ADV-4", "Medium"),
        ("ADV-5", "Low"),
    ] {
        let advisory = advisory_fixture(&ctx, name, Some(severity)).await;
        ctx.link_sbom_advisory(&sbom.id, &advisory.id).await;
    }

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{}/advisory-summary", sbom.id)).await;

    // Then the counts per severity match the linked advisories
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(
        body,
        SeveritySummary { critical: 2, high: 1, medium: 1, low: 1, total: 5 }
    );
}

/// Verifies that requesting a summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn nonexistent_sbom_returns_not_found() {
    // Given an SBOM ID that does not exist
    let ctx = TestContext::new().await;
    let missing_id = "urn:uuid:00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{missing_id}/advisory-summary")).await;

    // Then the endpoint responds with 404, consistent with GET /api/v2/sbom/{id}
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns zero for every severity and the total.
#[tokio::test]
async fn sbom_without_advisories_returns_all_zeros() {
    // Given an SBOM with no linked advisories
    let ctx = TestContext::new().await;
    let sbom = sbom_fixture(&ctx, "sbom-without-advisories").await;

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{}/advisory-summary", sbom.id)).await;

    // Then all counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(
        body,
        SeveritySummary { critical: 0, high: 0, medium: 0, low: 0, total: 0 }
    );
}

/// Verifies that an advisory linked to the same SBOM more than once is counted only once.
#[tokio::test]
async fn duplicate_advisory_links_are_deduplicated() {
    // Given an SBOM with one high advisory linked twice and one low advisory linked once
    let ctx = TestContext::new().await;
    let sbom = sbom_fixture(&ctx, "sbom-with-duplicate-links").await;
    let high = advisory_fixture(&ctx, "ADV-HIGH", Some("High")).await;
    let low = advisory_fixture(&ctx, "ADV-LOW", Some("Low")).await;
    ctx.link_sbom_advisory(&sbom.id, &high.id).await;
    ctx.link_sbom_advisory(&sbom.id, &high.id).await;
    ctx.link_sbom_advisory(&sbom.id, &low.id).await;

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{}/advisory-summary", sbom.id)).await;

    // Then each unique advisory is counted exactly once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(
        body,
        SeveritySummary { critical: 0, high: 1, medium: 0, low: 1, total: 2 }
    );
}
```

Notes:
- Fixture/helper names (`TestContext`, `sbom_fixture`, `advisory_fixture`, `link_sbom_advisory`) are
  placeholders for whatever `tests/api/advisory.rs` / `sbom.rs` actually use — they would be replaced with
  the real helpers found in Step 4; no new helper module is created.
- If `sbom_advisory` has a unique constraint on `(sbom_id, advisory_id)`, the duplicate-link case is
  seeded the way the ingestor produces duplicates (e.g., two link rows differing in another key column);
  the assertion still targets dedup by advisory ID.
- Fixture consistency: expected totals (5, 0, 2) equal the sum of buckets for each seeded fixture.
- Registration of this file in the tests crate (if not auto-discovered) is out of scope -> flagged in Step 9.
- Run: `cargo test -p <tests-crate-name> advisory_summary`.
