# Reuse Analysis: TC-9203

This document details how each Reuse Candidate from the task description would be applied during implementation. The goal is to maximize reuse of existing code and avoid duplicating logic that already exists in the codebase.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL IN clause generation. Given a string like `"MIT,Apache-2.0"`, it splits by comma, trims whitespace, and generates a SQL `WHERE column IN (...)` clause using SeaORM query builder methods.

**How it would be applied:** In `modules/fundamental/src/package/service/mod.rs`, when the `license` filter parameter is `Some(value)`, we call `apply_filter` directly with the license column and the raw query parameter string. This handles both single-value (`"MIT"`) and multi-value (`"MIT,Apache-2.0"`) inputs automatically.

**Why reuse instead of writing new code:** The `apply_filter` function already implements exactly the parsing and SQL generation logic we need. Writing a new function to parse comma-separated values and build an IN clause would directly duplicate `apply_filter`'s functionality, violating DRY and constraint 5.4 (reuse existing utilities). By reusing `apply_filter`, we also benefit from any future bug fixes or performance improvements to the shared helper -- they apply in one place.

**Decision: REUSE directly.** No new parsing or filtering utility functions will be created.

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** The advisory list endpoint already implements a `severity` query parameter filter using the exact same structural pattern needed for the license filter. This includes:
- A `Query` struct with an optional filter field (`pub severity: Option<String>`)
- Handler logic that extracts the filter from query parameters and passes it to the service layer
- Service-layer integration that calls `apply_filter` with the filter value

**How it would be applied:** This file serves as the structural guide (template) for implementing the license filter in the package endpoint. Specifically:
- The `Query` struct in `modules/fundamental/src/package/endpoints/list.rs` will add an optional `license` field following the same pattern as the advisory's `severity` field
- The handler function will extract and propagate the license filter using the same pattern as the advisory handler
- The service method in `modules/fundamental/src/package/service/mod.rs` will accept and apply the filter using the same pattern as `AdvisoryService::list`

**Why follow this pattern:** The advisory filter is a proven, reviewed, production-tested implementation of the exact same feature shape (optional query parameter -> comma-separated parsing -> SQL IN clause filtering). Following the same pattern ensures consistency across the codebase and reduces reviewer cognitive load.

**Decision: FOLLOW as structural template.** The advisory list endpoint provides the blueprint; the package list endpoint mirrors its approach for the license filter.

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:** The `package_license` SeaORM entity maps the join table between packages and their declared licenses. It defines the table columns, relationships, and SeaORM model needed to query the package-license association.

**How it would be applied:** In `modules/fundamental/src/package/service/mod.rs`, when applying the license filter, we join through the `package_license` entity to connect packages to their license identifiers. Using the existing SeaORM entity means we can write a type-safe join query:

```rust
// Conceptual approach:
query = query
    .join(JoinType::InnerJoin, package_license::Relation::Package.def())
    .filter(package_license::Column::License.is_in(license_values));
```

**Why reuse instead of raw SQL:** The `package_license` entity already defines the table structure, column types, and relationships as SeaORM models. Writing raw SQL for the join would:
- Bypass SeaORM's type safety and query builder
- Create a maintenance burden if the table schema changes
- Be inconsistent with how other joins are expressed in the codebase

Using the existing entity also avoids creating a duplicate entity definition, which would violate DRY.

**Decision: REUSE directly.** Use the existing `package_license` entity for the JOIN query. No new entity or raw SQL will be written.

## Summary

| Reuse Candidate | Source | Decision | Rationale |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Reuse directly | Handles comma-separated parsing and SQL IN clause; no new utility needed |
| Advisory list filter pattern | `modules/fundamental/src/advisory/endpoints/list.rs` | Follow as structural template | Proven pattern for optional query parameter filtering |
| `package_license` entity | `entity/src/package_license.rs` | Reuse directly | Type-safe SeaORM entity for the join; no raw SQL or new entity needed |

All three Reuse Candidates are leveraged in the implementation. No new utility functions are created that duplicate existing functionality.
