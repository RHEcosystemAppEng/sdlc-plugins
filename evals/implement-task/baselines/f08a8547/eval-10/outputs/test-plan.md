# Test Plan for TC-9208

## Test File

`tests/api/package_license.rs` -- integration tests for the license summary endpoint.

## Assertion Approach

### Guiding Principle

The skill's Step 7 explicitly requires **value-based assertions over length-only or existence-only checks**. This overrides the sibling test pattern found in `tests/api/advisory.rs` and `tests/api/sbom.rs`, which use `.any()` and `.count() > 0` existence checks. The conflict is documented in conventions.md.

All assertions in these tests will verify exact values -- specific counts, specific license identifiers, and specific response structure -- so that test failures reveal precisely what changed rather than merely that a count shifted.

### Status Code Assertions

Follow the sibling convention of `assert_eq!(resp.status(), StatusCode::OK)` -- this is already value-based and consistent with the skill guidance.

## Test Cases

### Test 1: Valid SBOM with known package licenses returns correct categorized counts

```rust
/// Verifies that a valid SBOM with known package licenses returns correctly
/// categorized counts and deduplicated license identifier lists.
#[tokio::test]
async fn test_license_summary_returns_categorized_licenses() {
    // Given an SBOM with packages having known licenses:
    //   - Package A: MIT (permissive), GPL-3.0-only (copyleft)
    //   - Package B: Apache-2.0 (permissive), MIT (permissive, duplicate)
    //   - Package C: CustomLicense-1.0 (unknown)
    // Setup: insert SBOM, packages, and package_license records into test DB

    // When requesting the license summary for this SBOM
    // GET /api/v2/sbom/{sbom_id}/license-summary

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // Then permissive licenses are correctly aggregated and deduplicated
    assert_eq!(result.permissive.count, 2);
    assert_eq!(result.permissive.licenses, vec!["Apache-2.0", "MIT"]);

    // Then copyleft licenses are correctly aggregated
    assert_eq!(result.copyleft.count, 1);
    assert_eq!(result.copyleft.licenses, vec!["GPL-3.0-only"]);

    // Then unknown licenses are correctly aggregated
    assert_eq!(result.unknown.count, 1);
    assert_eq!(result.unknown.licenses, vec!["CustomLicense-1.0"]);
}
```

**Assertion rationale**: Asserts exact counts AND exact license identifier lists (sorted alphabetically). If the classification logic or deduplication logic regresses, the assertion message will show exactly which licenses appeared or disappeared -- unlike a `.count() > 0` check which would only reveal that the count dropped to zero.

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting a license summary for a non-existent SBOM ID
/// returns HTTP 404 Not Found.
#[tokio::test]
async fn test_license_summary_returns_404_for_unknown_sbom() {
    // Given a UUID that does not correspond to any SBOM in the database
    let fake_id = Uuid::new_v4();

    // When requesting the license summary for this non-existent SBOM
    // GET /api/v2/sbom/{fake_id}/license-summary

    // Then the response status is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

**Assertion rationale**: Simple status code value assertion. This test is trivial (single assertion, no distinct phases beyond minimal setup), but given-when-then comments are included for consistency since other tests in the file use them.

### Test 3: SBOM with no packages returns all zeros with empty license lists

```rust
/// Verifies that an SBOM with no linked packages returns a license summary
/// with zero counts and empty license lists for all categories.
#[tokio::test]
async fn test_license_summary_empty_sbom_returns_zeros() {
    // Given an SBOM that exists but has no linked packages
    // Setup: insert SBOM only, no sbom_package or package_license records

    // When requesting the license summary for this empty SBOM
    // GET /api/v2/sbom/{sbom_id}/license-summary

    // Then the response status is 200 OK (not 404 -- SBOM exists, just empty)
    assert_eq!(resp.status(), StatusCode::OK);

    // Then all categories have zero counts
    assert_eq!(result.permissive.count, 0);
    assert_eq!(result.copyleft.count, 0);
    assert_eq!(result.unknown.count, 0);

    // Then all license lists are empty
    assert!(result.permissive.licenses.is_empty(), "permissive licenses should be empty");
    assert!(result.copyleft.licenses.is_empty(), "copyleft licenses should be empty");
    assert!(result.unknown.licenses.is_empty(), "unknown licenses should be empty");
}
```

**Assertion rationale**: Asserts exact zero counts for each category independently (not just total). The `.is_empty()` calls are value-based (they verify the collection is empty, which is the expected value). Each assertion includes a descriptive message so failures pinpoint which category unexpectedly contained data.

### Test 4: Duplicate licenses within a category are counted only once

```rust
/// Verifies that when multiple packages share the same license, the license
/// appears only once in the summary and the count reflects unique licenses,
/// not total occurrences.
#[tokio::test]
async fn test_license_summary_deduplicates_within_category() {
    // Given an SBOM with three packages, all using MIT (permissive):
    //   - Package A: MIT
    //   - Package B: MIT
    //   - Package C: MIT, Apache-2.0
    // Setup: insert SBOM, packages, and package_license records

    // When requesting the license summary for this SBOM
    // GET /api/v2/sbom/{sbom_id}/license-summary

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // Then permissive count reflects unique licenses, not occurrences
    assert_eq!(result.permissive.count, 2, "should count MIT and Apache-2.0, not three MITs");
    assert_eq!(result.permissive.licenses, vec!["Apache-2.0", "MIT"]);

    // Then categories with no licenses remain at zero
    assert_eq!(result.copyleft.count, 0);
    assert_eq!(result.unknown.count, 0);
}
```

**Assertion rationale**: The key assertion is `count == 2` (not 4, which would be the non-deduplicated count). Combined with the exact license list assertion (`vec!["Apache-2.0", "MIT"]`), this proves deduplication works correctly. A `.count() > 0` check (sibling pattern) would pass even if deduplication were broken -- it would merely confirm that at least one license exists.

## Why Value-Based Assertions Matter Here

The sibling patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs` use:
- `.filter(...).any(|_| true)` -- proves existence but not exclusivity or count correctness
- `.filter(...).count() > 0` -- proves non-emptiness but not specific values

For this endpoint, these patterns would miss critical regressions:
1. **Broken deduplication**: `.count() > 0` passes whether MIT appears once or three times
2. **Wrong classification**: `.any(|l| l == "MIT")` in permissive passes even if MIT also incorrectly appears in copyleft
3. **Missing licenses**: checking only one license per category misses dropped licenses

The value-based assertions catch all of these by verifying exact counts and exact sorted lists.

## Test Infrastructure

- Tests use the existing integration test infrastructure (real PostgreSQL test database)
- Test fixtures are inserted directly into the database using SeaORM entities
- Each test is self-contained with its own SBOM, package, and license setup
- Tests follow the `test_` prefix naming convention from siblings
- All test functions have `///` doc comments per skill guidance (overriding sibling pattern of no docs)
- All tests include `// Given`, `// When`, `// Then` section comments per skill guidance for non-trivial tests

## Parameterized Test Consideration

The four test cases exercise different behaviors with distinct setup requirements:
- Test 1: multi-package, multi-category, with duplicates
- Test 2: non-existent SBOM (error path, no setup beyond absence)
- Test 3: empty SBOM (different fixture: SBOM exists but no packages)
- Test 4: deduplication focus (different fixture: same license repeated)

Per the Meszaros heuristic from the skill: these tests have different setup and assertion structures, so individual test functions are appropriate. Parameterized tests would require conditionals in the test body to handle the different fixture shapes and assertion targets, which the skill says to avoid.
