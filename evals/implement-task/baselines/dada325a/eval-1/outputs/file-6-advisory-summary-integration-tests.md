# File 6 (CREATE): `tests/api/advisory_summary.rs`

## Purpose
Integration tests covering all four Test Requirements, run against the real PostgreSQL test database like
`tests/api/advisory.rs` and `tests/api/sbom.rs`.

## Content
```rust
use axum::http::StatusCode;
use trustify_module_fundamental::advisory::model::severity_summary::SeveritySummary;

// Test context / app helpers and fixture seeding helpers are the same ones used in
// tests/api/advisory.rs (e.g. `TestContext`, `ctx.ingest_sbom(..)`, `ctx.ingest_advisory(..)`,
// `ctx.link_advisory(..)`, `ctx.get(..)`).
use crate::common::*;

/// Verifies that an SBOM with known advisories returns the correct count for each severity level.
#[tokio::test]
async fn severity_summary_returns_counts_for_known_advisories() {
    // Given an SBOM linked to 2 critical, 1 high, 3 medium and 0 low advisories
    let ctx = TestContext::new().await;
    let sbom_id = ctx.ingest_sbom("fixtures/sbom-basic.json").await;
    for (name, severity) in [
        ("ADV-1", "critical"), ("ADV-2", "critical"),
        ("ADV-3", "high"),
        ("ADV-4", "medium"), ("ADV-5", "medium"), ("ADV-6", "medium"),
    ] {
        let adv = ctx.ingest_advisory(name, severity).await;
        ctx.link_advisory(sbom_id, adv).await;
    }

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary")).await;

    // Then the response is 200 with exact per-level counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(
        body,
        SeveritySummary { critical: 2, high: 1, medium: 3, low: 0, total: 6 }
    );
}

/// Verifies that requesting the summary for a non-existent SBOM ID returns 404.
#[tokio::test]
async fn severity_summary_returns_404_for_unknown_sbom() {
    // Given an SBOM ID that does not exist
    let ctx = TestContext::new().await;
    let missing_id = uuid::Uuid::new_v4();

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{missing_id}/advisory-summary")).await;

    // Then the response is 404, consistent with GET /api/v2/sbom/{id}
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns zero for every level and the total.
#[tokio::test]
async fn severity_summary_returns_zeros_when_no_advisories() {
    // Given an SBOM with no advisories linked
    let ctx = TestContext::new().await;
    let sbom_id = ctx.ingest_sbom("fixtures/sbom-basic.json").await;

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary")).await;

    // Then every count is zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(
        body,
        SeveritySummary { critical: 0, high: 0, medium: 0, low: 0, total: 0 }
    );
}

/// Verifies that an advisory linked to the same SBOM more than once is counted only once.
#[tokio::test]
async fn severity_summary_deduplicates_advisory_links() {
    // Given one high advisory linked twice and one low advisory linked once
    let ctx = TestContext::new().await;
    let sbom_id = ctx.ingest_sbom("fixtures/sbom-basic.json").await;
    let high = ctx.ingest_advisory("ADV-DUP", "high").await;
    ctx.link_advisory(sbom_id, high).await;
    ctx.link_advisory(sbom_id, high).await; // duplicate link (e.g. via a second package)
    let low = ctx.ingest_advisory("ADV-LOW", "low").await;
    ctx.link_advisory(sbom_id, low).await;

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary")).await;

    // Then the duplicated advisory contributes exactly 1 to its level and to the total
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(
        body,
        SeveritySummary { critical: 0, high: 1, medium: 0, low: 1, total: 2 }
    );
}
```

## Notes
- The fixture helper names are placeholders and get replaced by the actual helpers in `tests/api/advisory.rs`
  (found with `get_symbols_overview` in a live run). No new shared helpers are added outside this file.
- If the `sbom_advisory` table has a unique constraint on `(sbom_id, advisory_id)`, a duplicate link can't be
  inserted directly. In that case the dedup test links the same advisory through two distinct paths (e.g. two
  packages or ingestion runs) that produce two join rows, matching how duplicates actually arise.
- Assertions compare whole deserialized structs (value-based, per the skill guidance) instead of only status or length.
- No parameterization: the four tests differ in setup and expected status, so they're separate tests by the Meszaros heuristic.
- Registration: if the tests crate needs a `mod advisory_summary;` entry or a `[[test]]` entry in `tests/Cargo.toml`,
  that file is out of scope and flagged for user approval at Step 9.
- Run with `cargo test -p <tests-crate>`, with the name resolved via `cargo metadata`. A failure is a hard stop before commit.
