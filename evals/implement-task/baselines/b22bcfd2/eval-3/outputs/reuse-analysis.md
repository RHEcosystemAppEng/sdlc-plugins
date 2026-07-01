# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document analyzes each Reuse Candidate identified in the task description and details how it would be used in the implementation.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. Given a raw query parameter string like `"MIT,Apache-2.0"`, it splits on commas, produces individual filter terms, and generates the appropriate SQL `WHERE column IN (value1, value2, ...)` clause.

**How it is reused:** In `modules/fundamental/src/package/service/mod.rs`, the `PackageService::list` method calls `apply_filter` directly with the `license` query parameter value and the target column from the `package_license` entity. This handles both the single-value case (`license=MIT`) and the multi-value case (`license=MIT,Apache-2.0`) without any custom parsing code.

**Why no new utility is needed:** The `apply_filter` function already provides the exact capability required -- splitting comma-separated values and generating IN clauses. Writing a new helper function or inline parsing logic would duplicate this existing functionality. The implementation calls `apply_filter` directly, with no wrapper layer.

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** The advisory list endpoint implements a `severity` query parameter filter that is structurally identical to the `license` filter needed here. It demonstrates the established pattern for adding optional filters to list endpoints in this codebase:

1. A `Query` struct with an optional field (e.g., `severity: Option<String>`)
2. Axum query parameter extraction into the struct
3. Forwarding the optional filter value to the corresponding service method
4. The service method conditionally applying the filter only when the value is `Some`

**How it is reused:** The `license` filter in `modules/fundamental/src/package/endpoints/list.rs` follows the same structural pattern:

- Add `license: Option<String>` to the package endpoint's Query struct, mirroring how `severity: Option<String>` exists in the advisory endpoint's Query struct
- Extract it via Axum's query parameter deserialization (same mechanism)
- Forward `query.license` to `PackageService::list()`, just as the advisory endpoint forwards `query.severity` to `AdvisoryService`
- Apply the filter conditionally in the service layer

This is pattern reuse (following an established convention), not code copy. The advisory endpoint serves as the reference implementation that defines how filter parameters are added throughout the `modules/fundamental` crate.

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:** The `package_license` SeaORM entity defines the database mapping for the package-to-license join table. It includes:

- The entity struct and column definitions for the `package_license` table
- The relationship definitions connecting packages to their licenses
- The column enum that can be used in SeaORM query builder expressions

**How it is reused:** In `modules/fundamental/src/package/service/mod.rs`, the license filter implementation uses this entity to construct the JOIN between the `package` table and the `package_license` table. Specifically:

- The entity's relation definition is used with SeaORM's `.join()` or `.find_also_related()` API to express the JOIN without raw SQL
- The entity's column enum (e.g., `package_license::Column::License`) is used in the WHERE clause to filter by the license value(s) produced by `apply_filter`

No new entity definitions, raw SQL joins, or manual table/column references are needed. The existing entity encapsulates all the schema knowledge required for the join query.

## Summary

All three Reuse Candidates are used directly in the implementation. No new utility functions, entity definitions, or query helpers are created. The implementation composes existing infrastructure (shared query builder, established endpoint pattern, existing entity) to deliver the feature with minimal new code.

| Reuse Candidate | Location Used | Reuse Type |
|---|---|---|
| `apply_filter` | `package/service/mod.rs` | Direct function call for filter parsing and SQL generation |
| Advisory list filter pattern | `package/endpoints/list.rs` | Structural pattern reuse (Query struct, forwarding, conditional application) |
| `package_license` entity | `package/service/mod.rs` | SeaORM entity for JOIN query construction |
