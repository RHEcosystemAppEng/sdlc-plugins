# Reuse Analysis: TC-9203 -- Add Package License Filter

## Summary

The task description identifies three Reuse Candidates. All three should be reused directly rather than writing new code. This analysis details how each candidate is used and why reuse is the correct approach.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source:** `common/src/db/query.rs`

**What it provides:** The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL IN clause generation. It takes a raw query parameter string (e.g., `"MIT,Apache-2.0"`), splits it on commas, and produces the appropriate SQL filter (either a single equality check for one value or an IN clause for multiple values).

**How it will be reused:** Call `apply_filter` directly when processing the `license` query parameter in the package list endpoint. This avoids writing any custom string-splitting or SQL IN clause logic. The function is already used by the advisory severity filter, so it is proven to work correctly for this exact use case pattern.

**Reuse type:** Direct invocation -- no modification or extension of `apply_filter` is needed.

**What would happen without reuse:** Without using `apply_filter`, the implementation would need to manually split the comma-separated license string, handle edge cases (empty strings, whitespace, single values vs. multiple values), and construct the SQL WHERE clause. This would duplicate logic that already exists and is tested in `query.rs`.

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Source:** `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** The advisory list endpoint already implements a `severity` query parameter filter using a pattern that is structurally identical to the license filter needed for the package endpoint. This includes: (1) a Query struct with an optional filter field, (2) extraction of the filter value from the request query string, (3) passing the filter to the service layer, and (4) use of `apply_filter` for the actual filtering logic.

**How it will be reused:** The advisory severity filter serves as the structural template for the license filter implementation. The following elements will be replicated (not copied verbatim, but following the same pattern):

1. **Query struct pattern:** Add an optional `license: Option<String>` field to the package endpoint's query parameter struct, matching how the advisory endpoint defines its `severity` field.
2. **Handler pattern:** Extract the license value from the query struct and pass it to the service method, following the same control flow as the advisory handler.
3. **Service integration pattern:** Follow how the advisory service receives the severity filter and applies it to the database query, adapting for the license-specific table and column.

**Reuse type:** Structural pattern reuse -- the advisory endpoint is the reference implementation that dictates how the package endpoint should be structured. The code is not imported or called; rather, it is the blueprint for consistent implementation.

**What would happen without reuse:** Without following the advisory pattern, the developer might invent a different approach (e.g., filtering in application code instead of at the database layer, or using a different query parameter extraction mechanism). This would create inconsistency across endpoints and make the codebase harder to maintain.

## Reuse Candidate 3: `entity/src/package_license.rs`

**Source:** `entity/src/package_license.rs`

**What it provides:** The SeaORM entity definition for the `package_license` join table, which maps packages to their declared licenses. This entity defines the table structure, column types, and relationships needed to join packages with their licenses.

**How it will be reused:** Use the `package_license` entity in the `PackageService::list` method to construct a JOIN query that connects the `package` table to license data. Specifically:

1. **JOIN construction:** Use SeaORM's relation-based join (e.g., `find().join(JoinType::Inner, package_license::Relation::Package.def())`) or an explicit column-based join to connect the package query to the `package_license` table.
2. **Filter application:** After joining, filter on the license identifier column defined in the `package_license` entity, using the values parsed by `apply_filter`.

**Reuse type:** Direct usage of existing entity -- no modification to `package_license.rs` is needed. The entity is consumed as-is by the new query logic.

**What would happen without reuse:** Without using the existing entity, the implementation would need to write raw SQL JOINs or define a new entity/relation for the same table. This would bypass SeaORM's type safety, duplicate the schema definition, and risk inconsistency if the table schema changes.

## Additional Reuse Opportunities

Beyond the three listed candidates, the following existing code will also be reused:

- **`common/src/model/paginated.rs` (`PaginatedResults<T>`):** The response wrapper is already used by the package list endpoint. No changes needed -- the filtered results continue to use the same wrapper.
- **`common/src/error.rs` (`AppError`):** Used for the 400 Bad Request response on invalid license values. The existing `AppError` enum already supports this response type via its `IntoResponse` implementation.
- **Test patterns from `tests/api/advisory.rs`:** The advisory integration tests provide the pattern for assertion style, response validation, and test structure. The new package license filter tests will follow these same patterns.

## Reuse Decision Matrix

| Candidate | Reuse Type | Modification Needed | Risk |
|---|---|---|---|
| `apply_filter` | Direct call | None | None -- proven utility |
| Advisory `list.rs` | Pattern template | None (reference only) | None -- well-established pattern |
| `package_license` entity | Direct usage in JOIN | None | None -- existing entity |
| `PaginatedResults` | Direct usage | None | None -- already in use |
| `AppError` | Direct usage | None | None -- already in use |
