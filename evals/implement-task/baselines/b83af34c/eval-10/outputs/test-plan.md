# Test Plan for TC-9208

## Test File

`tests/api/package_license.rs`

## Assertion Approach

**Value-based assertions** are used throughout, per the skill's explicit quality
guidance in Step 7. Sibling tests in `tests/api/advisory.rs` and `tests/api/sbom.rs`
use `.filter().any()` and `.filter().count() > 0` patterns, but these are overridden
by the skill's instruction to "prefer value-based assertions over length-only checks."

Value-based assertions reveal *what* changed when a test fails, not just *how many*
items matched. This catches regressions that existence-only checks would miss.

## Test Cases

### 1. `test_license_summary_valid_sbom`

/// Verifies that an SBOM with known package licenses returns correctly categorized
/// counts and license identifiers.

**Setup:** Ingest a test SBOM containing packages with known licenses:
- 2 permissive licenses: MIT, Apache-2.0
- 1 copyleft license: GPL-3.0
- 1 unknown license: LicenseRef-custom

**Action:** `GET /api/v2/sbom/{id}/license-summary`

**Assertions (value-based):**
```rust
assert_eq!(resp.status(), StatusCode::OK);
let body: LicenseSummary = resp.json().await;

// Assert exact counts — not count > 0
assert_eq!(body.permissive.count, 2);
assert_eq!(body.copyleft.count, 1);
assert_eq!(body.unknown.count, 1);

// Assert specific license identifiers — not .any() existence checks
assert!(body.permissive.licenses.contains(&"MIT".to_string()));
assert!(body.permissive.licenses.contains(&"Apache-2.0".to_string()));
assert_eq!(body.copyleft.licenses, vec!["GPL-3.0".to_string()]);
assert_eq!(body.unknown.licenses, vec!["LicenseRef-custom".to_string()]);
```

**Why not `.any()` / `.count() > 0`:** If a regression changed the categorization
logic so that MIT was classified as "unknown" instead of "permissive," an
`.any()` check on permissive would still pass (Apache-2.0 remains). The
`assert_eq!(count, 2)` and `.contains("MIT")` assertions catch this.

### 2. `test_license_summary_not_found`

/// Verifies that requesting a license summary for a non-existent SBOM returns 404.

**Setup:** No fixture needed.

**Action:** `GET /api/v2/sbom/{nonexistent-uuid}/license-summary`

**Assertions (value-based):**
```rust
assert_eq!(resp.status(), StatusCode::NOT_FOUND);
```

This follows the sibling 404 test convention (no conflict with skill guidance).

### 3. `test_license_summary_empty_sbom`

/// Verifies that an SBOM with no packages returns zero counts and empty license lists.

**Setup:** Ingest a test SBOM that contains no packages (an empty SBOM document).

**Action:** `GET /api/v2/sbom/{id}/license-summary`

**Assertions (value-based):**
```rust
assert_eq!(resp.status(), StatusCode::OK);
let body: LicenseSummary = resp.json().await;

// Assert exact zero counts — not just "less than 1" or similar
assert_eq!(body.permissive.count, 0);
assert_eq!(body.copyleft.count, 0);
assert_eq!(body.unknown.count, 0);

// Assert empty lists — not just .is_empty() alone
assert_eq!(body.permissive.licenses, Vec::<String>::new());
assert_eq!(body.copyleft.licenses, Vec::<String>::new());
assert_eq!(body.unknown.licenses, Vec::<String>::new());
```

### 4. `test_license_summary_deduplication`

/// Verifies that duplicate licenses within the same category are counted only once.

**Setup:** Ingest a test SBOM containing multiple packages that share the same
license (e.g., three packages all using MIT).

**Action:** `GET /api/v2/sbom/{id}/license-summary`

**Assertions (value-based):**
```rust
assert_eq!(resp.status(), StatusCode::OK);
let body: LicenseSummary = resp.json().await;

// Even though 3 packages have MIT, deduplicated count should be 1
assert_eq!(body.permissive.count, 1);
assert_eq!(body.permissive.licenses, vec!["MIT".to_string()]);
```

**Why not `.count() > 0`:** The deduplication test specifically needs to verify
that the count is exactly 1, not merely that something exists. A `.count() > 0`
assertion would pass even if deduplication was broken and returned 3.

## Conventions Followed from Siblings (non-conflicting)

- **File location:** `tests/api/package_license.rs` (matches `tests/api/<entity>.rs` pattern)
- **Function naming:** `test_license_summary_<scenario>` (matches `test_<endpoint>_<scenario>`)
- **Setup:** Real PostgreSQL test database with fixture ingestion
- **Status assertions:** `assert_eq!(resp.status(), StatusCode::OK)` as first assertion
- **404 test:** Dedicated test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test documentation:** Every test function has a `///` doc comment (skill requirement,
  applied regardless of sibling practice)
- **Given-When-Then:** Section comments used in non-trivial tests (skill requirement)

## Conventions NOT Followed from Siblings (conflict resolved)

- **NOT using** `.filter().any()` existence checks (sibling pattern from `advisory.rs`)
- **NOT using** `.filter().count() > 0` existence checks (sibling pattern from `sbom.rs`)
- **Instead using** `assert_eq!` on exact counts and specific value comparisons
- **Reason:** Skill Step 7 guidance takes precedence per Step 4's explicit rule
