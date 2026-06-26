# File 7: tests/api/advisory_summary.rs (CREATE)

## Purpose
Integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Pre-implementation inspection
- Read `tests/api/advisory.rs` (sibling) to understand: test function naming, assertion patterns, response deserialization, 404 test patterns, test setup (database seeding, HTTP client setup), imports.
- Read `tests/api/sbom.rs` (sibling) for additional pattern confirmation, especially SBOM-related test setup.
- Check for shared test utilities (fixtures, helpers, test database setup) used across sibling test files.
- Check whether sibling tests use parameterized testing (e.g., `#[rstest]` with `#[case]`). If not, do not introduce parameterized tests.

## Detailed Changes

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with known advisories returns the correct
/// severity count breakdown in the response.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with linked advisories at known severity levels
    // (seed test database with SBOM and advisories: 2 critical, 3 high, 1 medium, 0 low)

    // When requesting the advisory summary for the SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response is 200 OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 3);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM
/// returns a 404 Not Found response, consistent with other SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID
    let fake_id = /* non-existent ID, e.g., Uuid::new_v4() or 999999 */;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary
/// with all severity counts set to zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    // (seed test database with an SBOM but no sbom_advisory entries)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response is 200 OK with all counts at zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}
```

### Test 4: Duplicate advisory links are deduplicated in count

```rust
/// Verifies that duplicate advisory links (same advisory linked to the
/// same SBOM multiple times) are deduplicated, so each advisory is
/// counted only once in the severity summary.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM with duplicate advisory links
    // (seed test database with SBOM and 1 critical advisory linked twice via sbom_advisory)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response counts the advisory only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 1);  // not 2, despite duplicate link
    assert_eq!(summary.total, 1);
}
```

### Conventions followed
- Test naming follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_returns_correct_counts`), matching sibling test conventions.
- Assertion style uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching sibling patterns.
- Error case tests use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`, matching sibling 404 tests.
- Each test function has a `///` doc comment explaining what it verifies.
- Non-trivial tests include given-when-then section comments (`// Given`, `// When`, `// Then`).
- Tests assert on specific field values (not just response length), following the "prefer value-based assertions" guideline.
- Tests hit a real PostgreSQL test database, matching sibling integration test patterns.
- Test setup and database seeding patterns would be copied exactly from sibling test files (e.g., `advisory.rs` or `sbom.rs`).

### Notes
- The exact test setup (HTTP client creation, database seeding functions, test harness macros) would be copied from sibling test files after reading them.
- If siblings use `#[rstest]` for parameterized tests, consider whether any of these 4 tests could be parameterized. However, since each test has distinct setup and assertions, individual test functions are likely more appropriate (following the Meszaros heuristic).
- The test file may need to be registered in `tests/Cargo.toml` or a `tests/api/mod.rs` if one exists -- would check sibling structure.
