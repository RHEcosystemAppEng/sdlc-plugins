# File 3: `tests/api/advisory_summary.rs` (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint,
verifying correct severity counts, 404 handling, empty advisory case, and
deduplication.

## Detailed Changes

### Test functions

Four test functions covering all test requirements:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories at known severity levels:
    //   2 Critical, 1 High, 3 Medium, 0 Low
    // (create SBOM and link advisories with known severities in test DB)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{sbom_id}/advisory-summary

    // Then the response status is 200 OK
    // assert_eq!(resp.status(), StatusCode::OK);
    // And the response body contains the correct counts:
    //   critical: 2, high: 1, medium: 3, low: 0, total: 6
    // assert_eq!(summary.critical, 2);
    // assert_eq!(summary.high, 1);
    // assert_eq!(summary.medium, 3);
    // assert_eq!(summary.low, 0);
    // assert_eq!(summary.total, 6);
}

/// Verifies that a non-existent SBOM ID returns a 404 response.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{nonexistent_id}/advisory-summary

    // Then the response status is 404 Not Found
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    // (create SBOM but do not link any advisories)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{sbom_id}/advisory-summary

    // Then the response status is 200 OK
    // assert_eq!(resp.status(), StatusCode::OK);
    // And all counts are zero:
    //   critical: 0, high: 0, medium: 0, low: 0, total: 0
    // assert_eq!(summary.critical, 0);
    // assert_eq!(summary.high, 0);
    // assert_eq!(summary.medium, 0);
    // assert_eq!(summary.low, 0);
    // assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM linked to the same advisory twice via sbom_advisory
    // (create SBOM, create one Critical advisory, insert two sbom_advisory rows
    //  pointing to the same advisory ID)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{sbom_id}/advisory-summary

    // Then the response status is 200 OK
    // assert_eq!(resp.status(), StatusCode::OK);
    // And the advisory is counted only once:
    //   critical: 1, total: 1
    // assert_eq!(summary.critical, 1);
    // assert_eq!(summary.total, 1);
}
```

### Design decisions

- **Separate test file**: follows the convention of one test file per domain feature
  in `tests/api/` (siblings: `advisory.rs`, `sbom.rs`, `search.rs`).
- **Value-based assertions**: each test asserts on specific count values, not just
  `total > 0` or length checks. This ensures failures reveal exactly what changed.
- **`assert_eq!(resp.status(), StatusCode::...)` pattern**: matches the assertion
  style found in sibling test files.
- **Given-When-Then comments**: added to all test functions since they have distinct
  setup, action, and assertion phases.
- **Doc comments on every test function**: required by the skill's test documentation
  convention, even though sibling tests may not have them.
- **No parameterized tests**: the four test cases exercise fundamentally different
  scenarios (valid data, 404, empty, deduplication) with different setup and assertions,
  so individual tests are appropriate per the Meszaros heuristic.

### Conventions followed

- Test file in `tests/api/` directory.
- Tests use `#[tokio::test]` for async test execution.
- Test names follow `test_<endpoint>_<scenario>` pattern.
- Status code checked first, then body deserialized and fields validated individually.
- 404 test included for non-existent resource.
