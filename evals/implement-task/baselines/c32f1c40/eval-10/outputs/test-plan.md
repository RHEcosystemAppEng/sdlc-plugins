# Test Plan for TC-9208: Package License Summary Endpoint

## Test File

`tests/api/package_license.rs`

## Test Approach

Integration tests against a real PostgreSQL test database, following the project's existing test infrastructure pattern from `tests/api/sbom.rs` and `tests/api/advisory.rs`.

### Assertion Philosophy

The skill's built-in quality guidance takes precedence over sibling assertion patterns. Sibling tests use existence-only checks (`.any()`, `.count() > 0`), but the new tests will use **value-based assertions** with `assert_eq!` on specific counts and specific license identifiers. This ensures test failures reveal exactly what changed, not just that something changed.

See `outputs/conventions.md` -- CONFLICT 1 for full rationale.

## Test Cases

### Test 1: Valid SBOM with known package licenses returns correct categorized counts

```rust
/// Verifies that a valid SBOM with packages having known licenses returns
/// correctly categorized counts and deduplicated license identifiers.
#[tokio::test]
async fn test_license_summary_with_known_licenses() {
    // Given an SBOM ingested with packages containing licenses:
    //   - Package A: MIT (permissive)
    //   - Package B: Apache-2.0 (permissive)
    //   - Package C: GPL-3.0 (copyleft)
    //   - Package D: LicenseRef-custom (unknown)
    // Setup: ingest test SBOM with known package-license mappings

    // When requesting the license summary
    // GET /api/v2/sbom/{id}/license-summary

    // Then the response status is 200
    assert_eq!(resp.status(), StatusCode::OK);

    // Then permissive category has exactly 2 licenses
    let summary: LicenseSummary = resp.json().await;
    assert_eq!(summary.permissive.count, 2);
    assert_eq!(summary.permissive.licenses, vec!["Apache-2.0", "MIT"]);

    // Then copyleft category has exactly 1 license
    assert_eq!(summary.copyleft.count, 1);
    assert_eq!(summary.copyleft.licenses, vec!["GPL-3.0"]);

    // Then unknown category has exactly 1 license
    assert_eq!(summary.unknown.count, 1);
    assert_eq!(summary.unknown.licenses, vec!["LicenseRef-custom"]);
}
```

**Assertion rationale:** Uses `assert_eq!` on exact counts and exact license lists (sorted), not `.any()` or `.count() > 0`. This follows the skill's value-based assertion guidance and deviates from sibling patterns intentionally.

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting a license summary for a non-existent SBOM ID
/// returns a 404 Not Found response.
#[tokio::test]
async fn test_license_summary_sbom_not_found() {
    // Given a random UUID that does not correspond to any ingested SBOM
    let fake_id = Uuid::new_v4();

    // When requesting the license summary for that ID
    // GET /api/v2/sbom/{fake_id}/license-summary

    // Then the response status is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

**Assertion rationale:** Simple status code assertion -- this is a trivial test with a single assertion and no distinct setup phase beyond creating a fake ID. Given-when-then comments are still included since the test has a clear setup (fake ID creation), action (HTTP request), and assertion (status check).

### Test 3: SBOM with no packages returns all zeros with empty license lists

```rust
/// Verifies that an SBOM with no associated packages returns a license summary
/// with all categories at zero count and empty license lists.
#[tokio::test]
async fn test_license_summary_empty_sbom() {
    // Given an SBOM ingested with no packages (empty SBOM)
    // Setup: ingest a minimal SBOM with no package entries

    // When requesting the license summary
    // GET /api/v2/sbom/{id}/license-summary

    // Then the response status is 200
    assert_eq!(resp.status(), StatusCode::OK);

    // Then all categories have zero counts and empty lists
    let summary: LicenseSummary = resp.json().await;
    assert_eq!(summary.permissive.count, 0);
    assert_eq!(summary.permissive.licenses, Vec::<String>::new());
    assert_eq!(summary.copyleft.count, 0);
    assert_eq!(summary.copyleft.licenses, Vec::<String>::new());
    assert_eq!(summary.unknown.count, 0);
    assert_eq!(summary.unknown.licenses, Vec::<String>::new());
}
```

**Assertion rationale:** Asserts exact zero values and empty vectors rather than using a length check. This ensures no stray licenses leak into the response for an empty SBOM.

### Test 4: Duplicate licenses within a category are counted only once

```rust
/// Verifies that when multiple packages share the same license identifier,
/// the license appears only once in the category and the count reflects
/// the number of distinct licenses, not the number of packages.
#[tokio::test]
async fn test_license_summary_deduplicates_licenses() {
    // Given an SBOM with packages where licenses repeat:
    //   - Package A: MIT (permissive)
    //   - Package B: MIT (permissive) -- duplicate
    //   - Package C: MIT (permissive) -- duplicate
    //   - Package D: GPL-3.0 (copyleft)
    // Setup: ingest test SBOM with duplicate license mappings

    // When requesting the license summary
    // GET /api/v2/sbom/{id}/license-summary

    // Then the response status is 200
    assert_eq!(resp.status(), StatusCode::OK);

    // Then MIT appears exactly once in permissive (not 3 times)
    let summary: LicenseSummary = resp.json().await;
    assert_eq!(summary.permissive.count, 1);
    assert_eq!(summary.permissive.licenses, vec!["MIT"]);

    // Then copyleft is unaffected by the duplication
    assert_eq!(summary.copyleft.count, 1);
    assert_eq!(summary.copyleft.licenses, vec!["GPL-3.0"]);

    // Then unknown remains empty
    assert_eq!(summary.unknown.count, 0);
    assert_eq!(summary.unknown.licenses, Vec::<String>::new());
}
```

**Assertion rationale:** This is the critical deduplication test. Asserting `count == 1` and exact `licenses` content proves deduplication works. An existence-only check (`.any(|l| l == "MIT")`) would pass even if MIT appeared three times, defeating the purpose of the test.

## Parameterized Test Decision

The sibling tests (`tests/api/advisory.rs`, `tests/api/sbom.rs`) do not use parameterized tests (no `rstest` or table-driven patterns). Per the skill's Step 7 guidance: "if the sibling test analysis shows the project does not use parameterized tests, do not introduce them." Therefore, all four test cases are written as individual test functions.

While tests 1 and 4 share a similar structure (setup SBOM, request summary, check categories), the test data and assertions differ meaningfully enough that individual functions are appropriate even under the Meszaros heuristic.

## Test Setup Considerations

- Each test needs to set up its own SBOM with specific package-license data using the project's test database infrastructure.
- The test database should be isolated per test or use transactions that roll back.
- Test data creation should follow patterns from `tests/api/sbom.rs` for SBOM ingestion helpers.
- The `package_license` entity relationships need to be populated for tests 1, 3, and 4.

## Coverage Summary

| Acceptance Criterion | Test Coverage |
|---|---|
| Returns categorized license counts | Test 1 (value-based assertion on exact counts) |
| Returns 404 for non-existent SBOM | Test 2 (status code assertion) |
| Each category includes count and license list | Tests 1, 3, 4 (assert both `count` and `licenses` fields) |
| Licenses are deduplicated within categories | Test 4 (explicit deduplication scenario with value assertion) |
| Empty SBOM returns zeros | Test 3 (all-zero baseline) |
