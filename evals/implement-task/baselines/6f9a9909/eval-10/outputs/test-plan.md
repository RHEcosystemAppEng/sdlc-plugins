# Test Plan: TC-9208 -- Package License Summary Endpoint

## Assertion Approach

The test assertion strategy prioritizes **value-based assertions** over existence-only
checks, per the skill's quality guidance (SKILL.md Step 7). This overrides the sibling
test pattern found in `advisory.rs` and `sbom.rs` which uses `.any()` and `.count() > 0`
existence checks. See conventions.md for the full conflict analysis.

Each test asserts on **specific expected values** -- exact counts, exact license
identifier lists, and exact HTTP status codes -- so that failures reveal precisely
what changed rather than just indicating something is different.

## Test File

`tests/api/package_license.rs`

## Test Functions

### 1. `test_license_summary_valid_sbom`

**Requirement**: Test that a valid SBOM with known package licenses returns correct
categorized counts.

**Doc comment**: `/// Verifies that an SBOM with known package licenses returns correctly categorized counts and identifiers.`

**Setup (Given)**:
- Insert a test SBOM into the database
- Insert packages linked to the SBOM via `sbom_package`
- Insert package licenses via `package_license`:
  - Package A: "MIT" (permissive)
  - Package B: "GPL-3.0-only" (copyleft)
  - Package C: "Apache-2.0" (permissive)
  - Package D: "CustomLicense-1.0" (unknown)

**Action (When)**:
- Send GET request to `/api/v2/sbom/{id}/license-summary`

**Assertions (Then)**:
```rust
assert_eq!(resp.status(), StatusCode::OK);

let body: LicenseSummary = resp.json().await;

// Value-based assertions -- exact counts
assert_eq!(body.permissive.count, 2);
assert_eq!(body.copyleft.count, 1);
assert_eq!(body.unknown.count, 1);

// Value-based assertions -- exact license identifiers (sorted for determinism)
let mut permissive = body.permissive.licenses.clone();
permissive.sort();
assert_eq!(permissive, vec!["Apache-2.0", "MIT"]);

assert_eq!(body.copyleft.licenses, vec!["GPL-3.0-only"]);
assert_eq!(body.unknown.licenses, vec!["CustomLicense-1.0"]);
```

**Why not the sibling pattern**: The sibling `.any()` pattern would only check
"contains at least one permissive license" -- it would not catch regressions where
the classification logic misassigns a license or the count is wrong.

### 2. `test_license_summary_not_found`

**Requirement**: Test that a non-existent SBOM ID returns 404.

**Doc comment**: `/// Verifies that requesting a license summary for a non-existent SBOM returns 404.`

**Setup (Given)**:
- No specific setup -- use a UUID that does not exist in the database

**Action (When)**:
- Send GET request to `/api/v2/sbom/{non_existent_id}/license-summary`

**Assertions (Then)**:
```rust
assert_eq!(resp.status(), StatusCode::NOT_FOUND);
```

**Note**: This is a trivial test (single assertion, no distinct setup phase), so
given-when-then section comments are optional per skill guidance.

### 3. `test_license_summary_empty_sbom`

**Requirement**: Test that an SBOM with no packages returns all zeros with empty
license lists.

**Doc comment**: `/// Verifies that an SBOM with no associated packages returns zero counts and empty license lists.`

**Setup (Given)**:
- Insert a test SBOM into the database
- Do NOT insert any packages or package licenses for this SBOM

**Action (When)**:
- Send GET request to `/api/v2/sbom/{id}/license-summary`

**Assertions (Then)**:
```rust
assert_eq!(resp.status(), StatusCode::OK);

let body: LicenseSummary = resp.json().await;

// All counts should be zero
assert_eq!(body.permissive.count, 0);
assert_eq!(body.copyleft.count, 0);
assert_eq!(body.unknown.count, 0);

// All license lists should be empty
assert!(body.permissive.licenses.is_empty());
assert!(body.copyleft.licenses.is_empty());
assert!(body.unknown.licenses.is_empty());
```

**Why not the sibling pattern**: The sibling pattern would use
`.count() > 0` which does not apply here -- we need to assert exact zeros. Even so,
`assert_eq!` with the expected value `0` is more informative than `assert!(count == 0)`.

### 4. `test_license_summary_deduplication`

**Requirement**: Test that duplicate licenses within a category are counted only once.

**Doc comment**: `/// Verifies that duplicate license identifiers within the same category are deduplicated in both count and list.`

**Setup (Given)**:
- Insert a test SBOM into the database
- Insert multiple packages linked to the SBOM
- Insert package licenses with duplicates:
  - Package A: "MIT"
  - Package B: "MIT" (duplicate)
  - Package C: "Apache-2.0"
  - Package D: "MIT" (another duplicate)

**Action (When)**:
- Send GET request to `/api/v2/sbom/{id}/license-summary`

**Assertions (Then)**:
```rust
assert_eq!(resp.status(), StatusCode::OK);

let body: LicenseSummary = resp.json().await;

// MIT should be counted only once despite appearing 3 times
assert_eq!(body.permissive.count, 2); // MIT + Apache-2.0

let mut permissive = body.permissive.licenses.clone();
permissive.sort();
assert_eq!(permissive, vec!["Apache-2.0", "MIT"]);

// Verify count matches list length (internal consistency)
assert_eq!(body.permissive.count, body.permissive.licenses.len());
assert_eq!(body.copyleft.count, body.copyleft.licenses.len());
assert_eq!(body.unknown.count, body.unknown.licenses.len());
```

**Why not the sibling pattern**: The sibling `.any()` pattern would check "has MIT"
which would pass even if MIT appeared 3 times in the list (no deduplication). The
value-based assertion catches this by verifying the exact list contents.

## Parameterized Test Consideration

Per skill guidance, parameterized tests are preferred for repetitive cases sharing the
same algorithm. However, these four tests have meaningfully different setup phases
(different data insertion patterns) and different assertion structures (status code
only vs. full body validation). The Meszaros heuristic applies: since the test bodies
would require conditionals to handle the variations, individual test functions are
appropriate.

Additionally, the sibling test files (`advisory.rs`, `sbom.rs`) do not use
parameterized tests (no `rstest` usage observed), which further supports individual
test functions per the skill's guidance to not introduce parameterized tests if the
project does not already use them.

## Test Execution

```bash
cargo test -p trustify-tests   # or whatever crate owns tests/api/
```

If the project uses nextest:

```bash
cargo nextest run -p trustify-tests
```

The crate name would be resolved via `cargo metadata --no-deps --format-version 1`
from the workspace root, finding the package whose manifest contains the `tests/`
directory.
