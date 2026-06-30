# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

This document details the Reuse Candidates listed in the task description and how
each one is applied during implementation.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:**
The `apply_filter` function handles comma-separated multi-value query parameter
parsing and SQL `IN` clause generation. It takes a raw query string value like
`"MIT,Apache-2.0"`, splits it on commas, and produces a SeaORM condition that
matches any of the provided values.

**How it is reused:**
- Called directly in `PackageService::list()` (in `modules/fundamental/src/package/service/mod.rs`)
  to transform the raw `license` query parameter string into a database filter condition.
- No modification or extension of `apply_filter` is needed — the existing function
  already handles the single-value case (no comma) and the multi-value case
  (comma-separated) identically.
- This avoids writing custom comma-splitting or SQL `IN` clause logic. The function
  is already tested and used by the advisory module, so its correctness is established.

**Reuse type:** Direct invocation (no changes to the reused code).

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:**
The advisory list endpoint implements a `severity` query parameter filter using a
pattern that is structurally identical to the license filter needed here. It
demonstrates:
- How to define an optional filter field in the query parameters struct (e.g.,
  `severity: Option<String>` inside a `Query` struct derived with `Deserialize`
  and `IntoParams`).
- How to extract the filter value from the Axum query extractor.
- How to pass the filter value to the corresponding service method.
- How to handle the case where the parameter is absent (skip filtering entirely).

**How it is reused:**
- The query parameters struct in `modules/fundamental/src/package/endpoints/list.rs`
  is extended to follow the same pattern: add an optional `license: Option<String>`
  field with the same derive macros and documentation attributes.
- The handler function mirrors the advisory handler's approach: extract the `license`
  field from the query struct and pass it to `PackageService::list()`.
- The error-handling pattern for invalid filter values (returning `AppError` which
  converts to a 400 response) is replicated from the advisory endpoint.

**Reuse type:** Structural pattern replication (the advisory code is the template;
the package code follows the same structure with domain-specific substitutions).

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:**
The existing SeaORM entity for the package-license join table. This entity defines
the database schema mapping between packages and their declared licenses, including:
- The table name and column definitions.
- The `Relation` enum linking to the `package` entity.
- The `Column` enum with a `License` variant for the SPDX identifier column.

**How it is reused:**
- Used in `PackageService::list()` to construct a `JoinType::InnerJoin` between the
  `package` table and the `package_license` table when the `license` filter is active.
- The `Column::License` enum variant is used as the filter target in the `apply_filter`
  call (e.g., `apply_filter(package_license::Column::License, &license_value)`).
- No changes to the entity are needed — it already maps the required columns and
  relationships.

**Reuse type:** Direct usage as a join target (no changes to the reused code).

---

## Additional Reuse Opportunities Identified

Beyond the three explicit Reuse Candidates in the task description, the implementation
also leverages:

| Existing Code | How Used |
|---|---|
| `common/src/model/paginated.rs::PaginatedResults<T>` | The response wrapper is already used by the package list endpoint. No changes needed — the filter only affects input, not output shape. |
| `common/src/error.rs::AppError` | Used to return 400 Bad Request for invalid license values. The existing `AppError` enum already has variants for validation errors — reuse the same variant and `.context()` wrapping pattern used throughout the codebase. |
| `tests/api/advisory.rs` (test patterns) | The assertion style, test naming convention, and response validation approach from the advisory integration tests are replicated in the new `package_license_filter.rs` test file. |

---

## Summary

All three Reuse Candidates listed in the task description are applied:

| # | Reuse Candidate | Reuse Type | Changes to Existing Code |
|---|---|---|---|
| 1 | `apply_filter` in `query.rs` | Direct invocation | None |
| 2 | Advisory list endpoint pattern | Structural replication | None |
| 3 | `package_license` entity | Direct join target | None |

No new utility functions or shared modules need to be created. The implementation
is entirely composed of existing building blocks, with new code limited to:
- The query parameter struct extension (in the endpoint layer)
- The filter application logic (in the service layer)
- Integration tests (new test file)
