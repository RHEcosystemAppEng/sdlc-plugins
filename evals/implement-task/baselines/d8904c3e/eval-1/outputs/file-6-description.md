# File 6: `tests/api/advisory_summary.rs` (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task description.

## Detailed Changes

### Imports

```rust
use axum::http::StatusCode;
use serde_json::Value;
// Plus test infrastructure imports (test client, database setup, fixtures)
// matching whatever pattern is used in tests/api/advisory.rs and tests/api/sbom.rs
```

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with known linked advisories returns the correct
/// severity count breakdown (critical, high, medium, low) and total.
#[tokio::test]
async fn test_advisory_summary_valid_sbom_with_advisories() {
    // Given: a test SBOM with known advisories at various severity levels
    //   - 2 Critical advisories
    //   - 3 High advisories
    //   - 1 Medium advisory
    //   - 0 Low advisories
    // (Create SBOM and advisory fixtures in the test database, then link them
    //  via the sbom_advisory join table)

    // When: GET /api/v2/sbom/{sbom_id}/advisory-summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then: response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // Then: response body contains correct severity counts
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 3);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}
```

### Test 2: Non-existent SBOM returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM ID
/// returns a 404 Not Found response, consistent with other SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given: a non-existent SBOM ID
    let fake_id = "00000000-0000-0000-0000-000000000000";

    // When: GET /api/v2/sbom/{fake_id}/advisory-summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .await;

    // Then: response status is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary with all
/// severity counts set to zero and total of zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories_returns_zeros() {
    // Given: a test SBOM with no linked advisories
    // (Create SBOM fixture but do not link any advisories)

    // When: GET /api/v2/sbom/{sbom_id}/advisory-summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then: response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // Then: all counts are zero
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that when an advisory is linked to an SBOM multiple times in the
/// sbom_advisory join table, it is counted only once in the severity summary.
#[tokio::test]
async fn test_advisory_summary_deduplicates_by_advisory_id() {
    // Given: a test SBOM with one High advisory linked twice in sbom_advisory
    // (Create SBOM and advisory fixtures, then insert two rows in sbom_advisory
    //  for the same advisory-SBOM pair)

    // When: GET /api/v2/sbom/{sbom_id}/advisory-summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then: response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // Then: the advisory is counted only once
    let body: Value = resp.json().await;
    assert_eq!(body["high"], 1);
    assert_eq!(body["total"], 1);
}
```

### Design Decisions

- **Test naming**: Follows `test_<feature>_<scenario>` pattern matching sibling tests in `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` pattern consistent with all sibling test files.
- **Value-based assertions**: Asserts on specific field values (e.g., `body["critical"] == 2`) rather than just checking collection lengths, per the skill's requirement to prefer value-based assertions.
- **Given-When-Then comments**: Each test includes section comments (`// Given`, `// When`, `// Then`) for navigability, since these are non-trivial tests with distinct setup, action, and assertion phases.
- **Documentation comments**: Every test function has a `///` doc comment explaining what it verifies, per the skill requirement that AI-generated tests must have documentation regardless of sibling conventions.
- **Real database**: Tests use the same PostgreSQL test database infrastructure as sibling tests.
- **No parameterized tests**: The four test cases exercise different scenarios with different setup requirements (different fixture data, different assertions), so individual test functions are more appropriate than parameterized tests per the Meszaros heuristic.

### Sibling Parity

Matches patterns from `tests/api/advisory.rs` and `tests/api/sbom.rs`:
- Same status code assertion pattern
- Same response body deserialization approach
- Same test database setup/teardown pattern
- Same test naming convention
- Adds `///` doc comments (new standard from skill requirements)
- Adds given-when-then section comments (new standard from skill requirements)

### Test Registration

The file `tests/api/advisory_summary.rs` would also need to be registered in the test crate. If the test crate uses a `mod.rs` or `main.rs` in `tests/`, a `mod advisory_summary;` declaration would need to be added. This would be verified during implementation by examining the test crate's structure.
