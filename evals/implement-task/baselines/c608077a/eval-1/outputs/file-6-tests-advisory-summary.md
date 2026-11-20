# File 6 — CREATE `tests/api/advisory_summary.rs`

Integration tests against the real PostgreSQL test DB, following `tests/api/advisory.rs` / `tests/api/sbom.rs` setup (test context, HTTP client helper, fixture ingestion). Applies skill guidance: `///` doc comment on every test, Given/When/Then sections, value-based assertions on the whole `SeveritySummary`. Individual tests (no `rstest`) since siblings don't use parameterization and each case has different setup/assertions.

Helper names (`TestContext`, `ctx.ingest_sbom`, `ctx.ingest_advisory`, `ctx.link_sbom_advisory`, `ctx.get`) are placeholders to be replaced with the exact helpers used in `tests/api/advisory.rs`.

```rust
use axum::http::StatusCode;
use trustify_module_fundamental::advisory::model::severity_summary::SeveritySummary;

/// Verifies that an SBOM with known advisories returns correct per-severity counts.
#[test_context(TestContext)]
#[tokio::test]
async fn advisory_summary_returns_counts_per_severity(ctx: &TestContext) -> anyhow::Result<()> {
    // Given an SBOM linked to 2 critical, 1 high, 1 medium and 3 low advisories
    let sbom_id = ctx.ingest_sbom("sbom-with-advisories").await?;
    for (name, severity) in [
        ("ADV-1", "critical"), ("ADV-2", "critical"),
        ("ADV-3", "high"),
        ("ADV-4", "medium"),
        ("ADV-5", "low"), ("ADV-6", "low"), ("ADV-7", "low"),
    ] {
        let adv = ctx.ingest_advisory(name, severity).await?;
        ctx.link_sbom_advisory(sbom_id, adv).await?;
    }

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary")).await;

    // Then the counts match each severity level and the total
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await?;
    assert_eq!(
        body,
        SeveritySummary { critical: 2, high: 1, medium: 1, low: 3, total: 7 }
    );
    Ok(())
}

/// Verifies that requesting a summary for a non-existent SBOM returns 404.
#[test_context(TestContext)]
#[tokio::test]
async fn advisory_summary_unknown_sbom_returns_404(ctx: &TestContext) -> anyhow::Result<()> {
    // Given an SBOM ID that does not exist
    let missing_id = "urn:uuid:00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{missing_id}/advisory-summary")).await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
    Ok(())
}

/// Verifies that an SBOM with no linked advisories returns zero for every level.
#[test_context(TestContext)]
#[tokio::test]
async fn advisory_summary_no_advisories_returns_zeros(ctx: &TestContext) -> anyhow::Result<()> {
    // Given an SBOM with no linked advisories
    let sbom_id = ctx.ingest_sbom("sbom-without-advisories").await?;

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary")).await;

    // Then all counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await?;
    assert_eq!(body, SeveritySummary::default());
    assert_eq!(
        body,
        SeveritySummary { critical: 0, high: 0, medium: 0, low: 0, total: 0 }
    );
    Ok(())
}

/// Verifies that an advisory linked to the same SBOM multiple times is counted once.
#[test_context(TestContext)]
#[tokio::test]
async fn advisory_summary_deduplicates_advisory_links(ctx: &TestContext) -> anyhow::Result<()> {
    // Given an SBOM where one high advisory is linked three times and one low advisory once
    let sbom_id = ctx.ingest_sbom("sbom-duplicate-links").await?;
    let high = ctx.ingest_advisory("ADV-DUP", "high").await?;
    for _ in 0..3 {
        ctx.link_sbom_advisory(sbom_id, high).await?;
    }
    let low = ctx.ingest_advisory("ADV-SINGLE", "low").await?;
    ctx.link_sbom_advisory(sbom_id, low).await?;

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary")).await;

    // Then the duplicated advisory contributes a single count
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await?;
    assert_eq!(
        body,
        SeveritySummary { critical: 0, high: 1, medium: 0, low: 1, total: 2 }
    );
    Ok(())
}
```

Notes:
- If `sbom_advisory` has a unique constraint on `(sbom_id, advisory_id)` preventing duplicate rows, the dedup test instead links the same advisory through multiple paths (e.g., re-ingesting the same advisory document / multiple package matches) — whatever produces duplicate join results in practice. Fixture approach confirmed during Step 4 by inspecting `entity/src/sbom_advisory.rs`.
- If `tests/Cargo.toml` declares test targets explicitly, a `[[test]]` entry would be needed — out of scope, flagged to user in Step 9 rather than edited.
- Run: `cargo test -p <tests-crate> --test advisory_summary` and `cargo test -p trustify-module-fundamental` (names resolved via `cargo metadata`).
