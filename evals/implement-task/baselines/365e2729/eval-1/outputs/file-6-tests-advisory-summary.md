# File 6 (CREATE): `tests/api/advisory_summary.rs`

## Purpose
Integration tests for `GET /api/v2/sbom/{id}/advisory-summary`, covering all four Test
Requirements.

## Conventions followed
- Mirrors `tests/api/advisory.rs` and `tests/api/sbom.rs`: real PostgreSQL test DB through the
  shared test context, `assert_eq!(resp.status(), StatusCode::...)`.
- Skill overrides: every test has a `///` doc comment and given/when/then sections, and the
  assertions compare the whole `SeveritySummary` value rather than only status or count.
- No parameterization: the four tests differ in setup and assertion shape (Meszaros heuristic).

## Content

```rust
use axum::http::StatusCode;
use trustify_module_fundamental::advisory::model::severity_summary::SeveritySummary;

// The helper names below (TestContext, ingest_sbom, ingest_advisory, link_advisory, get)
// mirror whatever sibling tests in tests/api/advisory.rs and tests/api/sbom.rs use.
use crate::common::TestContext;

/// Verifies that an SBOM with known advisories returns the correct count per severity level.
#[tokio::test]
async fn advisory_summary_returns_counts_per_severity() {
    // Given an SBOM linked to 2 critical, 1 high, 3 medium and 1 low advisory
    let ctx = TestContext::new().await;
    let sbom_id = ctx.ingest_sbom("sbom-with-advisories").await;
    for (name, severity) in [
        ("ADV-C1", "Critical"), ("ADV-C2", "Critical"),
        ("ADV-H1", "High"),
        ("ADV-M1", "Medium"), ("ADV-M2", "Medium"), ("ADV-M3", "Medium"),
        ("ADV-L1", "Low"),
    ] {
        let advisory_id = ctx.ingest_advisory(name, severity).await;
        ctx.link_advisory(&sbom_id, &advisory_id).await;
    }

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary")).await;

    // Then each severity count and the total match the linked advisories
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(
        body,
        SeveritySummary { critical: 2, high: 1, medium: 3, low: 1, total: 7 }
    );
}

/// Verifies that requesting a summary for a non-existent SBOM ID returns 404.
#[tokio::test]
async fn advisory_summary_unknown_sbom_returns_not_found() {
    let ctx = TestContext::new().await;

    let resp = ctx
        .get("/api/v2/sbom/urn:uuid:00000000-0000-0000-0000-000000000000/advisory-summary")
        .await;

    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an existing SBOM with no linked advisories returns zero for every level.
#[tokio::test]
async fn advisory_summary_no_advisories_returns_all_zeros() {
    // Given an SBOM with no linked advisories
    let ctx = TestContext::new().await;
    let sbom_id = ctx.ingest_sbom("sbom-without-advisories").await;

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary")).await;

    // Then the request succeeds and every count is zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body, SeveritySummary::default());
    assert_eq!(
        body,
        SeveritySummary { critical: 0, high: 0, medium: 0, low: 0, total: 0 }
    );
}

/// Verifies that an advisory linked to the same SBOM more than once is counted only once.
#[tokio::test]
async fn advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM where one high advisory is linked twice and one low advisory once
    let ctx = TestContext::new().await;
    let sbom_id = ctx.ingest_sbom("sbom-duplicate-links").await;
    let high = ctx.ingest_advisory("ADV-DUP-H", "High").await;
    let low = ctx.ingest_advisory("ADV-DUP-L", "Low").await;
    ctx.link_advisory(&sbom_id, &high).await;
    ctx.link_advisory(&sbom_id, &high).await; // duplicate link
    ctx.link_advisory(&sbom_id, &low).await;

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary")).await;

    // Then the duplicated advisory contributes a single count
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(
        body,
        SeveritySummary { critical: 0, high: 1, medium: 0, low: 1, total: 2 }
    );
}
```

## Notes
- If `sbom_advisory` has a unique constraint on `(sbom_id, advisory_id)`, a literal duplicate row
  cannot be inserted. In that case the dedup test models the real duplication source, for example
  the same advisory reached through two distinct join rows (different package or status
  columns). This would be checked against `entity/src/sbom_advisory.rs` first.
- Test registration: if `tests/Cargo.toml` declares each test file as an explicit `[[test]]`
  target, or tests are aggregated via a `tests/api/main.rs`/`mod.rs`, the new file needs
  registering there. That file is not in Files to Modify, so it would be flagged as out of scope
  for user approval in Step 9 rather than edited silently.
- Run: `cargo test -p <tests-crate-name>` (package resolved via `cargo metadata`) plus
  `cargo test -p trustify-module-fundamental`.
