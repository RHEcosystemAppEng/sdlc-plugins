# File 3: tests/api/advisory_summary.rs

**Action**: CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering the four test requirements specified in the task.

## Sibling Reference

Follows the patterns of `tests/api/advisory.rs` and `tests/api/sbom.rs` for:
- Test setup (database seeding with test data)
- HTTP request construction and execution
- Assertion style (`assert_eq!(resp.status(), StatusCode::OK)`)
- Response body deserialization
- Error case testing with `StatusCode::NOT_FOUND`

## Detailed Changes

```rust
use axum::http::StatusCode;
use crate::advisory::model::severity_summary::SeveritySummary;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories at known severity levels:
    //   2 Critical, 3 High, 1 Medium, 0 Low
    let sbom_id = seed_sbom_with_advisories(vec![
        ("adv-1", "Critical"),
        ("adv-2", "Critical"),
        ("adv-3", "High"),
        ("adv-4", "High"),
        ("adv-5", "High"),
        ("adv-6", "Medium"),
    ]).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response is 200 with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 3);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that a non-existent SBOM ID returns a 404 response.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let fake_id = "non-existent-sbom-id";

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await;

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let sbom_id = seed_sbom_with_advisories(vec![]).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response is 200 with all zeros
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links for the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory ID linked twice)
    let sbom_id = seed_sbom_with_advisories_duplicated(vec![
        ("adv-1", "Critical"),  // linked once
        ("adv-1", "Critical"),  // linked again (duplicate)
        ("adv-2", "High"),      // linked once
    ]).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then duplicates are not double-counted
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 1);  // adv-1 counted once
    assert_eq!(summary.high, 1);      // adv-2 counted once
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 2);     // 2 unique advisories
}
```

## Key Design Decisions

- **Value-based assertions**: Each test asserts on specific field values (not just count/length), per skill requirement "prefer value-based assertions over length-only checks"
- **Doc comments on every test**: Each test function has a `///` doc comment explaining what it verifies
- **Given-when-then comments**: All tests have distinct setup/action/assertion phases marked with section comments
- **Individual tests (not parameterized)**: Each test has different setup, action, and assertion logic -- the Meszaros heuristic favors separate tests when the algorithm differs between cases (different seed data shapes, different assertions)
- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern consistent with sibling tests
- **Status code assertions first**: Matches sibling pattern of checking status code before deserializing body
- **Deduplication test**: Uses a separate seed helper (`seed_sbom_with_advisories_duplicated`) that inserts duplicate join table entries to test the deduplication logic
- **Zero-count test**: Validates the `Default` behavior of `SeveritySummary` for all fields

## Notes

- The actual test setup helpers (`seed_sbom_with_advisories`, `seed_sbom_with_advisories_duplicated`, `client`) would follow existing patterns from `tests/api/sbom.rs` and `tests/api/advisory.rs` for database seeding and HTTP client setup
- Tests hit a real PostgreSQL test database per project convention
- The `tests/Cargo.toml` may need updating to include the new test file in the test harness, depending on how the project discovers test files
