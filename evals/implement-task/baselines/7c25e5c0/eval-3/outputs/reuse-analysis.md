# Reuse Analysis — TC-9203

## Reuse Candidates Evaluation

The task description lists 3 Reuse Candidates. All 3 are reused in the implementation plan. No new utility functions are created that would duplicate existing functionality.

### 1. `common/src/db/query.rs::apply_filter`

**What it provides:** Handles comma-separated multi-value query parameter parsing and SQL IN clause generation. When given a string like `"MIT,Apache-2.0"`, it splits on commas and generates a `WHERE column IN ('MIT', 'Apache-2.0')` clause.

**How it is reused:** Called directly in `PackageService::list()` (in `modules/fundamental/src/package/service/mod.rs`) to process the `license` query parameter. Instead of writing new parsing logic to split comma-separated values and build SQL filters, I pass the raw query parameter string to `apply_filter`, which handles:
- Splitting the comma-separated string into individual values
- Generating the appropriate SQL IN clause
- Handling the single-value case (no comma) as a simple equality filter

**Why reuse over new code:** `apply_filter` already handles all the edge cases for multi-value parameter parsing. Writing new parsing logic would duplicate this functionality and risk introducing inconsistencies (e.g., different whitespace handling, different escaping). This directly follows constraint §5.4 — no duplication of existing filtering logic.

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` — Severity filter pattern

**What it provides:** A structural template for implementing optional query parameter filters. The advisory list endpoint's severity filter follows this pattern:
1. Define an optional field in the `Query` struct: `severity: Option<String>`
2. Extract the field from query parameters via `serde::Deserialize`
3. Pass the filter value to the service method
4. In the service, conditionally apply the filter using `apply_filter`

**How it is reused:** The license filter in `package/endpoints/list.rs` follows the exact same structural pattern:
1. Add `license: Option<String>` to the existing `Query` struct
2. Serde deserializes it from the query string automatically
3. Pass `query.license` to `PackageService::list()` as a new parameter
4. In the service method, use `apply_filter` to apply the filter when present

**Why reuse over new code:** Following the established pattern ensures consistency across endpoints. The advisory severity filter is structurally identical to the license filter needed here — same optional parameter extraction, same pass-through to service, same `apply_filter` usage. Inventing a different approach would introduce unnecessary inconsistency.

### 3. `entity/src/package_license.rs` — Package-License entity

**What it provides:** The SeaORM entity representing the package-license join table in the database. It defines the columns (package_id, license_id/spdx_identifier) and relations needed to join packages to their declared licenses.

**How it is reused:** Used in `PackageService::list()` to construct the JOIN query that filters packages by license. Instead of writing raw SQL or creating a new entity, the existing `package_license` entity provides:
- Column definitions for the join table
- Relation definitions that SeaORM uses to generate JOIN clauses
- Type-safe query building via SeaORM's query builder API

**Why reuse over new code:** The join table entity already exists and correctly maps the database schema. Writing raw SQL would bypass SeaORM's type safety, and creating a new entity would duplicate the existing mapping. Using the existing entity ensures the query stays in sync with the database schema.

## Summary

| Reuse Candidate | Decision | Rationale |
|---|---|---|
| `apply_filter` from `query.rs` | **Reuse directly** | Handles all multi-value parameter parsing; no new parsing logic needed |
| Advisory severity filter pattern in `list.rs` | **Follow as structural template** | Identical filter pattern ensures cross-endpoint consistency |
| `package_license` entity | **Use for JOIN query** | Existing entity maps the join table; no raw SQL or new entity needed |

No new utility functions are proposed that would duplicate the functionality of `apply_filter`. All filtering logic flows through the existing shared helper.
