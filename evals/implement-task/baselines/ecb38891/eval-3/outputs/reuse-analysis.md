# Reuse Analysis: TC-9203 -- Package License Filter

## Overview

The task description includes three Reuse Candidates. This document details how each
candidate is applied in the implementation, confirming that no existing logic is
duplicated.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** The `apply_filter` function handles comma-separated multi-value query
parameter parsing and SQL IN clause generation. Given a filter string like `"MIT,Apache-2.0"`,
it splits on commas, produces the correct SQL `WHERE column IN (...)` clause, and handles
the single-value case (`"MIT"`) as a simple `WHERE column = ...` equality check.

**How it is reused:** The license filter calls `apply_filter` directly to process the
`license` query parameter value. This is invoked in `PackageService::list` (in
`modules/fundamental/src/package/service/mod.rs`) when constructing the database query.

**Why reuse instead of new code:** Writing a new parsing or filtering function would
duplicate the exact behavior that `apply_filter` already provides. The function is a
shared utility in the `common` crate specifically designed for this pattern. Creating a
new utility function for license filtering would violate the DRY principle and diverge
from the established pattern used by other endpoints (e.g., the advisory severity filter).
Therefore, **no new utility functions are created that duplicate `apply_filter`
functionality**.

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** The advisory list endpoint implements a severity filter using a
pattern that is structurally identical to what the license filter needs:
1. An optional field in the `Query` struct for deserialization from query parameters
2. Extraction of the filter value in the endpoint handler
3. Pass-through of the filter value to the service layer
4. Application of the filter in the service's database query using `apply_filter`

**How it is reused:** The license filter implementation in
`modules/fundamental/src/package/endpoints/list.rs` follows this exact same pattern.
The advisory severity filter serves as the structural guide:
- The `Query` struct in the package list endpoint gets an `Option<String>` field for
  `license`, mirroring how advisory's `Query` struct has an optional `severity` field
- The handler extracts and passes the filter value identically
- The service layer applies the filter using the same `apply_filter` call pattern

**Why reuse instead of new code:** Following the established pattern ensures consistency
across the codebase's list endpoints. Inventing a different filtering architecture would
create maintenance burden and confuse developers familiar with the advisory pattern.

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:** The `package_license` SeaORM entity represents the join table
mapping packages to their SPDX license identifiers. It includes:
- Column definitions for the join table
- SeaORM relation definitions linking to the `package` entity
- The necessary schema for constructing JOIN queries via SeaORM's type-safe API

**How it is reused:** In `PackageService::list` (in
`modules/fundamental/src/package/service/mod.rs`), when a license filter is present, the
query joins through the `package_license` entity using SeaORM's relation-based join API
(e.g., `find().join(JoinType::InnerJoin, package_license::Relation::Package.def())`).
The filter is then applied to `package_license.license` column.

**Why reuse instead of new code:** The entity already defines the schema and relations
needed for the join. Writing raw SQL or creating a new entity for the same join table
would duplicate the existing definition and bypass SeaORM's type safety. The existing
entity ensures that any future schema changes to the package-license mapping are reflected
in one place.

## Summary

All three Reuse Candidates from the task description are applied in the implementation:

| Reuse Candidate | Used For | Alternative Avoided |
|---|---|---|
| `apply_filter` from `query.rs` | Comma-separated parameter parsing and SQL IN clause | Writing new parsing/filtering utility functions |
| Advisory `list.rs` severity pattern | Structural template for endpoint + service flow | Inventing a different filtering architecture |
| `package_license.rs` entity | JOIN query for license-to-package mapping | Raw SQL or duplicate entity definition |

No existing filtering, parsing, or entity logic is duplicated. The implementation extends
the existing patterns rather than creating parallel implementations.
