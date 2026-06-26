# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Reuse Candidates from Task Description

The task's "Reuse Candidates" section identifies three candidates. All three are reused directly in the implementation plan. No new utility functions are created that would duplicate existing functionality.

---

### 1. `common/src/db/query.rs::apply_filter`

**What it provides:** Handles comma-separated multi-value query parameter parsing and SQL IN clause generation. Takes a raw query parameter string (e.g., `"MIT,Apache-2.0"`) and returns a parsed collection of individual values suitable for use in a SQL `IN` clause.

**How it is reused:**

- Called directly in `modules/fundamental/src/package/service/mod.rs` inside the `PackageService::list()` method.
- When the `license` query parameter is present (`Some`), the service passes the raw string to `apply_filter()`, which splits it by comma and returns the individual license identifiers.
- The returned values are fed directly into SeaORM's `.is_in()` filter method to construct the `WHERE license IN (...)` clause.
- No wrapper, adapter, or new utility is created around `apply_filter` — it is invoked exactly as the advisory severity filter uses it.

**Why reuse instead of reimplementing:** Writing custom comma-splitting and SQL clause generation would duplicate the logic already centralized in `query.rs`. The `apply_filter` function is the project's established pattern for multi-value query parameter handling, used by the advisory module and potentially others. Reusing it ensures consistent parsing behavior (handling edge cases like whitespace, empty segments) and reduces maintenance burden.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:** A structural reference implementation showing how to add an optional filter query parameter to a list endpoint. The advisory list endpoint's `severity` filter demonstrates the complete pattern: declaring an optional field in the `Query` struct, extracting it in the handler, passing it to the service layer, and using `apply_filter` to build the database filter.

**How it is reused:**

- The `Query` struct pattern is replicated in `modules/fundamental/src/package/endpoints/list.rs`: an `Option<String>` field named `license` is added alongside any existing query parameters, matching the structure of the advisory's `severity` field.
- The handler logic follows the same flow: extract the optional field from the deserialized query, pass it as `Option<&str>` to the service method.
- The service-layer integration follows the same pattern: check `if let Some(value) = filter`, call `apply_filter`, and chain the result into the query builder.
- This is structural reuse (following the same pattern) rather than code-level reuse (calling the same function). The advisory endpoint serves as a template that the package endpoint mirrors.

**Why reuse this pattern:** The advisory severity filter is described in the task's Implementation Notes as "structurally identical" to the needed license filter. Following the same pattern ensures consistency across list endpoints in the fundamental module, making the codebase predictable for future developers. Inventing a different approach (e.g., middleware-based filtering, a generic filter builder) would diverge from established conventions without justification.

---

### 3. `entity/src/package_license.rs` (package-license join entity)

**What it provides:** The SeaORM entity definition for the `package_license` join table, which maps packages to their declared licenses. Includes the entity struct, column definitions (with a `License` column for the SPDX identifier), and relation definitions (linking to the `package` table).

**How it is reused:**

- Used in `modules/fundamental/src/package/service/mod.rs` to build the JOIN query that connects packages to their licenses.
- The entity's `Relation::Package` definition is used with `.def().rev()` to set up the INNER JOIN from the package query to the package_license table, following SeaORM conventions.
- The entity's `Column::License` is used in the `.filter()` clause with `.is_in()` to filter by the parsed license values.
- No raw SQL is written — the entire JOIN and filter is expressed through SeaORM's entity and query builder API using the existing entity definition.

**Why reuse this entity:** The `package_license` entity already encapsulates the database schema for the package-to-license relationship, including column types and foreign key relations. Writing raw SQL JOINs would bypass the ORM's type safety and relation management, creating a maintenance liability if the schema evolves. Using the existing entity keeps the query consistent with how other parts of the codebase interact with the same table.

---

## Summary

| Reuse Candidate | Reuse Type | Used In | New Code Created |
|---|---|---|---|
| `apply_filter` (query.rs) | Direct function call | `package/service/mod.rs` | None — called as-is |
| Advisory severity filter pattern (list.rs) | Structural pattern | `package/endpoints/list.rs` | Query struct field + handler logic mirroring advisory pattern |
| `package_license` entity | ORM entity for JOIN | `package/service/mod.rs` | None — entity used directly in query builder |

No new utility functions, helper modules, or abstraction layers are proposed. All filtering and parsing logic leverages existing shared infrastructure (`apply_filter`) and domain entities (`package_license`). The only new code is the endpoint-specific wiring (query parameter extraction, service method parameter, and query builder chain) that connects these existing components for the license filter use case.
