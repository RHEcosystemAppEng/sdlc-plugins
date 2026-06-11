# File 3: tests/api/advisory_summary.rs

**Action**: Create new file

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Covers all four test requirements from the task description: valid SBOM with correct counts, non-existent SBOM returns 404, SBOM with no advisories returns zeros, and deduplication of advisory links.

## Detailed Changes

```rust
use reqwest::StatusCode;
use trustify_common::id::Id;

use crate::advisory::model::severity_summary::SeveritySummary;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_get_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisory severities:
    // 2 critical, 1 high, 3 medium, 0 low
    let sbom_id = setup_sbom_with_advisories(vec![
        ("adv-1", "critical"),
        ("adv-2", "critical"),
        ("adv-3", "high"),
        ("adv-4", "medium"),
        ("adv-5", "medium"),
        ("adv-6", "medium"),
    ])
    .await;

    // When requesting the advisory summary for that SBOM
    let resp = client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response is 200 with correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 3);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_get_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let non_existent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", non_existent_id))
        .send()
        .await
        .unwrap();

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_get_advisory_summary_empty() {
    // Given an SBOM with no advisories linked
    let sbom_id = setup_sbom_with_advisories(vec![]).await;

    // When requesting the advisory summary
    let resp = client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then all counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_get_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let sbom_id = setup_sbom_with_duplicate_advisories(vec![
        ("adv-1", "critical"),  // first link
        ("adv-1", "critical"),  // duplicate link for same advisory
        ("adv-2", "high"),
    ])
    .await;

    // When requesting the advisory summary
    let resp = client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then duplicates are counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 1);  // adv-1 counted once despite duplicate link
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 2);  // 2 unique advisories, not 3 links
}
```

## Conventions Applied

- **Assertion style**: uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching sibling test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`
- **Response validation**: asserts on specific field values (not just count/length), providing clear failure messages
- **Error cases**: includes 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`, matching sibling test pattern
- **Test naming**: follows `test_<endpoint>_<scenario>` pattern (e.g., `test_get_advisory_summary_valid_sbom`)
- **Documentation**: every test function has a `///` doc comment explaining what it verifies
- **Given-When-Then**: section comments (`// Given`, `// When`, `// Then`) in each test body for navigability
- **Test organization**: one file for the advisory summary endpoint group, matching the `tests/api/` convention
- **Value-based assertions**: asserts on actual severity count values, not just total or length
- **Test setup**: uses helper functions for fixture creation (exact helper signatures would be confirmed from sibling test files)

## Notes

- The exact test setup helpers (`setup_sbom_with_advisories`, `client()`, etc.) would be modeled after patterns found in sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`) via Serena inspection
- The test module may need to be registered in `tests/api/mod.rs` if a `mod` declaration file exists
