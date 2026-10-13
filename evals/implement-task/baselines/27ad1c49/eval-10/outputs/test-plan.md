# Test Plan for TC-9208

## Test File

`tests/api/package_license.rs` -- integration tests for `GET /api/v2/sbom/{id}/license-summary`

## Conventions Followed from Siblings

The following non-conflicting conventions from `tests/api/advisory.rs` and
`tests/api/sbom.rs` are adopted:

- **File location**: `tests/api/` directory
- **Naming**: `test_` prefix with descriptive snake_case names
- **Setup**: shared test database harness; insert known test data before assertions
- **Status code checks**: `assert_eq!(resp.status(), StatusCode::OK)` and
  `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **HTTP client**: use the project's test client to make requests against the test server

## Assertion Style Override

The sibling `.filter().any()` and `.filter().count() > 0` patterns are **not** used.
Per the skill's Step 7 guidance ("prefer value-based assertions over length-only
checks"), all assertions use `assert_eq!` on specific values so that failures reveal
exactly what changed.

## Test Cases

### 1. `test_license_summary_returns_categorized_counts`

/// Verifies that a valid SBOM with known package licenses returns the correct
/// categorized counts and license identifiers.

**Setup**: Insert an SBOM with packages having known licenses:
- 2 permissive licenses (e.g., "MIT", "Apache-2.0")
- 1 copyleft license (e.g., "GPL-3.0-only")
- 1 unknown license (e.g., "LicenseRef-custom")

**Assertions (value-based)**:
```rust
// Given an SBOM with known package licenses inserted into the test database
let sbom_id = insert_test_sbom_with_licenses(&db, vec![
    ("MIT", "permissive"),
    ("Apache-2.0", "permissive"),
    ("GPL-3.0-only", "copyleft"),
    ("LicenseRef-custom", "unknown"),
]).await;

// When requesting the license summary
let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", sbom_id)).await;

// Then the response status is OK
assert_eq!(resp.status(), StatusCode::OK);

let summary: LicenseSummary = resp.json().await;

// Then the permissive category contains exactly the expected licenses
assert_eq!(summary.permissive.count, 2);
assert_eq!(summary.permissive.licenses.len(), 2);
assert!(summary.permissive.licenses.contains(&"MIT".to_string()));
assert!(summary.permissive.licenses.contains(&"Apache-2.0".to_string()));

// Then the copyleft category contains exactly the expected license
assert_eq!(summary.copyleft.count, 1);
assert_eq!(summary.copyleft.licenses, vec!["GPL-3.0-only".to_string()]);

// Then the unknown category contains exactly the expected license
assert_eq!(summary.unknown.count, 1);
assert_eq!(summary.unknown.licenses, vec!["LicenseRef-custom".to_string()]);
```

This uses `assert_eq!` on exact counts and checks for specific license identifiers
rather than `.any()` or `.count() > 0`. A regression that swaps "MIT" for "BSD-2-Clause"
or drops "Apache-2.0" would be caught, whereas an existence check would not.

### 2. `test_license_summary_returns_404_for_nonexistent_sbom`

/// Verifies that requesting a license summary for a non-existent SBOM ID returns 404.

**Setup**: Use a UUID that does not correspond to any SBOM in the test database.

**Assertions (value-based)**:
```rust
// Given a non-existent SBOM ID
let fake_id = Uuid::new_v4();

// When requesting the license summary
let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", fake_id)).await;

// Then the response status is NOT_FOUND
assert_eq!(resp.status(), StatusCode::NOT_FOUND);
```

### 3. `test_license_summary_empty_sbom_returns_zeros`

/// Verifies that an SBOM with no packages returns all-zero counts with empty license lists.

**Setup**: Insert an SBOM with no associated packages.

**Assertions (value-based)**:
```rust
// Given an SBOM with no packages
let sbom_id = insert_test_sbom_without_packages(&db).await;

// When requesting the license summary
let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", sbom_id)).await;

// Then the response status is OK
assert_eq!(resp.status(), StatusCode::OK);

let summary: LicenseSummary = resp.json().await;

// Then all categories have zero counts and empty license lists
assert_eq!(summary.permissive.count, 0);
assert_eq!(summary.permissive.licenses, Vec::<String>::new());
assert_eq!(summary.copyleft.count, 0);
assert_eq!(summary.copyleft.licenses, Vec::<String>::new());
assert_eq!(summary.unknown.count, 0);
assert_eq!(summary.unknown.licenses, Vec::<String>::new());
```

Asserting `Vec::<String>::new()` rather than `.is_empty()` makes the expected value
explicit and produces a clearer diff on failure.

### 4. `test_license_summary_deduplicates_licenses`

/// Verifies that duplicate licenses within a category are counted only once.

**Setup**: Insert an SBOM with multiple packages that share the same license
(e.g., three packages all using "MIT").

**Assertions (value-based)**:
```rust
// Given an SBOM where three packages all use the MIT license
let sbom_id = insert_test_sbom_with_licenses(&db, vec![
    ("MIT", "permissive"),
    ("MIT", "permissive"),
    ("MIT", "permissive"),
]).await;

// When requesting the license summary
let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", sbom_id)).await;

// Then the response status is OK
assert_eq!(resp.status(), StatusCode::OK);

let summary: LicenseSummary = resp.json().await;

// Then MIT appears exactly once in the permissive category (deduplicated)
assert_eq!(summary.permissive.count, 1);
assert_eq!(summary.permissive.licenses, vec!["MIT".to_string()]);

// Then other categories remain empty
assert_eq!(summary.copyleft.count, 0);
assert_eq!(summary.copyleft.licenses, Vec::<String>::new());
assert_eq!(summary.unknown.count, 0);
assert_eq!(summary.unknown.licenses, Vec::<String>::new());
```

This asserts the exact deduplicated count (1, not 3) and the specific license
identifier, catching any regression in the deduplication logic. A `.count() > 0`
check would pass even if deduplication were broken (count would be 3, still > 0).

## Summary of Assertion Strategy

| Aspect | Sibling Pattern | This Test Plan | Reason |
|--------|----------------|----------------|--------|
| Status codes | `assert_eq!` on `StatusCode` | Same | No conflict |
| Collection contents | `.filter().any()` | `assert_eq!` on specific values | Skill Step 7 override |
| Collection size | `.filter().count() > 0` | `assert_eq!` on exact count | Skill Step 7 override |
| Test naming | `test_` + snake_case | Same | No conflict |
| Setup/teardown | Shared test DB harness | Same | No conflict |
| Test documentation | Not present in siblings | Added (doc comments + given/when/then) | Skill Step 7 requires it |
