# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Reuse Candidates from Task

The task specifies three reuse candidates. All three are adopted in the implementation plan.

---

### 1. `common/src/db/query.rs::apply_filter`

**What it provides:** A shared utility function that parses comma-separated multi-value query parameter strings and generates SQL `IN` clause conditions. It handles both single-value (`"MIT"`) and multi-value (`"MIT,Apache-2.0"`) inputs uniformly.

**How it is reused:** Called directly in `PackageService::list()` (in `modules/fundamental/src/package/service/mod.rs`) when the `license` parameter is present. Instead of writing custom parsing/splitting logic for comma-separated values or manually constructing SQL filter conditions, the implementation passes the raw license query string to `apply_filter`, which handles:
- Splitting on commas
- Trimming whitespace
- Generating the appropriate `WHERE ... IN (...)` clause

**Benefit:** Zero duplication of filtering logic. The same function is already used by the advisory severity filter, so behavior is consistent across endpoints. Any future improvements to `apply_filter` (e.g., escaping, normalization) automatically apply to the license filter as well.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** A complete, working example of the query-parameter-to-filter pattern used throughout the codebase. Specifically, the advisory list endpoint defines a `Query` struct with an optional `severity: Option<String>` field, extracts it from the request's query parameters via Axum's `Query` extractor, and passes it to `AdvisoryService::list()` for filtering.

**How it is reused:** The license filter implementation follows this pattern structurally:
- The `Query` struct in `modules/fundamental/src/package/endpoints/list.rs` gains an `pub license: Option<String>` field, mirroring how advisory has `pub severity: Option<String>`.
- The handler function extracts `query.license` and passes it to `PackageService::list()`, mirroring how advisory passes `query.severity` to `AdvisoryService::list()`.
- Validation and error-handling follow the same flow (returning `AppError` for bad input).

**Benefit:** Structural consistency across the codebase. Developers familiar with any one list endpoint can immediately understand the license filter. No new patterns or abstractions are introduced.

---

### 3. `entity/src/package_license.rs`

**What it provides:** The SeaORM entity definition for the `package_license` join table, which maps packages to their declared licenses. Contains the `Entity`, `Model`, `Column`, and `Relation` definitions needed for type-safe queries.

**How it is reused:** Used in `PackageService::list()` to build the JOIN from the `package` table to `package_license` when filtering by license:
- `package_license::Entity` is used to express the JOIN relationship.
- `package_license::Column::PackageId` joins to `package::Column::Id`.
- `package_license::Column::License` is the column filtered by `apply_filter`.

**Benefit:** Avoids raw SQL. The existing entity already encodes the table schema, column names, and relationships. Using it ensures the query is type-checked at compile time and stays in sync with any future migrations that alter the table.

---

## Summary

| Reuse Candidate | Location | Reuse Type | Duplication Avoided |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct function call | Comma-separated parsing, SQL IN clause generation |
| Advisory list endpoint | `modules/fundamental/src/advisory/endpoints/list.rs` | Structural pattern (follow same design) | Query struct design, handler flow, service call pattern |
| `package_license` entity | `entity/src/package_license.rs` | Direct entity usage (JOIN + filter) | Raw SQL, manual column references, schema drift risk |

All three candidates are integral to the implementation. No new filtering utilities, query patterns, or entity definitions need to be created. The implementation composes existing building blocks to deliver the feature.
