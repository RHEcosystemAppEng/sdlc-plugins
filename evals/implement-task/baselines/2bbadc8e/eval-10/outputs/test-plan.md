# Test Plan: TC-9208

## Assertion Approach

All tests use **value-based assertions** (`assert_eq!` on specific expected values)
per the implement-task skill's quality guidance. The sibling `.filter().any()` and
`.filter().count() > 0` patterns are explicitly not used, as documented in
`conventions.md`. This ensures test failures reveal *what* changed, not just *how many*.

## Test File

`tests/api/package_license.rs`

## Test 1: `test_license_summary_with_known_packages`

**Requirement:** Test that a valid SBOM with known package licenses returns correct
categorized counts.

**Doc comment:** `/// Verifies that an SBOM with known package licenses returns correctly categorized counts and license lists.`

**Setup (Given):**
- Insert an SBOM record into the test database.
- Insert packages with known licenses:
  - Package A with license "MIT" (permissive)
  - Package B with license "Apache-2.0" (permissive)
  - Package C with license "GPL-3.0-only" (copyleft)
  - Package D with license "UNKNOWN-LICENSE" (unknown)
- Link all packages to the SBOM via `sbom_package`.

**Action (When):**
- Send `GET /api/v2/sbom/{id}/license-summary` with the test SBOM's ID.

**Assertions (Then):**
```rust
assert_eq!(resp.status(), StatusCode::OK);

let body: LicenseSummary = resp.json().await;

// Value-based assertions on permissive category
assert_eq!(body.permissive.count, 2);
assert_eq!(body.permissive.licenses, vec!["Apache-2.0", "MIT"]);

// Value-based assertions on copyleft category
assert_eq!(body.copyleft.count, 1);
assert_eq!(body.copyleft.licenses, vec!["GPL-3.0-only"]);

// Value-based assertions on unknown category
assert_eq!(body.unknown.count, 1);
assert_eq!(body.unknown.licenses, vec!["UNKNOWN-LICENSE"]);
```

**Why not sibling pattern:** The sibling pattern would be:
```rust
// NOT USED -- existence check hides regressions
let has_mit = body.permissive.licenses.iter().any(|l| l == "MIT");
assert!(has_mit);
```
This would pass even if Apache-2.0 were missing or extra licenses appeared. The
`assert_eq!` approach catches any deviation from the expected set.

---

## Test 2: `test_license_summary_sbom_not_found`

**Requirement:** Test that a non-existent SBOM ID returns 404.

**Doc comment:** `/// Verifies that requesting a license summary for a non-existent SBOM returns 404.`

**Setup (Given):**
- Use a randomly generated UUID that does not correspond to any SBOM in the test database.

**Action (When):**
- Send `GET /api/v2/sbom/{non_existent_id}/license-summary`.

**Assertions (Then):**
```rust
assert_eq!(resp.status(), StatusCode::NOT_FOUND);
```

**Note:** This assertion is already value-based and consistent with both skill guidance
and sibling patterns. No conflict here.

---

## Test 3: `test_license_summary_empty_sbom`

**Requirement:** Test that an SBOM with no packages returns all zeros with empty license lists.

**Doc comment:** `/// Verifies that an SBOM with no linked packages returns zero counts and empty license lists for all categories.`

**Setup (Given):**
- Insert an SBOM record with no linked packages (no `sbom_package` entries).

**Action (When):**
- Send `GET /api/v2/sbom/{id}/license-summary` with the empty SBOM's ID.

**Assertions (Then):**
```rust
assert_eq!(resp.status(), StatusCode::OK);

let body: LicenseSummary = resp.json().await;

// Assert exact zero values and empty lists -- not just "count >= 0"
assert_eq!(body.permissive.count, 0);
assert_eq!(body.permissive.licenses, Vec::<String>::new());

assert_eq!(body.copyleft.count, 0);
assert_eq!(body.copyleft.licenses, Vec::<String>::new());

assert_eq!(body.unknown.count, 0);
assert_eq!(body.unknown.licenses, Vec::<String>::new());
```

**Why not sibling pattern:** A `.count() > 0` style check is meaningless here (we are
asserting zero), and `.any()` would be vacuously false without revealing whether the
structure is correct. The `assert_eq!` approach verifies the exact shape of the response.

---

## Test 4: `test_license_summary_deduplication`

**Requirement:** Test that duplicate licenses within a category are counted only once.

**Doc comment:** `/// Verifies that duplicate license identifiers within a single category are deduplicated, appearing only once in the count and list.`

**Setup (Given):**
- Insert an SBOM record.
- Insert three packages, two of which share the same license:
  - Package X with license "MIT" (permissive)
  - Package Y with license "MIT" (permissive -- duplicate)
  - Package Z with license "GPL-2.0-only" (copyleft)
- Link all packages to the SBOM.

**Action (When):**
- Send `GET /api/v2/sbom/{id}/license-summary`.

**Assertions (Then):**
```rust
assert_eq!(resp.status(), StatusCode::OK);

let body: LicenseSummary = resp.json().await;

// MIT should appear only once despite two packages having it
assert_eq!(body.permissive.count, 1);
assert_eq!(body.permissive.licenses, vec!["MIT"]);

assert_eq!(body.copyleft.count, 1);
assert_eq!(body.copyleft.licenses, vec!["GPL-2.0-only"]);

assert_eq!(body.unknown.count, 0);
assert_eq!(body.unknown.licenses, Vec::<String>::new());
```

**Why not sibling pattern:** The sibling pattern
`result.items.iter().filter(|s| s.name.contains("MIT")).count() > 0` would pass even
if deduplication were broken (two MITs would still satisfy `> 0`). The `assert_eq!`
on `count, 1` directly verifies the deduplication behavior.

---

## Conventions Followed (Non-Conflicting)

| Convention | Source | Applied |
|---|---|---|
| `#[tokio::test]` async test functions | Sibling tests | Yes |
| Test file in `tests/api/` directory | Sibling tests | Yes |
| `test_` prefix with descriptive name | Sibling tests | Yes |
| Shared test database setup harness | Sibling tests | Yes |
| `assert_eq!(resp.status(), StatusCode::OK)` for status checks | Sibling tests | Yes |
| `///` doc comments on every test function | Skill guidance (new standard) | Yes |
| `// Given` / `// When` / `// Then` section comments | Skill guidance | Yes |

## Convention Overridden

| Convention | Source | Overridden By | Reason |
|---|---|---|---|
| `.filter().any()` existence checks | `tests/api/advisory.rs` | Skill Step 7 | Skill says "prefer value-based assertions"; existence checks hide regressions |
| `.filter().count() > 0` non-zero checks | `tests/api/sbom.rs` | Skill Step 7 | Skill says "assert on specific items or key fields so failures reveal *what* changed" |
