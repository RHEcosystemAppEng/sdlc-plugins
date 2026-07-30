# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, enabling
consumers to filter packages by their declared license SPDX identifier. Support both
single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`)
filtering.

## Repository

trustify-backend (Rust backend service, Axum + SeaORM)

## Target Branch

main

## Branch

`TC-9203` (created from `main`)

## Project Configuration Validation

The mock CLAUDE.md contains all required sections:
- Repository Registry with `trustify-backend` entry and Serena instance `serena_backend`
- Jira Configuration with project key TC, Cloud ID, and custom field IDs
- Code Intelligence section with `serena_backend` for rust-analyzer

## Step 4 -- Code Understanding

### Files to Inspect

1. **`modules/fundamental/src/advisory/endpoints/list.rs`** -- the severity filter
   implementation that serves as the structural template. Inspect the `Query` struct to
   see how the optional `severity` field is declared, how it is extracted from query
   parameters, and how it is passed to the service layer.

2. **`common/src/db/query.rs`** -- inspect the `apply_filter` function to understand its
   signature, how it parses comma-separated values, and how it generates the SQL `IN`
   clause. This function will be called directly for the license filter.

3. **`entity/src/package_license.rs`** -- inspect the SeaORM entity definition for the
   package-license join table. Understand the column definitions (`package_id`,
   `license_id` or `license` text field) and available relations.

4. **`modules/fundamental/src/package/endpoints/list.rs`** -- the current package list
   endpoint. Inspect the existing `Query` struct and handler to understand where to add
   the new `license` field.

5. **`modules/fundamental/src/package/service/mod.rs`** -- the PackageService list method.
   Understand its current query construction to determine where to inject the license
   filter JOIN and WHERE clause.

6. **`modules/fundamental/src/package/model/summary.rs`** -- confirm the PackageSummary
   struct includes a `license` field (noted in repo structure).

### Sibling/Convention Analysis

- **Error handling convention**: all handlers use `Result<T, AppError>` with `.context()`.
- **Naming**: service methods follow `verb_noun` pattern.
- **Response type**: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- **Query struct pattern**: advisory's `list.rs` uses a `Query` struct with `#[serde(default)]`
  optional fields for each filter parameter.
- **Filter application**: advisory service uses `apply_filter` from `common/src/db/query.rs` to
  process multi-value filter parameters.

### Test Convention Analysis

- **Assertion style**: endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` followed
  by body deserialization.
- **Response validation**: list endpoint tests validate `total_count`, `items.len()`, and at
  least one item's key fields.
- **Error cases**: endpoint tests include status code checks for error responses.
- **Test naming**: `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).

### Documentation Files Identified

- `docs/api.md` -- may need updating if it documents the package list endpoint query parameters.
- `CONVENTIONS.md` -- check for CI check commands and code generation commands.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state**: Contains a `Query` struct for the package list endpoint and a handler
function that extracts query parameters, calls `PackageService::list()`, and returns
`PaginatedResults<PackageSummary>`.

**Changes**:

1. **Add `license` field to the `Query` struct**:
   ```rust
   /// Optional license SPDX identifier filter. Supports comma-separated values.
   #[serde(default)]
   pub license: Option<String>,
   ```
   This follows the exact pattern used by the `severity` field in the advisory endpoint's
   `Query` struct.

2. **Pass the license parameter to the service layer**: In the handler function, extract
   `query.license` and pass it to `PackageService::list()` as an additional parameter (or
   as part of a filter struct, matching how the advisory endpoint passes `severity`).

3. **Add validation**: If the license value contains invalid characters or is empty after
   splitting on commas, return a `400 Bad Request` using `AppError`. Follow the validation
   pattern from the advisory endpoint if one exists.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state**: Contains `PackageService` with a `list()` method that constructs a
SeaORM query, applies pagination/sorting via `common/src/db/query.rs` helpers, and
returns `PaginatedResults<PackageSummary>`.

**Changes**:

1. **Add `license` parameter to the `list()` method signature**: Add an
   `Option<String>` parameter (or add it to an existing filter/options struct if one is used).

2. **Apply the license filter using `apply_filter`**: When `license` is `Some`, use the
   `apply_filter` function from `common/src/db/query.rs` to parse the comma-separated
   values and generate a SQL `IN` clause. This reuses the existing utility directly rather
   than writing custom parsing logic.

3. **Join through `package_license` entity**: Use the `package_license` SeaORM entity from
   `entity/src/package_license.rs` to join the `package` table to the `package_license`
   table. Apply the license filter on the joined table's license column. This uses the
   existing entity definition rather than raw SQL.

   ```rust
   // Pseudocode for the join + filter:
   if let Some(license_filter) = license {
       let license_values = apply_filter(&license_filter); // parses "MIT,Apache-2.0" -> vec!["MIT", "Apache-2.0"]
       query = query
           .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
           .filter(package_license::Column::License.is_in(license_values));
   }
   ```

4. **Ensure DISTINCT results**: When the join is applied, packages with multiple license
   entries could appear multiple times. Add `.distinct()` to the query when the license
   filter is active, or use a subquery/EXISTS pattern if that is how the advisory endpoint
   handles it.

---

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests for the license filter on the `GET /api/v2/package` endpoint.

**Test cases**:

1. **`test_list_packages_filter_single_license`**: Seed the test database with packages
   having different licenses (MIT, Apache-2.0, GPL-3.0). Call
   `GET /api/v2/package?license=MIT`. Assert that only MIT-licensed packages are returned.
   Verify specific package names/identifiers in the response, not just count.

2. **`test_list_packages_filter_multi_license`**: Seed packages with MIT, Apache-2.0,
   GPL-3.0 licenses. Call `GET /api/v2/package?license=MIT,Apache-2.0`. Assert that
   packages with MIT or Apache-2.0 licenses are returned, and GPL-3.0 packages are excluded.
   Verify by checking specific items.

3. **`test_list_packages_no_license_filter`**: Seed packages with various licenses. Call
   `GET /api/v2/package` without the license parameter. Assert that all packages are
   returned (no regression). Verify count matches total seeded packages.

4. **`test_list_packages_invalid_license_returns_400`**: Call
   `GET /api/v2/package?license=` with an empty or invalid license value. Assert
   `StatusCode::BAD_REQUEST` (400) response.

**Structure**:
- Each test function includes a `///` doc comment explaining what it verifies.
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments.
- Follows the `test_<endpoint>_<scenario>` naming convention.
- Uses `assert_eq!` on specific field values (license identifiers, package names), not
  just `items.len()`.

### 2. `tests/api/mod.rs` (modify, if module registration is needed)

If the test directory uses a `mod.rs` to register test modules, add
`mod package_license_filter;` to ensure the new test file is compiled. Check existing
test files (`sbom.rs`, `advisory.rs`, `search.rs`) to see if they are registered in
a `mod.rs` or discovered automatically by the test harness.

---

## API Changes

### `GET /api/v2/package`

- **New query parameter**: `license` (optional, string)
- **Single value**: `?license=MIT` -- returns packages where the declared license matches `MIT`
- **Multi-value**: `?license=MIT,Apache-2.0` -- returns packages matching any of the listed
  licenses (OR semantics)
- **No value**: omitting the parameter returns all packages (existing behavior, no regression)
- **Invalid value**: empty string or malformed values return `400 Bad Request`
- **Response shape**: `PaginatedResults<PackageSummary>` remains unchanged -- only the input
  accepts the new optional parameter

---

## Data-Flow Trace

```
GET /api/v2/package?license=MIT
  -> endpoints/list.rs: extract Query { license: Some("MIT"), ... }
    -> validate license parameter (non-empty, valid chars) -> 400 if invalid
    -> PackageService::list(license: Some("MIT"), ...)
      -> apply_filter("MIT") -> vec!["MIT"]
      -> SELECT ... FROM package INNER JOIN package_license ON ... WHERE license IN ("MIT")
      -> apply pagination/sorting
    -> return PaginatedResults<PackageSummary>
  -> 200 OK with JSON body
```

**Status**: COMPLETE -- all stages connected (input -> validation -> query construction -> persistence query -> response).

---

## Self-Verification Checklist

- [ ] `git diff --name-only` matches Files to Modify + Files to Create
- [ ] No out-of-scope files modified
- [ ] Sensitive-pattern check passes (no secrets in diff)
- [ ] New test file registered in test module if needed
- [ ] Response shape unchanged (PaginatedResults<PackageSummary>)
- [ ] `cargo test` passes for all new and existing tests
- [ ] CI checks from CONVENTIONS.md pass (if any)
- [ ] Documentation updated if `docs/api.md` documents package endpoint parameters
