# File 3 -- CREATE: tests/api/advisory_summary.rs

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all test requirements and acceptance criteria.

## Conventions Applied

- **Location:** `tests/api/` directory, consistent with sibling test files (`sbom.rs`, `advisory.rs`, `search.rs`).
- **Assertion style:** Uses `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` pattern from siblings.
- **Test naming:** Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom`).
- **Infrastructure:** Hits a real PostgreSQL test database, consistent with integration test approach.
- **Documentation:** Every test function has a `///` doc comment explaining what it verifies.
- **Body structure:** Non-trivial tests use `// Given`, `// When`, `// Then` section comments.

## Detailed Changes

```rust
use axum::http::StatusCode;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_with_advisories(&app, vec![
        ("ADV-001", "Critical"),
        ("ADV-002", "High"),
        ("ADV-003", "High"),
        ("ADV-004", "Medium"),
        ("ADV-005", "Low"),
    ]).await;

    // When requesting the advisory severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response should contain correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: serde_json::Value = resp.json().await;
    assert_eq!(summary["critical"], 1);
    assert_eq!(summary["high"], 2);
    assert_eq!(summary["medium"], 1);
    assert_eq!(summary["low"], 1);
    assert_eq!(summary["total"], 5);
}

/// Verifies that a non-existent SBOM ID returns a 404 status code.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let app = setup_test_app().await;
    let nonexistent_id = uuid::Uuid::new_v4();

    // When requesting the advisory severity summary for the non-existent ID
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .await;

    // Then a 404 response should be returned
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_without_advisories(&app).await;

    // When requesting the advisory severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then all severity counts should be zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: serde_json::Value = resp.json().await;
    assert_eq!(summary["critical"], 0);
    assert_eq!(summary["high"], 0);
    assert_eq!(summary["medium"], 0);
    assert_eq!(summary["low"], 0);
    assert_eq!(summary["total"], 0);
}

/// Verifies that duplicate advisory links to the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_with_advisories(&app, vec![
        ("ADV-001", "Critical"),
        ("ADV-001", "Critical"),  // duplicate link to same advisory
        ("ADV-002", "High"),
    ]).await;

    // When requesting the advisory severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the duplicate should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: serde_json::Value = resp.json().await;
    assert_eq!(summary["critical"], 1);  // ADV-001 counted once despite duplicate link
    assert_eq!(summary["high"], 1);
    assert_eq!(summary["medium"], 0);
    assert_eq!(summary["low"], 0);
    assert_eq!(summary["total"], 2);  // Only 2 unique advisories
}
```

## Key Design Decisions

- **Value-based assertions over length-only checks:** Tests assert on specific count values, not just that the response is non-empty. This follows the skill's Step 7 guidance to prefer value-based assertions.
- **All four test requirements covered:** Each test function maps to a specific test requirement from the task.
- **Deduplication test uses concrete data:** The duplicate test seeds the same advisory ID twice and verifies the count reflects deduplication.
- **No parameterized tests:** Sibling test files in `tests/api/` do not use `#[rstest]` or parameterized patterns, so individual test functions are used per convention.
- **Helper functions assumed:** `setup_test_app()`, `seed_sbom_with_advisories()`, and `seed_sbom_without_advisories()` would be implemented as test helpers, following patterns established in sibling test files for database seeding.
