# Test Plan -- TC-9208

## Assertion Approach

All tests use **value-based assertions** per skill guidance (Step 7). The sibling
patterns `.filter().any()` and `.filter().count() > 0` are explicitly not adopted
because they only check existence without verifying specific values, hiding regressions
behind a passing boolean or count. See `conventions.md` for the full conflict analysis.

Value-based assertions mean:
- Assert exact counts with `assert_eq!` rather than `assert!(count > 0)`.
- Assert specific license identifiers appear in category lists.
- Assert structural properties (empty lists have count 0, counts match list lengths).

## Test File

`tests/api/package_license.rs`

## Test Cases

### Test 1: Valid SBOM with known package licenses returns correct categorized counts

```rust
/// Verifies that a valid SBOM with known package licenses returns correctly
/// categorized counts and license identifiers.
#[tokio::test]
async fn test_license_summary_with_known_licenses() {
    // Given an SBOM ingested with packages having known licenses:
    //   - Package A: MIT (permissive)
    //   - Package B: Apache-2.0 (permissive)
    //   - Package C: GPL-3.0 (copyleft)
    //   - Package D: LicenseRef-custom (unknown)
    // (Setup: ingest SBOM with these packages and license associations into test DB)

    // When requesting the license summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", sbom_id)).await;

    // Then the response status is 200
    assert_eq!(resp.status(), StatusCode::OK);

    // Then the response contains exact categorized counts and license identifiers
    let summary: LicenseSummary = resp.json().await;

    assert_eq!(summary.permissive.count, 2);
    assert_eq!(summary.permissive.licenses.len(), 2);
    assert!(summary.permissive.licenses.contains(&"MIT".to_string()));
    assert!(summary.permissive.licenses.contains(&"Apache-2.0".to_string()));

    assert_eq!(summary.copyleft.count, 1);
    assert_eq!(summary.copyleft.licenses.len(), 1);
    assert_eq!(summary.copyleft.licenses[0], "GPL-3.0");

    assert_eq!(summary.unknown.count, 1);
    assert_eq!(summary.unknown.licenses.len(), 1);
    assert_eq!(summary.unknown.licenses[0], "LicenseRef-custom");
}
```

**Assertion approach:** Uses `assert_eq!` on exact counts and `assert!(...contains())`
on specific license identifiers. This verifies *what* is returned, not just *that
something* is returned.

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting a license summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_license_summary_not_found() {
    // Given a UUID that does not correspond to any ingested SBOM
    let fake_id = Uuid::new_v4();

    // When requesting the license summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", fake_id)).await;

    // Then the response status is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

**Assertion approach:** Direct status code comparison with `assert_eq!`. This is already
value-based (exact status code match).

### Test 3: SBOM with no packages returns all zeros with empty license lists

```rust
/// Verifies that an SBOM with no associated packages returns zero counts
/// and empty license lists for all categories.
#[tokio::test]
async fn test_license_summary_empty_sbom() {
    // Given an SBOM ingested with no packages
    // (Setup: ingest a minimal SBOM with no package associations)

    // When requesting the license summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", empty_sbom_id)).await;

    // Then the response status is 200
    assert_eq!(resp.status(), StatusCode::OK);

    // Then all categories have zero counts and empty lists
    let summary: LicenseSummary = resp.json().await;

    assert_eq!(summary.permissive.count, 0);
    assert!(summary.permissive.licenses.is_empty());

    assert_eq!(summary.copyleft.count, 0);
    assert!(summary.copyleft.licenses.is_empty());

    assert_eq!(summary.unknown.count, 0);
    assert!(summary.unknown.licenses.is_empty());
}
```

**Assertion approach:** Asserts exact zero counts and empty lists using `assert_eq!`
and `is_empty()`. Does not use `.count() > 0` or any existence-only check.

### Test 4: Duplicate licenses within a category are counted only once

```rust
/// Verifies that duplicate license identifiers within the same category
/// are deduplicated -- each license appears exactly once.
#[tokio::test]
async fn test_license_summary_deduplicates_licenses() {
    // Given an SBOM with multiple packages sharing the same license:
    //   - Package X: MIT (permissive)
    //   - Package Y: MIT (permissive)  -- duplicate
    //   - Package Z: GPL-3.0 (copyleft)
    // (Setup: ingest SBOM with these packages, two of which have MIT)

    // When requesting the license summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", sbom_id)).await;

    // Then the response status is 200
    assert_eq!(resp.status(), StatusCode::OK);

    // Then MIT appears only once in the permissive category
    let summary: LicenseSummary = resp.json().await;

    assert_eq!(summary.permissive.count, 1, "MIT should be deduplicated to a single entry");
    assert_eq!(summary.permissive.licenses.len(), 1);
    assert_eq!(summary.permissive.licenses[0], "MIT");

    // And copyleft has exactly one entry
    assert_eq!(summary.copyleft.count, 1);
    assert_eq!(summary.copyleft.licenses[0], "GPL-3.0");
}
```

**Assertion approach:** Asserts the exact count is 1 (not 2) to prove deduplication
occurred. Verifies the specific license identifier. A `.count() > 0` check would pass
even if deduplication failed (count would still be > 0 at 2), making it useless for
this test case.

## Why Value-Based Assertions Matter Here

The sibling `.filter().any()` and `.filter().count() > 0` patterns would be particularly
harmful for TC-9208's tests:

1. **Test 1 (categorized counts):** A `.count() > 0` check would pass even if the
   categorization logic is wrong (e.g., MIT classified as copyleft) as long as any
   license exists in the category.

2. **Test 3 (empty SBOM):** An existence check is meaningless for an empty result --
   there is nothing to check existence of. Value assertions (`count == 0`,
   `is_empty()`) directly express the expected state.

3. **Test 4 (deduplication):** An existence check (`any()`) would pass regardless of
   whether deduplication works, since at least one MIT license always exists.
   Only an exact count assertion (`count == 1`) can verify deduplication.

Value-based assertions make test failures diagnostic: they tell you *what* value was
wrong, not just that "something was missing."
