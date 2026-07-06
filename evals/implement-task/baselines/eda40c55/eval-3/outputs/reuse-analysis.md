# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document details the reuse candidates identified in the task description and how each would be used during implementation.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source:** `common/src/db/query.rs`
**Symbol:** `apply_filter` function
**Listed in task as:** "handles comma-separated multi-value query parameter parsing and SQL IN clause generation; reuse directly for the license filter"

### How It Would Be Reused

The `apply_filter` function is the core reuse item for this task. It would be called directly from `PackageService::list` in `modules/fundamental/src/package/service/mod.rs` to handle the license filtering logic.

**Specific usage:**
1. When the `license` query parameter is present (e.g., `"MIT,Apache-2.0"`), pass the raw string value to `apply_filter`.
2. `apply_filter` parses the comma-separated values into individual tokens (`["MIT", "Apache-2.0"]`).
3. `apply_filter` generates the appropriate SQL `IN` clause (e.g., `WHERE package_license.license IN ('MIT', 'Apache-2.0')`).
4. This eliminates the need to write custom parsing or SQL generation code -- the exact same logic that powers the advisory severity filter is reused here.

**Reuse type:** Direct invocation -- no modification to `apply_filter` is needed. The function is generic enough to handle any comma-separated query parameter value.

**Benefit:** Avoids duplicating comma-separated parsing logic and SQL IN clause generation. Ensures consistent behavior with other filters in the codebase (e.g., if `apply_filter` trims whitespace or handles edge cases, the license filter inherits that behavior automatically).

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Source:** `modules/fundamental/src/advisory/endpoints/list.rs`
**Symbol:** The severity filter implementation (Query struct pattern and handler logic)
**Listed in task as:** "the severity filter implementation is structurally identical to the license filter needed here; follow the same Query struct pattern with an optional field"

### How It Would Be Reused

This is a structural pattern reference, not a direct function call. The advisory list endpoint's severity filter serves as the template for how to implement the license filter in the package list endpoint.

**Specific patterns to replicate:**

1. **Query struct extension:** The advisory list endpoint defines a Query struct (or similar Axum extractor struct) with an `Option<String>` field for `severity`. The package list endpoint's Query struct in `modules/fundamental/src/package/endpoints/list.rs` would be extended with the same pattern:
   ```rust
   #[derive(Deserialize)]
   pub struct Query {
       // ... existing fields (pagination, sorting, etc.)
       /// Optional license filter. Supports comma-separated SPDX identifiers.
       pub license: Option<String>,
   }
   ```

2. **Handler parameter extraction:** The advisory handler extracts `query.severity` and passes it to `AdvisoryService::list()`. The package handler would extract `query.license` and pass it to `PackageService::list()` in the same way.

3. **Service layer integration:** The advisory service's `list` method accepts the optional severity parameter and conditionally applies the filter using `apply_filter`. The package service's `list` method would follow the same conditional-filter pattern.

4. **Input validation pattern:** If the advisory handler validates the severity parameter (e.g., checking for empty strings), the same validation approach would be applied to the license parameter.

**Reuse type:** Structural pattern -- the advisory implementation is read and its architecture is replicated for the license filter. No code is copy-pasted; instead, the same architectural decisions (struct shape, parameter flow, conditional filtering) are applied consistently.

**Benefit:** Ensures the new license filter is architecturally consistent with existing filters in the codebase. Reduces the risk of introducing a different filtering pattern that would be harder to maintain. Any developer familiar with the advisory severity filter will immediately understand the license filter.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Source:** `entity/src/package_license.rs`
**Symbol:** The `package_license` SeaORM entity (join table mapping packages to licenses)
**Listed in task as:** "existing entity for the package-license join table; use for the JOIN query rather than writing raw SQL"

### How It Would Be Reused

The `package_license` entity provides the database mapping needed to associate packages with their licenses. It would be used in the `PackageService::list` method to perform the JOIN operation.

**Specific usage:**

1. **JOIN construction:** When the license filter is active, the query in `PackageService::list` needs to join the `package` table with the `package_license` table. Instead of writing raw SQL (`JOIN package_license ON ...`), use SeaORM's relation-based join:
   ```rust
   // Join through the package_license entity
   query = query.join(
       JoinType::InnerJoin,
       entity::package_license::Relation::Package.def().rev(),
   );
   ```

2. **Column reference for filtering:** After joining, the filter condition references the license column from the `package_license` entity:
   ```rust
   // Filter on the license column
   entity::package_license::Column::License
   ```

3. **No raw SQL needed:** SeaORM's entity definitions include the column types, relations, and table name -- all the information needed to construct type-safe queries. Using the entity ensures the query is checked at compile time and stays in sync with the database schema.

**Reuse type:** Direct entity usage -- the existing SeaORM entity is used as-is in query construction. No modification to the entity file is needed.

**Benefit:** Avoids raw SQL strings that could contain typos or drift from the schema. Leverages SeaORM's type system to catch column name or relation errors at compile time. Consistent with how other join queries in the codebase are constructed (e.g., the `sbom_package` and `sbom_advisory` join entities in the same `entity/src/` directory).

---

## Additional Reuse Discovered During Analysis

### `common/src/model/paginated.rs` -- PaginatedResults<T>

While not listed as a reuse candidate in the task, the `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs` is already used by the package list endpoint. The implementation must ensure that adding the license filter does not change the response shape -- the same `PaginatedResults<PackageSummary>` wrapper continues to be used. This is a passive reuse item (already in place, must not be disrupted).

### `common/src/error.rs` -- AppError

The `AppError` enum and its `IntoResponse` implementation would be reused for input validation errors. When an invalid license value is provided (e.g., empty string), the handler returns an `AppError` variant that maps to HTTP 400. This follows the same error handling pattern used by all other endpoints in the codebase.

---

## Summary

| Reuse Candidate | Reuse Type | Modification Needed | Where Used |
|---|---|---|---|
| `common/src/db/query.rs::apply_filter` | Direct function call | None | `package/service/mod.rs` |
| `advisory/endpoints/list.rs` (severity filter pattern) | Structural pattern | None (pattern reference) | `package/endpoints/list.rs`, `package/service/mod.rs` |
| `entity/src/package_license.rs` | Direct entity usage in JOIN | None | `package/service/mod.rs` |
| `common/src/model/paginated.rs` (PaginatedResults) | Passive (already in use) | None | Response shape preserved |
| `common/src/error.rs` (AppError) | Direct usage for validation errors | None | `package/endpoints/list.rs` |

All three explicitly listed reuse candidates are used. No new utility functions or helper modules need to be created -- the existing codebase provides all the building blocks required for this feature.
