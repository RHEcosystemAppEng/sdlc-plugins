# Reuse Analysis — TC-9203

## Reuse Candidates Evaluation

The task description lists 3 Reuse Candidates. Each is analyzed below with the decision on how it will be applied.

---

### 1. `common/src/db/query.rs::apply_filter`

**What it does**: Handles comma-separated multi-value query parameter parsing and generates SQL `IN` clause expressions. Given a string like `"MIT,Apache-2.0"`, it splits on commas, trims whitespace, and produces the appropriate SeaORM filter condition.

**Reuse decision**: **Reuse directly** — call `apply_filter` in `PackageService::list` to process the `license` query parameter value. This handles both single-value (`license=MIT`) and multi-value (`license=MIT,Apache-2.0`) cases without writing any new parsing logic.

**How it will be applied**: In `modules/fundamental/src/package/service/mod.rs`, when the `license` parameter is `Some(value)`, pass the value and the target column (the license SPDX identifier column from the package_license join) to `apply_filter`. The function returns a SeaORM `Condition` that is added to the query builder. No new utility functions are created that would duplicate `apply_filter`'s functionality.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it does**: The advisory list endpoint implements a `severity` query parameter filter using a `Query` struct with an optional field, which is deserialized from URL query parameters and passed to the service layer. This is the structural template for how list-endpoint filters are implemented across the codebase.

**Reuse decision**: **Follow as structural guide** — replicate the same pattern (Query struct with optional filter field → extract in handler → pass to service) for the license filter in the package list endpoint. This is not code-level reuse (we don't import from advisory), but architectural pattern reuse ensuring consistency across modules.

**How it will be applied**: In `modules/fundamental/src/package/endpoints/list.rs`:
- Add `license: Option<String>` to the existing `Query` struct, matching the same serde attributes used for the severity field in the advisory Query struct
- In the handler function, extract `query.license` and pass it to `PackageService::list()` as an additional parameter
- Follow the same control flow: check if the filter is `Some`, then apply via `apply_filter`

---

### 3. `entity/src/package_license.rs` (package-license entity)

**What it does**: SeaORM entity definition for the package-license mapping table. Defines the schema for the join table that connects packages to their declared licenses, including the SPDX license identifier column.

**Reuse decision**: **Reuse for JOIN query** — use this existing entity to construct the join between the package table and the license data rather than writing raw SQL or creating a new entity.

**How it will be applied**: In `modules/fundamental/src/package/service/mod.rs`, when the license filter is active:
- Use `package_license::Entity` to construct a SeaORM `JoinType::InnerJoin` from the package table to the package_license table
- Apply the filter condition (from `apply_filter`) against the license identifier column defined in this entity
- This avoids writing raw SQL joins and ensures the query benefits from SeaORM's type safety and the entity's existing column definitions

---

## Summary

| Reuse Candidate | Reuse Type | Rationale |
|---|---|---|
| `common/src/db/query.rs::apply_filter` | Direct function call | Handles comma-separated parsing and IN clause generation — no new parsing logic needed |
| `advisory/endpoints/list.rs` severity filter | Structural pattern guide | Ensures the license filter follows the established Query struct → handler → service pattern |
| `entity/src/package_license.rs` | Entity for JOIN query | Provides type-safe join table access — no raw SQL or new entities required |

No new utility functions or helpers are created. All filtering logic is delegated to existing code (`apply_filter`) and existing data access patterns (`package_license` entity).
