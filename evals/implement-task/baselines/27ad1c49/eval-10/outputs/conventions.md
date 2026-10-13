# Convention Conformance Analysis for TC-9208

## Production Code Conventions (from sibling analysis)

### Naming conventions
- **Files**: lowercase_snake_case (e.g., `list.rs`, `get.rs`, `summary.rs`, `details.rs`)
- **Types**: PascalCase structs (e.g., `SbomSummary`, `AdvisoryDetails`, `PackageSummary`)
- **Functions**: snake_case handlers matching HTTP verb + noun (e.g., `list_sboms`, `get_advisory`)

### Module structure
- Each domain module follows `model/ + service/ + endpoints/` structure
- Models in `model/` directory with `mod.rs` re-exporting submodules
- Endpoints in `endpoints/` directory with `mod.rs` registering routes

### Error handling
- All handlers return `Result<T, AppError>` with `.context()` wrapping
- `AppError` enum from `common/src/error.rs` implements `IntoResponse`

### Response types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Individual resource endpoints return the model struct directly

### Import organization
- Framework imports (axum) first, then crate imports, then local module imports

## Test Conventions (from sibling analysis)

### Test file organization
- Integration tests live in `tests/api/` directory
- One test file per domain area (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)
- Tests hit a real PostgreSQL test database

### Test naming
- Test functions use `test_` prefix with descriptive snake_case names
- Names describe the scenario being tested

### Setup/teardown
- Tests use shared test database setup (common test harness)
- Test data is inserted before assertions and cleaned up after

### Status code assertions
- `assert_eq!(resp.status(), StatusCode::OK)` pattern for HTTP status validation
- `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for error cases

### Assertion patterns (CONFLICT IDENTIFIED)

**Sibling patterns found in `tests/api/advisory.rs`:**
```rust
let has_critical = result.items.iter()
    .filter(|a| a.severity == "Critical")
    .any(|_| true);
assert!(has_critical, "should contain a Critical advisory");
```

**Sibling patterns found in `tests/api/sbom.rs`:**
```rust
let matching = result.items.iter()
    .filter(|s| s.name.contains("openssl"))
    .count();
assert!(matching > 0, "should find at least one openssl SBOM");
```

These patterns use `.filter().any()` and `.filter().count() > 0` to check for the
mere existence of items matching a predicate. They do not verify specific values,
exact counts, or the identity of matching items.

## Conflict: Sibling Assertion Patterns vs. Skill Quality Guidance

**Sibling pattern**: `.filter().any()` and `.filter().count() > 0` -- existence-only
checks that verify something matching a predicate exists, without asserting what
specifically was returned or how many.

**Skill guidance (Step 7)**: "Prefer value-based assertions over length-only checks:
When verifying collections or response data, assert on the actual values -- not just
the count. Assert on specific items or key fields so that test failures reveal *what*
changed, not just *how many*. Length checks alone hide regressions behind a passing
count and prevent subsequent assertions from running."

**Resolution**: The skill's built-in quality guidance takes precedence over sibling
patterns, as stated in both Step 4 ("Skill guidance takes precedence over sibling
patterns") and Step 7 ("Skill guidance overrides sibling patterns"). The existence-only
assertion style from `advisory.rs` and `sbom.rs` will NOT be adopted for the new
`package_license.rs` tests. Instead, value-based assertions (`assert_eq!` on specific
license identifiers, exact category counts, and exact list contents) will be used.

Non-conflicting sibling conventions (test naming, file organization, setup/teardown,
status code assertions, test database usage) will be followed as-is.
