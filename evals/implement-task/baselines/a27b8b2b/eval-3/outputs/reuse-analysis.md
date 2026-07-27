# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document details how each of the three Reuse Candidates identified in the task
description is used in the implementation, following the implement-task skill's
"Reuse first" principle (Step 6).

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** The `apply_filter` function is a shared query builder helper that
handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation.
Given a string like `"MIT,Apache-2.0"`, it splits on commas, trims whitespace, and produces
a SeaORM condition equivalent to `WHERE column IN ('MIT', 'Apache-2.0')`. For single values
(no comma), it produces a simple `WHERE column = 'MIT'` equality check.

**How it is reused:**

- **In `modules/fundamental/src/package/service/mod.rs`:** The `PackageService::list()`
  method receives the raw license query parameter string from the endpoint layer. Instead
  of writing custom comma-splitting or filter-building logic, it passes the value directly
  to `apply_filter`, which returns the appropriate SeaORM `Condition` to attach to the
  query. This handles both the single-value case (`?license=MIT`) and the multi-value case
  (`?license=MIT,Apache-2.0`) without any new parsing code.

- **No new utility functions created:** The task explicitly requires not duplicating
  `apply_filter` functionality. No new helper, parser, or filter-builder is written.
  The existing `apply_filter` is called directly from the service layer, exactly as
  other modules (like the advisory service) already do.

**Why reuse is appropriate:** `apply_filter` was designed as a shared utility in the
`common` crate precisely for this use case -- it is already used by other list endpoints
for their filter parameters. Writing a separate comma parser or filter builder would
duplicate tested, battle-hardened logic.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** The advisory list endpoint implements a `severity` query parameter
filter using a specific structural pattern:

1. A `Query` struct with optional filter fields, derived with Axum's query parameter
   deserializer (`#[derive(Deserialize)]`)
2. The endpoint handler extracts the `Query` struct from the request
3. When the optional filter field is `Some(value)`, it passes the value to the service
   layer
4. The service layer uses `apply_filter` to convert the value into a database condition

This pattern is the established convention for adding filters to list endpoints in the
trustify-backend codebase.

**How it is reused:**

- **As a structural guide for `modules/fundamental/src/package/endpoints/list.rs`:**
  The package list endpoint's `Query` struct is extended by adding an
  `license: Option<String>` field, mirroring how the advisory endpoint has its
  `severity: Option<String>` field. The handler code follows the same conditional
  pattern: check if `query.license.is_some()`, and if so, pass it to the service.

- **As a structural guide for service-layer integration:** The way
  `AdvisoryService::list()` accepts and applies the severity filter informs how
  `PackageService::list()` accepts and applies the license filter. The parameter
  passing pattern (optional filter value from endpoint to service) and the
  `apply_filter` invocation pattern are replicated.

**Why reuse is appropriate:** Following the advisory endpoint's pattern ensures
consistency across the codebase. All list endpoints that support filtering will use
the same Query struct pattern, the same optional-field approach, and the same
service-layer delegation. This makes the codebase predictable for developers and
reviewers -- seeing one filtered list endpoint teaches you how all of them work.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:** The `package_license` entity is a SeaORM entity definition that
maps the `package_license` database table -- a join table that associates packages with
their declared licenses. It defines:

- The `Model` struct with columns for the foreign keys (package ID, license SPDX
  identifier) and any additional metadata
- The `Relation` enum defining SeaORM relationships to the `package` entity and
  the license reference
- The `Entity` type alias and column definitions used by SeaORM's query builder

**How it is reused:**

- **In `modules/fundamental/src/package/service/mod.rs`:** When a license filter is
  present, the service constructs a SeaORM query that JOINs the `package` table with
  `package_license` using the entity's defined `Relation`. The query uses
  `package_license::Entity` and `package_license::Column::LicenseSpdxId` (or equivalent
  column name) to build the JOIN and WHERE clause. This avoids raw SQL and leverages
  SeaORM's type-safe query building.

- **No new entity or join table created:** The `package_license` entity already exists
  and correctly models the relationship. The implementation does not create a new entity,
  define a new relation, or write raw SQL JOIN statements. It uses the existing entity's
  columns and relations as SeaORM intended.

**Why reuse is appropriate:** The `package_license` entity is the canonical representation
of the package-to-license relationship in the codebase. Using it ensures that:

1. The JOIN uses the correct table and column names (defined once in the entity)
2. Any future schema changes to the join table are reflected automatically via the entity
3. The query is type-safe -- SeaORM will catch column name mismatches at compile time
4. The approach is consistent with how other modules perform JOINs (e.g., `sbom_package`
   for SBOM-package relationships, `sbom_advisory` for SBOM-advisory relationships)

---

## Summary

All three Reuse Candidates are used directly in the implementation. No new utility
functions, parsers, or entity definitions are created that would duplicate existing
functionality:

| Reuse Candidate | Used In | Purpose |
|---|---|---|
| `apply_filter` (query.rs) | `package/service/mod.rs` | Parse comma-separated license values and generate SQL IN clause |
| Advisory list pattern (list.rs) | `package/endpoints/list.rs` | Structural guide for Query struct, handler flow, and service delegation |
| `package_license` entity | `package/service/mod.rs` | JOIN query to filter packages by license through the existing join table |
