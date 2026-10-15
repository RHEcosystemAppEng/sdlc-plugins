# Conventions Discovered from Sibling Analysis

## Source of conventions

Sibling files analyzed:
- `modules/fundamental/src/sbom/endpoints/list.rs` and `get.rs` (endpoint patterns)
- `modules/fundamental/src/advisory/endpoints/list.rs` and `get.rs` (endpoint patterns)
- `modules/fundamental/src/sbom/model/summary.rs` and `details.rs` (model patterns)
- `modules/fundamental/src/package/model/summary.rs` (model pattern in the same module)
- `modules/fundamental/src/package/endpoints/list.rs` (endpoint pattern in the same module)
- `tests/api/sbom.rs` and `tests/api/advisory.rs` (test patterns)
- `common/src/error.rs` (error handling)
- `common/src/model/paginated.rs` (response wrapper)

## Production Code Conventions

### Naming conventions
- **Files:** lowercase_snake_case for all Rust source files
- **Modules:** each domain follows `model/ + service/ + endpoints/` directory structure
- **Structs:** PascalCase (e.g., `SbomSummary`, `AdvisoryDetails`, `PackageSummary`)
- **Functions:** snake_case, typically `verb_noun` pattern (e.g., `get_sbom`, `list_advisories`)
- **Endpoints:** registered in `endpoints/mod.rs`, each handler in its own file

### Error handling
- All handlers return `Result<T, AppError>` where `AppError` is from `common/src/error.rs`
- Error wrapping uses `.context()` pattern (from `anyhow` or similar)
- `AppError` implements `IntoResponse` for automatic HTTP error responses
- 404 errors for missing resources follow a consistent pattern across `get.rs` siblings

### Module structure
- Route registration happens in each module's `endpoints/mod.rs`
- Models are plain structs with `Serialize` and likely `ToSchema` derives
- Services encapsulate database access; endpoints call services
- New sub-modules are registered with `pub mod <name>;` in the parent `mod.rs`

### Response types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Single-item endpoints return the model struct directly (wrapped in `Json<T>`)
- The license summary endpoint is a single-item response (not paginated)

### Import organization
- External crates first, then internal crates (`common`, `entity`), then local modules
- SeaORM entities imported from the `entity` crate

### Database patterns
- SeaORM for all database operations
- JOIN queries use SeaORM's relation and query builder patterns
- Entity definitions in `entity/src/` with one file per entity

## Test Conventions

### Structure and setup
- Integration tests live in `tests/api/` directory
- Tests hit a real PostgreSQL test database
- Each test file corresponds to a domain (e.g., `sbom.rs`, `advisory.rs`)
- Status code assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)`

### Naming
- Test functions follow descriptive naming (e.g., test scenarios described in the function name)

### Assertion style (sibling pattern)
- Existing tests use existence-checking assertions:
  ```rust
  // From tests/api/advisory.rs:
  let has_critical = result.items.iter()
      .filter(|a| a.severity == "Critical")
      .any(|_| true);
  assert!(has_critical, "should contain a Critical advisory");

  // From tests/api/sbom.rs:
  let matching = result.items.iter()
      .filter(|s| s.name.contains("openssl"))
      .count();
  assert!(matching > 0, "should find at least one openssl SBOM");
  ```
- These patterns verify existence but do NOT verify specific values (counts, exact items, field values).

## Conflicts with Skill Built-in Quality Guidance

### CONFLICT 1: Assertion style -- value-based vs existence-only

**Sibling pattern:** Tests use `.any()` and `.count() > 0` checks that only verify something exists, without asserting on specific values or exact counts.

**Skill guidance (Step 7):** "Prefer value-based assertions over length-only checks: When verifying collections or response data, assert on the actual values -- not just the count. Assert on specific items or key fields so that test failures reveal *what* changed, not just *how many*."

**Resolution:** Follow the skill guidance. The new tests will use `assert_eq!` on specific counts and specific license identifiers rather than just checking existence. This deviates from the sibling pattern but produces higher-quality tests that reveal the nature of failures rather than just that something changed.

Example of what we will write (skill-guided) vs what siblings do:
```rust
// Sibling pattern (NOT adopted):
let has_permissive = summary.permissive.licenses.iter().any(|l| l == "MIT");
assert!(has_permissive, "should contain MIT");

// Skill-guided pattern (ADOPTED):
assert_eq!(summary.permissive.count, 2);
assert_eq!(summary.permissive.licenses, vec!["Apache-2.0", "MIT"]);
```

### CONFLICT 2: Test documentation

**Sibling pattern:** Existing tests in `tests/api/advisory.rs` and `tests/api/sbom.rs` do not appear to have doc comments on test functions (not mentioned in the task description's sibling patterns section).

**Skill guidance (Step 7):** "Document every test function: Add a documentation comment before every test function explaining what it verifies... This applies regardless of whether sibling tests have documentation; AI-generated tests introduce this as a new standard."

**Resolution:** Follow the skill guidance. All new test functions will have `///` doc comments explaining what they verify. This is explicitly stated as a standard that overrides sibling conventions for documentation.

### NO CONFLICT: Given-when-then structure

**Sibling pattern:** No given-when-then comments observed in sibling tests.

**Skill guidance (Step 7):** Add given-when-then section comments for non-trivial tests.

**Resolution:** Follow the skill guidance. New non-trivial tests will include `// Given`, `// When`, `// Then` section comments. This does not conflict with siblings since it is additive.

### NO CONFLICT: Parameterized tests

**Sibling pattern:** No parameterized test usage observed in sibling tests.

**Skill guidance (Step 7):** "If the sibling test analysis shows the project does not use parameterized tests, do not introduce them -- follow the project's existing test patterns instead."

**Resolution:** Follow sibling convention. Do NOT introduce `rstest` or other parameterized test frameworks. Write individual test functions for each case, since the project does not use parameterized tests.

## Conventions Adopted for Implementation

1. Return `Result<T, AppError>` with `.context()` error wrapping
2. Place endpoint handler in its own file under `endpoints/`
3. Register route in `endpoints/mod.rs`
4. Register model module in `model/mod.rs`
5. Use SeaORM for database queries with `package_license` entity
6. Place integration test in `tests/api/package_license.rs`
7. Use `assert_eq!` with specific values (skill override of sibling pattern)
8. Add `///` doc comments on all new test functions (skill override)
9. Add given-when-then comments in non-trivial tests (skill additive)
10. Do NOT use parameterized tests (sibling convention honored)
11. Use `assert_eq!(resp.status(), StatusCode::OK)` for status checks (sibling convention)
12. Add doc comments on all new public structs and functions (skill quality guidance)
13. Use defensive `.unwrap_or_default()` for external data access (skill quality guidance)
