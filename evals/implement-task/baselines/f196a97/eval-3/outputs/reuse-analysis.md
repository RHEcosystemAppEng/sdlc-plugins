# Reuse Analysis for TC-9203: Add package license filter to list endpoint

## Reuse Candidates from Task Description

All three Reuse Candidates identified in the task description are reused directly. No new utility functions or helpers need to be created.

---

### 1. `common/src/db/query.rs::apply_filter`

**What it provides:** Handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation.

**How it is reused:** Called directly in `PackageService::list()` (in `modules/fundamental/src/package/service/mod.rs`) to process the `license` query parameter value. When the endpoint receives `license=MIT,Apache-2.0`, the raw string is passed to `apply_filter`, which:
- Splits the comma-separated values into individual license identifiers
- Generates the appropriate SQL `WHERE ... IN (...)` clause
- Handles the single-value case (`license=MIT`) identically to the multi-value case

**Justification for direct reuse:** This function already implements the exact parsing and SQL generation logic needed. Writing a custom parser or SQL builder would duplicate this existing, tested utility. The license filter's comma-separated semantics are identical to the pattern `apply_filter` was designed for.

**Modifications to `apply_filter`:** None. The function is used as-is.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:** A complete, working example of adding an optional filter query parameter to a list endpoint. The advisory endpoint's `severity` filter demonstrates:
- How to define an optional field in the endpoint's query parameter struct
- How to extract and validate the parameter in the handler
- How to pass the filter value through to the service layer
- How to integrate with the `apply_filter` utility

**How it is reused:** Used as a structural template (not imported as code). The package list endpoint's query struct, handler logic, and service call are written to mirror the advisory list endpoint's severity filter implementation:

| Advisory (severity) pattern | Package (license) implementation |
|---|---|
| `severity: Option<String>` field in query struct | `license: Option<String>` field in query struct |
| Extract `query.severity` in handler | Extract `query.license` in handler |
| Pass to `AdvisoryService::list(severity_filter)` | Pass to `PackageService::list(license_filter)` |
| Call `apply_filter` in service with severity values | Call `apply_filter` in service with license values |

**Justification for pattern reuse:** The task description explicitly states the severity filter implementation is "structurally identical" to the license filter needed. Following this established pattern ensures consistency across endpoints, makes the codebase predictable for maintainers, and avoids introducing a novel filtering approach that would diverge from established conventions.

**Modifications to advisory code:** None. The advisory endpoint is read-only -- it serves as a reference pattern.

---

### 3. `entity/src/package_license.rs` (package-license join entity)

**What it provides:** The SeaORM entity definition for the `package_license` join table, which maps packages to their declared licenses. This entity defines the table schema, column types, and relations needed for SeaORM queries.

**How it is reused:** Used in the `PackageService::list()` method to construct the JOIN query when a license filter is active. Instead of writing raw SQL to join the `package` and `package_license` tables, the service uses SeaORM's relation-based join API with this existing entity:

```
// Conceptual usage (not exact code):
Package::find()
    .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
    .filter(package_license::Column::License.is_in(license_values))
```

**Justification for entity reuse:** The entity already defines the correct table name, column mappings, and relations. Using it through SeaORM's query builder (rather than raw SQL) ensures:
- Type safety for column references
- Automatic handling of table aliases and join conditions
- Consistency with how other parts of the codebase perform entity joins
- Protection against schema changes (if columns are renamed, the entity definition is the single source of truth)

**Modifications to entity:** None. The entity is used as-is.

---

## Additional Reuse (discovered, not listed in task)

### `common/src/error.rs::AppError`

**What it provides:** The shared error enum that implements `IntoResponse` for returning HTTP error responses.

**How it is reused:** Used to return `400 Bad Request` when the `license` query parameter contains invalid values (empty segments, malformed input). This follows the existing error handling convention where all handlers return `Result<T, AppError>` with `.context()` wrapping.

**Justification:** This is the established error handling mechanism across all endpoints in the codebase. Creating a custom error type would violate the convention.

### `common/src/model/paginated.rs::PaginatedResults<T>`

**What it provides:** The generic pagination wrapper used by all list endpoints.

**How it is reused:** The response type remains `PaginatedResults<PackageSummary>` -- unchanged. No new response type is created.

---

## What is NOT Created

The following are explicitly **not** created because existing code covers the functionality:

| Avoided duplication | Existing code used instead |
|---|---|
| Custom comma-separated value parser | `apply_filter` in `common/src/db/query.rs` |
| Custom SQL `IN` clause builder | `apply_filter` in `common/src/db/query.rs` |
| Raw SQL join for package-license | `package_license` SeaORM entity in `entity/src/package_license.rs` |
| New query parameter extraction pattern | Follows advisory endpoint's established pattern |
| Custom error response type | `AppError` from `common/src/error.rs` |
| New response wrapper type | `PaginatedResults<T>` from `common/src/model/paginated.rs` |
