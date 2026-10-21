# Reuse Analysis -- TC-9203: Add package license filter to list endpoint

This document analyzes the three Reuse Candidates identified in the task description
and describes how each is reused in the implementation.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source:** `common/src/db/query.rs`

**What it provides:** The `apply_filter` function handles comma-separated multi-value
query parameter parsing and SQL `IN` clause generation. It accepts a raw filter string
(e.g., `"MIT,Apache-2.0"`), splits it on commas, and generates the appropriate SeaORM
condition (a single `=` for one value, or `IN (...)` for multiple values).

**How it is reused:** `apply_filter` is called directly from `PackageService::list()`
in `modules/fundamental/src/package/service/mod.rs`. The license filter string received
from the endpoint layer is passed to `apply_filter` along with the target column
(the license column from the `package_license` entity). No wrapper, adapter, or
reimplementation is needed -- the function's existing interface matches the license
filter use case exactly.

**Why direct reuse is correct:** The `common` crate is already a dependency of the
`fundamental` module (it provides `PaginatedResults`, `AppError`, and other shared
types). There is no new dependency to introduce. Creating a new filtering utility would
violate constraint 5.4 (no duplication of existing utility functionality) and the DRY
principle. `apply_filter` is a shared utility designed for exactly this pattern.

**What is NOT done:** No new parsing function is written to split comma-separated values.
No new SQL generation helper is created. No duplicate of `apply_filter` is introduced
in the package module.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**Source:** `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** The advisory list endpoint implements a `severity` query parameter
filter using a Query struct pattern -- an Axum-deserialized struct with an
`Option<String>` field for the filter value. The handler extracts the field, passes it
to the service layer, and the service applies it using `apply_filter`. This is a
complete, working reference for the "optional filter on a list endpoint" pattern.

**How it is reused:** The pattern is followed structurally in the package list endpoint.
Specifically:

1. **Query struct pattern:** The package endpoint's Query struct in
   `modules/fundamental/src/package/endpoints/list.rs` gains an `Option<String>` field
   named `license`, mirroring how the advisory endpoint's Query struct has an
   `Option<String>` field for `severity`.

2. **Handler-to-service plumbing:** The package handler extracts `query.license` and
   passes it to `PackageService::list()`, following the same flow as the advisory handler
   extracting `query.severity` and passing it to `AdvisoryService::list()`.

3. **Error handling:** The same `Result<T, AppError>` return type with `.context()`
   wrapping is used, matching the advisory endpoint's error handling approach.

**Why pattern reuse is correct:** The severity filter and the license filter are
structurally identical -- both are optional string filters on a list endpoint that
support comma-separated multi-value input. Following the established pattern ensures
consistency across endpoints, reduces review friction (reviewers recognize the pattern),
and avoids inventing a different approach that would diverge from the codebase's
conventions.

---

## Reuse Candidate 3: `entity/src/package_license.rs` (package_license entity)

**Source:** `entity/src/package_license.rs`

**What it provides:** A SeaORM entity mapping for the `package_license` database table,
which is the join table linking packages to their declared licenses. The entity defines
the table's columns (including the license identifier column) and its relationships
to the package entity.

**How it is reused:** The `package_license` entity is used in
`modules/fundamental/src/package/service/mod.rs` to construct the JOIN query when
filtering packages by license. When `PackageService::list()` receives a `license` filter:

1. A SeaORM `JoinType::InnerJoin` (or `LeftJoin` depending on the query builder pattern)
   is added between the `package` table and the `package_license` table using the
   entity's relationship definition.

2. The `apply_filter` function targets the license column defined in the
   `package_license` entity, producing a `WHERE package_license.license IN (...)`
   condition.

3. When no license filter is provided (`None`), the join is omitted entirely, keeping
   the unfiltered query unchanged and avoiding unnecessary join overhead.

**Why entity reuse is correct:** The `package_license` entity already exists and
correctly maps the join table. Writing raw SQL (`JOIN package_license ON ...`) would
bypass SeaORM's type safety and relationship management. Using the existing entity
ensures:
- Type-safe column references (compile-time errors if the schema changes)
- Consistency with how other modules query related entities
- No duplication of table/column name strings

---

## Summary

All three Reuse Candidates are used in the implementation. No new utility functions
are created that duplicate `apply_filter` functionality. The implementation follows the
established severity filter pattern rather than inventing a new filtering approach.
The existing `package_license` entity is used for the database join rather than writing
raw SQL.

| Reuse Candidate | Reuse Type | Location Used |
|-----------------|-----------|---------------|
| `apply_filter` from `query.rs` | Direct function call | `package/service/mod.rs` |
| Severity filter pattern from `advisory/endpoints/list.rs` | Structural pattern | `package/endpoints/list.rs` |
| `package_license` entity | Entity import for JOIN | `package/service/mod.rs` |
