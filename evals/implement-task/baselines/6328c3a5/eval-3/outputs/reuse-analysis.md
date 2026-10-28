# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

## Overview

The task description includes three Reuse Candidates. All three are used in the
implementation. No new filtering, parsing, or query-building logic is written -- the
implementation composes existing components following established patterns. This adheres
to constraint 5.4 (do not duplicate existing filtering logic).

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** Handles comma-separated multi-value query parameter parsing and SQL
IN clause generation. When given a string like `"MIT,Apache-2.0"`, it splits on commas
and generates a `WHERE column IN ('MIT', 'Apache-2.0')` clause.

**How it is reused:** Called directly in `modules/fundamental/src/package/service/mod.rs`
within the `list` method. When the `license` parameter is `Some`, `apply_filter` is
invoked with the `package_license::Column::License` column and the raw license string
from the query parameter. This handles both the single-value case (`license=MIT` produces
`WHERE license IN ('MIT')`) and multi-value case (`license=MIT,Apache-2.0` produces
`WHERE license IN ('MIT', 'Apache-2.0')`) without writing any custom parsing.

**Justification:** `apply_filter` already handles the exact parsing and SQL generation
pattern needed. Writing custom comma-splitting or IN clause logic would duplicate this
existing utility. The advisory endpoint's severity filter already uses `apply_filter` for
the same purpose, confirming it is the established pattern.

**Dependency check:** `common` is already a dependency of `modules/fundamental` (it
provides `PaginatedResults`, `AppError`, and query helpers), so no new dependency is
introduced.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** A complete structural pattern for adding an optional query parameter
filter to a list endpoint. The advisory list endpoint's severity filter demonstrates:
- How to add an optional field to the endpoint's Query struct
- How to extract the filter from the Axum query parameters
- How to pass the filter value from the endpoint handler to the service layer
- How to call `apply_filter` in the service method

**How it is reused:** The advisory endpoint's pattern is followed structurally (not
copied verbatim) in two files:

1. **`modules/fundamental/src/package/endpoints/list.rs`**: The package endpoint's Query
   struct gains a `license: Option<String>` field, mirroring the advisory endpoint's
   `severity: Option<String>` field. The handler extracts `query.license` and passes it
   to `PackageService::list()`, mirroring how the advisory handler extracts
   `query.severity` and passes it to `AdvisoryService::list()`.

2. **`modules/fundamental/src/package/service/mod.rs`**: The `PackageService::list()`
   method gains a `license: Option<String>` parameter and conditionally applies the filter,
   mirroring the `AdvisoryService::list()` method's handling of the severity parameter.

**Justification:** Using the advisory endpoint as a structural template ensures the
license filter follows the same conventions, error handling patterns, and code
organization. This makes the codebase consistent and reduces review friction. The task's
Implementation Notes explicitly state: "Follow the existing filter pattern in
`modules/fundamental/src/advisory/endpoints/list.rs`."

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:** The SeaORM entity definition for the `package_license` join table
that maps packages to their licenses. This entity includes:
- Column definitions (including the license SPDX identifier column)
- Relation definitions linking back to the `package` table
- SeaORM model and active model derivations

**How it is reused:** Used in `modules/fundamental/src/package/service/mod.rs` to
construct the JOIN query when the license filter is active. Instead of writing raw SQL
joins, the implementation uses the entity's relation definition:

```rust
query = query.join(JoinType::InnerJoin, package_license::Relation::Package.def().rev());
apply_filter(&mut query, package_license::Column::License, license);
```

This leverages SeaORM's type-safe relation system -- the join path is defined by the
entity's `Relation::Package` and the filter column is `package_license::Column::License`.

**Justification:** The `package_license` entity already defines the relationship between
packages and licenses. Using its SeaORM relations for the join ensures type safety,
avoids raw SQL string construction, and stays consistent with how other modules perform
joins in the codebase. Writing a raw SQL `JOIN package_license ON ...` would bypass the
ORM layer and diverge from project conventions.

---

## Additional Reuse (discovered, not listed in Reuse Candidates)

### `common/src/model/paginated.rs::PaginatedResults<T>`

The response wrapper `PaginatedResults<PackageSummary>` is already used by the package
list endpoint. No changes needed -- the filter narrows results but the response shape is
unchanged.

### `common/src/error.rs::AppError`

The existing `AppError` enum is reused for the 400 Bad Request response when an invalid
license value is provided. The handler returns `Err(AppError::BadRequest(...))` or
equivalent, following the established error handling pattern with `.context()`.

---

## Summary Table

| Reuse Candidate | Location | Reuse Type | New Code Written |
|----------------|----------|-----------|-----------------|
| `apply_filter` | `common/src/db/query.rs` | Direct call | None -- called as-is |
| Advisory severity filter pattern | `advisory/endpoints/list.rs` | Structural template | Query struct field + handler plumbing (following pattern) |
| `package_license` entity | `entity/src/package_license.rs` | Direct use (join + column) | None -- entity used as-is |
| `PaginatedResults<T>` | `common/src/model/paginated.rs` | Unchanged (no modification) | None |
| `AppError` | `common/src/error.rs` | Direct use | None -- existing error variant used |

No filtering logic is duplicated. All comma-separated parsing, SQL IN clause generation,
and join-table traversal use existing infrastructure.
