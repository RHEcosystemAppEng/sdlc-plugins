# Conventions Discovered from Sibling Analysis

## Source Files Analyzed

**Production siblings:**
- `modules/fundamental/src/package/endpoints/list.rs` -- existing package list endpoint
- `modules/fundamental/src/sbom/endpoints/list.rs` -- SBOM list endpoint (same module pattern)
- `modules/fundamental/src/advisory/endpoints/list.rs` -- advisory list endpoint (same module pattern)
- `modules/fundamental/src/package/model/summary.rs` -- existing PackageSummary struct
- `modules/fundamental/src/sbom/model/summary.rs` -- SbomSummary struct
- `modules/fundamental/src/advisory/model/summary.rs` -- AdvisorySummary struct

**Test siblings:**
- `tests/api/sbom.rs` -- SBOM endpoint integration tests
- `tests/api/advisory.rs` -- advisory endpoint integration tests

---

## Production Code Conventions

### Module Structure
- Each domain follows `model/ + service/ + endpoints/` structure.
- New submodules are declared in the parent `mod.rs` with `pub mod <name>;`.

### Naming
- Endpoint handler functions use `verb_noun` pattern (e.g., `get_license_summary`, `list_packages`).
- Model structs use PascalCase domain names (e.g., `SbomSummary`, `PackageSummary`, `LicenseSummary`).
- Files are named in `snake_case` matching the struct or concept they contain.

### Error Handling
- All handlers return `Result<T, AppError>`.
- Errors are wrapped with `.context("descriptive message")` using anyhow-style context.
- 404 errors are returned when an entity is not found by ID.

### Response Types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Single-resource endpoints return `Json<T>` directly.

### Import Organization
- External crates first, then internal crate imports, matching Rust convention.

### Derives and Traits
- Model structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`.
- OpenAPI schema support via `utoipa::ToSchema`.

---

## Test Conventions

### File and Test Naming
- Test files live in `tests/api/` and are named after the domain entity (e.g., `sbom.rs`, `advisory.rs`).
- Test functions use `test_<description>` naming pattern (e.g., `test_list_sboms`, `test_get_advisory_by_id`).

### Setup and Teardown
- Tests hit a real PostgreSQL test database.
- Test setup provisions test data (SBOMs, advisories, packages) before assertions.
- Common test utilities and database setup helpers are shared across test files.

### Response Status Validation
- Tests validate HTTP status codes with `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.

### Assertion Patterns (CONFLICT IDENTIFIED)

The sibling test files use existence-only assertion patterns:

**Pattern from `tests/api/advisory.rs`:**
```rust
let has_critical = result.items.iter()
    .filter(|a| a.severity == "Critical")
    .any(|_| true);
assert!(has_critical, "should contain a Critical advisory");
```

**Pattern from `tests/api/sbom.rs`:**
```rust
let matching = result.items.iter()
    .filter(|s| s.name.contains("openssl"))
    .count();
assert!(matching > 0, "should find at least one openssl SBOM");
```

These patterns check only for **existence** (`.any()` returns bool, `.count() > 0` returns bool) but do **not** verify specific values, exact counts, or the identity of matched items. A test using these patterns would pass even if the wrong licenses were returned, as long as at least one item matched the filter.

---

## Conflict with Skill Quality Guidance

**Conflict:** The sibling `.filter().any()` and `.filter().count() > 0` assertion patterns conflict with the implement-task skill's built-in quality guidance in Step 7:

> "Prefer value-based assertions over length-only checks: When verifying collections or
> response data, assert on the actual values -- not just the count. Assert on specific items
> or key fields so that test failures reveal *what* changed, not just *how many*. Length
> checks alone hide regressions behind a passing count and prevent subsequent assertions
> from running."

**Resolution:** Per the skill's explicit precedence rule -- "Skill guidance overrides sibling patterns" (Step 7) and "Skill guidance takes precedence over sibling patterns" (Step 4) -- the skill's value-based assertion guidance takes precedence over the sibling existence-check patterns. The new tests will use `assert_eq!` on specific license names, exact counts, and category membership rather than `.filter().any()` or `.filter().count() > 0`.

**What is adopted from siblings (non-conflicting aspects):**
- Test file location: `tests/api/` directory
- Test naming: `test_<description>` pattern
- Setup/teardown: real PostgreSQL test database with provisioned test data
- Status code validation: `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Descriptive assertion messages in `assert!` / `assert_eq!` macros

**What is NOT adopted from siblings (conflicting aspect):**
- `.filter().any()` existence-only checks -- replaced by `assert_eq!` on specific values
- `.filter().count() > 0` count-threshold checks -- replaced by `assert_eq!` on exact counts
