# Convention Conformance Analysis: TC-9208

## Sibling Files Analyzed

**Production siblings:**
- `modules/fundamental/src/package/endpoints/list.rs` -- existing package list endpoint
- `modules/fundamental/src/sbom/endpoints/list.rs` -- SBOM list endpoint (parallel module)
- `modules/fundamental/src/advisory/endpoints/list.rs` -- advisory list endpoint (parallel module)
- `modules/fundamental/src/package/model/summary.rs` -- existing PackageSummary model
- `modules/fundamental/src/sbom/model/summary.rs` -- SbomSummary model (parallel module)

**Test siblings:**
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests
- `tests/api/search.rs` -- search endpoint integration tests

## Discovered Conventions

### Naming Conventions
- **Files:** lowercase_snake_case for all Rust source files (e.g., `summary.rs`, `list.rs`)
- **Structs:** PascalCase (e.g., `SbomSummary`, `AdvisoryDetails`, `PackageSummary`)
- **Functions:** snake_case with verb_noun pattern (e.g., `get_sbom`, `list_advisories`)
- **Test functions:** `test_` prefix with descriptive snake_case (e.g., `test_sbom_list`, `test_advisory_search`)
- **Modules:** snake_case, declared with `pub mod <name>;` in parent `mod.rs`

**Status:** No conflict. Will follow for all new symbols.

### Error Handling
- All endpoint handlers return `Result<T, AppError>`.
- Database and service errors wrapped with `.context("descriptive message")`.
- 404 cases return `AppError::NotFound` (or similar variant).

**Status:** No conflict. Will follow exactly.

### Module Structure
- Domain modules follow `model/ + service/ + endpoints/` structure.
- `endpoints/mod.rs` contains route registration; individual endpoint files contain handlers.
- `model/mod.rs` re-exports sub-modules with `pub mod <name>;`.

**Status:** No conflict. New files placed according to this structure.

### Response Types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Individual resource endpoints return the model struct directly wrapped in `Json<T>`.

**Status:** No conflict. The license summary endpoint returns `Json<LicenseSummary>` (not paginated, since it is an aggregate, not a list).

### Import Organization
- External crate imports first, then internal crate imports, then local module imports.
- Grouped by blank lines between sections.

**Status:** No conflict. Will follow.

### Test Setup and Organization
- Integration tests live in `tests/api/` directory, one file per domain area.
- Tests use a shared test database setup (likely a test harness that provisions a PostgreSQL database).
- Test functions are `#[tokio::test]` async functions.
- Test data is inserted via service calls or direct entity insertion before assertions.

**Status:** No conflict. Will follow for test file placement, setup, and async test annotation.

### Test Naming
- Test function names use `test_` prefix with descriptive snake_case.
- Names describe the scenario being tested.

**Status:** No conflict. Will follow.

## Conflict: Test Assertion Style

### Sibling Pattern (NOT adopted)

The sibling test files `tests/api/advisory.rs` and `tests/api/sbom.rs` use existence-check
assertion patterns:

```rust
// advisory.rs pattern:
let has_critical = result.items.iter()
    .filter(|a| a.severity == "Critical")
    .any(|_| true);
assert!(has_critical, "should contain a Critical advisory");

// sbom.rs pattern:
let matching = result.items.iter()
    .filter(|s| s.name.contains("openssl"))
    .count();
assert!(matching > 0, "should find at least one openssl SBOM");
```

These patterns verify existence (`.any()`) or non-zero counts (`.count() > 0`) but do
not assert on specific expected values. When a regression changes *which* items are
returned or *how many*, these assertions still pass as long as at least one match exists.

### Skill Guidance (ADOPTED)

The implement-task skill (Step 7) explicitly states:

> "Prefer value-based assertions over length-only checks: When verifying collections or
> response data, assert on the actual values -- not just the count. Assert on specific
> items or key fields so that test failures reveal *what* changed, not just *how many*.
> Length checks alone hide regressions behind a passing count and prevent subsequent
> assertions from running."

And further:

> "Skill guidance takes precedence over sibling patterns: When a sibling pattern
> conflicts with this skill's built-in quality guidance (e.g., Step 7's 'prefer
> value-based assertions' vs sibling `.any()` checks), follow the skill guidance.
> Record the conflict but do not adopt the sibling pattern."

### Resolution

**Skill guidance wins.** The new tests in `tests/api/package_license.rs` will use
`assert_eq!` on specific expected values (exact counts, exact license identifier lists)
rather than `.filter().any()` or `.filter().count() > 0` patterns. This means:

- Assert `assert_eq!(response.permissive.count, 2)` instead of `assert!(response.permissive.count > 0)`
- Assert `assert_eq!(response.permissive.licenses, vec!["Apache-2.0", "MIT"])` instead of
  `response.permissive.licenses.iter().any(|l| l == "MIT")`
- Assert `assert_eq!(response.status(), StatusCode::NOT_FOUND)` for error cases (this
  pattern is already value-based and consistent with siblings)

All non-conflicting sibling conventions (naming, setup, organization, error handling,
module structure) are adopted as-is.

## Test Documentation Convention

The skill requires doc comments on every test function regardless of sibling practice.
Sibling tests may not have doc comments. This is explicitly stated as a new standard
that overrides sibling patterns for documentation specifically. All new test functions
will include `///` doc comments.

## Given-When-Then Structure

For non-trivial tests (those with distinct setup, action, and assertion phases), the
skill requires `// Given`, `// When`, `// Then` section comments inside the test body.
This will be applied to all four test functions in `package_license.rs` since each has
distinct setup (insert test data), action (call the endpoint), and assertion phases.
