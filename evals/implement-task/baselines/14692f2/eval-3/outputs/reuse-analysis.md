# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

This document details the Reuse Candidates identified in the task description and how each would be used during implementation.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL IN clause generation. It takes a raw query parameter string (e.g., `"MIT,Apache-2.0"`), splits it on commas, and generates the appropriate SQL `WHERE column IN (...)` clause for SeaORM queries.

**How it would be reused:** This function is reused **directly** in `modules/fundamental/src/package/service/mod.rs` when building the license filter query. Instead of writing custom parsing logic for the comma-separated `license` parameter, the service layer calls `apply_filter` with the raw license string and the target column reference (the license identifier column from the `package_license` join table). This handles both the single-value case (`?license=MIT` produces `WHERE license = 'MIT'`) and the multi-value case (`?license=MIT,Apache-2.0` produces `WHERE license IN ('MIT', 'Apache-2.0')`) without any new parsing code.

**Reuse type:** Direct invocation — no modifications to `apply_filter` are needed.

**Benefit:** Eliminates the need to write and test custom comma-separated value parsing. The function is already battle-tested across other endpoints (e.g., the advisory severity filter) and handles edge cases like trimming whitespace around values.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:** The advisory list endpoint already implements a query parameter filter (`severity`) using a pattern where:
1. The query parameter extraction struct has an optional field for the filter value.
2. The handler extracts the field and passes it to the corresponding service method.
3. The service method conditionally applies the filter to the database query using `apply_filter`.

This is structurally identical to the license filter needed for the package endpoint.

**How it would be reused:** This file serves as a **structural template** for the implementation. The exact same pattern is replicated in the package endpoint:

1. Add an `Option<String>` field named `license` to the query parameter struct in `modules/fundamental/src/package/endpoints/list.rs` — mirroring how `severity` is defined in the advisory query struct.
2. Extract the `license` value from the query parameters in the handler function — mirroring how the advisory handler extracts `severity`.
3. Pass the `license` value to `PackageService::list()` — mirroring how the advisory handler passes `severity` to `AdvisoryService::list()`.
4. In the service method, conditionally apply the filter when the parameter is `Some` — mirroring the advisory service's conditional severity filter logic.

**Reuse type:** Pattern replication — the advisory endpoint's code structure is followed but adapted for the package/license domain. No code is copied verbatim; instead, the same architectural pattern (optional query field -> handler extraction -> service filter application) is applied to the new domain.

**Benefit:** Ensures consistency with existing filter implementations in the codebase. Reduces design decisions — the pattern is proven and reviewed. Makes the codebase more uniform, which simplifies future maintenance and onboarding.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:** The existing SeaORM entity definition for the `package_license` join table, which maps packages to their declared licenses. This entity defines the table schema, column types, and relationships needed to query the package-license association.

**How it would be reused:** This entity is used **directly** in the database query within `PackageService::list()` to perform the JOIN between the `package` table and the `package_license` table when filtering by license. Instead of writing raw SQL for the join, the implementation uses SeaORM's relation-based query builder with this entity:

1. Import the `package_license` entity module.
2. In the list query, add a `.join()` clause referencing the `package_license` entity's relation to the `package` entity.
3. Apply the filter condition on the license column from the `package_license` entity using `apply_filter`.

**Reuse type:** Direct usage — the entity is imported and used in SeaORM query construction. No modifications to the entity definition are needed.

**Benefit:** Avoids writing raw SQL for the join, which would bypass SeaORM's type safety and query builder benefits. The entity already defines the correct column names, types, and relationships, eliminating the risk of typos or schema mismatches in hand-written SQL. It also means that if the `package_license` table schema changes in a migration, the entity update will surface compile-time errors in the filter query rather than runtime failures.

---

## Summary

| Reuse Candidate | Location | Reuse Type | What It Eliminates |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct invocation | Custom comma-separated value parsing and SQL IN clause generation |
| Advisory severity filter | `modules/fundamental/src/advisory/endpoints/list.rs` | Pattern replication | Design decisions for filter implementation structure |
| `package_license` entity | `entity/src/package_license.rs` | Direct usage | Raw SQL joins and manual schema references |

All three reuse candidates are explicitly listed in the task's Reuse Candidates section, and all three are appropriate for direct use. No additional reusable code was identified beyond what the task description specified — the three candidates fully cover the implementation needs without requiring any new shared utilities.
