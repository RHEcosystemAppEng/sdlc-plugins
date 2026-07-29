# Test Plan for TC-9208: Package License Summary Endpoint

## Test File

`tests/api/package_license.rs`

## Conventions Followed from Siblings

The following non-conflicting conventions from `tests/api/advisory.rs` and
`tests/api/sbom.rs` are adopted:

- **Test naming:** `test_<endpoint>_<scenario>` pattern
- **Test setup:** Real PostgreSQL test database with fixtures created via the ingestion
  pipeline or direct DB insertion
- **Test organization:** Separate file in `tests/api/` dedicated to the license summary
  endpoint
- **Status code assertions:** `assert_eq!(resp.status(), StatusCode::OK)` and
  `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Response handling:** Deserialize response body into typed structs before asserting

## Assertion Approach: Value-Based (Overriding Sibling Pattern)

The sibling tests use `.filter().any()` and `.filter().count() > 0` existence checks.
These are overridden in favor of value-based assertions per the skill's Step 7 guidance.
Value-based assertions reveal *what* changed on failure, not just that something is
missing.

## Test Cases

### 1. `test_license_summary_valid_sbom`

/// Verifies that a valid SBOM with known package licenses returns correctly categorized
/// counts and license identifiers.

**Setup:** Create a test SBOM with packages that have known licenses:
- Package A: MIT (permissive)
- Package B: Apache-2.0 (permissive)
- Package C: GPL-3.0 (copyleft)
- Package D: Unknown-License-XYZ (unknown)

**Action:** `GET /api/v2/sbom/{test_sbom_id}/license-summary`

**Assertions (value-based):**
```rust
// Given a test SBOM with known package licenses
// ... (fixture setup)

// When requesting the license summary
let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", sbom_id)).await;

// Then the response status is OK
assert_eq!(resp.status(), StatusCode::OK);

let summary: LicenseSummary = resp.json().await;

// Then the permissive category contains exactly MIT and Apache-2.0
assert_eq!(summary.permissive.count, 2);
assert_eq!(
    summary.permissive.licenses.iter().collect::<HashSet<_>>(),
    HashSet::from([&"MIT".to_string(), &"Apache-2.0".to_string()])
);

// Then the copyleft category contains exactly GPL-3.0
assert_eq!(summary.copyleft.count, 1);
assert_eq!(summary.copyleft.licenses, vec!["GPL-3.0"]);

// Then the unknown category contains exactly the unrecognized license
assert_eq!(summary.unknown.count, 1);
assert_eq!(summary.unknown.licenses, vec!["Unknown-License-XYZ"]);
```

Note: We use `assert_eq!` on specific license identifiers and exact counts rather than
the sibling `.filter().any()` or `.count() > 0` patterns. This ensures that if a
license is misclassified or missing, the test failure message shows exactly which
license and category are wrong.

### 2. `test_license_summary_not_found`

/// Verifies that requesting a license summary for a non-existent SBOM ID returns 404.

**Setup:** No specific fixture needed; use a UUID that does not exist in the database.

**Action:** `GET /api/v2/sbom/{nonexistent_id}/license-summary`

**Assertions:**
```rust
// Given a non-existent SBOM ID
let fake_id = Uuid::new_v4();

// When requesting the license summary
let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", fake_id)).await;

// Then the response status is NOT FOUND
assert_eq!(resp.status(), StatusCode::NOT_FOUND);
```

### 3. `test_license_summary_empty_sbom`

/// Verifies that an SBOM with no packages returns zero counts and empty license lists
/// for all categories.

**Setup:** Create a test SBOM with no packages attached.

**Action:** `GET /api/v2/sbom/{empty_sbom_id}/license-summary`

**Assertions (value-based):**
```rust
// Given an SBOM with no packages
// ... (fixture setup)

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

### 4. `test_license_summary_deduplication`

/// Verifies that duplicate licenses within a category are counted only once in both
/// the count and the license list.

**Setup:** Create a test SBOM with multiple packages sharing the same license:
- Package A: MIT (permissive)
- Package B: MIT (permissive) -- duplicate
- Package C: Apache-2.0 (permissive)

**Action:** `GET /api/v2/sbom/{test_sbom_id}/license-summary`

**Assertions (value-based):**
```rust
// Given an SBOM where two packages share the MIT license
// ... (fixture setup)

// When requesting the license summary
let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", sbom_id)).await;

// Then the response status is OK
assert_eq!(resp.status(), StatusCode::OK);

let summary: LicenseSummary = resp.json().await;

// Then the permissive category has exactly 2 deduplicated licenses (MIT, Apache-2.0)
// not 3 (which would happen without deduplication)
assert_eq!(summary.permissive.count, 2);
assert_eq!(
    summary.permissive.licenses.iter().collect::<HashSet<_>>(),
    HashSet::from([&"MIT".to_string(), &"Apache-2.0".to_string()])
);

// Then copyleft and unknown are empty
assert_eq!(summary.copyleft.count, 0);
assert_eq!(summary.copyleft.licenses, Vec::<String>::new());
assert_eq!(summary.unknown.count, 0);
assert_eq!(summary.unknown.licenses, Vec::<String>::new());
```

## Summary of Assertion Strategy

| Aspect | Sibling Pattern | This Test Plan | Reason |
|---|---|---|---|
| Status codes | `assert_eq!(resp.status(), ...)` | `assert_eq!(resp.status(), ...)` | No conflict -- follow sibling |
| Collection values | `.filter().any()` existence check | `assert_eq!` on specific identifiers | Skill guidance overrides sibling |
| Counts | `.filter().count() > 0` | `assert_eq!` on exact counts | Skill guidance overrides sibling |
| Test naming | `test_<endpoint>_<scenario>` | `test_license_summary_<scenario>` | No conflict -- follow sibling |
| Setup/teardown | Real PostgreSQL test DB | Real PostgreSQL test DB | No conflict -- follow sibling |
| Test organization | File per endpoint in `tests/api/` | `tests/api/package_license.rs` | No conflict -- follow sibling |
| Test documentation | Not present in siblings | Doc comment on every test fn | Skill guidance adds new standard |
| Given-when-then | Not present in siblings | Section comments in test body | Skill guidance adds new standard |
