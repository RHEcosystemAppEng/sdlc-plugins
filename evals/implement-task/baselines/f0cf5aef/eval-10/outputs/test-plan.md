# Test Plan for TC-9208

## Test File

`tests/api/package_license.rs` -- integration tests for `GET /api/v2/sbom/{id}/license-summary`.

## Assertion Strategy

**Value-based assertions** are used throughout, per the implement-task skill's Step 7
guidance. The sibling test pattern of `.filter().any()` and `.filter().count() > 0`
(existence-only checks) is explicitly NOT adopted because it conflicts with the skill's
quality standard:

> "Prefer value-based assertions over length-only checks: assert on the actual values --
> not just the count."

Skill guidance takes precedence over sibling patterns for assertion style. All other
test conventions (naming, setup, organization, HTTP status checks) follow siblings.

## Test Functions

### 1. `test_license_summary_returns_correct_categorized_counts`

**Requirement:** Test that a valid SBOM with known package licenses returns correct
categorized counts.

**Setup (Given):**
- Create an SBOM in the test database.
- Create packages linked to the SBOM via `sbom_package`.
- Create `package_license` entries with known licenses:
  - "MIT" and "Apache-2.0" (permissive)
  - "GPL-3.0" (copyleft)
  - "LicenseRef-Custom" (unknown)

**Action (When):**
- Send `GET /api/v2/sbom/{id}/license-summary`.

**Assertions (Then):**
```rust
assert_eq!(resp.status(), StatusCode::OK);

let body: LicenseSummary = resp.json().await;

// Value-based assertions on exact counts
assert_eq!(body.permissive.count, 2);
assert_eq!(body.copyleft.count, 1);
assert_eq!(body.unknown.count, 1);

// Value-based assertions on specific license names
assert_eq!(body.permissive.licenses.len(), 2);
assert!(body.permissive.licenses.contains(&"MIT".to_string()));
assert!(body.permissive.licenses.contains(&"Apache-2.0".to_string()));

assert_eq!(body.copyleft.licenses.len(), 1);
assert_eq!(body.copyleft.licenses[0], "GPL-3.0");

assert_eq!(body.unknown.licenses.len(), 1);
assert_eq!(body.unknown.licenses[0], "LicenseRef-Custom");
```

**Why value-based:** Asserting `assert_eq!(body.permissive.count, 2)` and checking for
specific license names ("MIT", "Apache-2.0") reveals exactly what broke if the
categorization logic changes. A `.count() > 0` check would pass even if MIT were
miscategorized as copyleft, hiding a regression.

---

### 2. `test_license_summary_returns_404_for_nonexistent_sbom`

**Requirement:** Test that a non-existent SBOM ID returns 404.

**Setup (Given):**
- Generate a random UUID that does not correspond to any SBOM in the database.

**Action (When):**
- Send `GET /api/v2/sbom/{nonexistent-id}/license-summary`.

**Assertions (Then):**
```rust
assert_eq!(resp.status(), StatusCode::NOT_FOUND);
```

**Note:** This test is trivial (single assertion, no distinct setup phase), so
given-when-then section comments are omitted per skill guidance.

---

### 3. `test_license_summary_returns_empty_for_sbom_with_no_packages`

**Requirement:** Test that an SBOM with no packages returns all zeros with empty
license lists.

**Setup (Given):**
- Create an SBOM in the test database with no associated packages (no `sbom_package` entries).

**Action (When):**
- Send `GET /api/v2/sbom/{id}/license-summary`.

**Assertions (Then):**
```rust
assert_eq!(resp.status(), StatusCode::OK);

let body: LicenseSummary = resp.json().await;

// Value-based: assert exact zero counts, not just "less than something"
assert_eq!(body.permissive.count, 0);
assert_eq!(body.copyleft.count, 0);
assert_eq!(body.unknown.count, 0);

// Value-based: assert empty vectors, not just "length is 0"
assert!(body.permissive.licenses.is_empty());
assert!(body.copyleft.licenses.is_empty());
assert!(body.unknown.licenses.is_empty());
```

**Why value-based:** Explicitly asserting `count == 0` and `licenses.is_empty()` for each
category ensures no ghost data appears. A `.any()` check cannot verify absence.

---

### 4. `test_license_summary_deduplicates_licenses_within_category`

**Requirement:** Test that duplicate licenses within a category are counted only once.

**Setup (Given):**
- Create an SBOM in the test database.
- Create multiple packages linked to the SBOM.
- Assign the same license ("MIT") to multiple packages, creating duplicate
  `package_license` entries for "MIT".
- Also assign "Apache-2.0" to one package (to verify non-duplicates are unaffected).

**Action (When):**
- Send `GET /api/v2/sbom/{id}/license-summary`.

**Assertions (Then):**
```rust
assert_eq!(resp.status(), StatusCode::OK);

let body: LicenseSummary = resp.json().await;

// Value-based: exact count after deduplication (MIT appears once, Apache-2.0 once)
assert_eq!(body.permissive.count, 2);
assert_eq!(body.permissive.licenses.len(), 2);

// Value-based: verify specific deduplicated license names are present
assert!(body.permissive.licenses.contains(&"MIT".to_string()));
assert!(body.permissive.licenses.contains(&"Apache-2.0".to_string()));

// Value-based: verify copyleft and unknown are empty (no such licenses in test data)
assert_eq!(body.copyleft.count, 0);
assert_eq!(body.unknown.count, 0);
```

**Why value-based:** If deduplication fails, `count` would be 3 (MIT appearing twice plus
Apache-2.0) instead of the expected 2. An `assert!(count > 0)` check would pass regardless
of whether deduplication works, completely defeating the purpose of this test case.

## Documentation Convention

Every test function will have a `///` doc comment explaining what it verifies, per the
skill's Step 7 guidance. Example:

```rust
/// Verifies that a valid SBOM with known package licenses returns correctly
/// categorized counts and specific license identifiers in each category.
#[tokio::test]
async fn test_license_summary_returns_correct_categorized_counts() {
    // Given ...
    // When ...
    // Then ...
}
```

## Conventions Followed from Siblings (Non-Conflicting)

- **Test file location:** `tests/api/package_license.rs` (follows `tests/api/<domain>.rs` pattern)
- **Test naming:** `test_<action>_<scenario>` format
- **Test attribute:** `#[tokio::test]` for async integration tests
- **HTTP status checks:** `assert_eq!(resp.status(), StatusCode::OK)` and `StatusCode::NOT_FOUND`
- **Database setup:** Real PostgreSQL test database with test data created per function
- **No parameterized tests:** Sibling tests do not use `rstest`; individual test functions are used

## Convention Overridden

- **Assertion style:** Sibling patterns `.filter().any()` and `.filter().count() > 0` are
  replaced with value-based `assert_eq!` assertions on specific counts, specific license
  names, and exact list contents. This is the ONLY override; all other conventions match siblings.
