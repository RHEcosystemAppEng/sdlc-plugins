# File 6: tests/api/advisory_summary.rs

**Action**: Create (new file)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests hit a real PostgreSQL test database following the established testing conventions found in sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`).

## Content

Four test functions corresponding to the Test Requirements:

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with known advisories returns the correct
/// severity count breakdown.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with known advisories at various severity levels
    // (seed test database with SBOM and linked advisories: 2 Critical, 3 High, 1 Medium, 0 Low)

    // When requesting the advisory summary for that SBOM
    let resp = client
        .get("/api/v2/sbom/{id}/advisory-summary")
        .send()
        .await;

    // Then the response should contain correct severity counts
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
/// returns a 404 Not Found response.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/non-existent-id/advisory-summary")
        .send()
        .await;

    // Then the response should be 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary
/// with all severity counts at zero.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories
    // (seed test database with SBOM but no advisory links)

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/{id}/advisory-summary")
        .send()
        .await;

    // Then all counts should be zero
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
/// Verifies that duplicate advisory links in the SBOM-advisory join table
/// are deduplicated when computing severity counts.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links
    // (seed test database: same advisory linked to SBOM multiple times)

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/{id}/advisory-summary")
        .send()
        .await;

    // Then the advisory should only be counted once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.total, 1); // not 2+ from duplicates
    // Assert on the specific severity level of the duplicated advisory
}
```

## Design Decisions

- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching the pattern in `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- **Value-based assertions**: Asserts on specific field values (not just collection lengths) so failures reveal what changed.
- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern consistent with sibling test files.
- **Documentation**: Every test function has a `///` doc comment explaining what it verifies.
- **Given/When/Then**: Non-trivial tests include `// Given`, `// When`, `// Then` section comments.
- **Test independence**: Each test sets up its own test data and does not depend on other tests.
- **Real database**: Tests use the PostgreSQL test database infrastructure established by the project.
