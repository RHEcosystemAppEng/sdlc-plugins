# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document details the three Reuse Candidates identified in the task description and how each would be used during implementation.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL IN clause generation. Given a string like `"MIT,Apache-2.0"`, it splits on commas, produces individual values, and generates the appropriate SQL `WHERE column IN (...)` clause for SeaORM queries.

**How it is reused:** Called directly in `modules/fundamental/src/package/service/mod.rs` within the `PackageService::list()` method. When the `license` query parameter is present, the raw string value (e.g., `"MIT"` or `"MIT,Apache-2.0"`) is passed to `apply_filter`, which handles:

1. Splitting comma-separated values into individual license identifiers
2. Generating the SQL IN clause targeting the license SPDX identifier column in the `package_license` join table
3. Handling the single-value case (where the string contains no commas) as a degenerate case of multi-value

**Why reuse instead of writing new code:** Writing a new function to split comma-separated strings and build an IN clause would exactly duplicate what `apply_filter` already does. The task description explicitly states to use this function, and the SKILL.md mandates checking for reusable code before writing new logic. Creating a new utility for the same purpose would violate the DRY principle and diverge from the established pattern used by other filter implementations in the codebase.

**No wrapper or adapter needed:** The function's interface accepts the raw query parameter string and a column reference, which is exactly what the license filter requires. No intermediate parsing, transformation, or adapter function is necessary.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:** The advisory list endpoint implements a `severity` query parameter filter using a pattern that is structurally identical to the license filter needed here. The pattern consists of:

1. A **Query struct** with an optional field (e.g., `severity: Option<String>`) that Axum automatically deserializes from query parameters
2. **Handler extraction** that reads the optional field from the deserialized Query struct
3. **Service delegation** that passes the filter value to the service layer method
4. The service method calls `apply_filter` (Reuse Candidate 1) to build the SQL filter

**How it is reused:** The same structural pattern is replicated in `modules/fundamental/src/package/endpoints/list.rs`:

- Add `license: Option<String>` to the package endpoint's Query struct, mirroring how `severity: Option<String>` exists in the advisory endpoint's Query struct
- In the handler function, extract `query.license` and pass it to `PackageService::list()`, mirroring how the advisory handler extracts `query.severity` and passes it to `AdvisoryService::list()`
- The service layer call to `apply_filter` follows the same invocation pattern

**Why reuse this pattern:** The advisory severity filter is confirmed working and follows established conventions in the codebase. Using the same structural pattern ensures consistency across endpoints, makes the codebase easier to maintain, and reduces the risk of introducing bugs through a novel approach. Developers familiar with the advisory filter will immediately recognize the license filter's structure.

**Scope of reuse:** This is pattern reuse (following the same code structure), not code sharing (importing a function). The Query struct fields, handler logic, and service method calls are written for the package module but follow the advisory module's proven approach.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:** The `package_license` entity is an existing SeaORM entity that maps the join table between packages and licenses. It defines the schema, column types, and relationships for the `package_license` database table, which contains foreign keys to both the `package` table and a license identifier column (the SPDX identifier).

**How it is reused:** Used in `modules/fundamental/src/package/service/mod.rs` to construct the JOIN query when filtering by license:

1. **JOIN construction:** When a license filter is provided, the service method joins the `package` table with the `package_license` table using SeaORM's `JoinType::InnerJoin` (or equivalent), referencing the `package_license` entity's relation definitions. This filters the result set to only packages that have a matching entry in the join table.

2. **Column reference for filtering:** The `package_license` entity's license column (SPDX identifier column) is passed to `apply_filter` (Reuse Candidate 1) as the target column for the IN clause. This ensures the filter operates on the correct column in the correct table.

3. **No raw SQL:** By using the existing SeaORM entity, the implementation avoids raw SQL strings for the JOIN. SeaORM handles SQL generation, parameter binding, and type safety through the entity definition. This is consistent with how other join queries in the codebase (e.g., `sbom_package.rs`, `sbom_advisory.rs`) are constructed.

**Why reuse instead of writing raw SQL:** The entity already encodes the table schema, column names, and relationships. Writing raw SQL would bypass SeaORM's type checking, risk column name typos, and diverge from the codebase's convention of using entity-based queries. Every other join query in the `modules/fundamental/` directory uses SeaORM entities for JOINs.
