# File 6 — CREATE `tests/api/advisory_summary.rs`

**Purpose**: integration tests for `GET /api/v2/sbom/{id}/advisory-summary`, covering all 4 Test
Requirements.

**Pattern followed**: `tests/api/advisory.rs` and `tests/api/sbom.rs`. These use the real PostgreSQL test DB, the
shared test context/app helpers, and `assert_eq!(resp.status(), StatusCode::OK)`. The fixture helper names
below (`TestContext`, `ingest_sbom`, `ingest_advisory`, `link_advisory`) are placeholders. The real names
come from the sibling tests.

**Skill guidance applied**: every test has a `///` doc comment and Given/When/Then sections, and the
assertions compare the whole `SeveritySummary` value. There are no parameterized tests, because the
siblings do not use `rstest` and each case has different setup and assertions.

```rust
use axum::http::StatusCode;
use trustify_module_fundamental::advisory::model::severity_summary::SeveritySummary;

use crate::common::TestContext; // sibling test harness

/// Verifies that an SBOM with known advisories returns the correct count for each severity level.
#[tokio::test]
async fn test_severity_summary_returns_correct_counts() {
    // Given an SBOM linked to 2 critical, 1 high, 3 medium and 1 low advisories
    let ctx = TestContext::new().await;
    let sbom = ctx.ingest_sbom("sbom-with-advisories").await;
    for (id, sev) in [
        ("ADV-1", "Critical"), ("ADV-2", "Critical"), ("ADV-3", "High"),
        ("ADV-4", "Medium"), ("ADV-5", "Medium"), ("ADV-6", "Medium"), ("ADV-7", "Low"),
    ] {
        let adv = ctx.ingest_advisory(id, sev).await;
        ctx.link_advisory(&sbom, &adv).await;
    }

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{}/advisory-summary", sbom.id)).await;

    // Then the response is 200 with the exact counts per level
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(
        body,
        SeveritySummary { critical: 2, high: 1, medium: 3, low: 1, total: 7 }
    );
}

/// Verifies that requesting the summary for a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_severity_summary_nonexistent_sbom_returns_404() {
    // Given an SBOM ID that does not exist
    let ctx = TestContext::new().await;
    let missing_id = ctx.random_sbom_id();

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{missing_id}/advisory-summary")).await;

    // Then the response is 404, consistent with GET /api/v2/sbom/{id}
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns zero for every level and for the total.
#[tokio::test]
async fn test_severity_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    let ctx = TestContext::new().await;
    let sbom = ctx.ingest_sbom("sbom-without-advisories").await;

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{}/advisory-summary", sbom.id)).await;

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
async fn test_severity_summary_deduplicates_advisories() {
    // Given an SBOM where one high advisory is linked twice, plus one distinct low advisory
    let ctx = TestContext::new().await;
    let sbom = ctx.ingest_sbom("sbom-duplicate-links").await;
    let high = ctx.ingest_advisory("ADV-DUP", "High").await;
    let low = ctx.ingest_advisory("ADV-LOW", "Low").await;
    ctx.link_advisory(&sbom, &high).await;
    ctx.link_advisory(&sbom, &high).await; // duplicate link
    ctx.link_advisory(&sbom, &low).await;

    // When requesting the advisory summary
    let resp = ctx.get(&format!("/api/v2/sbom/{}/advisory-summary", sbom.id)).await;

    // Then the duplicated advisory is counted once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(
        body,
        SeveritySummary { critical: 0, high: 1, medium: 0, low: 1, total: 2 }
    );
}
```

Notes:
- If the `sbom_advisory` primary key prevents duplicate rows, the dedup test creates the duplication the
  way it can happen in practice instead, e.g. the same advisory reached through two ingestion paths or
  two linked documents. The assertion stays the same.
- Registration: if `tests/Cargo.toml` or a `tests/api/main.rs`/`mod.rs` must list test modules, that file is
  outside Files to Create/Modify. It is flagged in Step 9 for user approval rather than edited silently.
- Run with `cargo test -p <tests-crate-name>`. The crate name is resolved via
  `cargo metadata --no-deps --format-version 1`, not taken from the nearest `Cargo.toml`.
