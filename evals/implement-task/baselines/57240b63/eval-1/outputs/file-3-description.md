# File 3: Create `tests/api/advisory_summary.rs`

## Purpose
Integration tests for the GET /api/v2/sbom/{id}/advisory-summary endpoint, covering all 4 test requirements.

## Reference Files to Inspect First
- Sibling test files in `tests/api/` (e.g., tests for advisory listing, SBOM endpoints) -- inspect for test setup patterns, assertion style, fixture creation, and HTTP client usage.
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- The response struct to deserialize into.

## Changes

Create a new file with 4 test functions. Each test function includes a doc comment and given-when-then comments for non-trivial tests:

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with known advisory severities returns the correct
/// count per severity level and the correct total.
#[tokio::test]
async fn test_advisory_summary_valid_counts() {
    // Given an SBOM with advisories at known severity levels
    // (set up test SBOM and link advisories with Critical, High, Medium, Low severities)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response contains correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, expected_critical_count);
    assert_eq!(summary.high, expected_high_count);
    assert_eq!(summary.medium, expected_medium_count);
    assert_eq!(summary.low, expected_low_count);
    assert_eq!(summary.total, expected_total);
}
```

### Test 2: Non-existent SBOM returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM ID
/// returns a 404 Not Found response.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/nonexistent-id/advisory-summary")
        .send()
        .await;

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a severity summary
/// with all counts set to zero.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", empty_sbom_id))
        .send()
        .await;

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory links (same advisory linked to the SBOM
/// multiple times) are deduplicated, counting each advisory only once.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with the same advisory linked multiple times

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.total, 1);  // Not 2 or more from duplicates
}
```

## Notes
- The exact test setup (fixture creation, HTTP client initialization, database seeding) must be confirmed by reading sibling test files in `tests/api/`.
- Assertion patterns (status code checks, JSON deserialization approach) should follow whatever conventions are discovered from sibling tests.
- Parameterized tests are not used here because each test has distinct setup requirements (different SBOM states) -- they do not share the same algorithm per the Meszaros heuristic.
- Every test function has a `///` doc comment as required by implement-task Step 7.
- Non-trivial tests (all 4 in this case) include given-when-then inline comments.
