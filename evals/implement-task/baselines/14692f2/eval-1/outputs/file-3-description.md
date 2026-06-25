# File 3: tests/api/advisory_summary.rs

## Action: CREATE

## Purpose
Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all test requirements: valid SBOM with known advisories, non-existent SBOM (404), SBOM with no advisories (all zeros), and deduplication of advisory links.

## Detailed Changes

Create a new test file with the following tests:

### Test 1: `test_advisory_summary_with_known_advisories`

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (set up test database with an SBOM linked to advisories:
    //  2 Critical, 1 High, 3 Medium, 0 Low)
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_with_advisories(&app, vec![
        ("ADV-001", "Critical"),
        ("ADV-002", "Critical"),
        ("ADV-003", "High"),
        ("ADV-004", "Medium"),
        ("ADV-005", "Medium"),
        ("ADV-006", "Medium"),
    ]).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response is 200 OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.critical, 2);
    assert_eq!(body.high, 1);
    assert_eq!(body.medium, 3);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 6);
}
```

### Test 2: `test_advisory_summary_nonexistent_sbom`

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let app = setup_test_app().await;
    let fake_id = "non-existent-sbom-id";

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: `test_advisory_summary_no_advisories`

```rust
/// Verifies that an SBOM with no linked advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_without_advisories(&app).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response is 200 OK with all counts at zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.critical, 0);
    assert_eq!(body.high, 0);
    assert_eq!(body.medium, 0);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 0);
}
```

### Test 4: `test_advisory_summary_deduplicates_advisories`

```rust
/// Verifies that duplicate advisory links for the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked multiple times)
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_with_duplicate_advisories(&app, vec![
        ("ADV-001", "Critical"),  // first link
        ("ADV-001", "Critical"),  // duplicate link of same advisory
        ("ADV-002", "High"),
    ]).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then counts reflect unique advisories only (ADV-001 counted once)
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.critical, 1);  // ADV-001 deduplicated
    assert_eq!(body.high, 1);      // ADV-002
    assert_eq!(body.medium, 0);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 2);     // only 2 unique advisories
}
```

## Conventions Applied
- **Test location**: `tests/api/` directory, following `sbom.rs`, `advisory.rs`, `search.rs` sibling pattern
- **Test naming**: `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_with_known_advisories`)
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` following sibling tests
- **Value-based assertions**: Assert on specific field values (critical, high, medium, low, total), not just lengths
- **Documentation**: Every test function has a `///` doc comment explaining what it verifies
- **Given-When-Then**: Section comments (`// Given`, `// When`, `// Then`) for test structure
- **Test database**: Tests use real PostgreSQL test database, following existing integration test setup pattern
- **Error case coverage**: Includes 404 test with non-existent ID, matching sibling test patterns
