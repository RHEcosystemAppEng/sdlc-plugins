# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document covers all three Reuse Candidates identified in the task description and explains how each would be applied in the implementation.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides**: The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. Given a string like `"MIT,Apache-2.0"`, it splits on commas, produces individual values, and constructs the appropriate SQL filter (an `IN` clause for multiple values, or a simple equality check for a single value).

**How it is reused**: In `modules/fundamental/src/package/service/mod.rs`, when the `license` parameter is present, `apply_filter` is called directly with the raw license string from the query parameter. It handles all parsing and SQL generation. This means:

- No custom comma-splitting logic is written. `apply_filter` already handles the `"MIT,Apache-2.0"` -> `["MIT", "Apache-2.0"]` transformation.
- No custom SQL `IN` clause construction is written. `apply_filter` already generates the correct `WHERE license_column IN (...)` predicate.
- Edge cases (single value, multiple values, whitespace handling) are handled by the existing tested utility rather than reimplemented.

**Justification for direct reuse**: The license filter has identical semantics to other filters already using `apply_filter` -- it takes an optional comma-separated string and produces a set-membership filter. Writing a new parser or SQL builder would duplicate this function's exact responsibility.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides**: The advisory list endpoint already implements a query-parameter-based filter (severity) using a consistent structural pattern:

1. A `Query` struct (or equivalent) with an `Option<String>` field for the filter parameter, annotated with the appropriate serde/actix-web attributes for query string extraction.
2. An endpoint handler that extracts the query parameters and forwards the filter value to the service layer.
3. Validation logic that rejects malformed values with a 400 response.

**How it is reused**: The advisory severity filter serves as the structural template for the license filter. Specifically:

- **Query struct pattern**: The `license` field in the package endpoint's `Query` struct is declared identically to how `severity` is declared in the advisory endpoint's `Query` struct -- same type (`Option<String>`), same serde attributes, same extraction mechanism.
- **Handler flow pattern**: The package endpoint handler follows the same sequence as the advisory handler: extract query params, forward the filter value to the service method, return the service result. This keeps the endpoint layer thin and consistent across the codebase.
- **Validation pattern**: Whatever validation the advisory endpoint applies to the severity value (before or after calling `apply_filter`) is replicated for the license value. This ensures consistent error responses across endpoints.

**Justification for following this pattern**: Using the same structural pattern as an existing, working filter endpoint ensures consistency across the API surface. It also reduces cognitive overhead for developers who already understand the advisory filter -- the license filter works the same way. Deviating from this pattern would introduce unnecessary inconsistency.

---

## Reuse Candidate 3: `entity/src/package_license.rs` (package-license join entity)

**What it provides**: The `package_license` entity defines the ORM mapping for the join table that associates packages with their licenses. It includes the table structure, column definitions, and relationship definitions (linking to the `package` entity via a foreign key on `package_id`). This entity is part of the existing SeaORM / Diesel entity layer (depending on the ORM used by the project).

**How it is reused**: In `modules/fundamental/src/package/service/mod.rs`, the license filter requires joining the `package` table with the `package_license` table to access the license SPDX identifier column. The `package_license` entity is used for this join:

- **JOIN construction**: The entity's relationship definitions are used to construct the JOIN between `package` and `package_license`. This avoids writing raw SQL joins and keeps the query within the ORM's type-safe query builder.
- **Column reference**: The license SPDX identifier column is referenced through the entity's column enum (e.g., `package_license::Column::License` or similar), which `apply_filter` uses to build the `WHERE` clause.
- **No raw SQL**: By reusing the existing entity, the implementation stays within the ORM layer. Raw SQL strings for the join condition (`package.id = package_license.package_id`) are not needed because the entity already encodes this relationship.

**Justification for reusing the entity**: The `package_license` table and its ORM mapping already exist. Writing raw SQL to join these tables would bypass the entity layer, lose type safety, and risk inconsistency with how the same join is performed elsewhere in the codebase. Using the entity directly is both safer and more maintainable.

---

## Summary

All three reuse candidates are applied in this implementation. No new utility functions or abstractions are created that would duplicate existing functionality. The implementation adds one field to the endpoint query struct, one parameter to the service method, one JOIN using an existing entity, and one call to an existing filter utility. The result is a minimal, consistent addition that leverages the codebase's established patterns.
