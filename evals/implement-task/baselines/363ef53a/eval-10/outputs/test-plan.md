# Test Plan: TC-9208 -- Package License Summary Endpoint

## Test File

`tests/api/package_license.rs`

## Assertion Approach

All tests use **value-based assertions** per the implement-task skill's quality guidance.
This means using `assert_eq!` on specific license identifiers and exact counts rather than
the `.filter().any()` or `.filter().count() > 0` existence-check patterns found in sibling
test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`).

Value-based assertions reveal *what* changed when a test fails, not just *how many* items
matched, making regressions immediately diagnosable.

## Sibling Conventions Followed (Non-Conflicting)

- **Test naming**: `test_<verb>_license_summary_<scenario>` matching the sibling naming pattern
- **Setup/teardown**: use the shared PostgreSQL test database helpers used by `advisory.rs`
  and `sbom.rs`
- **Status code check first**: every test begins with `assert_eq!(resp.status(), StatusCode::OK)`
  (or the expected error status) before inspecting the response body
- **Test organization**: one test function per distinct scenario; test file in `tests/api/`
- **Given-When-Then comments**: added per skill guidance for non-trivial tests (this is
  additive, not conflicting with siblings)
- **Doc comments**: every test function has a `///` doc comment per skill guidance

## Test Cases

### 1. `test_get_license_summary_with_known_licenses`

> Verifies that a valid SBOM with known package licenses returns the correct categorized
> counts and specific license identifiers in each category.

**Setup**: Ingest an SBOM containing packages with known licenses -- e.g., two permissive
(MIT, Apache-2.0), one copyleft (GPL-3.0-only), and one unknown (LicenseRef-custom).

**Assertions (value-based)**:
```rust
// Then the permissive category contains exactly the expected licenses
assert_eq!(body.permissive.count, 2);
assert_eq!(body.permissive.licenses, vec!["Apache-2.0", "MIT"]);

// And the copyleft category contains exactly the expected license
assert_eq!(body.copyleft.count, 1);
assert_eq!(body.copyleft.licenses, vec!["GPL-3.0-only"]);

// And the unknown category contains exactly the expected license
assert_eq!(body.unknown.count, 1);
assert_eq!(body.unknown.licenses, vec!["LicenseRef-custom"]);
```

Note: license lists are sorted alphabetically for deterministic comparison. This is a
deliberate departure from the sibling pattern (which would use
`.filter(|l| l == "MIT").any(|_| true)`) because it verifies the complete response
content, not just existence.

### 2. `test_get_license_summary_sbom_not_found`

> Verifies that requesting a license summary for a non-existent SBOM ID returns 404.

**Setup**: Use a UUID that does not correspond to any ingested SBOM.

**Assertions**:
```rust
// Then the response status is 404
assert_eq!(resp.status(), StatusCode::NOT_FOUND);
```

This test is trivial (single assertion, no distinct setup phase) so Given-When-Then
comments are omitted per skill guidance.

### 3. `test_get_license_summary_empty_sbom`

> Verifies that an SBOM with no packages returns all-zero counts and empty license lists.

**Setup**: Ingest an SBOM that contains no package entries.

**Assertions (value-based)**:
```rust
// Then all categories have zero counts and empty license lists
assert_eq!(body.permissive.count, 0);
assert_eq!(body.permissive.licenses, Vec::<String>::new());
assert_eq!(body.copyleft.count, 0);
assert_eq!(body.copyleft.licenses, Vec::<String>::new());
assert_eq!(body.unknown.count, 0);
assert_eq!(body.unknown.licenses, Vec::<String>::new());
```

### 4. `test_get_license_summary_deduplicates_licenses`

> Verifies that duplicate licenses within a category are counted only once.

**Setup**: Ingest an SBOM with multiple packages that share the same license (e.g., three
packages all licensed under MIT, and two packages under Apache-2.0).

**Assertions (value-based)**:
```rust
// Then MIT and Apache-2.0 each appear exactly once despite multiple packages using them
assert_eq!(body.permissive.count, 2);
assert_eq!(body.permissive.licenses, vec!["Apache-2.0", "MIT"]);

// And no copyleft or unknown licenses are present
assert_eq!(body.copyleft.count, 0);
assert_eq!(body.copyleft.licenses, Vec::<String>::new());
assert_eq!(body.unknown.count, 0);
assert_eq!(body.unknown.licenses, Vec::<String>::new());
```

This asserts the exact deduplicated content -- not just that `count < total_packages` or
that `.filter(|l| l == "MIT").count() > 0`. If deduplication fails, the assertion will
show the actual duplicate entries rather than silently passing on a correct count.

## Why Not Sibling Assertion Patterns

The sibling tests in `advisory.rs` and `sbom.rs` use `.filter().any()` and
`.filter().count() > 0` existence checks. These patterns have two weaknesses for the
license summary use case:

1. **They hide regressions**: if the categorization logic assigns MIT to the "unknown"
   category instead of "permissive", an `.any()` check on the permissive category would
   fail, but it would not reveal *what* is actually in the category. A value-based
   `assert_eq!` immediately shows the actual vs. expected content.

2. **They skip completeness validation**: checking that at least one permissive license
   exists does not verify that *all* expected licenses are present and *no* unexpected
   ones are included. `assert_eq!` on the full sorted list validates both presence and
   absence.

The skill's Step 7 guidance explicitly requires value-based assertions over existence
checks, and Step 4 establishes that skill guidance takes precedence over sibling patterns.
The sibling conventions are followed for all non-conflicting aspects (naming, setup,
organization, status code checks).
