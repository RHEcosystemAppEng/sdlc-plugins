# File 6: tests/api/advisory_summary.rs

**Action**: Create (new file)

## Pre-Implementation Inspection

Before creating, inspect sibling test files for exact test pattern conformance:
- Read or `mcp__serena_backend__get_symbols_overview` on `tests/api/advisory.rs` to see test naming, assertion style, fixture setup, and error case coverage patterns
- Read or `mcp__serena_backend__get_symbols_overview` on `tests/api/sbom.rs` to cross-check test conventions are consistent across test files
- Identify how test database setup, HTTP client creation, and fixture seeding are done in sibling tests

## Test Cases

The following four tests are required per the Test Requirements section:

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with linked advisories of known severities returns the correct
/// severity counts in the response.
#[tokio::test]
async fn test_advisory_summary_valid_sbom_with_advisories() {
    // Given an SBOM with advisories at various severity levels seeded in the test database
    // (e.g., 2 Critical, 1 High, 3 Medium, 0 Low)

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK
    // And the response body contains:
    //   critical: 2, high: 1, medium: 3, low: 0, total: 6
    // Assert on actual field values, not just that the response deserializes
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM ID returns a 404 status.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting GET /api/v2/sbom/{non_existent_id}/advisory-summary

    // Then the response status is 404 NOT_FOUND
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary with all severity counts
/// set to zero.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories in the test database

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK
    // And all severity counts are 0:
    //   critical: 0, high: 0, medium: 0, low: 0, total: 0
}
```

### Test 4: Duplicate advisory links are deduplicated in the count

```rust
/// Verifies that when an advisory is linked to the same SBOM multiple times (e.g., via different
/// vulnerability paths), it is counted only once in the severity summary.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with the same advisory linked multiple times
    // (e.g., same advisory_id appears in sbom_advisory twice with different context)

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory is counted only once
    // And the total reflects unique advisory count, not link count
}
```

## Design Decisions

- **Test naming**: follows `test_advisory_summary_<scenario>` pattern consistent with sibling tests `test_get_advisory_*` and `test_list_advisories_*`
- **Assertion style**: uses `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` per sibling test conventions
- **Response validation**: deserializes response body into `SeveritySummary` struct and asserts on individual field values (not just length or shape)
- **Doc comments**: every test function has a `///` doc comment per skill requirements
- **Given-When-Then**: all tests include section comments since they have distinct setup, action, and assertion phases
- **No parameterized tests**: sibling test files do not use `#[rstest]` or other parameterized test frameworks, so individual test functions are used
- **Fixture setup**: follows whatever database seeding pattern is used in `tests/api/advisory.rs` and `tests/api/sbom.rs` (e.g., ingesting test SBOMs and advisories via service methods or direct entity creation)
