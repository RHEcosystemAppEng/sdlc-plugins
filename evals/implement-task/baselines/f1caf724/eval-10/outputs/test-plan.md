# Test Plan: TC-9208 -- Package License Summary Tests

## Test file

`tests/api/package_license.rs`

## Assertion approach

### Why value-based assertions (not existence checks)

The sibling test files (`tests/api/advisory.rs` and `tests/api/sbom.rs`) use `.filter().any()` and `.filter().count() > 0` patterns that only check for existence of items in collections. These patterns are insufficient for the license summary tests because:

1. They hide regressions -- a test checking `.count() > 0` passes even if the count drops from 5 to 1
2. They do not reveal *what* changed -- only *how many*
3. They prevent subsequent assertions from running when the first collection check fails

Per the implement-task skill's explicit quality standard (Step 7): "Prefer value-based assertions over length-only checks." This guidance takes precedence over sibling patterns.

**This test plan uses `assert_eq!` on specific license identifiers and exact counts per category** rather than copying the sibling `.any()` or `.count() > 0` existence-check patterns.

### Sibling conventions followed (non-conflicting aspects)

The tests follow sibling conventions from `tests/api/advisory.rs` and `tests/api/sbom.rs` for all non-conflicting aspects:

- **Test naming**: `test_` prefix with descriptive name (e.g., `test_license_summary_valid_sbom`)
- **Setup/teardown**: Use the shared test database setup with real PostgreSQL fixtures
- **Test organization**: Tests in `tests/api/package_license.rs`, one test function per requirement
- **Response status validation**: `assert_eq!(resp.status(), StatusCode::OK)` for success cases
- **Error case pattern**: Verify 404 status for non-existent resources
- **Structure**: Arrange/Act/Assert (with given-when-then comments for non-trivial tests)

Only the assertion style for collection/response data is overridden to follow skill guidance.

---

## Test cases

### Test 1: Valid SBOM with known package licenses returns correct categorized counts

```rust
/// Verifies that a valid SBOM with known package licenses returns the correct
/// categorized counts and license identifiers for each category.
#[test]
async fn test_license_summary_valid_sbom() {
    // Given an SBOM with known packages containing MIT (permissive),
    // Apache-2.0 (permissive), GPL-3.0 (copyleft), and UnknownLicense (unknown)
    let sbom_id = setup_sbom_with_licenses(&[
        ("MIT", "permissive"),
        ("Apache-2.0", "permissive"),
        ("GPL-3.0-only", "copyleft"),
        ("UnknownLicense", "unknown"),
    ]).await;

    // When requesting the license summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", sbom_id)).await;

    // Then the response is 200 OK with correct categorization
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: LicenseSummary = resp.json().await;

    // Value-based assertions on permissive category
    assert_eq!(summary.permissive.count, 2);
    assert_eq!(summary.permissive.licenses.len(), 2);
    assert!(summary.permissive.licenses.contains(&"MIT".to_string()));
    assert!(summary.permissive.licenses.contains(&"Apache-2.0".to_string()));

    // Value-based assertions on copyleft category
    assert_eq!(summary.copyleft.count, 1);
    assert_eq!(summary.copyleft.licenses, vec!["GPL-3.0-only".to_string()]);

    // Value-based assertions on unknown category
    assert_eq!(summary.unknown.count, 1);
    assert_eq!(summary.unknown.licenses, vec!["UnknownLicense".to_string()]);
}
```

**Note**: Uses `assert_eq!` on specific license identifiers ("MIT", "Apache-2.0", "GPL-3.0-only") and exact counts (2, 1, 1) rather than `.filter().any()` or `.count() > 0`.

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting a license summary for a non-existent SBOM returns 404.
#[test]
async fn test_license_summary_not_found() {
    // Given a non-existent SBOM ID
    let non_existent_id = 999999;

    // When requesting the license summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", non_existent_id)).await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no packages returns all zeros with empty license lists

```rust
/// Verifies that an SBOM with no packages returns zero counts and empty license lists
/// for all categories.
#[test]
async fn test_license_summary_empty_sbom() {
    // Given an SBOM with no packages
    let sbom_id = setup_sbom_with_licenses(&[]).await;

    // When requesting the license summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", sbom_id)).await;

    // Then all categories have zero counts and empty lists
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: LicenseSummary = resp.json().await;

    assert_eq!(summary.permissive.count, 0);
    assert_eq!(summary.permissive.licenses, Vec::<String>::new());

    assert_eq!(summary.copyleft.count, 0);
    assert_eq!(summary.copyleft.licenses, Vec::<String>::new());

    assert_eq!(summary.unknown.count, 0);
    assert_eq!(summary.unknown.licenses, Vec::<String>::new());
}
```

**Note**: Asserts exact zero counts and empty Vec, not just `.count() == 0`.

### Test 4: Duplicate licenses within a category are counted only once

```rust
/// Verifies that duplicate licenses within the same category are deduplicated --
/// each unique license identifier appears exactly once in the category's list.
#[test]
async fn test_license_summary_deduplication() {
    // Given an SBOM where MIT appears on multiple packages
    let sbom_id = setup_sbom_with_licenses(&[
        ("MIT", "permissive"),
        ("MIT", "permissive"),
        ("MIT", "permissive"),
        ("Apache-2.0", "permissive"),
    ]).await;

    // When requesting the license summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", sbom_id)).await;

    // Then MIT appears only once in the permissive list
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: LicenseSummary = resp.json().await;

    assert_eq!(summary.permissive.count, 2, "should have exactly 2 unique permissive licenses");
    assert_eq!(summary.permissive.licenses.len(), 2);
    assert!(summary.permissive.licenses.contains(&"MIT".to_string()));
    assert!(summary.permissive.licenses.contains(&"Apache-2.0".to_string()));

    // Copyleft and unknown should be empty
    assert_eq!(summary.copyleft.count, 0);
    assert_eq!(summary.unknown.count, 0);
}
```

**Note**: Asserts the exact count is 2 (not 4), verifying deduplication. Uses `assert_eq!` on the specific count and checks for specific license names, rather than using `.filter(|l| l == "MIT").count() > 0`.

---

## Summary of assertion approach

| Aspect | Sibling pattern | This test plan | Reason |
|--------|----------------|----------------|--------|
| Response status | `assert_eq!(resp.status(), StatusCode::OK)` | Same | No conflict |
| Collection counts | `.filter().count() > 0` | `assert_eq!(count, 2)` | Skill guidance: value-based assertions |
| Item existence | `.filter().any()` | `assert_eq!` on specific identifiers | Skill guidance: assert on actual values |
| Error cases | `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` | Same | No conflict |
| Test naming | `test_` prefix + descriptive | Same | No conflict |
| Setup/teardown | Shared test DB fixtures | Same | No conflict |
| Test documentation | (not present in siblings) | Doc comments on every test | Skill guidance: document every test function |
| Given-when-then | (not present in siblings) | Added for non-trivial tests | Skill guidance: section comments for clarity |

The key override: where siblings use `.filter().any()` and `.filter().count() > 0` to check existence, this test plan uses `assert_eq!` on specific license identifiers (e.g., "MIT", "Apache-2.0", "GPL-3.0-only") and exact integer counts per category (e.g., `assert_eq!(summary.permissive.count, 2)`). This follows the skill's explicit quality standard over the sibling pattern.
