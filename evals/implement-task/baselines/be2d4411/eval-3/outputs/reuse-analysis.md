# Reuse Analysis for TC-9203: Add package license filter to list endpoint

This document analyzes all three Reuse Candidates listed in the task description and details how each is used in the implementation.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** The `apply_filter` function is a shared query builder helper that handles comma-separated multi-value query parameter parsing and SQL IN clause generation. Given a raw query string value like `"MIT,Apache-2.0"`, it splits on commas, trims whitespace, and generates the appropriate SQL `WHERE column IN (...)` clause for the database query.

**How it is reused:** Called directly in `modules/fundamental/src/package/service/mod.rs` within the `PackageService::list` method. When the `license` query parameter is present, the raw string value is passed to `apply_filter` which handles:
- Parsing the comma-separated string into individual license identifiers
- Generating the SQL IN clause for filtering
- Handling the single-value case (one license) identically to the multi-value case

**What this avoids:** Without reusing `apply_filter`, the implementation would need to:
- Write custom string splitting logic (`license_str.split(',').map(|s| s.trim())...`)
- Manually construct SQL IN clauses or SeaORM filter conditions
- Handle edge cases (trailing commas, whitespace) that `apply_filter` already handles correctly

**Reuse type:** Direct function call -- no wrapping, extension, or modification needed. The function's existing API matches the license filter use case exactly.

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** The advisory list endpoint implements a `severity` query parameter filter using a specific structural pattern: an Axum `Query` struct with an optional filter field, extraction in the handler, and delegation to the service layer. This is the established pattern for adding optional filters to list endpoints in the codebase.

**How it is reused:** Used as a structural template (not a direct code call) for the license filter implementation in `modules/fundamental/src/package/endpoints/list.rs`. Specifically, the following patterns are replicated:

1. **Query struct pattern**: Add `pub license: Option<String>` to the package endpoint's `Query` struct, mirroring how the advisory endpoint has `pub severity: Option<String>` in its Query struct.
2. **Handler extraction pattern**: Extract `query.license` in the handler and pass it to the service method, following the same flow as `query.severity` in the advisory handler.
3. **Service delegation pattern**: The handler does not parse or validate the filter value itself -- it passes the raw `Option<String>` to the service layer, which is responsible for applying the filter using `apply_filter`. This separation of concerns matches the advisory endpoint's architecture.

**What this avoids:** Without following this structural template, the implementation might:
- Invent a different parameter extraction approach (e.g., custom middleware, manual URL parsing)
- Place filter logic in the wrong layer (e.g., parsing in the handler instead of the service)
- Use a different type for the query parameter (e.g., `Vec<String>` instead of `Option<String>` with comma-separated parsing downstream)

**Reuse type:** Structural pattern replication -- the advisory endpoint serves as a reference implementation that the package endpoint mirrors for consistency and convention adherence.

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:** The `package_license` entity is an existing SeaORM entity definition that maps the join table between packages and their licenses. It defines the `Model`, `Column`, `Relation`, and `ActiveModel` types for the `package_license` database table, including the foreign key relationships to both the `package` and `license` tables.

**How it is reused:** Used in `modules/fundamental/src/package/service/mod.rs` to construct the JOIN query when the license filter is active. Instead of writing raw SQL (`JOIN package_license ON ...`), the implementation uses SeaORM's relation-based JOIN API with the entity's predefined relations:

```rust
use entity::package_license;

// In the list method, when license filter is present:
query = query.join(
    JoinType::InnerJoin,
    package_license::Relation::Package.def().rev(),
);
```

The entity's `Relation` definitions encode the foreign key relationships, so the JOIN conditions are derived automatically by SeaORM. The `Column` enum from the entity is also used when applying the filter condition to specify which column to filter on (e.g., `package_license::Column::License`).

**What this avoids:** Without reusing this entity, the implementation would need to:
- Write raw SQL JOIN clauses with hardcoded table and column names
- Manually specify foreign key relationships that are already defined in the entity
- Risk inconsistency if the table schema changes (the entity definition is the single source of truth)

**Reuse type:** Direct entity usage via SeaORM's ORM API -- the entity's relations and columns are used programmatically for type-safe query construction.

## Summary

| # | Reuse Candidate | Reuse Type | Location Used |
|---|---|---|---|
| 1 | `common/src/db/query.rs::apply_filter` | Direct function call | `modules/fundamental/src/package/service/mod.rs` |
| 2 | `modules/fundamental/src/advisory/endpoints/list.rs` | Structural pattern template | `modules/fundamental/src/package/endpoints/list.rs` |
| 3 | `entity/src/package_license.rs` | Direct entity usage (SeaORM JOIN) | `modules/fundamental/src/package/service/mod.rs` |

All three Reuse Candidates are used. No new utility functions are created that would duplicate `apply_filter` functionality. The implementation follows the existing codebase conventions by reusing shared infrastructure rather than writing parallel implementations.
