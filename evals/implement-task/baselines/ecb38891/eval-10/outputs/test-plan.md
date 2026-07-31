# Test Plan: TC-9208 — Package License Summary Tests

## Test File Location

`tests/api/package_license.rs` — following the sibling convention of placing integration
tests in `tests/api/<domain>.rs` (consistent with `tests/api/advisory.rs` and
`tests/api/sbom.rs`).

## Assertion Strategy

### Sibling Convention Override

The sibling tests in `tests/api/advisory.rs` and `tests/api/sbom.rs` use `.filter().any()`
and `.filter().count() > 0` existence-check patterns. These patterns verify that at least
one matching item exists but do not assert on specific values.

Per the implement-task skill's Step 7 guidance ("prefer value-based assertions over
length-only checks"), this test plan uses **value-based assertions** instead. This means:

- `assert_eq!` on specific license identifier strings (e.g., `"MIT"`, `"GPL-3.0"`)
- `assert_eq!` on exact counts per category (e.g., `permissive.count == 2`)
- Assertions that verify the complete expected set of licenses, not just that "some" exist

This approach ensures test failures reveal *what* changed rather than just *how many*,
catching regressions that existence checks would miss.

### Adopted Sibling Conventions (Non-Conflicting)

The following sibling conventions are adopted without modification:

- **Test naming**: `test_<scenario>` pattern (e.g., `test_license_summary_valid_sbom`)
- **Test database**: real PostgreSQL test database, not mocks
- **HTTP status assertions**: `assert_eq!(resp.status(), StatusCode::OK)` for status validation
- **Setup pattern**: ingest test fixture data, then query the API endpoint
- **Test organization**: all tests in a single file under `tests/api/`

## Test Functions

### 1. `test_license_summary_valid_sbom`

/// Verifies that a valid SBOM with known package licenses returns correctly categorized counts and license identifiers.

**Setup (Given):**
- Ingest a test SBOM containing packages with known licenses:
  - Package A: MIT (permissive)
  - Package B: Apache-2.0 (permissive)
  - Package C: GPL-3.0 (copyleft)
  - Package D: Unknown-License-X (unknown)

**Action (When):**
- `GET /api/v2/sbom/{id}/license-summary`

**Assertions (Then):**
```rust
assert_eq!(resp.status(), StatusCode::OK);

let summary: LicenseSummary = resp.json().await;

// Value-based assertions on permissive category
assert_eq!(summary.permissive.count, 2);
assert!(summary.permissive.licenses.contains(&"MIT".to_string()));
assert!(summary.permissive.licenses.contains(&"Apache-2.0".to_string()));

// Value-based assertions on copyleft category
assert_eq!(summary.copyleft.count, 1);
assert_eq!(summary.copyleft.licenses, vec!["GPL-3.0"]);

// Value-based assertions on unknown category
assert_eq!(summary.unknown.count, 1);
assert_eq!(summary.unknown.licenses, vec!["Unknown-License-X"]);
```

### 2. `test_license_summary_nonexistent_sbom`

/// Verifies that requesting a license summary for a non-existent SBOM ID returns 404.

**Setup (Given):**
- No specific setup; use a UUID that does not correspond to any ingested SBOM.

**Action (When):**
- `GET /api/v2/sbom/{nonexistent-id}/license-summary`

**Assertions (Then):**
```rust
assert_eq!(resp.status(), StatusCode::NOT_FOUND);
```

### 3. `test_license_summary_empty_sbom`

/// Verifies that an SBOM with no packages returns all zeros with empty license lists.

**Setup (Given):**
- Ingest a test SBOM that contains no packages (empty SBOM).

**Action (When):**
- `GET /api/v2/sbom/{id}/license-summary`

**Assertions (Then):**
```rust
assert_eq!(resp.status(), StatusCode::OK);

let summary: LicenseSummary = resp.json().await;

// Value-based assertions: all categories are zero with empty lists
assert_eq!(summary.permissive.count, 0);
assert_eq!(summary.permissive.licenses, Vec::<String>::new());
assert_eq!(summary.copyleft.count, 0);
assert_eq!(summary.copyleft.licenses, Vec::<String>::new());
assert_eq!(summary.unknown.count, 0);
assert_eq!(summary.unknown.licenses, Vec::<String>::new());
```

### 4. `test_license_summary_deduplication`

/// Verifies that duplicate licenses within a category are counted only once.

**Setup (Given):**
- Ingest a test SBOM containing multiple packages with the same license:
  - Package A: MIT (permissive)
  - Package B: MIT (permissive) -- duplicate
  - Package C: GPL-3.0 (copyleft)

**Action (When):**
- `GET /api/v2/sbom/{id}/license-summary`

**Assertions (Then):**
```rust
assert_eq!(resp.status(), StatusCode::OK);

let summary: LicenseSummary = resp.json().await;

// MIT should be counted only once despite appearing in two packages
assert_eq!(summary.permissive.count, 1);
assert_eq!(summary.permissive.licenses, vec!["MIT"]);

// GPL-3.0 counted normally
assert_eq!(summary.copyleft.count, 1);
assert_eq!(summary.copyleft.licenses, vec!["GPL-3.0"]);

// No unknown licenses
assert_eq!(summary.unknown.count, 0);
assert_eq!(summary.unknown.licenses, Vec::<String>::new());
```

## Documentation

Every test function includes a `///` doc comment (Rust convention) explaining what it
verifies, per the skill's test documentation guidance. Non-trivial tests include
`// Given`, `// When`, `// Then` section comments to make the structure navigable.
