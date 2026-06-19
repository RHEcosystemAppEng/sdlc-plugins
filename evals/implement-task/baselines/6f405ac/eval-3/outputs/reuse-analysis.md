# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

This document details how each Reuse Candidate listed in the task description
would be applied during implementation, and confirms that no new utility
functions duplicating existing functionality are proposed.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Description from task:** Handles comma-separated multi-value query parameter
parsing and SQL IN clause generation.

**How it would be reused:**

The `apply_filter` function is the core reuse target for this task. It would be
called in two places:

1. **In `modules/fundamental/src/package/endpoints/list.rs`** — When the `license`
   query parameter is present (`Some(license_string)`), call `apply_filter` to
   parse the comma-separated string (e.g., `"MIT,Apache-2.0"`) into a
   `Vec<String>` of individual license identifiers. This is the same parsing
   behavior used by the advisory severity filter.

2. **In `modules/fundamental/src/package/service/mod.rs`** — Use `apply_filter`
   (or its output) to construct the SQL `IN` clause for the
   `package_license.license_id` column. Rather than manually building
   `WHERE license_id IN ('MIT', 'Apache-2.0')`, delegate to the existing
   `apply_filter` function which already handles:
   - Splitting comma-separated values
   - Generating parameterized SQL IN clauses
   - Handling single-value vs. multi-value cases
   - Proper SQL parameter binding (preventing SQL injection)

**Justification:** Writing custom comma-splitting or IN-clause generation logic
would directly duplicate what `apply_filter` already provides. No new parsing or
SQL generation utilities are needed.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Description from task:** The severity filter implementation is structurally
identical to the license filter needed here; follow the same Query struct pattern
with an optional field.

**How it would be reused:**

This file serves as the **structural template** for the implementation. It would
be studied and its patterns replicated (not copied verbatim) in the package
endpoint:

1. **Query struct pattern** — The advisory list endpoint defines a query
   parameter struct with an optional `severity` field (e.g.,
   `pub severity: Option<String>`). The package list endpoint's query struct
   would add a `license` field following the identical pattern:
   ```rust
   pub license: Option<String>,
   ```

2. **Handler function pattern** — The advisory handler extracts the `severity`
   field from the query struct, passes it through `apply_filter` for parsing,
   and forwards the result to `AdvisoryService::list()`. The package handler
   would follow the exact same sequence:
   - Extract `query.license`
   - If `Some`, parse with `apply_filter`
   - Pass parsed values to `PackageService::list()`

3. **Validation pattern** — If the advisory endpoint validates the severity
   parameter before filtering (e.g., checking for empty strings or invalid
   formats), the same validation approach would be applied to the license
   parameter.

4. **Error response pattern** — The advisory endpoint's error handling for
   invalid filter values (returning 400 Bad Request via `AppError`) would be
   replicated for invalid license values.

**Justification:** The advisory severity filter is a proven, reviewed
implementation of the exact same pattern needed for the license filter. Following
it ensures consistency across endpoints and avoids inventing a new approach for
a solved problem. This is structural reuse (following the same pattern) rather
than code reuse (calling the same function), which is the appropriate form since
the advisory and package endpoints are parallel implementations, not shared
abstractions.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Description from task:** Existing entity for the package-license join table;
use for the JOIN query rather than writing raw SQL.

**How it would be reused:**

The `package_license` SeaORM entity would be used in
`modules/fundamental/src/package/service/mod.rs` to build the database query
for the license filter:

1. **JOIN construction** — Instead of writing raw SQL
   (`JOIN package_license ON ...`), use the SeaORM entity's relation definitions
   to construct a type-safe join:
   ```rust
   // Conceptual — use the entity's Column and Relation enums
   query.join(package_license::Entity, ...)
        .filter(package_license::Column::LicenseId.is_in(license_values))
   ```

2. **Column references** — Use `package_license::Column::LicenseId` (or the
   equivalent column name defined in the entity) for the WHERE clause rather
   than string-based column references. This provides compile-time validation
   that the column exists and the types match.

3. **Relation traversal** — The entity likely defines a `Relation` to the
   `package` entity. Use this relation for the join condition rather than
   manually specifying `ON package.id = package_license.package_id`.

**Justification:** The `package_license` entity already encapsulates the schema
knowledge (table name, column names, relations) for the package-license mapping
table. Writing raw SQL would bypass SeaORM's type safety, risk column name
mismatches, and diverge from the project's convention of using entities for all
database access. Every other query in the codebase uses SeaORM entities — this
must too.

---

## Summary

| Reuse Candidate | Reuse Type | Where Applied | New Code Avoided |
|---|---|---|---|
| `apply_filter` (query.rs) | Direct function call | Endpoint handler + service query | Custom comma-parsing, IN-clause generation |
| Advisory list endpoint | Structural pattern | Query struct + handler flow | Novel filter architecture |
| `package_license` entity | SeaORM entity usage | Service query construction | Raw SQL joins, string column refs |

**No new utility functions are proposed.** All filtering, parsing, and query
construction needs are covered by existing code. The implementation consists
entirely of:
- Adding a field to an existing struct (query params)
- Adding a parameter to an existing method (service list)
- Wiring existing utilities together (apply_filter + package_license entity)
- Writing integration tests (new file, following existing test patterns)
