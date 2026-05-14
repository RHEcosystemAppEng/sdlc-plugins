# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Overview

Add a `license` query parameter to `GET /api/v2/package` supporting single-value and comma-separated multi-value filtering by SPDX license identifier. This implementation maximizes reuse of existing infrastructure: the `apply_filter` utility for parameter parsing, the advisory severity filter as a structural template, and the `package_license` entity for the JOIN query.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

- Add an optional `license: Option<String>` field to the existing `Query` struct, following the identical pattern used for the severity filter in `modules/fundamental/src/advisory/endpoints/list.rs`.
- In the list handler, pass the `license` field from the parsed query through to the service layer. No manual parsing of comma-separated values is needed here; that responsibility belongs to `common/src/db/query.rs::apply_filter`, which already handles splitting comma-separated multi-value parameters and generating the appropriate SQL `IN` clause.

### 2. `modules/fundamental/src/package/service/mod.rs`

- Extend the `list` method on `PackageService` to accept the optional license filter parameter.
- When the license filter is present, use `entity/src/package_license.rs` (the existing `package_license` SeaORM entity) to construct a JOIN between the packages table and the package-license join table. Do NOT write raw SQL or create a new entity; the join table entity already exists and models the relationship.
- Call `common/src/db/query.rs::apply_filter` to convert the comma-separated license string into the correct `sea_orm` filter condition (an `IN` clause for multiple values, or an equality check for a single value). Do NOT write new parsing logic or create a new utility function that would duplicate `apply_filter`.
- Chain the resulting filter condition onto the existing query builder, preserving the established pattern of returning `PaginatedResults<T>` and using `.context()` for error propagation via `Result<T, AppError>`.

## Files to Create

### 3. `tests/api/package_license_filter.rs`

- Add integration tests covering:
  - Single license filter: `?license=MIT` returns only packages with an MIT license.
  - Multi-value comma-separated filter: `?license=MIT,Apache-2.0` returns packages matching either license.
  - No filter: omitting the `license` parameter returns all packages (existing behavior unchanged).
  - No matches: filtering by a license with no associated packages returns an empty `PaginatedResults`.
- Follow the existing integration test conventions (Axum test client setup, database seeding, assertion on `PaginatedResults` shape).

## Reuse Strategy

| Reuse Candidate | How It Is Used |
|---|---|
| `common/src/db/query.rs::apply_filter` | Reuse directly to parse comma-separated license values and generate the SQL `IN` clause. No new parsing or utility code is written. |
| `modules/fundamental/src/advisory/endpoints/list.rs` | Follow the same `Query` struct pattern (optional filter field, pass-through to service). The severity filter is structurally identical to the license filter being added. |
| `entity/src/package_license.rs` | Use the existing SeaORM entity for the package-license join table to construct the JOIN query. No raw SQL and no new entity creation. |

## Constraints

- Only the three files listed above are in scope (two modifications, one creation).
- No new utility functions that duplicate `apply_filter` behavior.
- No duplication of existing filtering logic from the advisory module; follow the established pattern.
- All error handling uses `Result<T, AppError>` with `.context()`.
- Pagination via `PaginatedResults<T>` is preserved.
