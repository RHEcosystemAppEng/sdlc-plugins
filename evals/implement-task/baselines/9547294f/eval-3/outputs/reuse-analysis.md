# Reuse Analysis for TC-9203: Add package license filter to list endpoint

## Overview

The task description includes a **Reuse Candidates** section listing three reusable code
artifacts. This analysis details how each candidate would be used during implementation,
along with any additional reuse opportunities discovered during code inspection (Step 4).

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source**: `common/src/db/query.rs`
**Symbol**: `apply_filter` function

### What it provides

The `apply_filter` function is a shared query builder utility that handles comma-separated
multi-value query parameter parsing and SQL IN clause generation. When given a column
reference and a string value:

- If the string contains no commas, it generates a `column = value` SQL clause (single-value match)
- If the string contains commas, it splits on commas, trims whitespace, and generates a `column IN (value1, value2, ...)` SQL clause (multi-value match)

### How it would be reused

This function is the core building block for the license filter. It would be called
directly in `PackageService::list()` (in `modules/fundamental/src/package/service/mod.rs`)
to apply the license filter to the database query:

```rust
use common::db::query::apply_filter;

// In the list() method, when license filter is provided:
if let Some(license) = &license_filter {
    query = query.filter(apply_filter(package_license::Column::License, license));
}
```

### Reuse type: Direct reuse (no modification needed)

The function already handles both single-value and comma-separated multi-value parameters,
which is exactly what the task requires. No extension or modification of the utility itself
is needed -- it is called as-is.

### Impact

- Eliminates the need to write custom comma-parsing logic
- Eliminates the need to manually build SQL IN clauses
- Ensures consistency with all other filter implementations in the codebase (advisory severity filter, etc.)
- Reduces implementation from ~15-20 lines of parsing/filtering code to a single function call

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**Source**: `modules/fundamental/src/advisory/endpoints/list.rs`
**Type**: Structural pattern reference (not direct code reuse)

### What it provides

The advisory list endpoint implements a `severity` query parameter filter that is
structurally identical to the license filter needed for this task. The pattern consists of:

1. A `Query` struct with `#[derive(Deserialize)]` containing an `Option<String>` field for the filter parameter
2. A handler function that extracts the query parameter and passes it to the service layer
3. Service-layer code that conditionally applies the filter using `apply_filter` when the parameter is `Some`

### How it would be reused

The advisory severity filter serves as the **template** for the package license filter
implementation. Each component of the advisory pattern maps directly to the package
implementation:

| Advisory (pattern source) | Package (new implementation) |
|---|---|
| `AdvisoryQuery.severity: Option<String>` | `PackageQuery.license: Option<String>` |
| Handler extracts `query.severity` | Handler extracts `query.license` |
| `AdvisoryService::list(severity_filter)` | `PackageService::list(license_filter)` |
| `apply_filter(advisory::Column::Severity, &severity)` | `apply_filter(package_license::Column::License, &license)` |

### Reuse type: Pattern reuse (structural template)

The advisory code is not imported or called directly. Instead, its structure is followed
as a template to ensure the package license filter is implemented consistently with
existing codebase conventions. The key difference is that the package filter requires a
JOIN through the `package_license` table (since licenses are in a separate join table),
whereas the advisory severity filter operates on a column directly on the advisory entity.

### Impact

- Ensures the new filter follows established conventions (convention conformance)
- Reduces design decisions to zero -- the pattern is already proven
- Makes the codebase more consistent and easier to maintain
- Reviewers can immediately recognize the pattern from the advisory endpoint

---

## Reuse Candidate 3: `entity/src/package_license.rs` (package-license join entity)

**Source**: `entity/src/package_license.rs`
**Type**: Existing SeaORM entity

### What it provides

The `package_license` entity is a SeaORM model that maps the `package_license` database
table. This table serves as a join table linking packages to their declared licenses.
The entity provides:

- Column definitions (e.g., `PackageId`, `License` or `LicenseId`)
- Relation definitions connecting to the `package` table
- SeaORM query builder integration for joins and filters

### How it would be reused

The entity is used in `PackageService::list()` to perform the JOIN that connects
packages to their licenses. Without this entity, we would need to write raw SQL
for the join, which would violate the project's convention of using SeaORM entities
for all database operations:

```rust
use entity::package_license;

// In the list() method:
let query = query
    .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev());
```

### Reuse type: Direct reuse (no modification needed)

The entity already exists and defines the relations needed for the join. No changes
to the entity file itself are required.

### Impact

- Eliminates the need to write raw SQL JOIN clauses
- Uses the existing relation definitions, ensuring referential correctness
- Follows the project's convention of using SeaORM entities for all database access
- If the table schema changes, the entity's migration will catch it at compile time

---

## Additional Reuse Discovered During Code Inspection

### `common/src/model/paginated.rs::PaginatedResults<T>`

**Discovery**: Found during Step 4 when inspecting the existing `PackageService::list()` return type.

**What it provides**: A generic pagination wrapper that includes `items: Vec<T>`, `total_count: i64`, and pagination metadata.

**How it is reused**: The response shape remains `PaginatedResults<PackageSummary>`. No changes are needed to this type -- it continues to wrap the filtered results. This confirms acceptance criterion #4 (response shape unchanged).

### `common/src/error.rs::AppError`

**Discovery**: Found during Step 4 convention conformance analysis.

**What it provides**: A shared error enum that implements Axum's `IntoResponse` trait. Includes variants for common HTTP errors (400, 404, 500) with context wrapping.

**How it is reused**: The handler function returns `Result<T, AppError>`, and validation failures on the `license` parameter would use `AppError` to return a 400 Bad Request. This follows the error handling convention used by all sibling endpoints.

---

## Summary

| Reuse Candidate | Source | Reuse Type | Modified? | Lines Saved (est.) |
|---|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct function call | No | ~15-20 |
| Advisory severity filter pattern | `advisory/endpoints/list.rs` | Structural template | N/A (pattern) | N/A |
| `package_license` entity | `entity/src/package_license.rs` | Direct entity import | No | ~10-15 |
| `PaginatedResults<T>` | `common/src/model/paginated.rs` | Existing return type | No | N/A |
| `AppError` | `common/src/error.rs` | Existing error type | No | N/A |

All three explicitly listed Reuse Candidates from the task description are utilized in the
implementation. Two additional reuse points were discovered during code inspection. No new
utility code needs to be written -- the implementation is composed entirely from existing
building blocks, with the only new code being the wiring logic in the endpoint handler and
service method, plus the integration tests.
