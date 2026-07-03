# Reuse Analysis for TC-9203: Add package license filter to list endpoint

## Overview

The task description identifies three Reuse Candidates. All three are reused directly in the implementation -- no new utility functions are created that would duplicate existing functionality.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. It accepts a string value (e.g., `"MIT,Apache-2.0"`), splits it on commas, and constructs the appropriate SeaORM filter condition -- a single equality check for one value, or an `IN` clause for multiple values.

**How it is reused:** In `modules/fundamental/src/package/service/mod.rs`, when the `license` parameter is `Some(value)`, the service calls `apply_filter` directly with the raw license string from the query parameter. This handles all the parsing and SQL generation without writing any new string-splitting or clause-building logic.

**Why reuse instead of writing new code:** Writing a custom comma-split-and-filter function would directly duplicate what `apply_filter` already does. The function is designed for exactly this use case -- it lives in `common/src/db/` as a shared query helper. Using it ensures consistent behavior with other filters across the codebase and avoids introducing a second code path for the same operation.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** The advisory list endpoint implements a `severity` query parameter filter that is structurally identical to the license filter needed here. It demonstrates the established pattern for adding optional query parameters to list endpoints: a Query struct with an optional field, deserialization by Axum, passing the value to the service layer, and conditional filter application.

**How it is reused:** This file serves as the structural template for the changes to `modules/fundamental/src/package/endpoints/list.rs`. Specifically:

1. **Query struct pattern**: The advisory endpoint defines a Query struct (or equivalent) with `pub severity: Option<String>`. The package endpoint replicates this with `pub license: Option<String>`.
2. **Handler flow**: The advisory handler extracts `query.severity` and passes it to `AdvisoryService::list()`. The package handler follows the same flow, extracting `query.license` and passing it to `PackageService::list()`.
3. **Service integration**: The advisory service conditionally applies the severity filter when the parameter is present. The package service follows the same conditional pattern for the license filter.

**Why reuse this pattern:** The advisory severity filter is the closest sibling implementation in the codebase. Following the same pattern ensures consistency across the `fundamental` module's list endpoints, makes the code reviewable by comparison, and adheres to the project's convention conformance requirements. Inventing a different approach would break the established module pattern.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:** The `package_license` entity is a SeaORM entity definition that maps the `package_license` database table -- the join table between packages and their declared licenses. It defines the table's columns (including the license SPDX identifier and the foreign key to the package table) and the SeaORM `Relation` definitions needed for JOIN queries.

**How it is reused:** In `modules/fundamental/src/package/service/mod.rs`, the license filter query uses the `package_license` entity to construct a SeaORM JOIN between the `package` table and the `package_license` table. Specifically:

1. **JOIN construction**: The query joins `package` to `package_license` using the entity's defined relations, rather than writing raw SQL JOIN clauses.
2. **Column reference**: The filter condition references the license column through the entity's column enum (e.g., `package_license::Column::License`), ensuring type safety and compile-time verification.
3. **Foreign key traversal**: The entity's `Relation` definitions provide the join condition automatically, so the service code does not need to manually specify the foreign key columns.

**Why reuse this entity:** The `package_license` entity already exists and encapsulates the table schema and relationships. Using it provides type-safe column references, automatic join condition generation, and consistency with how other parts of the codebase query this table. Writing raw SQL for the join would bypass SeaORM's type system and diverge from the project's ORM-based query convention.

---

## Summary

| Reuse Candidate | Location | Role in Implementation | Avoids Duplicating |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Parses comma-separated license values and generates SQL IN clause | Custom string splitting and filter clause building |
| Advisory severity filter | `modules/fundamental/src/advisory/endpoints/list.rs` | Structural template for query struct, handler flow, and service integration | Inventing a new endpoint filter pattern |
| `package_license` entity | `entity/src/package_license.rs` | Provides typed JOIN and column references for the license filter query | Raw SQL joins and manual column references |
