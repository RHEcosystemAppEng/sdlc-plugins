# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

## Overview

The task description identifies three Reuse Candidates. All three are directly applicable
and should be used as the foundation of the implementation rather than writing new logic.
This analysis details each candidate, how it would be reused, and why.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:**
- Parses comma-separated multi-value query parameter strings (e.g., `"MIT,Apache-2.0"`)
- Generates SQL `IN` clause conditions for the parsed values
- Handles both single-value and multi-value cases uniformly

**How it would be reused:**
- Import `apply_filter` into `modules/fundamental/src/package/service/mod.rs`
- Call `apply_filter` with the raw `license` query parameter string and the target column
  (the SPDX identifier column from the `package_license` entity)
- This completely eliminates the need to write custom comma-splitting logic or manual SQL
  `IN` clause construction
- The function already handles edge cases like trimming whitespace and single vs. multiple values

**Reuse type:** Direct invocation -- no modification to `apply_filter` needed. Call the
existing function with the license-specific column reference.

**Benefit:** Avoids duplicating the comma-separated parsing and SQL IN clause generation
that already exists in the shared query module. Ensures consistent behavior with all other
filters in the application that use the same helper.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:**
- A working example of the Query struct pattern with an optional filter field
- Shows how to declare the filter field in the query parameters struct
- Shows how to thread the filter value from the endpoint handler through to the service layer
- Demonstrates the complete wiring: query param extraction -> service call -> database filtering

**How it would be reused:**
- Use as a structural template for the changes to `modules/fundamental/src/package/endpoints/list.rs`
- Mirror the Query struct pattern: add an `Option<String>` field named `license` to the
  package endpoint's query parameters struct, following the same serde deserialization approach
  as the advisory endpoint's `severity` field
- Mirror the handler wiring: extract `query.license` and pass it to `PackageService::list()`
  in the same way the advisory handler passes `query.severity` to `AdvisoryService::list()`
- Mirror the validation approach: apply the same input validation pattern used for severity
  to the license parameter

**Reuse type:** Pattern replication -- the advisory endpoint's structure is followed as a
template. No code is copied verbatim; instead, the same architectural pattern is applied
to the package domain with license-specific names and types.

**Benefit:** Ensures the package license filter is structurally consistent with the existing
advisory severity filter, maintaining codebase uniformity. Reduces design decisions to zero --
every structural choice has a precedent in the advisory module.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:**
- The SeaORM entity definition for the package-license join table
- Defines columns (likely package_id, license identifier) and relations to the package entity
- Provides typed, ORM-level access to the package-license relationship

**How it would be reused:**
- Import the entity in `modules/fundamental/src/package/service/mod.rs`
- Use SeaORM's `JoinType::InnerJoin` (or `LeftJoin` as appropriate) with this entity to
  join the package table to the package_license table when the license filter is active
- Reference the entity's columns (e.g., `package_license::Column::License` or equivalent)
  when building the filter condition with `apply_filter`
- The entity provides compile-time type safety for column references, avoiding raw SQL
  string errors

**Reuse type:** Direct usage -- import the existing entity and use its Column and Relation
definitions in the query builder. No modification to the entity needed.

**Benefit:** Eliminates raw SQL for the JOIN operation. Leverages the existing SeaORM entity
that already maps the package-license relationship, ensuring type safety and consistency with
how other entity relationships are queried throughout the codebase.

---

## Additional Reuse Opportunities (discovered during analysis)

### `common/src/model/paginated.rs` -- PaginatedResults<T>

**Already in use** by the package list endpoint. The license filter does not change the
response shape -- `PaginatedResults<PackageSummary>` continues to be the return type. No
modification needed, but this is worth noting as a non-change: the filter is purely additive
to the query, and the pagination wrapper is reused unchanged.

### `common/src/error.rs` -- AppError

**Already in use** by all endpoint handlers. The license filter's error cases (invalid input
returning 400 Bad Request) would use the existing `AppError` enum and its `IntoResponse`
implementation. No new error variants are needed if `AppError` already has a variant for
bad request / validation errors (which is expected given that the advisory severity filter
handles similar validation).

---

## Summary

| Reuse Candidate | Reuse Type | Where Used | New Code Avoided |
|---|---|---|---|
| `apply_filter` (query.rs) | Direct invocation | PackageService::list() | Comma parsing + SQL IN clause generation |
| Advisory list.rs severity pattern | Pattern replication | Package endpoints/list.rs | Query struct design + handler wiring |
| `package_license.rs` entity | Direct usage | PackageService::list() | Raw SQL JOIN + column references |
| `PaginatedResults<T>` | Already in use | Package list handler | Response wrapper (no change needed) |
| `AppError` | Already in use | Package list handler | Error type for 400 responses |

All three task-identified reuse candidates are used. No new utility functions, helpers, or
shared modules need to be created. The implementation is composed almost entirely of
reusing existing patterns and invoking existing shared code.
