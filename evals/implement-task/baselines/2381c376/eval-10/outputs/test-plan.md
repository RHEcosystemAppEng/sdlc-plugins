# Test Plan for TC-9208

## Test File

`tests/api/package_license.rs`

## Assertion Approach

### Guiding Principle

Use **value-based assertions** per the implement-task skill's Step 7 guidance. This
overrides the sibling test patterns found in `tests/api/advisory.rs` and
`tests/api/sbom.rs`, which use existence-only checks (`.filter().any()` and
`.filter().count() > 0`). Value-based assertions reveal *what* changed on failure,
not just *how many* items are present.

### Non-Conflicting Sibling Conventions Adopted

- Test naming: `test_<noun>_<scenario>` pattern
- Setup: shared PostgreSQL test database initialization from sibling tests
- HTTP client: same test client pattern as `advisory.rs` and `sbom.rs`
- Status code checks: `assert_eq!(resp.status(), StatusCode::OK)` and
  `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Descriptive assertion messages in all `assert!`/`assert_eq!` calls

### Documentation Standard

Every test function will have a `///` doc comment explaining what it verifies
(skill requirement, applied regardless of sibling convention).

Non-trivial tests will include `// Given`, `// When`, `// Then` section comments.

## Test Cases

### Test 1: `test_license_summary_valid_sbom`

```rust
/// Verifies that a valid SBOM with known package licenses returns correctly
/// categorized counts and license identifiers.
#[test]
fn test_license_summary_valid_sbom() {
    // Given an SBOM with packages that have known licenses:
    //   - MIT (permissive)
    //   - Apache-2.0 (permissive)
    //   - GPL-3.0-only (copyleft)
    //   - UnknownLicense (unknown)
    // (set up via test database fixtures)

    // When requesting the license summary
    let resp = client.get("/api/v2/sbom/{id}/license-summary").await;

    // Then the response status is 200
    assert_eq!(resp.status(), StatusCode::OK);

    // Then the categorized counts match expected values
    let summary: LicenseSummary = resp.json().await;
    assert_eq!(summary.permissive.count, 2, "permissive license count");
    assert_eq!(summary.copyleft.count, 1, "copyleft license count");
    assert_eq!(summary.unknown.count, 1, "unknown license count");

    // Then the specific license identifiers are present in each category
    assert_eq!(
        summary.permissive.licenses.iter().sorted().collect::<Vec<_>>(),
        vec!["Apache-2.0", "MIT"],
        "permissive license identifiers"
    );
    assert_eq!(
        summary.copyleft.licenses,
        vec!["GPL-3.0-only"],
        "copyleft license identifiers"
    );
    assert_eq!(
        summary.unknown.licenses,
        vec!["UnknownLicense"],
        "unknown license identifiers"
    );
}
```

**Assertion style**: Value-based. Asserts exact counts and exact license identifier
lists. A regression that miscategorizes a license will show the actual vs expected
values, not just a boolean failure.

### Test 2: `test_license_summary_nonexistent_sbom`

```rust
/// Verifies that requesting a license summary for a non-existent SBOM ID returns 404.
#[test]
fn test_license_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID

    // When requesting the license summary
    let resp = client.get("/api/v2/sbom/{nonexistent-id}/license-summary").await;

    // Then the response status is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

**Assertion style**: Status code check -- this is a simple error case where value-based
assertions on the response body are not applicable. The status code assertion aligns
with both the skill guidance and sibling conventions.

### Test 3: `test_license_summary_empty_sbom`

```rust
/// Verifies that an SBOM with no packages returns all-zero counts and empty license lists.
#[test]
fn test_license_summary_empty_sbom() {
    // Given an SBOM that exists but has no associated packages
    // (set up via test database fixtures -- SBOM with no sbom_package rows)

    // When requesting the license summary
    let resp = client.get("/api/v2/sbom/{empty-sbom-id}/license-summary").await;

    // Then the response status is 200
    assert_eq!(resp.status(), StatusCode::OK);

    // Then all categories have zero counts and empty license lists
    let summary: LicenseSummary = resp.json().await;
    assert_eq!(summary.permissive.count, 0, "permissive count should be zero");
    assert_eq!(summary.copyleft.count, 0, "copyleft count should be zero");
    assert_eq!(summary.unknown.count, 0, "unknown count should be zero");
    assert!(summary.permissive.licenses.is_empty(), "permissive licenses should be empty");
    assert!(summary.copyleft.licenses.is_empty(), "copyleft licenses should be empty");
    assert!(summary.unknown.licenses.is_empty(), "unknown licenses should be empty");
}
```

**Assertion style**: Value-based. Asserts exact zero counts and empty lists rather than
just checking that the response is OK. This catches regressions where default/fallback
logic incorrectly populates empty SBOMs.

### Test 4: `test_license_summary_deduplication`

```rust
/// Verifies that duplicate licenses within a category are counted only once,
/// producing deduplicated license identifier lists.
#[test]
fn test_license_summary_deduplication() {
    // Given an SBOM with multiple packages that share the same license:
    //   - Package A: MIT
    //   - Package B: MIT
    //   - Package C: Apache-2.0
    // (set up via test database fixtures)

    // When requesting the license summary
    let resp = client.get("/api/v2/sbom/{dedup-sbom-id}/license-summary").await;

    // Then the response status is 200
    assert_eq!(resp.status(), StatusCode::OK);

    // Then MIT appears only once in the permissive list (deduplicated)
    let summary: LicenseSummary = resp.json().await;
    assert_eq!(summary.permissive.count, 2, "should have 2 unique permissive licenses");
    assert_eq!(
        summary.permissive.licenses.iter().sorted().collect::<Vec<_>>(),
        vec!["Apache-2.0", "MIT"],
        "permissive licenses should be deduplicated"
    );

    // Then copyleft and unknown are both empty
    assert_eq!(summary.copyleft.count, 0);
    assert_eq!(summary.unknown.count, 0);
}
```

**Assertion style**: Value-based. Asserts the exact deduplicated count (2, not 3) and
the exact license list. A regression that breaks deduplication would show
`count: 3` vs expected `count: 2` and a duplicated `"MIT"` entry in the list --
far more diagnostic than `assert!(count > 0)`.

## Parameterized Tests

The skill recommends parameterized tests for repetitive cases sharing the same
algorithm. These four tests do NOT share the same algorithm -- each has distinct setup
(different fixture data), different assertions (counts vs status codes vs empty checks),
and different verification goals. Per the Meszaros heuristic, individual test functions
are appropriate here.

Additionally, sibling tests (`advisory.rs`, `sbom.rs`) do not use parameterized test
mechanisms (no `rstest` usage observed), so introducing parameterized tests would
diverge from project conventions without benefit.

## Summary of Sibling Convention Overrides

| Aspect | Sibling Pattern | Skill Guidance | Decision |
|--------|----------------|----------------|----------|
| Assertion style | `.filter().any()`, `.filter().count() > 0` (existence-only) | Prefer value-based assertions (`assert_eq!` on specific values) | **Skill guidance wins** -- use value-based assertions |
| Test documentation | No doc comments on test functions observed | Every test function must have a `///` doc comment | **Skill guidance wins** -- add doc comments |
| Given/When/Then | Not observed in siblings | Non-trivial tests should include section comments | **Skill guidance wins** -- add section comments |
| Test naming | `test_<noun>_<scenario>` | No specific override | **Sibling convention adopted** |
| Setup/teardown | Shared test DB setup | No specific override | **Sibling convention adopted** |
| Status code checks | `assert_eq!(resp.status(), StatusCode::OK)` | No conflict (this is value-based) | **Sibling convention adopted** |
| Assertion messages | Descriptive messages in assert macros | No specific override | **Sibling convention adopted** |
