# Discovered Conventions for TC-9208

## Production Code Conventions (from sibling analysis)

Siblings analyzed: `modules/fundamental/src/sbom/endpoints/list.rs`,
`modules/fundamental/src/advisory/endpoints/list.rs`,
`modules/fundamental/src/package/endpoints/list.rs`

- **Module structure:** Each domain module follows the `model/ + service/ + endpoints/`
  directory layout. New code in the `package` module must follow this same structure.
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
  for error messages. No raw `unwrap()` or `expect()` in handler code.
- **Naming:** Service methods follow the `verb_noun` pattern (e.g., `get_advisory`,
  `create_sbom`, `list_packages`). The new handler should use a name like
  `get_license_summary`.
- **Response types:** List endpoints return `PaginatedResults<T>` from
  `common/src/model/paginated.rs`. The license summary endpoint returns a custom struct
  rather than a paginated list, which is acceptable since it is an aggregation endpoint,
  not a list endpoint.
- **Route registration:** Each module's `endpoints/mod.rs` registers routes and
  `server/main.rs` mounts all modules. The new route must be registered in
  `modules/fundamental/src/package/endpoints/mod.rs`.
- **Framework:** Axum for HTTP handlers, SeaORM for database queries. Follow these
  throughout.

## Test Conventions (from sibling test analysis)

Siblings analyzed: `tests/api/advisory.rs`, `tests/api/sbom.rs`, `tests/api/search.rs`

- **Test naming:** Tests follow the `test_<endpoint>_<scenario>` pattern (e.g.,
  `test_list_advisories_filtered`, `test_get_sbom_not_found`). New tests should follow
  this: `test_license_summary_valid_sbom`, `test_license_summary_not_found`, etc.
- **Test setup:** Tests use a real PostgreSQL test database with test fixtures. Setup
  involves creating test SBOMs and packages via the ingestion pipeline or direct DB
  insertion. The new tests should follow the same setup pattern.
- **Test organization:** Tests are organized by endpoint in separate files under
  `tests/api/`. The new tests belong in `tests/api/package_license.rs`.
- **Status code assertions:** All endpoint tests use
  `assert_eq!(resp.status(), StatusCode::OK)` or `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
  for status validation. Follow this convention.
- **Response deserialization:** Tests deserialize response bodies into typed structs and
  then assert on the deserialized fields. Follow this convention.

### Assertion style patterns in siblings

The sibling test files use existence-based assertion patterns for validating collection
contents:

**Pattern from `tests/api/advisory.rs` -- `.filter().any()` pattern:**
```rust
let has_critical = result.items.iter()
    .filter(|a| a.severity == "Critical")
    .any(|_| true);
assert!(has_critical, "should contain a Critical advisory");
```

**Pattern from `tests/api/sbom.rs` -- `.filter().count() > 0` pattern:**
```rust
let matching = result.items.iter()
    .filter(|s| s.name.contains("openssl"))
    .count();
assert!(matching > 0, "should find at least one openssl SBOM");
```

These patterns check only for the *existence* of matching items. They do not verify
specific values, exact counts, or the complete set of expected items. A test using
`.any()` or `.count() > 0` will pass as long as at least one match exists, even if
the actual data has changed significantly -- regressions are hidden behind a passing
existence check.

## Conflict: Sibling Assertion Patterns vs Skill Quality Guidance

**Conflict identified:** The sibling `.filter().any()` and `.filter().count() > 0`
assertion patterns conflict with the skill's built-in quality guidance in Step 7:

> "Prefer value-based assertions over length-only checks: When verifying collections or
> response data, assert on the actual values -- not just the count. Assert on specific
> items or key fields so that test failures reveal *what* changed, not just *how many*.
> Length checks alone hide regressions behind a passing count and prevent subsequent
> assertions from running."

**Resolution:** The skill guidance takes precedence over the sibling patterns. Per the
skill's convention conformance analysis rules in Step 4:

> "Skill guidance takes precedence over sibling patterns: When a sibling pattern conflicts
> with this skill's built-in quality guidance (e.g., Step 7's 'prefer value-based
> assertions' vs sibling `.any()` checks), follow the skill guidance. Record the conflict
> in the convention output but do not adopt the sibling pattern. Sibling conventions are
> defaults when the skill has no opinion -- not overrides of explicit skill instructions."

Therefore:
- **OVERRIDE:** The `.filter().any()` and `.filter().count() > 0` assertion patterns will
  NOT be adopted. Tests will use value-based assertions (`assert_eq!` on specific license
  identifiers and exact counts per category) instead.
- **FOLLOW:** All non-conflicting sibling conventions (test naming with
  `test_<endpoint>_<scenario>`, test setup with real PostgreSQL, test organization in
  `tests/api/`, status code assertions with `assert_eq!(resp.status(), ...)`, response
  deserialization into typed structs) will be adopted as-is.
