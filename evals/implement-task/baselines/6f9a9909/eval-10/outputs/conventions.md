# Conventions Discovered from Sibling Analysis

## Source Files Analyzed

**Production siblings** (same module, similar role):
- `modules/fundamental/src/package/endpoints/list.rs` -- existing GET endpoint in the same package endpoints directory
- `modules/fundamental/src/sbom/endpoints/list.rs` -- GET list endpoint in a sibling domain module
- `modules/fundamental/src/sbom/endpoints/get.rs` -- GET-by-ID endpoint in a sibling domain module
- `modules/fundamental/src/package/model/summary.rs` -- existing model in the same package model directory
- `modules/fundamental/src/sbom/model/summary.rs` -- model in a sibling domain module

**Test siblings** (same test directory):
- `tests/api/advisory.rs` -- integration tests for advisory endpoints
- `tests/api/sbom.rs` -- integration tests for SBOM endpoints

## Discovered Conventions

### Naming Conventions
- **Endpoint handler functions**: named descriptively (e.g., handler function in `list.rs`, `get.rs`)
- **Model structs**: `<Entity>Summary`, `<Entity>Details` naming pattern
- **Test functions**: `test_<entity>_<behavior>` pattern
- **File naming**: lowercase snake_case, one file per concern (e.g., `list.rs`, `get.rs`, `summary.rs`)

### Error Handling
- All handlers return `Result<T, AppError>` with `.context()` wrapping on fallible operations
- `AppError` enum is defined in `common/src/error.rs` and implements `IntoResponse`

### Module Structure
- Each domain follows `model/ + service/ + endpoints/` sub-module pattern
- `endpoints/mod.rs` handles route registration
- `model/mod.rs` re-exports sub-modules via `pub mod`

### Response Types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Single-resource endpoints return the model struct directly (e.g., `Json<SbomDetails>`)

### Import Organization
- Framework imports (axum extractors, status codes) first
- Crate-internal imports next
- Model/entity imports last

### Test Patterns -- Structure
- Integration tests live in `tests/api/<entity>.rs`
- Tests hit a real PostgreSQL test database
- Tests use `assert_eq!(resp.status(), StatusCode::OK)` for status validation
- Each test function sets up its own test data

### Test Patterns -- Assertion Style (CONFLICT IDENTIFIED)

**Sibling pattern**: The existing tests in `advisory.rs` and `sbom.rs` use
existence-only assertions that check whether items matching a filter exist, without
verifying specific values:

```rust
// From advisory.rs:
let has_critical = result.items.iter()
    .filter(|a| a.severity == "Critical")
    .any(|_| true);
assert!(has_critical, "should contain a Critical advisory");

// From sbom.rs:
let matching = result.items.iter()
    .filter(|s| s.name.contains("openssl"))
    .count();
assert!(matching > 0, "should find at least one openssl SBOM");
```

These patterns verify existence but not exact values (counts, specific identifiers,
completeness of results).

**Skill guidance (Step 7)**: "Prefer value-based assertions over length-only checks:
When verifying collections or response data, assert on the actual values -- not just
the count. Assert on specific items or key fields so that test failures reveal *what*
changed, not just *how many*."

### Conflict Resolution

**The skill's built-in quality guidance takes precedence over sibling patterns.**
Per the SKILL.md Step 4 convention conformance analysis:

> "Skill guidance takes precedence over sibling patterns: When a sibling pattern
> conflicts with this skill's built-in quality guidance (e.g., Step 7's 'prefer
> value-based assertions' vs sibling `.any()` checks), follow the skill guidance.
> Record the conflict but do not adopt the sibling pattern."

**Decision**: The new tests in `package_license.rs` will:
- Follow sibling conventions for test file structure, setup, imports, naming,
  and database interaction
- **Override** the sibling assertion style: use `assert_eq!` with specific expected
  values (exact counts, exact license identifier lists) instead of `.any()`/`.count() > 0`
  existence checks
- Add doc comments on every test function (skill guidance, applies regardless of
  whether siblings have them)
- Add given-when-then section comments for non-trivial tests (skill guidance)

### Conventions Adopted Without Conflict

| Category | Convention | Source |
|----------|-----------|--------|
| Error handling | `Result<T, AppError>` with `.context()` | Sibling endpoints + task description |
| Module structure | `model/ + service/ + endpoints/` | Repo conventions |
| Route registration | `pub mod` in `endpoints/mod.rs` | Sibling `mod.rs` files |
| Model derives | `Serialize, Deserialize, Debug, Clone` | Sibling model structs |
| Test location | `tests/api/<entity>.rs` | Sibling test files |
| Test naming | `test_<entity>_<behavior>` | Sibling test files |
| Status assertion | `assert_eq!(resp.status(), StatusCode::OK)` | Repo key conventions |
| Framework | Axum extractors, SeaORM entities | Repo key conventions |
