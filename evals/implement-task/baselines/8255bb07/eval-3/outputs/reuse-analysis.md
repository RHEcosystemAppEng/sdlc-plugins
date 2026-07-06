# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

## Overview

The task description includes three Reuse Candidates. All three are directly applicable and would be reused in the implementation. No new shared logic or utility functions need to be written -- the existing infrastructure covers the full requirements.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:**
The `apply_filter` function in the shared query builder module handles comma-separated multi-value query parameter parsing and SQL IN clause generation. Given a raw query parameter string like `"MIT,Apache-2.0"`, it splits the value on commas, trims whitespace, and produces the appropriate SQL filter condition (an IN clause when multiple values are present, or an equality check for a single value). It also handles error cases -- returning an `AppError` (which maps to 400 Bad Request) for malformed or invalid filter values.

**How it would be applied:**

The `license` query parameter must support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. Rather than writing custom parsing logic in the package service, the implementation calls `apply_filter` directly with the raw license string from the query parameter. This is done in `modules/fundamental/src/package/service/mod.rs` inside the `list` method:

```rust
use common::db::query::apply_filter;

// In PackageService::list(), after building the base query:
if let Some(license_filter) = license {
    query = apply_filter(query, package_license::Column::License, license_filter)?;
}
```

The function's existing signature and behavior match the license filter requirements exactly:
- Splits `"MIT,Apache-2.0"` into `["MIT", "Apache-2.0"]`
- Generates a `WHERE license IN ('MIT', 'Apache-2.0')` condition (or equivalent SeaORM filter)
- Handles the single-value case (`"MIT"`) without special-casing
- Returns appropriate errors for malformed input

**Reuse type:** Direct invocation -- no wrapper, extension, adapter, or modification needed. The existing shared code is called as-is.

**Why reuse instead of writing new code:**
- Avoids duplicating comma-separated parsing logic that is already implemented and tested
- Ensures consistent error handling (400 for invalid values) across all filter parameters in the API
- The function already handles edge cases (empty strings, whitespace trimming) that would need to be reimplemented if written from scratch
- Creating a new parsing or filtering utility would violate the project convention of centralizing query helpers in `common/src/db/query.rs`

---

## Reuse Candidate 2: Filter pattern from `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:**
The advisory list endpoint (`GET /api/v2/advisory`) implements a `severity` query parameter filter using a structural pattern. This is not a function to import but a design pattern to replicate. The pattern consists of:

1. A `Query` struct (or equivalent) with an optional filter field (e.g., `severity: Option<String>`)
2. Axum query parameter extraction that automatically deserializes the struct from the request URL
3. A handler function that passes the optional filter value to the service layer's list method using `.as_deref()` to convert `Option<String>` to `Option<&str>`
4. The service layer conditionally applying the filter only when the value is `Some`, leaving the query unchanged when `None`

**How it would be applied:**

The license filter is structurally identical to the severity filter. The implementation follows the same pattern in three places:

1. **Query struct modification** (`modules/fundamental/src/package/endpoints/list.rs`):
   Add `license: Option<String>` to the existing query parameter struct, mirroring how `severity: Option<String>` is declared in the advisory endpoint's Query struct. The field is optional so that omitting the parameter returns all packages (no regression).

   ```rust
   #[derive(Debug, Deserialize)]
   pub struct PackageQuery {
       // ... existing fields ...
       /// Optional license filter. Supports single SPDX identifier or comma-separated list.
       pub license: Option<String>,
   }
   ```

2. **Handler parameter passing** (`modules/fundamental/src/package/endpoints/list.rs`):
   Pass `query.license.as_deref()` to the `PackageService::list` method, following the same pattern the advisory handler uses to pass `query.severity.as_deref()` to `AdvisoryService::list`. The `.as_deref()` converts `Option<String>` to `Option<&str>`, matching the service method's expected parameter type.

3. **Service-layer conditional filtering** (`modules/fundamental/src/package/service/mod.rs`):
   When `license` is `Some`, join the package_license table and apply the filter using `apply_filter`. When `None`, skip the filter entirely. This matches the advisory service's conditional severity filter pattern where the filter is only added to the query when the parameter is present.

**Reuse type:** Structural pattern replication -- no code is copied or imported; the same architectural pattern is followed to ensure consistency.

**Why reuse instead of inventing a new pattern:**
- Maintains consistency across all list endpoints in the `modules/fundamental` module
- A reviewer familiar with the advisory endpoint will immediately recognize the same structure in the package endpoint
- Ensures the same Axum deserialization behavior for optional query parameters
- Avoids inventing a novel approach that diverges from established conventions in the codebase

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:**
The `package_license` entity is an existing SeaORM entity definition that maps the `package_license` database table (the join table between packages and their declared licenses). The entity includes:

- The SeaORM `Model` struct representing a row in the `package_license` table
- Column definitions (typed column accessors such as `package_license::Column::License` for the SPDX identifier and `package_license::Column::PackageId` for the foreign key)
- Relation definitions linking to the `package` entity (e.g., `package_license::Relation::Package`) that can be used in SeaORM `.join()` calls
- ActiveModel definitions for any create/update operations (not needed for this read-only filtering task)

**How it would be applied:**

The license filter requires joining the `package` table with the `package_license` table to find packages that have a matching license SPDX identifier. Instead of writing raw SQL (`JOIN package_license ON package.id = package_license.package_id`), the implementation uses the existing SeaORM entity and its defined relations:

1. **JOIN construction** (`modules/fundamental/src/package/service/mod.rs`):
   Use SeaORM's `JoinType::InnerJoin` with the relation definition from the package entity to join the package_license table. The entity's relation definitions provide the correct join columns automatically:

   ```rust
   use entity::package_license;

   query = query.join(
       JoinType::InnerJoin,
       package::Relation::PackageLicense.def(),
   );
   ```

2. **Filter column reference**:
   Reference `package_license::Column::License` as the target column for the `apply_filter` call. This ensures the filter operates on the correct table and column without hardcoding table or column names as strings.

3. **Type safety**:
   Using the SeaORM entity provides compile-time verification that the column names and types are correct. If the database schema changes (e.g., a column is renamed in a migration), the entity update will cause a compile error at the filter site, catching the issue immediately rather than at runtime.

**Reuse type:** Direct entity usage -- import the entity module and reference its columns and relations in the query builder. No modifications to the entity are needed.

**Why reuse instead of raw SQL:**
- The entity already defines the correct table name, column names, and foreign key relationships -- no risk of typos in SQL strings
- Using SeaORM relations ensures type-safe joins that the compiler can verify
- Consistent with how every other module in the codebase performs joins (no raw SQL for join operations anywhere in the project)
- If the `package_license` table schema changes, the entity will be updated centrally and all consumers (including this filter) will get compile-time errors pointing to the exact lines that need updating

---

## Summary

| Reuse Candidate | Source File | Reuse Type | Changes to Source | What It Eliminates |
|---|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct invocation | None | Custom comma-separated parsing, IN clause generation, input validation |
| Advisory severity filter pattern | `modules/fundamental/src/advisory/endpoints/list.rs` | Structural pattern replication | None | Need to design a new Query struct pattern or handler-to-service flow |
| `package_license` entity | `entity/src/package_license.rs` | Direct entity usage (import) | None | Raw SQL joins, hardcoded table/column names, runtime join errors |

No modifications to any shared or reused code are required. All reuse is additive -- importing and calling existing code from the new filter implementation. No new utility functions are created that would duplicate `apply_filter` functionality.
