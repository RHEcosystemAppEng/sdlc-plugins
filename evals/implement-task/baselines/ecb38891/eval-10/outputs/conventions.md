# Convention Conformance Analysis

## Sibling Analysis Scope

Analyzed sibling files in the same module structure and test directory to identify
established conventions for the trustify-backend project.

### Production Code Siblings

Examined:
- `modules/fundamental/src/package/endpoints/list.rs` (sibling endpoint handler)
- `modules/fundamental/src/advisory/endpoints/list.rs` (parallel module endpoint)
- `modules/fundamental/src/advisory/model/summary.rs` (parallel module model)
- `modules/fundamental/src/sbom/endpoints/list.rs` (parallel module endpoint)

### Test Code Siblings

Examined:
- `tests/api/advisory.rs` (advisory endpoint integration tests)
- `tests/api/sbom.rs` (SBOM endpoint integration tests)

---

## Discovered Conventions

### 1. Module Structure

- Each domain module follows the `model/ + service/ + endpoints/` directory pattern.
- New modules register sub-modules via `pub mod <name>;` in the parent `mod.rs`.
- Endpoint handlers live in individual files under `endpoints/`.

### 2. Error Handling

- All endpoint handlers return `Result<T, AppError>`.
- Error wrapping uses `.context("descriptive message")` from `anyhow`.
- 404 responses are produced by returning `AppError::NotFound` or equivalent.

### 3. Naming Conventions

- Files: `snake_case.rs` (e.g., `license_summary.rs`).
- Structs: `PascalCase` (e.g., `LicenseSummary`, `AdvisorySummary`).
- Functions: `verb_noun` pattern (e.g., `list_advisories`, `get_sbom`).
- Test functions: `test_<what_is_being_tested>` pattern (e.g., `test_list_advisories`).

### 4. Response Types

- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Single-item endpoints return the model struct directly.
- All response structs derive `Serialize, Deserialize`.

### 5. Import Organization

- Standard library imports first, then external crates, then internal crate modules.
- SeaORM entity imports grouped together.

### 6. Endpoint Registration

- Routes are registered in each module's `endpoints/mod.rs`.
- The `server/main.rs` mounts all module routers.

### 7. Query Patterns

- Shared filtering/pagination via `common/src/db/query.rs`.
- Entity queries use SeaORM query builder patterns.
- JOINs reference entity relationship definitions.

### 8. Test Conventions (Non-Conflicting)

- **Test location**: Integration tests live in `tests/api/<module>.rs`.
- **Test database**: Tests use a real PostgreSQL test database (not mocks).
- **Status assertions**: `assert_eq!(resp.status(), StatusCode::OK)` for HTTP status validation.
- **Test naming**: `test_<scenario>` pattern (e.g., `test_list_advisories`, `test_get_sbom_by_id`).
- **Setup/teardown**: Tests set up test data by ingesting fixtures, then query the API and validate responses.
- **Test organization**: One test file per module/domain area in `tests/api/`.

---

## Conflict: Assertion Style

### Sibling Pattern (from tests/api/advisory.rs and tests/api/sbom.rs)

The existing integration tests use `.filter().any()` and `.filter().count() > 0` patterns
for validating list response contents:

```rust
// Pattern from tests/api/advisory.rs:
let has_critical = result.items.iter()
    .filter(|a| a.severity == "Critical")
    .any(|_| true);
assert!(has_critical, "should contain a Critical advisory");

// Pattern from tests/api/sbom.rs:
let matching = result.items.iter()
    .filter(|s| s.name.contains("openssl"))
    .count();
assert!(matching > 0, "should find at least one openssl SBOM");
```

These patterns verify existence only -- they confirm that at least one matching item
exists but do not assert on specific values, exact counts, or the full set of expected
results. A regression that changes values or drops items would go undetected as long as
at least one match remains.

### Skill Built-in Guidance (Step 7)

The implement-task skill explicitly states:

> "Prefer value-based assertions over length-only checks: When verifying collections or
> response data, assert on the actual values -- not just the count. Assert on specific items
> or key fields so that test failures reveal *what* changed, not just *how many*. Length
> checks alone hide regressions behind a passing count and prevent subsequent assertions
> from running."

### Resolution

**The skill guidance takes precedence over the sibling patterns.** Sibling conventions
serve as defaults for structure, naming, setup, and organization -- but they do not
override explicit quality guidance built into the skill. The skill's Step 7 contains an
unambiguous directive to prefer value-based assertions, which directly conflicts with
the `.filter().any()` and `.filter().count() > 0` existence-check patterns found in
sibling tests.

**Action:** New tests for `package_license.rs` will:
- Follow sibling conventions for all non-conflicting aspects (test naming with `test_` prefix,
  test location in `tests/api/`, PostgreSQL test database setup, status code assertions,
  test file organization).
- Override the sibling assertion style: use `assert_eq!` on specific license identifiers,
  exact counts per category, and concrete expected values rather than `.any()` or
  `.count() > 0` existence checks.
