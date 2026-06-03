# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document details how each Reuse Candidate identified in the task description is used in the implementation, and confirms that no duplicated logic is introduced.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides**: The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL IN clause generation. Given a raw query string like `"MIT,Apache-2.0"` and a target SeaORM column, it splits the string on commas, validates the individual values, and produces the appropriate filter condition (equality for a single value, IN clause for multiple values).

**How it is reused**: In `modules/fundamental/src/package/service/mod.rs`, when the `license` query parameter is present, it is passed directly to `apply_filter` along with the `package_license::Column::License` column reference. This single call handles all of the following:

- Parsing `"MIT"` into a single-value equality filter
- Parsing `"MIT,Apache-2.0"` into a multi-value IN filter
- Generating the correct SeaORM condition to attach to the query

**What is NOT done**: No new parsing logic is written. No custom comma-splitting, no manual SQL IN clause construction, no new helper functions that would duplicate what `apply_filter` already provides. The function is called as-is with no modifications to `query.rs`.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides**: The advisory list endpoint already implements a `severity` query parameter using an `Option<String>` field on a Query struct, which is then passed to the service layer for filtering. This establishes a proven pattern for optional filter parameters in list endpoints.

**How it is reused**: The advisory severity filter serves as the structural template for the package license filter. Specifically, the following elements are replicated in the package endpoint:

1. **Query struct pattern**: An `Option<String>` field named `license` is added to the package endpoint's Query struct, mirroring the `severity` field on the advisory Query struct.
2. **Handler flow**: The handler extracts `query.license` and passes it to the service method, exactly as the advisory handler passes `query.severity`.
3. **Service integration**: The service method conditionally applies the filter when the parameter is `Some`, following the same conditional logic structure used in the advisory service.

**What is NOT done**: No new architectural pattern is invented. The advisory filter pattern is followed directly, ensuring consistency across the codebase and reducing the risk of structural divergence between list endpoints.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides**: The existing SeaORM entity that maps the `package_license` database table. This entity defines the columns (including the license SPDX identifier column) and the relations (including the relation to the `package` table) needed to join packages to their licenses.

**How it is reused**: In `modules/fundamental/src/package/service/mod.rs`, the license filter implementation uses this entity in two ways:

1. **JOIN definition**: The `package_license::Relation::Package` relation (reversed) is used to define the `INNER JOIN` from the packages query to the package_license table. This leverages SeaORM's relation system rather than writing raw SQL JOIN clauses.
2. **Column reference**: The `package_license::Column::License` column is passed to `apply_filter` as the target column for the filter condition. This ensures the filter is applied to the correct column via SeaORM's type-safe column references.

**What is NOT done**: No raw SQL is written for the join. No new entity or model is created. The existing entity's column definitions and relation definitions are used directly, maintaining consistency with how other entity-based joins work throughout the codebase.

---

## Summary

| Reuse Candidate | Location | Reuse Approach | New Code Written |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Called directly for comma-separated parsing and IN clause generation | None -- used as-is |
| Advisory severity filter | `modules/fundamental/src/advisory/endpoints/list.rs` | Structural pattern followed for Query struct, handler flow, and service integration | Analogous code in package module following same pattern |
| `package_license` entity | `entity/src/package_license.rs` | Used for JOIN relation and column reference in the filter query | None -- used as-is |

No new utility functions, helpers, or shared modules are introduced. All filtering, parsing, and query-building logic is delegated to existing reusable code.
