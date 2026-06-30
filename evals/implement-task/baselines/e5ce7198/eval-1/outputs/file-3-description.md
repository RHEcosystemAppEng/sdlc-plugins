# File 3: tests/api/advisory_summary.rs

**Action**: CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, verifying correct severity counting, 404 handling, empty results, and deduplication behavior.

## Detailed Changes

### Test 1: Valid SBOM with known advisories

```rust
/// Verifies that a valid SBOM with associated advisories returns correct severity counts
/// broken down by critical, high, medium, and low levels.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisory associations at various severity levels
    // (setup: create test SBOM, create advisories with known severities,
    //  link them via sbom_advisory join table)

    // When requesting the advisory summary for that SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response is 200 OK with correct severity counts
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
/// returns a 404 Not Found response, consistent with other SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let fake_id = /* non-existent UUID or ID */;

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
/// Verifies that an SBOM with no linked advisories returns a summary where all
/// severity counts and the total are zero.
#[tokio::test]
async fn test_advisory_summary_empty_sbom() {
    // Given an SBOM with no advisory associations
    // (setup: create test SBOM with no linked advisories)

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
/// Verifies that when an SBOM has duplicate advisory links (same advisory linked
/// multiple times), the severity summary counts each unique advisory only once.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate links to the same advisory
    // (setup: create test SBOM, create one advisory, link it multiple times
    //  via sbom_advisory join table)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.total, 1); // not duplicated
}
```

### Design Decisions

- **Integration tests**: hitting real PostgreSQL test database, matching the pattern in `tests/api/advisory.rs` and `tests/api/sbom.rs`
- **Assertion style**: uses `assert_eq!(resp.status(), StatusCode::OK)` pattern from siblings
- **Value-based assertions**: checks specific field values (critical, high, medium, low, total), not just collection length
- **Test naming**: follows `test_<feature>_<scenario>` pattern from sibling tests
- **Test documentation**: every test has a `///` doc comment (per constraint 5.11, regardless of sibling patterns)
- **Given-when-then comments**: all four tests have distinct setup/action/assertion phases, so all get `// Given`, `// When`, `// Then` comments (per constraint 5.12)
- **No parameterized tests**: would first check if sibling tests use `#[rstest]`; if not, use individual test functions (per constraint 5.10). Each test has a sufficiently different setup that parameterization would require conditionals anyway.

### Convention Compliance

- Follows `tests/api/` directory organization
- Uses same test database setup pattern as sibling test files
- Assertion patterns match existing advisory and SBOM endpoint tests
- Test file named `advisory_summary.rs` following snake_case convention
