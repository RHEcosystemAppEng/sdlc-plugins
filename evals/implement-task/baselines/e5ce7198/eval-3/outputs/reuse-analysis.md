# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Overview

The task description identifies three reuse candidates. All three should be reused directly to avoid duplicating existing logic and to maintain consistency with established patterns in the codebase.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source:** `common/src/db/query.rs`

**What it provides:** The `apply_filter` function is a shared query builder helper that handles comma-separated multi-value query parameter parsing and generates SQL `IN` clause conditions for SeaORM queries. It takes a raw query string value (e.g., `"MIT,Apache-2.0"`), splits it on commas, and produces the appropriate `ColumnFilter::IsIn(...)` condition.

**How we reuse it:** In `modules/fundamental/src/package/service/mod.rs`, when the `license` parameter is `Some(value)`, call `apply_filter` directly with the license column from the `package_license` entity and the raw comma-separated string. This handles both the single-value case (`"MIT"` produces an equality check or single-element IN) and the multi-value case (`"MIT,Apache-2.0"` produces `IN ('MIT', 'Apache-2.0')`).

**Why reuse instead of reimplementing:** Writing custom comma-splitting and IN-clause generation would duplicate logic that already exists, is tested, and handles edge cases (trimming whitespace, empty segments). Using `apply_filter` keeps the codebase DRY and ensures consistent behavior across all list endpoints that support filtering.

---

## Reuse Candidate 2: Severity filter pattern from `modules/fundamental/src/advisory/endpoints/list.rs`

**Source:** `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** The advisory list endpoint already implements a structurally identical filter pattern for the `severity` query parameter. This includes:
1. A query parameter struct with an `Option<String>` field for the filter value
2. Extraction logic in the handler that reads the optional field
3. Forwarding the filter value to the service layer
4. The service layer conditionally applying the filter via `apply_filter` when the value is present

**How we reuse it:** Follow the same structural pattern in the package module:
- In `modules/fundamental/src/package/endpoints/list.rs`: Add `license: Option<String>` to the endpoint's Query struct, mirroring how `severity: Option<String>` is defined in the advisory Query struct.
- In the handler function: Extract `query.license` and pass it to `PackageService::list`, following the same conditional forwarding pattern the advisory handler uses for `query.severity`.
- In `modules/fundamental/src/package/service/mod.rs`: Accept the optional license parameter and conditionally apply the filter, following the same pattern as `AdvisoryService::list` applies the severity filter.

**Why reuse instead of reimplementing:** The severity filter and license filter are structurally identical — both are optional string parameters that filter a list endpoint by matching values in a related table. Following the established pattern ensures architectural consistency, makes the code predictable for other developers, and avoids inventing a new filtering approach when a proven one already exists. We do NOT duplicate the filtering logic; we follow the same pattern and delegate to the same shared `apply_filter` function.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Source:** `entity/src/package_license.rs`

**What it provides:** The existing SeaORM entity that maps the `package_license` database table. This table represents the many-to-many relationship between packages and their declared licenses. The entity defines the table columns (including package ID, license identifier), relations to the `package` entity, and SeaORM model/ActiveModel types.

**How we reuse it:** In `modules/fundamental/src/package/service/mod.rs`, use this entity to construct the JOIN when filtering:
- Add a `join(JoinType::InnerJoin, ...)` to the package query that joins through `package_license` on the package ID.
- Apply the filter condition (from `apply_filter`) on the `package_license::Column::License` (or equivalent license identifier column).
- This uses SeaORM's type-safe relation API rather than raw SQL strings.

**Why reuse instead of reimplementing:** The entity already exists and correctly maps the database schema. Writing raw SQL joins would bypass SeaORM's type safety, skip its relation definitions, and create a maintenance burden if the schema changes. Using the entity ensures the join is schema-aware and benefits from compile-time checking.

---

## Summary Table

| Reuse Candidate | Location | Reuse Type | Used In |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct function call | `package/service/mod.rs` — parse comma-separated license values and generate filter condition |
| Severity filter pattern | `advisory/endpoints/list.rs` | Structural pattern | `package/endpoints/list.rs` — Query struct field, handler extraction, service forwarding |
| `package_license` entity | `entity/src/package_license.rs` | Direct entity usage | `package/service/mod.rs` — JOIN for filtering packages by license |

## What we avoid duplicating

- No custom comma-splitting logic — `apply_filter` handles this.
- No raw SQL for the package-license join — the `package_license` entity provides SeaORM relations.
- No novel filter pattern — the advisory severity filter is the proven template.
