# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose
Integration tests for the GET `/api/v2/sbom/{id}/advisory-summary` endpoint covering all acceptance criteria and test requirements.

## Full File Content

```rust
use crate::common::{setup_test_app, TestContext};
use trustify_common::id::Id;
use uuid::Uuid;

/// Test that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    let ctx = TestContext::new().await;
    let app = setup_test_app(&ctx).await;

    // Seed test data: create an SBOM and link advisories with known severities
    let sbom_id = ctx.seed_sbom("test-sbom-1").await;
    ctx.seed_advisory_for_sbom(sbom_id, "ADV-001", "critical").await;
    ctx.seed_advisory_for_sbom(sbom_id, "ADV-002", "high").await;
    ctx.seed_advisory_for_sbom(sbom_id, "ADV-003", "high").await;
    ctx.seed_advisory_for_sbom(sbom_id, "ADV-004", "medium").await;
    ctx.seed_advisory_for_sbom(sbom_id, "ADV-005", "low").await;

    let response = app
        .get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary"))
        .await;

    assert_eq!(response.status(), 200);

    let body: serde_json::Value = response.json().await;
    assert_eq!(body["critical"], 1);
    assert_eq!(body["high"], 2);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 1);
    assert_eq!(body["total"], 5);
}

/// Test that requesting a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    let ctx = TestContext::new().await;
    let app = setup_test_app(&ctx).await;

    let fake_id = Uuid::new_v4();
    let response = app
        .get(&format!("/api/v2/sbom/{fake_id}/advisory-summary"))
        .await;

    assert_eq!(response.status(), 404);
}

/// Test that an SBOM with no linked advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_empty() {
    let ctx = TestContext::new().await;
    let app = setup_test_app(&ctx).await;

    // Seed an SBOM with no advisories linked
    let sbom_id = ctx.seed_sbom("test-sbom-empty").await;

    let response = app
        .get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary"))
        .await;

    assert_eq!(response.status(), 200);

    let body: serde_json::Value = response.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Test that duplicate advisory links are deduplicated — each advisory counted once.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    let ctx = TestContext::new().await;
    let app = setup_test_app(&ctx).await;

    let sbom_id = ctx.seed_sbom("test-sbom-dedup").await;

    // Link the same advisory twice to the SBOM
    let advisory_id = ctx.seed_advisory("ADV-DUP", "critical").await;
    ctx.link_advisory_to_sbom(advisory_id, sbom_id).await;
    ctx.link_advisory_to_sbom(advisory_id, sbom_id).await; // duplicate link

    // Also add a unique advisory
    ctx.seed_advisory_for_sbom(sbom_id, "ADV-UNIQUE", "high").await;

    let response = app
        .get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary"))
        .await;

    assert_eq!(response.status(), 200);

    let body: serde_json::Value = response.json().await;
    assert_eq!(body["critical"], 1); // ADV-DUP counted once despite two links
    assert_eq!(body["high"], 1);     // ADV-UNIQUE
    assert_eq!(body["total"], 2);    // Only 2 unique advisories
}
```

## Design Decisions

- **Test naming**: Follows `test_{feature}_{scenario}` convention observed in the `tests/api/` directory.
- **Test harness**: Uses the project's `TestContext` and `setup_test_app` helpers (exact names will be adjusted to match the actual test infrastructure during implementation).
- **Data seeding**: Uses helper methods on `TestContext` to create SBOM and advisory entities. The exact seeding API will be determined by inspecting existing test files — the above uses plausible method signatures.
- **Assertion style**: Asserts on HTTP status code first, then deserializes and asserts individual JSON fields. This matches the pattern in sibling test files.
- **Deduplication test**: Explicitly creates duplicate links in the join table to verify the service-level deduplication logic.
- **Registration**: This file must also be registered as `mod advisory_summary;` in the test module root (e.g., `tests/api/mod.rs` or the test binary's `main.rs`).

## Additional Registration

In `tests/api/mod.rs` (or equivalent), add:

```rust
mod advisory_summary;
```
