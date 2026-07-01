# Reuse Analysis for TC-9203: Add package license filter to list endpoint

## Overview

The task description provides three Reuse Candidates. All three are directly applicable and must be used during implementation. No new utility functions need to be created -- the existing codebase already provides all necessary building blocks.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** A shared utility function that handles comma-separated multi-value query parameter parsing and SQL IN clause generation.

**How it will be reused:** Called directly from `modules/fundamental/src/package/service/mod.rs` when constructing the license filter query.

**Specific usage:**
- When `PackageService::list` receives a `license: Option<String>` parameter with a value like `"MIT,Apache-2.0"`, it passes this string to `apply_filter`.
- `apply_filter` parses the comma-separated string into individual values (`["MIT", "Apache-2.0"]`) and generates the appropriate SQL `WHERE ... IN (...)` clause.
- This eliminates the need to write any custom comma-parsing or SQL IN clause generation logic.

**Why reuse is mandatory:** The task's Implementation Notes explicitly state: "Use the `query.rs` helpers in `common/src/db/query.rs` for building the filter -- specifically the `apply_filter` function which handles both single and multi-value comma-separated parameters." Writing a custom parser or IN clause builder would duplicate this existing, tested functionality.

**No modifications needed:** `apply_filter` is used as-is. Its existing interface accepts a string value and generates the appropriate filter clause, which is exactly what the license filter requires.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:** A structurally identical implementation of an optional query parameter filter on a list endpoint. The advisory list endpoint supports a `severity` query parameter using a Query struct with an optional field.

**How it will be reused:** The pattern (not the code itself) is followed to implement the license filter in `modules/fundamental/src/package/endpoints/list.rs`.

**Specific pattern elements to replicate:**
1. **Query struct**: The advisory endpoint defines a Query struct (e.g., `#[derive(Deserialize)] struct Query { severity: Option<String>, ... }`). The package endpoint's Query struct will add an identical `license: Option<String>` field following the same derive macros and field conventions.
2. **Handler extraction**: The advisory handler extracts `query.severity` from the deserialized query parameters and passes it to the service layer. The package handler will extract `query.license` in the same way.
3. **Service call pattern**: The advisory handler passes the filter value to `AdvisoryService::list`. The package handler will pass the license filter to `PackageService::list` using the same calling convention.

**Why reuse is mandatory:** The task's Implementation Notes state: "Follow the existing filter pattern in `modules/fundamental/src/advisory/endpoints/list.rs` -- the advisory list endpoint already supports a `severity` query parameter using the same filtering approach." Inventing a different pattern would violate convention conformance and create inconsistency across endpoints.

**No code duplication:** This is pattern reuse (following the same structural approach), not code copying. The advisory endpoint code stays unchanged; the package endpoint adopts the same conventions.

---

## Reuse Candidate 3: `entity/src/package_license.rs` (package-license join entity)

**What it provides:** An existing SeaORM entity that maps the `package_license` database table, which joins packages to their declared licenses. Includes column definitions, relations, and primary key configuration.

**How it will be reused:** Used in `modules/fundamental/src/package/service/mod.rs` to construct the JOIN query that filters packages by license.

**Specific usage:**
- When building the filter query in `PackageService::list`, use the `package_license::Entity` to join from the `package` table to the `package_license` table.
- Use `package_license::Column::LicenseId` (or equivalent column name) in the WHERE clause to filter by the license SPDX identifiers parsed by `apply_filter`.
- Use the SeaORM `Relation` definitions in `package_license.rs` to construct the join rather than writing raw SQL JOIN statements.

**Why reuse is mandatory:** The task's Implementation Notes state: "The `package_license` entity in `entity/src/package_license.rs` maps packages to licenses -- join through this table when filtering." Writing raw SQL or creating a new entity would duplicate this existing mapping and bypass SeaORM's type-safe query construction.

**No modifications needed:** The entity already exists with the necessary columns and relations. It is used as a query building block, not modified.

---

## Summary

| Reuse Candidate | Location | Usage Type | Modified? |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct function call for comma-separated parsing and IN clause | No |
| Severity filter pattern | `modules/fundamental/src/advisory/endpoints/list.rs` | Structural pattern for Query struct and handler flow | No (pattern only) |
| `package_license` entity | `entity/src/package_license.rs` | SeaORM entity for JOIN query construction | No |

**New utility functions created:** None. All required functionality is covered by existing code.

**Duplicated logic:** None. The implementation exclusively reuses existing utilities (`apply_filter`), follows established patterns (advisory severity filter), and leverages existing entities (`package_license`).
