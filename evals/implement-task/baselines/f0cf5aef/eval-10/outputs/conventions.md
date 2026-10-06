# Convention Conformance Analysis for TC-9208

Conventions discovered from sibling analysis of the trustify-backend repository,
organized by category. These serve as a binding reference during implementation.

## Production Code Conventions

### Module Structure
- **Pattern:** Each domain module follows `model/ + service/ + endpoints/` structure.
- **Source:** `sbom/`, `advisory/`, `package/` modules all follow this layout.
- **Applies to:** New files in `package/model/` and `package/endpoints/`.

### Endpoint Registration
- **Pattern:** Each module's `endpoints/mod.rs` declares sub-modules and registers routes;
  `server/main.rs` mounts all top-level modules.
- **Source:** `sbom/endpoints/mod.rs`, `advisory/endpoints/mod.rs`.
- **Applies to:** Adding the `license_summary` route in `package/endpoints/mod.rs`.

### Error Handling
- **Pattern:** All handlers return `Result<T, AppError>` with `.context()` wrapping for
  database and service errors. `AppError` is defined in `common/src/error.rs` and
  implements `IntoResponse`.
- **Source:** All endpoint handlers across `sbom`, `advisory`, `package` modules.
- **Applies to:** The new `license_summary` handler.

### Response Types
- **Pattern:** List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Single-resource endpoints return the model struct directly wrapped in `Json<T>`.
- **Source:** `sbom/endpoints/list.rs` (paginated), `sbom/endpoints/get.rs` (single).
- **Applies to:** The license summary is a single aggregated response (not paginated),
  so it should return `Json<LicenseSummary>` directly.

### Model Structs
- **Pattern:** Response structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`.
  Located in `model/` sub-directory with one struct per file.
- **Source:** `sbom/model/summary.rs`, `advisory/model/summary.rs`, `package/model/summary.rs`.
- **Applies to:** The new `LicenseSummary` and `LicenseCategory` structs.

### Naming Conventions
- **Pattern:** `verb_noun` for functions. `PascalCase` for types/structs. File names use
  `snake_case` matching the primary type or action they contain.
- **Source:** Consistent across all modules.
- **Applies to:** All new symbols.

### Import Organization
- **Pattern:** Standard library imports first, then external crates, then local crate imports.
  Grouped with blank lines between groups.
- **Source:** Observed across endpoint and model files.
- **Applies to:** All new files.

### Query Construction
- **Pattern:** SeaORM query builders with shared helpers from `common/src/db/query.rs`.
  JOIN queries use SeaORM's `JoinType::InnerJoin` or `JoinType::LeftJoin` with entity relations.
- **Source:** Service layer files across modules.
- **Applies to:** The license aggregation query joining `sbom_package` and `package_license`.

## Test Conventions

### Test File Location and Organization
- **Pattern:** Integration tests live in `tests/api/` with one file per domain area.
  File names correspond to the feature being tested (e.g., `sbom.rs`, `advisory.rs`).
- **Source:** `tests/api/sbom.rs`, `tests/api/advisory.rs`, `tests/api/search.rs`.
- **Applies to:** New file `tests/api/package_license.rs`. **ADOPTED.**

### Test Setup and Teardown
- **Pattern:** Tests hit a real PostgreSQL test database. Setup involves creating test
  data (SBOMs, packages, advisories) through the service layer or direct DB inserts.
  Each test function sets up its own data context.
- **Source:** `tests/api/sbom.rs`, `tests/api/advisory.rs`.
- **Applies to:** All four test functions. **ADOPTED.**

### Test Naming
- **Pattern:** Test function names use `test_<action>_<subject>` or
  `test_<subject>_<scenario>` format with `#[tokio::test]` attribute.
- **Source:** `tests/api/sbom.rs`, `tests/api/advisory.rs`.
- **Applies to:** All four test functions. **ADOPTED.**

### HTTP Response Status Assertion
- **Pattern:** `assert_eq!(resp.status(), StatusCode::OK)` for success cases;
  `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404 cases.
- **Source:** `tests/api/sbom.rs`, `tests/api/advisory.rs`.
- **Applies to:** All test functions. **ADOPTED** -- no conflict with skill guidance.

### Assertion Style on Collection Data

- **Sibling pattern:** Existence-only checks using `.filter().any()` and `.filter().count() > 0`.

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

- **Source:** `tests/api/advisory.rs`, `tests/api/sbom.rs`.

### **CONFLICT: Assertion Style**

The sibling `.filter().any()` and `.filter().count() > 0` patterns check only for
existence, not specific values. This conflicts with the implement-task skill's
Step 7 guidance:

> "Prefer value-based assertions over length-only checks: When verifying collections
> or response data, assert on the actual values -- not just the count. Assert on
> specific items or key fields so that test failures reveal *what* changed, not just
> *how many*. Length checks alone hide regressions behind a passing count and prevent
> subsequent assertions from running."

**Resolution: SKILL GUIDANCE TAKES PRECEDENCE over sibling patterns.** The new tests
will use value-based assertions (`assert_eq!` on specific license names, exact counts,
and specific list contents) rather than the `.any()` / `.count() > 0` patterns found
in siblings.

This override applies ONLY to assertion style. All other test conventions (file location,
setup/teardown, naming, HTTP status assertions, test organization) follow sibling patterns
as discovered above.

### Parameterized Tests
- **Sibling pattern:** The existing tests in `tests/api/` do not use parameterized test
  mechanisms (no `rstest` usage observed).
- **Skill guidance:** "If the sibling test analysis shows the project does not use
  parameterized tests, do not introduce them."
- **Resolution:** No parameterized tests will be introduced. Individual test functions
  will be written for each test case. **No conflict.**

### Test Documentation
- **Sibling pattern:** Sibling test functions in `tests/api/sbom.rs` and
  `tests/api/advisory.rs` do not have doc comments.
- **Skill guidance:** "Document every test function... This applies regardless of whether
  sibling tests have documentation; AI-generated tests introduce this as a new standard."
- **Resolution:** SKILL GUIDANCE TAKES PRECEDENCE. All new test functions will have
  `///` doc comments explaining what they verify. This is an additive improvement, not
  a conflict with existing code -- it does not modify sibling files.

## Summary of Convention Decisions

| Category | Source | Decision |
|---|---|---|
| Module structure | Sibling | ADOPT |
| Endpoint registration | Sibling | ADOPT |
| Error handling | Sibling | ADOPT |
| Response types | Sibling | ADOPT |
| Model struct derives | Sibling | ADOPT |
| Naming conventions | Sibling | ADOPT |
| Import organization | Sibling | ADOPT |
| Test file location | Sibling | ADOPT |
| Test setup/teardown | Sibling | ADOPT |
| Test naming | Sibling | ADOPT |
| HTTP status assertions | Sibling | ADOPT |
| Collection assertion style | **CONFLICT** | **OVERRIDE -- use skill guidance (value-based)** |
| Parameterized tests | Sibling (none used) | ADOPT (do not introduce) |
| Test documentation | Skill (additive) | ADOPT skill guidance |
