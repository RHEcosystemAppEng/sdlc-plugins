# Conventions Discovered from Sibling Analysis -- TC-9208

## Production Code Conventions

### Module Structure
- Each domain module follows `model/ + service/ + endpoints/` directory structure.
- Models are in separate files under `model/` with a `mod.rs` re-exporting them.
- Endpoints are in separate files under `endpoints/` with a `mod.rs` handling route
  registration.
- Sibling modules analyzed: `sbom/`, `advisory/`, `package/` (existing files).

### Naming Conventions
- Structs use PascalCase with domain prefix: `SbomSummary`, `AdvisoryDetails`,
  `PackageSummary`.
- Handler functions use `verb_noun` pattern (e.g., list, get handlers).
- File names match the concept: `summary.rs`, `details.rs`, `list.rs`, `get.rs`.

### Error Handling
- All handlers return `Result<T, AppError>` where `AppError` is from `common/src/error.rs`.
- Fallible operations use `.context()` wrapping for error messages.
- Non-existent resources return appropriate HTTP status codes (404).

### Response Types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Single-resource endpoints return the model struct directly (wrapped in `Json<T>`).
- The license summary endpoint returns a single aggregate struct, not a paginated list.

### Import Organization
- External crates first (`serde`, `utoipa`, `axum`).
- Internal imports next (`common::`, `entity::`).
- Local module imports last.

### Derive Macros
- Model structs derive `Debug, Clone, Serialize, Deserialize, ToSchema`.
- `ToSchema` is for OpenAPI/utoipa integration.

### Framework
- Axum for HTTP routing and handlers.
- SeaORM for database queries and entity definitions.
- `tower-http` for middleware (caching).

## Test Code Conventions

### Test File Organization
- Integration tests live in `tests/api/` directory.
- One test file per domain or endpoint group: `sbom.rs`, `advisory.rs`, `search.rs`.
- Tests hit a real PostgreSQL test database.

### Test Naming
- Test function names are descriptive of the scenario being tested.

### Response Status Assertions
- Tests assert HTTP status codes using `assert_eq!(resp.status(), StatusCode::OK)`.

### Test Assertion Patterns (Sibling Analysis)

The following patterns were found in sibling test files:

**Pattern 1 -- `.filter().any()` (from `tests/api/advisory.rs`):**
```rust
let has_critical = result.items.iter()
    .filter(|a| a.severity == "Critical")
    .any(|_| true);
assert!(has_critical, "should contain a Critical advisory");
```

**Pattern 2 -- `.filter().count() > 0` (from `tests/api/sbom.rs`):**
```rust
let matching = result.items.iter()
    .filter(|s| s.name.contains("openssl"))
    .count();
assert!(matching > 0, "should find at least one openssl SBOM");
```

Both patterns check for the *existence* of items matching a predicate but do not
verify *specific values* (exact counts, exact field contents). A test using these
patterns will pass as long as at least one matching item exists, hiding regressions
where the wrong number of items is returned or field values change unexpectedly.

## Convention Conflicts with Skill Guidance

### CONFLICT: Assertion style -- existence checks vs. value-based assertions

**Sibling pattern:** Tests use `.filter().any()` and `.filter().count() > 0` to assert
that at least one matching item exists without verifying exact values or counts.

**Skill guidance (Step 7):** "Prefer value-based assertions over length-only checks.
When verifying collections or response data, assert on the actual values -- not just the
count. Assert on specific items or key fields so that test failures reveal *what* changed,
not just *how many*. Length checks alone hide regressions behind a passing count and
prevent subsequent assertions from running."

**Resolution:** Skill guidance takes precedence. The new tests for `package_license.rs`
will use value-based assertions (e.g., `assert_eq!(summary.permissive.count, 2)`,
`assert!(summary.permissive.licenses.contains(&"MIT".to_string()))`) rather than
adopting the `.filter().any()` or `.count() > 0` sibling patterns. This deviation is
intentional per the skill's explicit override rule: "Skill guidance overrides sibling
patterns."

## Conventions Adopted Without Conflict

The following sibling conventions are adopted as-is for the new tests:

- **Test file location:** `tests/api/package_license.rs` following `tests/api/<domain>.rs`.
- **Test database setup:** Use the same real PostgreSQL test database setup as siblings.
- **Status code assertions:** `assert_eq!(resp.status(), StatusCode::OK)` and
  `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- **Naming:** Descriptive test function names matching sibling style.
- **Error handling style:** Follow the same `Result<T, AppError>` and `.context()`
  patterns in production code.
- **Struct derives:** `Debug, Clone, Serialize, Deserialize, ToSchema`.
- **Module registration:** `pub mod license_summary;` in parent `mod.rs` files.

## Documentation Convention (Skill Override)

**Sibling pattern:** Existing sibling tests may not have doc comments on every test
function.

**Skill guidance (Step 7):** "Document every test function. Add a documentation comment
before every test function explaining what it verifies."

**Resolution:** Skill guidance takes precedence. All new test functions will have `///`
doc comments regardless of sibling test documentation practices.
