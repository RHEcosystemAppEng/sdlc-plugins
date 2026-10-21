# Test Plan -- TC-9208

## Assertion Approach

All tests use **value-based assertions** (`assert_eq!` on specific values and counts),
not existence checks (`.any()` or `.count() > 0`). This follows the skill's explicit
quality guidance, which takes precedence over the sibling `.filter().any()` and
`.filter().count() > 0` patterns found in `tests/api/advisory.rs` and `tests/api/sbom.rs`.

See `conventions.md` for the full conflict analysis.

## Test File

`tests/api/package_license.rs`

## Test Functions

### 1. `test_license_summary_returns_correct_categorized_counts`

**Covers**: "Test that a valid SBOM with known package licenses returns correct categorized counts"

**Setup (Given)**:
- Insert a test SBOM into the database.
- Insert packages linked to the SBOM via `sbom_package`.
- Insert package licenses with known SPDX identifiers spanning all three categories:
  - Permissive: "MIT", "Apache-2.0"
  - Copyleft: "GPL-3.0-only"
  - Unknown: "LicenseRef-Custom"

**Action (When)**:
- Send `GET /api/v2/sbom/{id}/license-summary` with the test SBOM's ID.

**Assertions (Then)**:
```rust
assert_eq!(resp.status(), StatusCode::OK);
let summary: LicenseSummary = resp.json().await;

// Value-based assertions on exact counts
assert_eq!(summary.permissive.count, 2);
assert_eq!(summary.copyleft.count, 1);
assert_eq!(summary.unknown.count, 1);

// Value-based assertions on specific license identifiers
assert_eq!(summary.permissive.licenses, vec!["Apache-2.0", "MIT"]);
assert_eq!(summary.copyleft.licenses, vec!["GPL-3.0-only"]);
assert_eq!(summary.unknown.licenses, vec!["LicenseRef-Custom"]);
```

Note: License lists are sorted alphabetically for deterministic comparison.

### 2. `test_license_summary_returns_404_for_nonexistent_sbom`

**Covers**: "Test that a non-existent SBOM ID returns 404"

**Setup (Given)**:
- Generate a random UUID that does not correspond to any SBOM in the database.

**Action (When)**:
- Send `GET /api/v2/sbom/{id}/license-summary` with the non-existent UUID.

**Assertions (Then)**:
```rust
assert_eq!(resp.status(), StatusCode::NOT_FOUND);
```

This test is trivial (single assertion, no distinct setup phase), so given-when-then
section comments are optional per skill guidance.

### 3. `test_license_summary_returns_empty_for_sbom_with_no_packages`

**Covers**: "Test that an SBOM with no packages returns all zeros with empty license lists"

**Setup (Given)**:
- Insert a test SBOM with no associated packages (no `sbom_package` rows).

**Action (When)**:
- Send `GET /api/v2/sbom/{id}/license-summary` with the empty SBOM's ID.

**Assertions (Then)**:
```rust
assert_eq!(resp.status(), StatusCode::OK);
let summary: LicenseSummary = resp.json().await;

// Value-based assertions: all counts are exactly zero
assert_eq!(summary.permissive.count, 0);
assert_eq!(summary.copyleft.count, 0);
assert_eq!(summary.unknown.count, 0);

// Value-based assertions: all license lists are empty
assert_eq!(summary.permissive.licenses, Vec::<String>::new());
assert_eq!(summary.copyleft.licenses, Vec::<String>::new());
assert_eq!(summary.unknown.licenses, Vec::<String>::new());
```

### 4. `test_license_summary_deduplicates_licenses_within_category`

**Covers**: "Test that duplicate licenses within a category are counted only once"

**Setup (Given)**:
- Insert a test SBOM with multiple packages.
- Assign the same license identifier ("MIT") to two different packages via `package_license`.
- Also assign "Apache-2.0" to one package (to verify non-duplicated licenses are unaffected).

**Action (When)**:
- Send `GET /api/v2/sbom/{id}/license-summary` with the test SBOM's ID.

**Assertions (Then)**:
```rust
assert_eq!(resp.status(), StatusCode::OK);
let summary: LicenseSummary = resp.json().await;

// "MIT" appears on two packages but should be counted only once after deduplication
assert_eq!(summary.permissive.count, 2);  // MIT + Apache-2.0
assert_eq!(summary.permissive.licenses, vec!["Apache-2.0", "MIT"]);

// Other categories unaffected
assert_eq!(summary.copyleft.count, 0);
assert_eq!(summary.unknown.count, 0);
```

## Documentation

Every test function has a `///` documentation comment explaining what it verifies,
per skill guidance (Step 7). Non-trivial tests (1, 3, 4) include `// Given`,
`// When`, `// Then` section comments inside the test body.

## Why Not Sibling Assertion Patterns

The sibling tests in `advisory.rs` and `sbom.rs` use `.filter().any()` and
`.filter().count() > 0` for response validation. These are existence checks that:

1. Do not verify exact counts -- a regression adding extra items would pass silently.
2. Do not verify specific values -- a regression changing license categorization would
   pass as long as at least one item remains.
3. Produce unhelpful failure messages -- "assertion failed: has_critical" does not
   reveal what the response actually contained.

The skill's Step 7 explicitly states: "Prefer value-based assertions over length-only
checks" and "Skill guidance overrides sibling patterns." Therefore, all assertions in
this test plan use `assert_eq!` with specific expected values. The sibling patterns are
followed for all non-conflicting aspects: file naming (`package_license.rs` in
`tests/api/`), test setup and teardown patterns, HTTP client usage, and status code
assertion style (`assert_eq!(resp.status(), StatusCode::OK)`).
