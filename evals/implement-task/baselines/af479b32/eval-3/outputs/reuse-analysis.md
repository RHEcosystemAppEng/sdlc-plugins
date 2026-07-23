# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

## Overview

The task description identifies three Reuse Candidates. All three are directly applicable and would be reused in the implementation. No new filtering infrastructure needs to be written -- the existing patterns provide complete coverage for the license filter feature.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides**: A shared helper function that parses comma-separated multi-value query parameter strings and generates SQL `IN` clause conditions via SeaORM's query builder. It handles both single-value (equality) and multi-value (IN) cases transparently.

**How it would be reused**: Called directly in `PackageService::list()` to apply the license filter to the query. The license query parameter value (e.g., `"MIT"` or `"MIT,Apache-2.0"`) is passed as-is to `apply_filter` along with the `package_license::Column::License` column reference. The function handles:
- Splitting on commas to extract individual license identifiers
- Generating a `WHERE license IN ('MIT', 'Apache-2.0')` clause for multi-value input
- Generating a `WHERE license = 'MIT'` clause for single-value input
- Returning an error (mapped to 400 Bad Request) for invalid/empty values

**Reuse type**: Direct invocation -- no modification to `apply_filter` is needed. The function is generic over column types and filter values, so it works with the license column without changes.

**Location in code**: Called from `modules/fundamental/src/package/service/mod.rs` within the `list` method's query-building logic.

**Benefit**: Eliminates the need to write custom comma-parsing and SQL generation logic. Ensures consistent filter behavior across all endpoints (advisory severity, package license, and any future filters).

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides**: A structural pattern for adding an optional filter query parameter to a list endpoint. The advisory endpoint's severity filter demonstrates the complete pattern:
1. A query struct (e.g., `AdvisoryQuery`) with an `Option<String>` field for the filter
2. Axum `Query<T>` extraction in the handler
3. Passing the filter value as `Option<&str>` to the service layer
4. Conditional filter application in the service method (only when `Some`)

**How it would be reused**: The pattern is replicated structurally (not copied verbatim) in two files:

- **`modules/fundamental/src/package/endpoints/list.rs`**: Add a `license: Option<String>` field to the existing `PackageQuery` struct (mirroring how `AdvisoryQuery` has a `severity: Option<String>` field). Pass `query.license.as_deref()` to the service call (mirroring how the advisory handler passes `query.severity.as_deref()`).

- **`modules/fundamental/src/package/service/mod.rs`**: Add `license: Option<&str>` parameter to the `list` method signature (mirroring `AdvisoryService::list`'s severity parameter). Apply the filter conditionally with `if let Some(license_filter) = license { ... }` (mirroring the advisory service's severity filter application).

**Reuse type**: Structural pattern replication -- follow the same code organization and flow, adapted for the `license` domain. The advisory code serves as a template but is not imported or called.

**Benefit**: Ensures consistency across all list endpoints in the fundamental module. Developers familiar with the advisory severity filter will immediately recognize the license filter pattern. Reduces the risk of architectural divergence between similar features.

## Reuse Candidate 3: `entity/src/package_license.rs` (package-license join entity)

**What it provides**: A SeaORM entity definition for the `package_license` table, which maps packages to their declared licenses. Includes:
- `Entity` -- the table reference
- `Model` -- the row struct with fields (likely `package_id`, `license` or `license_id`)
- `Column` -- enum of column references (used for building filter conditions)
- `Relation` -- defined relationships to the `package` table (and possibly a `license` table)

**How it would be reused**: Used in the `PackageService::list()` method to perform a JOIN between the `package` table and the `package_license` table when a license filter is active:

```rust
// JOIN package_license table to filter by license
query = query.join(
    JoinType::InnerJoin,
    package_license::Relation::Package.def().rev(),
);
// Apply filter on the license column
query = apply_filter(query, package_license::Column::License, license_filter)?;
```

The entity's `Column::License` enum variant is passed to `apply_filter` to specify which column the filter condition targets. The entity's `Relation::Package` definition is used to construct the JOIN condition without writing raw SQL.

**Reuse type**: Direct usage of existing entity -- no modification to `package_license.rs` is needed. The entity already defines the table structure and relationships required for the filter JOIN.

**Benefit**: Avoids raw SQL for the JOIN query. Uses SeaORM's type-safe relation definitions, which are validated at compile time. If the `package_license` table schema changes in the future, the entity will be updated in one place and the filter will automatically use the updated definition.

## Additional Reuse Opportunities

Beyond the three candidates listed in the task description, the following existing code would also be reused:

| Code | Location | Usage |
|---|---|---|
| `PaginatedResults<T>` | `common/src/model/paginated.rs` | Return type for the list endpoint -- already in use, no changes needed |
| `AppError` | `common/src/error.rs` | Error type for handler return -- used for 400 Bad Request on invalid license values |
| Test helpers | `tests/api/` (shared setup code) | Database seeding and HTTP client setup patterns from sibling test files |

## Summary

| Candidate | Reuse Type | Modified? | Files Where Used |
|---|---|---|---|
| `apply_filter` | Direct invocation | No | `package/service/mod.rs` |
| Advisory severity filter pattern | Structural replication | N/A (pattern, not code) | `package/endpoints/list.rs`, `package/service/mod.rs` |
| `package_license` entity | Direct usage (JOIN + Column) | No | `package/service/mod.rs` |

All three reuse candidates eliminate the need for new infrastructure code. The implementation consists entirely of wiring existing components together following an established pattern, plus writing integration tests for the new behavior.
