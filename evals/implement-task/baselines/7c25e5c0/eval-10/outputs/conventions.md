# Convention Conformance Analysis — TC-9208

## Sibling Files Analyzed

### Production Code Siblings
- `modules/fundamental/src/package/endpoints/list.rs` — existing package list endpoint
- `modules/fundamental/src/advisory/endpoints/list.rs` — advisory list endpoint
- `modules/fundamental/src/advisory/endpoints/get.rs` — advisory get endpoint
- `modules/fundamental/src/sbom/endpoints/list.rs` — SBOM list endpoint

### Test Siblings
- `tests/api/advisory.rs` — advisory integration tests
- `tests/api/sbom.rs` — SBOM integration tests

## Discovered Conventions

### Naming Conventions
- Endpoint handler files named after the operation: `list.rs`, `get.rs`
- Model files named after the data shape: `summary.rs`, `details.rs`
- Test files named after the domain: `advisory.rs`, `sbom.rs`
- Functions follow `verb_noun` pattern

### Error Handling
- All handlers return `Result<T, AppError>` with `.context()` wrapping
- AppError enum defined in `common/src/error.rs`, implements `IntoResponse`

### Module Structure
- Each domain follows `model/ + service/ + endpoints/` structure
- `endpoints/mod.rs` handles route registration
- Models use `#[derive(Debug, Clone, Serialize, Deserialize, utoipa::ToSchema)]`

### Import Organization
- Framework imports (axum, serde) first
- Internal crate imports second
- Module-local imports last

### Test Patterns
- Integration tests live in `tests/api/` and hit a real PostgreSQL test database
- Status code assertions: `assert_eq!(resp.status(), StatusCode::OK)`
- Test naming: descriptive names matching the tested behavior
- Setup: tests create test fixtures using helper functions

### Test Assertion Patterns (from siblings)

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

These patterns use `.filter().any()` and `.filter().count() > 0` to check for existence of items matching a predicate. They verify that *some* matching item exists, but do not verify specific values, exact counts, or the complete set of expected results.

## Convention Conflict: Assertion Style

### Conflict Identified

The sibling test assertion patterns (`.filter().any()` and `.filter().count() > 0` existence checks) conflict with the implement-task skill's built-in quality guidance in Step 7:

> **Prefer value-based assertions over length-only checks:** When verifying collections or response data, assert on the actual values — not just the count. Assert on specific items or key fields so that test failures reveal *what* changed, not just *how many*. Length checks alone hide regressions behind a passing count and prevent subsequent assertions from running.

### Resolution

**The skill's built-in guidance takes precedence over sibling patterns.** Per the implement-task skill:

> **Skill guidance overrides sibling patterns:** The test conventions from Step 4 are defaults. The guidance below (value-based assertions, parameterized tests, test documentation) is the skill's explicit quality standard and takes precedence over conflicting sibling patterns. Note any deviation in the convention output.

Therefore:
- **Sibling conventions adopted** (non-conflicting): test file location (`tests/api/`), test naming, setup/teardown using real PostgreSQL, status code assertion pattern (`assert_eq!(resp.status(), StatusCode::OK)`), test organization
- **Sibling conventions overridden** (conflicting): assertion style — use value-based assertions (`assert_eq!` on specific license identifiers and exact counts) instead of `.filter().any()` or `.filter().count() > 0` existence checks

This deviation is intentional and required by the skill's explicit instructions. The sibling existence-check patterns are defaults, not overrides of explicit skill guidance.
