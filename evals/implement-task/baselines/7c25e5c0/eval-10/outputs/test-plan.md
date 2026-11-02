# Test Plan — TC-9208: Package License Summary Tests

## Assertion Approach

### Convention Conflict Resolution

The sibling test files (`tests/api/advisory.rs` and `tests/api/sbom.rs`) use `.filter().any()` and `.filter().count() > 0` patterns — existence checks that verify something matching a predicate is present without asserting on specific values.

The implement-task skill's built-in guidance (Step 7) explicitly requires **value-based assertions** over length-only or existence checks:

> Assert on specific items or key fields so that test failures reveal *what* changed, not just *how many*.

**The skill guidance takes precedence.** The new tests will use `assert_eq!` on specific license identifiers and exact counts per category rather than `.any()` or `.count() > 0` existence checks. This ensures that if the categorization logic changes, test failures reveal exactly which licenses were miscategorized or missing — not just that "some" license was present.

### Sibling Conventions Followed (Non-Conflicting)

- **Test file location**: `tests/api/package_license.rs` (matches `tests/api/` pattern)
- **Test naming**: descriptive names matching the tested behavior
- **Setup/teardown**: use real PostgreSQL test database, create fixtures via helper functions
- **Status code assertions**: `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test organization**: one test function per acceptance criterion

## Test Cases

### Test 1: `test_license_summary_returns_categorized_counts`
/// Verifies that a valid SBOM with known package licenses returns correctly categorized counts and license identifiers.

```rust
/// Verifies that a valid SBOM with known package licenses returns correctly categorized counts and license identifiers.
#[test]
fn test_license_summary_returns_categorized_counts() {
    // Given an SBOM with packages having known licenses:
    //   - "MIT" (permissive), "Apache-2.0" (permissive), "GPL-3.0" (copyleft)
    // (create test SBOM and associate packages with these licenses)

    // When requesting the license summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", sbom_id)).await;

    // Then the response is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: LicenseSummary = resp.json().await;

    // Then the permissive category contains exactly MIT and Apache-2.0
    assert_eq!(summary.permissive.count, 2);
    assert_eq!(summary.permissive.licenses, vec!["Apache-2.0", "MIT"]);

    // Then the copyleft category contains exactly GPL-3.0
    assert_eq!(summary.copyleft.count, 1);
    assert_eq!(summary.copyleft.licenses, vec!["GPL-3.0"]);

    // Then the unknown category is empty
    assert_eq!(summary.unknown.count, 0);
    assert_eq!(summary.unknown.licenses, Vec::<String>::new());
}
```

Value-based assertions: asserts on exact license identifiers (e.g., `"MIT"`, `"Apache-2.0"`) and exact counts (2, 1, 0) — not `.any()` or `.count() > 0`.

### Test 2: `test_license_summary_returns_404_for_nonexistent_sbom`
/// Verifies that requesting a license summary for a non-existent SBOM ID returns 404.

```rust
/// Verifies that requesting a license summary for a non-existent SBOM ID returns 404.
#[test]
fn test_license_summary_returns_404_for_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let fake_id = Uuid::new_v4();

    // When requesting the license summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", fake_id)).await;

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: `test_license_summary_empty_sbom_returns_zeros`
/// Verifies that an SBOM with no packages returns all zero counts with empty license lists.

```rust
/// Verifies that an SBOM with no packages returns all zero counts with empty license lists.
#[test]
fn test_license_summary_empty_sbom_returns_zeros() {
    // Given an SBOM with no associated packages
    // (create test SBOM without package associations)

    // When requesting the license summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", empty_sbom_id)).await;

    // Then the response is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: LicenseSummary = resp.json().await;

    // Then all categories have zero counts and empty lists
    assert_eq!(summary.permissive.count, 0);
    assert_eq!(summary.permissive.licenses, Vec::<String>::new());
    assert_eq!(summary.copyleft.count, 0);
    assert_eq!(summary.copyleft.licenses, Vec::<String>::new());
    assert_eq!(summary.unknown.count, 0);
    assert_eq!(summary.unknown.licenses, Vec::<String>::new());
}
```

Value-based: asserts exact zero counts and empty vectors — not just `is_empty()`.

### Test 4: `test_license_summary_deduplicates_within_category`
/// Verifies that duplicate licenses within a category are counted only once.

```rust
/// Verifies that duplicate licenses within a category are counted only once.
#[test]
fn test_license_summary_deduplicates_within_category() {
    // Given an SBOM where two packages both have "MIT" license
    // (create test SBOM with two packages, both referencing MIT)

    // When requesting the license summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", sbom_id)).await;

    // Then the response is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: LicenseSummary = resp.json().await;

    // Then MIT appears only once in the permissive category
    assert_eq!(summary.permissive.count, 1);
    assert_eq!(summary.permissive.licenses, vec!["MIT"]);
}
```

Value-based: asserts the exact count (1, not 2) and the exact license identifier, verifying deduplication happened correctly.
