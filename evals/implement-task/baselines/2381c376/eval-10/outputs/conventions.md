# Convention Conformance Analysis for TC-9208

## Source Files Analyzed

**Production siblings**:
- `modules/fundamental/src/package/endpoints/list.rs` -- sibling endpoint in same module
- `modules/fundamental/src/sbom/endpoints/get.rs` -- GET single-resource pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` -- list endpoint pattern
- `modules/fundamental/src/package/model/summary.rs` -- sibling model struct

**Test siblings**:
- `tests/api/advisory.rs` -- integration test for advisory endpoints
- `tests/api/sbom.rs` -- integration test for SBOM endpoints
- `tests/api/search.rs` -- integration test for search endpoints

## Discovered Conventions

### Naming Conventions
- **Files**: lowercase with underscores (e.g., `license_summary.rs`, `package_license.rs`)
- **Structs**: PascalCase (e.g., `SbomSummary`, `AdvisoryDetails`, `PackageSummary`)
- **Functions**: snake_case verb_noun pattern (e.g., `get_sbom`, `list_packages`)
- **Test functions**: `test_<noun>_<scenario>` pattern
- **Modules**: lowercase with underscores, matching file names

### Error Handling
- All handlers return `Result<T, AppError>`
- Errors are wrapped with `.context()` for additional context
- `AppError` enum from `common/src/error.rs` implements `IntoResponse`
- 404 cases return `AppError` (not raw status codes)

### Module Structure
- Domain modules follow `model/ + service/ + endpoints/` structure
- Each sub-module has a `mod.rs` that re-exports public items
- Endpoint modules have a `mod.rs` for route registration

### Response Types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Single-resource endpoints return `Json<T>` directly
- Query helpers from `common/src/db/query.rs` for filtering/pagination/sorting

### Import Organization
- Standard library imports first
- External crate imports second
- Internal crate imports last
- Grouped by blank lines between sections

### Test Conventions (from sibling tests)

#### Structure and Setup
- Integration tests in `tests/api/` directory
- Tests hit a real PostgreSQL test database
- Shared test setup for database initialization and HTTP client creation
- Each test file corresponds to a domain module

#### Naming
- Test functions: `test_<noun>_<scenario>` (e.g., `test_advisory_list`, `test_sbom_get`)
- Descriptive assertion messages in `assert!` and `assert_eq!` macros

#### Status Code Validation
- `assert_eq!(resp.status(), StatusCode::OK)` for success cases
- `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404 cases

#### Assertion Patterns (CONFLICT IDENTIFIED -- see below)
- **Sibling pattern 1** (from `tests/api/advisory.rs`):
  ```rust
  let has_critical = result.items.iter()
      .filter(|a| a.severity == "Critical")
      .any(|_| true);
  assert!(has_critical, "should contain a Critical advisory");
  ```
- **Sibling pattern 2** (from `tests/api/sbom.rs`):
  ```rust
  let matching = result.items.iter()
      .filter(|s| s.name.contains("openssl"))
      .count();
  assert!(matching > 0, "should find at least one openssl SBOM");
  ```

Both patterns check only for existence/non-zero count without verifying specific values.

## Conflicts with Skill Quality Guidance

### CONFLICT: Assertion Style

**Sibling pattern**: `.filter().any()` and `.filter().count() > 0` -- existence-only
checks that verify something is present but not what specific values are returned.

**Skill guidance (Step 7)**: "Prefer value-based assertions over length-only checks:
When verifying collections or response data, assert on the actual values -- not just
the count. Assert on specific items or key fields so that test failures reveal *what*
changed, not just *how many*. Length checks alone hide regressions behind a passing
count and prevent subsequent assertions from running."

**Resolution**: The skill guidance takes precedence. The new tests will use value-based
assertions (e.g., `assert_eq!(summary.permissive.count, 3)`,
`assert_eq!(summary.permissive.licenses, vec!["MIT", "Apache-2.0", "BSD-3-Clause"])`)
instead of the sibling existence-check patterns. This ensures test failures reveal
exactly what changed rather than just whether something is present.

**What we adopt from siblings**: Test file structure, naming conventions
(`test_<noun>_<scenario>`), setup/teardown patterns, database initialization, HTTP
client usage, status code assertion style (`assert_eq!(resp.status(), StatusCode::OK)`),
and assertion message conventions. These are all non-conflicting aspects.

**What we do NOT adopt from siblings**: The `.filter().any()` and `.filter().count() > 0`
assertion patterns. These conflict with the skill's explicit quality standard for
value-based assertions.

### No Other Conflicts Detected

- Error handling convention (Result<T, AppError> with .context()) aligns with both
  siblings and task Implementation Notes.
- Module structure convention aligns with task Files to Create layout.
- Naming conventions are consistent across siblings and task description.
