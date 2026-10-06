# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the GET `/api/v2/sbom/{id}/advisory-summary` endpoint, covering
all four test requirements from the task description.

## Content

```rust
use reqwest::StatusCode;

// Test helpers and setup (following sibling test patterns in tests/api/advisory.rs)

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_known_advisories() {
    // Given an SBOM linked to advisories with known severities:
    //   - 2 Critical, 3 High, 1 Medium, 0 Low
    let sbom_id = setup_sbom_with_advisories(vec![
        ("ADV-001", "critical"),
        ("ADV-002", "critical"),
        ("ADV-003", "high"),
        ("ADV-004", "high"),
        ("ADV-005", "high"),
        ("ADV-006", "medium"),
    ]).await;

    // When requesting the advisory summary
    let resp = client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response should be 200 OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 3);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Verifies that a non-existent SBOM ID returns HTTP 404.
#[tokio::test]
async fn test_severity_summary_nonexistent_sbom_returns_404() {
    // Given a SBOM ID that does not exist
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .send()
        .await
        .unwrap();

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_severity_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    let sbom_id = setup_sbom_with_advisories(vec![]).await;

    // When requesting the advisory summary
    let resp = client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response should be 200 OK with all zero counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links to the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    // Given an SBOM linked to the same advisory multiple times
    //   (e.g., advisory ADV-001 linked through two different packages)
    let sbom_id = setup_sbom_with_duplicate_advisory_links(
        "ADV-001",
        "high",
        3,  // linked 3 times
    ).await;

    // When requesting the advisory summary
    let resp = client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the advisory should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(body["high"], 1);
    assert_eq!(body["total"], 1);
}
```

## Test Coverage Matrix

| Test | Acceptance Criterion | Test Requirement |
|------|---------------------|------------------|
| `test_severity_summary_with_known_advisories` | Returns correct counts per severity | Valid SBOM with known advisories returns correct severity counts |
| `test_severity_summary_nonexistent_sbom_returns_404` | Returns 404 when SBOM ID does not exist | Non-existent SBOM ID returns 404 |
| `test_severity_summary_no_advisories_returns_zeros` | All severity levels default to 0 | SBOM with no advisories returns all zeros |
| `test_severity_summary_deduplicates_advisories` | Counts only unique advisories | Duplicate advisory links are deduplicated |

## Conventions Applied

- **File location**: `tests/api/advisory_summary.rs` matching sibling `advisory.rs`, `sbom.rs`
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` matching sibling pattern
- **Value-based assertions**: Asserting on specific field values (`body["critical"]`, etc.)
  rather than just checking response length (per skill guidance)
- **Doc comments**: `///` on every test function (per skill guidance, overriding sibling
  pattern if siblings lack them)
- **Given-when-then comments**: All tests are non-trivial (setup + request + assertion),
  so given-when-then section comments are included
- **Async tests**: `#[tokio::test]` matching sibling async test pattern
- **Test naming**: `test_<action>_<scenario>` pattern
