# Reuse Analysis for TC-9203: Add package license filter to list endpoint

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** The `apply_filter` function is a shared query builder helper that handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. It takes a raw query parameter string (e.g., `"MIT,Apache-2.0"`), splits it by commas, and generates the appropriate SQL filter -- a simple equality check for single values or an `IN (...)` clause for multiple values.

**How it would be applied:** In `modules/fundamental/src/package/service/mod.rs`, the license filter implementation calls `apply_filter` directly when the `license` query parameter is present. The license string from the request (e.g., `"MIT"` or `"MIT,Apache-2.0"`) is passed directly to `apply_filter`, which handles all the parsing and clause generation.

**Why reuse instead of rewrite:** Writing new comma-splitting and IN-clause generation logic would directly duplicate what `apply_filter` already does. The function is specifically designed for this use case -- it lives in the shared `common/src/db/` module and is already used by other endpoints for similar filtering. Creating a new utility for license parsing would violate DRY and diverge from the established pattern, making the codebase harder to maintain.

**Integration point:** `modules/fundamental/src/package/service/mod.rs` -- called inside the `list` method when the license filter is `Some`.

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** The advisory list endpoint implements a `severity` query parameter filter that is structurally identical to the license filter needed here. It demonstrates the established pattern for adding optional filter parameters to list endpoints in this codebase:
- A `Query` struct with an optional field for the filter parameter (e.g., `pub severity: Option<String>`)
- Deserialization of the query parameter via the framework's query extraction
- Propagation of the filter value from the endpoint handler to the service layer
- Validation and error handling for invalid values

**How it would be applied:** The advisory `list.rs` serves as the structural blueprint for modifying `modules/fundamental/src/package/endpoints/list.rs`. The implementation follows the same pattern step-by-step:
1. Add `pub license: Option<String>` to the package endpoint's `Query` struct, mirroring how `severity` is defined in the advisory `Query` struct
2. Extract `query.license` in the handler function, following the same extraction pattern used for `query.severity`
3. Pass the license value to `PackageService::list()` as an additional parameter, mirroring how the advisory handler passes severity to `AdvisoryService`
4. Apply the same validation approach for invalid values (returning 400 Bad Request via `AppError`)

**Why reuse instead of rewrite:** This pattern is the established convention for list endpoint filters in the `modules/fundamental` crate. Inventing a different approach (e.g., a different struct layout, different parameter passing style, or different validation strategy) would break consistency with sibling endpoints and make the codebase harder to navigate. Following the advisory pattern ensures the license filter is immediately recognizable to anyone familiar with the existing code.

**Integration point:** `modules/fundamental/src/package/endpoints/list.rs` -- the `Query` struct and handler function are modified to follow the advisory endpoint's pattern.

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:** The existing `package_license` entity is a SeaORM entity definition that maps the `package_license` join table in the database. This table associates packages with their declared licenses. The entity defines:
- The table structure and column mappings (package ID, license identifier)
- SeaORM relations to the `package` entity
- The necessary types for constructing JOINs in SeaORM queries

**How it would be applied:** In `modules/fundamental/src/package/service/mod.rs`, when the license filter is active, the query builder uses `entity::package_license` to construct a SeaORM JOIN between the `package` table and the `package_license` table. This allows filtering packages by their associated license identifiers using SeaORM's typed query API. The JOIN is conditional -- it is only added when the `license` parameter is present, avoiding unnecessary JOINs for unfiltered requests.

```rust
// Conceptual usage in service/mod.rs:
use entity::package_license;

// When license filter is present, join through the existing entity:
// query = query.join(package_license::Entity, ...)
// Then apply_filter operates on the joined license column
```

**Why reuse instead of rewrite:** The `package_license` entity already encodes the table schema, column names, and relationships needed for the JOIN. Writing raw SQL (`JOIN package_license ON ...`) would bypass SeaORM's type safety, break the ORM pattern used throughout the codebase, and duplicate the schema knowledge already captured in the entity definition. Creating a new entity for the same table would be redundant and could lead to schema drift.

**Integration point:** `modules/fundamental/src/package/service/mod.rs` -- imported and used for constructing the JOIN query when the license filter is applied.

## Summary

All three reuse candidates are applied in the implementation:

| # | Candidate | Role | File Where Applied |
|---|---|---|---|
| 1 | `apply_filter` | Direct function call for parsing and SQL generation | `service/mod.rs` |
| 2 | Advisory `list.rs` | Structural pattern guide for Query struct and handler | `endpoints/list.rs` |
| 3 | `package_license` entity | SeaORM JOIN construction | `service/mod.rs` |

No new utility functions are created that duplicate the functionality of any reuse candidate. The implementation strictly follows the "reuse first" principle from the skill definition.
