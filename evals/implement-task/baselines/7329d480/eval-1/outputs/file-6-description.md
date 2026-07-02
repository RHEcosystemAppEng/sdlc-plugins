# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task description.

## Detailed Changes

### Inspection of sibling tests

Before writing tests, inspect `tests/api/advisory.rs` and `tests/api/sbom.rs` using `mcp__serena_backend__get_symbols_overview` to understand:
- Test setup and database initialization patterns
- HTTP client usage pattern (how requests are made to the test server)
- Assertion conventions (status code checks, body deserialization)
- Test naming conventions

### Test 1: test_advisory_summary_with_known_advisories

```rust
/// Verifies that the severity summary endpoint returns correct counts for
/// an SBOM with advisories at known severity levels.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with linked advisories of known severity levels
    //   - 2 Critical advisories
    //   - 3 High advisories
    //   - 1 Medium advisory
    //   - 0 Low advisories

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK
    // And the response body contains:
    //   critical: 2, high: 3, medium: 1, low: 0, total: 6
    assert_eq!(resp.status(), StatusCode::OK);
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 3);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}
```

### Test 2: test_advisory_summary_nonexistent_sbom

```rust
/// Verifies that requesting severity summary for a non-existent SBOM ID
/// returns 404 Not Found, consistent with other SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID

    // When requesting GET /api/v2/sbom/{non-existent-id}/advisory-summary

    // Then the response status is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: test_advisory_summary_no_advisories

```rust
/// Verifies that the severity summary for an SBOM with no linked advisories
/// returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK
    // And all severity counts are 0
    assert_eq!(resp.status(), StatusCode::OK);
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}
```

### Test 4: test_advisory_summary_deduplication

```rust
/// Verifies that duplicate advisory links (the same advisory linked to the
/// SBOM multiple times) are deduplicated in the severity counts.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with one Critical advisory linked twice via sbom_advisory

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response body counts the advisory only once
    assert_eq!(resp.status(), StatusCode::OK);
    assert_eq!(summary.critical, 1);
    assert_eq!(summary.total, 1);
}
```

## Conventions followed

- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` matching sibling tests
- **Response validation**: Validates individual field values (not just length), consistent with value-based assertion preference
- **Error cases**: Includes 404 test for non-existent entity, matching sibling test pattern
- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern
- **Test documentation**: Every test has a `///` doc comment (AI-generated standard)
- **Test structure**: Given-when-then section comments in every test
- **No parameterized tests**: Sibling tests do not use `#[rstest]`, so individual test functions are used
- **Test setup**: Would use the same database initialization and HTTP client patterns found in `tests/api/advisory.rs` and `tests/api/sbom.rs`
