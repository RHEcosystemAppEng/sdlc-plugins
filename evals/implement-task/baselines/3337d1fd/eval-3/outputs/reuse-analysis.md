# Reuse Analysis for TC-9203: Add package license filter to list endpoint

## Reuse Candidates from Task Description

The task description provides three explicit reuse candidates. Each is analyzed below with details on how it would be used in the implementation.

---

### 1. `common/src/db/query.rs::apply_filter`

**Description from task**: Handles comma-separated multi-value query parameter parsing and SQL IN clause generation.

**How reused**: Directly invoked in `PackageService::list()` (in `modules/fundamental/src/package/service/mod.rs`) to process the `license` query parameter value.

**Reuse details**:

- When the `license` parameter is `Some("MIT")`, `apply_filter` produces a single-value equality condition (e.g., `WHERE license = 'MIT'`).
- When the `license` parameter is `Some("MIT,Apache-2.0")`, `apply_filter` splits on commas and generates a SQL `IN` clause (e.g., `WHERE license IN ('MIT', 'Apache-2.0')`).
- When the `license` parameter is `None`, `apply_filter` is not called -- the query runs without a license filter, returning all packages.
- This eliminates the need to write custom comma-parsing or SQL generation logic. The function already handles edge cases (trimming whitespace, deduplication, empty values) that would otherwise need to be manually implemented.
- The function likely also handles validation, returning an error for malformed input that can be mapped to a 400 Bad Request response via `AppError`.

**Modification needed**: None. `apply_filter` is used as-is -- no extension or modification required.

**Risk**: Low. This is a well-established utility already used by the advisory endpoint for the same purpose.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**Description from task**: The severity filter implementation is structurally identical to the license filter needed here; follow the same Query struct pattern with an optional field.

**How reused**: Used as a structural template (pattern reuse, not code-level import). The advisory list endpoint demonstrates the complete pattern for adding an optional filter parameter to a list endpoint.

**Reuse details**:

The advisory endpoint's severity filter establishes the following pattern to replicate:

1. **Query struct**: The advisory endpoint defines a `Query` struct (or equivalent Axum extractor) with an `Option<String>` field for `severity`. The package endpoint's Query struct should add a `license: Option<String>` field following the same structure.

2. **Handler function**: The advisory handler extracts `query.severity` and passes it as a parameter to `AdvisoryService::list()`. The package handler should extract `query.license` and pass it to `PackageService::list()` in the same way.

3. **Service integration**: The advisory service's `list` method accepts the optional severity filter and conditionally applies it to the database query. The package service should follow the same conditional application pattern.

4. **Error handling**: The advisory handler wraps errors with `.context()` and returns `Result<T, AppError>`. The package handler should use the same error handling approach.

**Modification needed**: None to the advisory endpoint itself. The pattern is replicated in the package endpoint files, adapting field names from `severity` to `license` and adjusting the entity join (advisory uses its own entity; package uses `package_license`).

**Risk**: Low. This is pattern reuse from a stable, working sibling implementation. The structural similarity means the implementation is well-understood and proven.

---

### 3. `entity/src/package_license.rs`

**Description from task**: Existing entity for the package-license join table; use for the JOIN query rather than writing raw SQL.

**How reused**: Used in `PackageService::list()` (in `modules/fundamental/src/package/service/mod.rs`) to build the SeaORM JOIN query that connects packages to their licenses.

**Reuse details**:

- The `package_license` entity is a SeaORM model that maps the join table between `package` and license records. It provides:
  - A `Column` enum with fields like `PackageId` and `License` (or `LicenseId`) for building filter conditions
  - `Relation` definitions that enable SeaORM's type-safe JOIN builder
  - The `Entity` type for referencing the table in queries

- In the service layer, when the license filter is active, the query builder uses this entity to add an `INNER JOIN` from the package table through the `package_license` table:

  ```rust
  // Conceptual usage:
  use entity::package_license;
  
  query.join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
       .filter(apply_filter(package_license::Column::License, &license_value)?);
  ```

- This approach is consistent with how SeaORM joins are used elsewhere in the codebase (e.g., `sbom_package`, `sbom_advisory` join entities).

**Modification needed**: None. The entity is used as-is -- its existing column definitions and relations provide everything needed for the JOIN.

**Risk**: Low. The entity already exists and is presumably tested through other code paths that use the package-license relationship.

---

## Additional Reuse Opportunities Discovered

Beyond the three explicit reuse candidates listed in the task, the following existing code would also be reused:

### 4. `common/src/model/paginated.rs::PaginatedResults<T>`

**How reused**: The response type for the package list endpoint remains `PaginatedResults<PackageSummary>`. No modification needed -- the filter only affects which packages are included in the paginated results, not the pagination structure itself.

### 5. `common/src/error.rs::AppError`

**How reused**: Used to return 400 Bad Request when invalid license values are provided. The `AppError` enum already includes variants for bad request responses (or a generic variant that maps to 400). The implementation uses this existing error type rather than creating custom error handling.

### 6. Sibling test patterns from `tests/api/advisory.rs` and `tests/api/sbom.rs`

**How reused**: Test structure, assertion patterns, database seeding approach, and response deserialization patterns are replicated from existing integration tests. This ensures the new test file `tests/api/package_license_filter.rs` is consistent with the test suite conventions.

---

## Summary

| Reuse Candidate | Reuse Type | Modified? | Used In |
|---|---|---|---|
| `common/src/db/query.rs::apply_filter` | Direct function call | No | `package/service/mod.rs` |
| `advisory/endpoints/list.rs` (severity filter) | Structural pattern template | No | `package/endpoints/list.rs` |
| `entity/src/package_license.rs` | SeaORM entity for JOIN | No | `package/service/mod.rs` |
| `common/src/model/paginated.rs` | Return type (unchanged) | No | `package/endpoints/list.rs` |
| `common/src/error.rs::AppError` | Error type for 400 responses | No | `package/endpoints/list.rs` |
| Sibling test files | Test convention template | No | `tests/api/package_license_filter.rs` |

All three task-specified reuse candidates are used directly without modification. No new utility code needs to be written -- the existing shared infrastructure (`apply_filter`, `AppError`, `PaginatedResults`) and the advisory endpoint's proven filter pattern provide everything needed to implement the license filter cleanly.
