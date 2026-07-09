# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document analyzes the three Reuse Candidates identified in the task description for TC-9203. Each candidate is an existing codebase component that should be reused rather than duplicating its functionality.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** The `apply_filter` function in `common/src/db/query.rs` is a shared query builder helper that handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. When given a comma-separated string like `"MIT,Apache-2.0"`, it splits the values, validates them, and produces the corresponding SQL filter condition (e.g., `column IN ('MIT', 'Apache-2.0')`). For single values (e.g., `"MIT"`), it produces an equality condition.

**How it applies to TC-9203:** The license filter needs to support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) query parameters. Rather than writing custom string-splitting and SQL generation logic in the package service or endpoint, the implementation will call `apply_filter` directly, passing the raw `license` query parameter string and the target column from the `package_license` entity. This function handles all parsing, validation, and SQL construction.

**Where it is used:** In `modules/fundamental/src/package/service/mod.rs`, inside the list method. When the optional `license` filter parameter is `Some`, the service will invoke `apply_filter` with the license string and the appropriate SeaORM column reference to build the WHERE clause for the filtered query.

**Why reuse is critical:** Writing new comma-separated parsing logic would directly duplicate the functionality that `apply_filter` already provides. The function is the project's established pattern for this type of filtering -- it is used by other modules (e.g., the advisory severity filter) and encapsulates edge-case handling (empty strings, whitespace trimming, SQL injection prevention via parameterized queries). Creating a new utility function for the same purpose would violate the DRY principle and diverge from the codebase's established conventions.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** The advisory list endpoint (`GET /api/v2/advisory`) implements a `severity` query parameter filter using a Query struct pattern. The file demonstrates the complete end-to-end approach for adding an optional filter to a list endpoint in this codebase: defining the Query struct with an optional field, deserializing from query parameters via serde, extracting the filter value in the handler, and passing it to the service layer.

**How it applies to TC-9203:** The license filter in `modules/fundamental/src/package/endpoints/list.rs` is structurally identical to the severity filter in the advisory endpoint. The implementation will follow the advisory list endpoint as a template:

1. **Query struct pattern** -- Add an `license: Option<String>` field to the package list Query struct, mirroring how `severity: Option<String>` is defined in the advisory list Query struct. Apply the same serde and OpenAPI derive attributes.

2. **Handler wiring** -- In the package list handler, extract `query.license` and pass it to the `PackageService::list()` method, following the same parameter-passing pattern used by the advisory handler when it passes `query.severity` to `AdvisoryService::list()`.

3. **Error handling** -- Follow the same `Result<T, AppError>` pattern with `.context()` wrapping that the advisory endpoint uses for validation errors.

**Where it is used:** As a structural reference when modifying `modules/fundamental/src/package/endpoints/list.rs`. The advisory endpoint is not imported or called -- it serves as a pattern guide to ensure the package endpoint follows the same conventions and structure.

**Why reuse is critical:** Following the established advisory filter pattern ensures consistency across the codebase's list endpoints. Inventing a different approach for the license filter (e.g., different struct layout, different parameter passing mechanism, different error handling) would create inconsistency between sibling modules and make maintenance harder. The advisory endpoint is a proven, reviewed pattern in the same codebase -- deviating from it would be an unjustified risk.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:** The `package_license.rs` file in the `entity/` crate defines the SeaORM entity for the package-license join table. This entity maps the database table that associates packages with their declared licenses, providing typed column references, relation definitions, and model structs that SeaORM uses for query building. It represents the many-to-many relationship between the `package` table and license data.

**How it applies to TC-9203:** The license filter requires joining the `package` table with the `package_license` table to find packages that have a specific license. Instead of writing raw SQL for this JOIN, the implementation will use the `package_license` entity's SeaORM model:

1. **JOIN construction** -- Use `entity::package_license::Entity` and its `Relation` definitions to construct the JOIN clause in the service layer query. SeaORM's `find_also_linked()` or `join()` methods accept entity references, producing type-safe JOINs without raw SQL.

2. **Column reference** -- Use the entity's column enum (e.g., `entity::package_license::Column::LicenseId` or the SPDX identifier column) as the target for the filter condition generated by `apply_filter`. This provides compile-time type checking on the column reference.

3. **Model deserialization** -- The entity's `Model` struct ensures that query results from the JOIN are correctly deserialized, maintaining type safety throughout the query pipeline.

**Where it is used:** In `modules/fundamental/src/package/service/mod.rs`, when constructing the filtered query. The service imports the `package_license` entity and uses it to build the JOIN and apply the license filter condition.

**Why reuse is critical:** The `package_license` entity already encapsulates the database schema for the package-license relationship. Writing raw SQL or defining inline table/column references would bypass SeaORM's type safety, risk schema drift (if the table structure changes, the entity is updated but raw SQL would not be), and diverge from how every other entity relationship is queried in the codebase. Using the existing entity ensures the license filter query is consistent with the rest of the data access layer.

---

## Summary

| Reuse Candidate | Location | Role in Implementation | Layer |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Comma-separated parameter parsing and SQL IN clause generation | Service (query building) |
| Advisory list endpoint | `modules/fundamental/src/advisory/endpoints/list.rs` | Structural template for Query struct and handler wiring | Endpoint (request handling) |
| Package-license entity | `entity/src/package_license.rs` | SeaORM entity for JOIN query between packages and licenses | Service (data access) |

All three candidates address distinct layers of the implementation (endpoint, service/query, data access) and together eliminate the need for any custom parsing, raw SQL, or ad-hoc query construction. No new utility functions duplicating existing functionality will be created.
