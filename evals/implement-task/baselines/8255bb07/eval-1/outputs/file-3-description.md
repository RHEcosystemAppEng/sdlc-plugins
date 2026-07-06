# File 3: Create `tests/api/advisory_summary.rs`

## Purpose

Integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements specified in the task.

## Pre-Implementation Inspection

Before creating this file, inspect:
- **`tests/api/advisory.rs`** — Examine the existing advisory endpoint integration tests: test structure, setup patterns, assertion style, status code checks, body deserialization approach, test naming convention.
- **`tests/api/sbom.rs`** — Examine the SBOM endpoint tests as a second sibling for test pattern confirmation.
- **`tests/api/search.rs`** — Additional sibling test file for convention verification.

## Changes

Create a new file with the following tests:

```rust
use common::error::AppError;
use reqwest::StatusCode;
use serde_json::Value;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories at known severity levels
    let sbom_id = setup_sbom_with_advisories(vec![
        ("ADV-001", "Critical"),
        ("ADV-002", "High"),
        ("ADV-003", "High"),
        ("ADV-004", "Medium"),
        ("ADV-005", "Low"),
    ])
    .await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response contains correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 1);
    assert_eq!(body["high"], 2);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 1);
    assert_eq!(body["total"], 5);
}

/// Verifies that a non-existent SBOM ID returns 404, consistent with existing SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .send()
        .await
        .unwrap();

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let sbom_id = setup_sbom_with_advisories(vec![]).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let sbom_id = setup_sbom_with_advisories(vec![
        ("ADV-001", "Critical"),
        ("ADV-001", "Critical"),  // duplicate
        ("ADV-002", "High"),
    ])
    .await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then duplicate advisories are counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 1);  // ADV-001 counted once despite duplicate link
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 2);  // Only 2 unique advisories
}
```

## Conventions Applied

- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching the pattern in `tests/api/advisory.rs`.
- **Response validation**: Checks status code first, then deserializes body and validates specific field values (not just lengths).
- **Error cases**: Includes a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`, matching sibling test patterns.
- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom`).
- **Documentation**: Every test function has a `///` doc comment explaining what it verifies, as required by the skill's documentation practice.
- **Given-When-Then**: Non-trivial tests include `// Given`, `// When`, `// Then` section comments for navigability.
- **Value-based assertions**: Asserts on actual severity count values, not just collection lengths.
