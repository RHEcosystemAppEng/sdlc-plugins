# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Reuse Candidates from Task Description

The task description lists three reuse candidates. All three are reused in the
implementation. No new utility functions are created that would duplicate their
functionality.

---

### 1. `common/src/db/query.rs::apply_filter`

**What it provides:** Handles comma-separated multi-value query parameter parsing and
SQL `IN` clause generation. Given a string like `"MIT,Apache-2.0"`, it splits on commas,
trims whitespace, and produces the appropriate SQL filter (single `=` for one value,
`IN (...)` for multiple values).

**How it is reused:**

- In `modules/fundamental/src/package/service/mod.rs`, the `license` filter string
  received from the endpoint handler is passed directly to `apply_filter` to generate
  the database filter condition.
- No custom comma-parsing logic is written. The `apply_filter` function is called
  with the raw `license` query parameter value and the target column
  (`package_license.license`), and it handles all parsing and SQL generation internally.
- This is a direct reuse — `apply_filter` is invoked as-is, with no wrapper, extension,
  or duplication.

**Why not create a new utility:** `apply_filter` already handles the exact use case
needed (comma-separated values to SQL `IN` clause). Creating a separate
`parse_license_filter` or `split_comma_values` function would duplicate logic that
`apply_filter` already provides.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:** A working reference implementation of an optional query parameter
filter on a list endpoint. The advisory list endpoint's `Query` struct includes an
optional `severity: Option<String>` field, and the handler passes it to
`AdvisoryService::list()` which applies the filter using `apply_filter`.

**How it is reused:**

- The `Query` struct in `modules/fundamental/src/package/endpoints/list.rs` is extended
  with an `license: Option<String>` field, following the identical pattern as `severity`
  in the advisory endpoint's `Query` struct.
- The handler function passes the `license` value to `PackageService::list()` using the
  same parameter-forwarding pattern that the advisory handler uses to pass `severity` to
  `AdvisoryService::list()`.
- The validation approach (checking for empty/invalid values and returning 400) follows
  the same error-handling pattern used in the advisory endpoint.
- This is a structural/pattern reuse — the advisory endpoint's code is not called directly,
  but its design is replicated exactly for consistency across list endpoints.

**Why follow this pattern:** The advisory list endpoint is the closest structural sibling
to the package list endpoint. Using the same `Query` struct pattern with an optional
filter field ensures consistency across the codebase's list endpoints and makes the
codebase predictable for developers who already understand the advisory endpoint.

---

### 3. `entity/src/package_license.rs` (package-license join entity)

**What it provides:** A SeaORM entity definition for the `package_license` database table
that maps packages to their declared licenses. This entity defines the table schema,
column types, and relations to the `package` table.

**How it is reused:**

- In `modules/fundamental/src/package/service/mod.rs`, the `PackageService::list()` method
  uses the `package_license` entity to perform a JOIN between the `package` table and the
  `package_license` table when a license filter is active.
- The join is performed using SeaORM's relation-based query builder (e.g.,
  `find().join(JoinType::InnerJoin, package_license::Relation::Package.def())`) rather
  than writing raw SQL. The entity's defined `Relation` enum provides the join condition.
- The `package_license::Column::License` enum variant is used as the target column when
  calling `apply_filter`, ensuring type-safe column references.
- This is a direct reuse — the existing entity and its relations are used as-is. No new
  entity, migration, or raw SQL join is needed.

**Why not write raw SQL:** The `package_license` entity already encodes the table schema
and relations. Using it through SeaORM's query builder provides compile-time safety,
automatic SQL generation, and consistency with how other joins are performed throughout
the codebase.

---

## Summary

| Reuse Candidate | Reuse Type | Where Used |
|---|---|---|
| `common/src/db/query.rs::apply_filter` | Direct invocation | `package/service/mod.rs` — comma parsing and SQL IN clause |
| `advisory/endpoints/list.rs` (severity filter) | Structural pattern | `package/endpoints/list.rs` — Query struct and handler pattern |
| `entity/src/package_license.rs` | Direct invocation | `package/service/mod.rs` — JOIN query via SeaORM relations |

No new utility functions are created. All comma-separated parameter parsing is handled
by the existing `apply_filter` function. All join operations use the existing
`package_license` entity. The endpoint structure follows the established advisory
list pattern.
