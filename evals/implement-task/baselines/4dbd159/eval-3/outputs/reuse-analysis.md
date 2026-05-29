# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Overview

The task description identifies three Reuse Candidates. All three are used in the
implementation plan. No new filtering, parsing, or query-building logic is written;
the implementation composes existing building blocks following an established pattern.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:**
The `apply_filter` function is a shared query-builder helper that handles optional filter
parameters. It parses comma-separated multi-value strings, generates SQL `IN` clauses for
multi-value inputs, and generates simple equality conditions for single-value inputs. When
the input is `None`, it skips the filter entirely.

**How it is reused:**
The license filter calls `apply_filter` directly in both the endpoint handler
(`modules/fundamental/src/package/endpoints/list.rs`) and the service layer
(`modules/fundamental/src/package/service/mod.rs`) to process the `license` query parameter.
This eliminates the need to write any custom parsing logic for comma-separated license
values or to manually construct SQL `IN` clauses.

**Reuse type:** Direct invocation — no modification or extension of `apply_filter` is needed.

**What would happen without reuse:**
Without `apply_filter`, the implementation would need to:
1. Parse the `license` string, splitting on commas
2. Trim whitespace from each value
3. Conditionally build either an equality or IN clause depending on the number of values
4. Handle the `None` case (no filter parameter provided)

All of this logic already exists in `apply_filter` and is battle-tested across other
endpoints (e.g., advisory severity filter). Duplicating it would introduce maintenance
burden and risk inconsistent behavior across filter parameters.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:**
The advisory list endpoint implements a severity filter using a pattern that is structurally
identical to the license filter needed here. The pattern consists of:
1. A `Query` struct with `#[derive(Deserialize)]` containing an `Option<String>` field for the filter
2. Axum automatic extraction of the Query struct from URL query parameters
3. A call to `apply_filter` passing the optional field and the target column
4. The service layer receiving the filter and incorporating it into the SeaORM query

**How it is reused:**
The implementation follows this pattern exactly for the license filter:
- The `Query` struct in `package/endpoints/list.rs` gains a `license: Option<String>` field,
  mirroring the `severity: Option<String>` field in the advisory Query struct
- The handler applies the filter using the same `apply_filter` call pattern
- The service method extends its query in the same way the advisory service does

**Reuse type:** Structural pattern replication — the advisory endpoint serves as the
template, and the package endpoint follows the same architecture. No code is copied
verbatim; instead, the same design pattern is applied to a different domain entity.

**What would happen without reuse:**
Without following this established pattern, the implementation might:
- Invent a different struct layout or extraction mechanism
- Place filter logic in a different layer (e.g., middleware instead of handler)
- Use a different approach to optional parameter handling

This would create inconsistency across endpoints, making the codebase harder to navigate
and maintain. Following the proven pattern ensures that developers familiar with one
filter endpoint can immediately understand all others.

---

## Reuse Candidate 3: `entity/src/package_license.rs` (package-license entity)

**What it provides:**
The `package_license` entity is a SeaORM entity definition for the package-license join
table. It maps the relationship between packages and their declared licenses, providing:
- Column definitions (including the `License` column containing the SPDX identifier)
- Relation definitions linking back to the `package` entity
- SeaORM model and ActiveModel types for type-safe queries

**How it is reused:**
The implementation uses this entity to build the JOIN clause when the license filter is
active. Instead of writing raw SQL joins, the code uses SeaORM's `.join()` method with
the `package_license` entity's relation definitions:
- In the service layer, when `license` is `Some(...)`, the query joins `package` to
  `package_license` using the entity's defined relation
- The `package_license::Column::License` column is used as the target for the
  `apply_filter` condition
- The entity's type-safe column references prevent typos and column name mismatches

**Reuse type:** Direct usage of existing entity — no modification to the entity is needed.
The join table and its columns already exist; the filter simply queries against them.

**What would happen without reuse:**
Without the `package_license` entity, the implementation would need to:
1. Write raw SQL or use string-based column references for the join, losing type safety
2. Manually specify the join condition (foreign key relationships), risking errors
3. Potentially duplicate the table/column definitions that already exist in the entity

Using the existing entity ensures the filter query stays consistent with the database
schema and benefits from any future schema changes propagated through SeaORM's entity
definitions.

---

## Summary Table

| Reuse Candidate | Location | Reuse Type | Custom Code Avoided |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct invocation | Comma parsing, IN clause generation, None handling |
| Severity filter pattern | `advisory/endpoints/list.rs` | Structural pattern replication | Query struct design, handler flow, service integration |
| `package_license` entity | `entity/src/package_license.rs` | Direct entity usage | Raw SQL joins, manual column references, FK specification |

## Conclusion

All three Reuse Candidates listed in the task description are used. The implementation
introduces zero new utility functions or query-building helpers. The only new code
consists of:
1. A new `license` field on the existing `Query` struct (one line)
2. An `apply_filter` call in the handler (one line, reusing the existing function)
3. A conditional JOIN through `package_license` in the service (a few lines, reusing the existing entity)
4. Integration tests in a new test file (new code, but following established test patterns from sibling files)

No duplicated logic is introduced.
