# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document details how each of the three Reuse Candidates identified in the task
description would be applied during implementation. No new utility functions are
created that duplicate existing functionality (constraint 5.4).

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:**
`apply_filter` is a shared query builder helper that handles comma-separated
multi-value query parameter parsing and SQL `IN` clause generation. Given a raw
string like `"MIT,Apache-2.0"`, it splits on commas, trims whitespace from each
value, and produces the appropriate filter expression for use with SeaORM's query
builder (an `IN` clause when multiple values are present, or an equality check for
a single value).

**How it is reused:**
In `modules/fundamental/src/package/service/mod.rs`, the `PackageService::list`
method receives the raw `license` query parameter as an `Option<String>`. When the
value is `Some`, it is passed directly to `apply_filter` to obtain the parsed filter
values and the corresponding SQL condition. This filter condition is then applied to
the `package_license` table's license identifier column in the SeaORM query.

**Why no new parsing logic is written:**
`apply_filter` already implements the exact parsing behavior needed: splitting a
comma-separated string into individual values and generating an `IN` clause. Writing
a new function to parse `"MIT,Apache-2.0"` into `vec!["MIT", "Apache-2.0"]` would
directly duplicate `apply_filter`'s functionality. By reusing `apply_filter`, the
implementation stays consistent with every other multi-value filter in the codebase
and avoids duplication (constraint 5.4).

**Call site:**
```rust
// In PackageService::list(), when license filter is provided:
use common::db::query::apply_filter;

if let Some(license_param) = license {
    let filter = apply_filter(&license_param);
    // Apply filter to the query on package_license::Column::LicenseId
    query = query.filter(package_license::Column::LicenseId.is_in(filter));
}
```

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:**
The advisory list endpoint implements a `severity` query parameter filter using a
Query struct pattern. The endpoint defines a `Query` struct with optional filter
fields (including `severity: Option<String>`), deserializes query parameters into
this struct via Axum's query extractor, and passes the filter values down to the
service layer for SQL query construction. This is the established pattern for adding
optional filters to list endpoints throughout the codebase.

**How it is reused:**
The advisory list endpoint serves as the structural guide for the package list
endpoint changes. Specifically:

1. **Query struct pattern:** The package list endpoint's Query struct in
   `modules/fundamental/src/package/endpoints/list.rs` is extended with a
   `license: Option<String>` field, mirroring how the advisory endpoint has
   `severity: Option<String>`.

2. **Handler flow:** The handler function follows the same flow as the advisory
   handler: extract the Query struct from the request, pass the optional filter
   value to the service method, and return the paginated results unchanged.

3. **Validation pattern:** Input validation for the license parameter follows the
   same approach used by the advisory endpoint for severity validation -- checking
   for empty or malformed values and returning `AppError` (which maps to 400 Bad
   Request).

**What is NOT copied:**
The advisory endpoint's domain-specific logic (severity enum matching, advisory-specific
joins) is not copied. Only the structural pattern -- Query struct with optional field,
handler extraction flow, service delegation -- is followed.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:**
The `package_license` entity is an existing SeaORM entity definition that maps the
`package_license` database table. This table represents the many-to-many relationship
between packages and their declared licenses. The entity defines the table's columns
(including the package ID foreign key and the license identifier), its relationships
to the `package` entity, and the SeaORM model and active model types needed for
query construction.

**How it is reused:**
In `modules/fundamental/src/package/service/mod.rs`, the license filter query uses
the `package_license` entity to construct a JOIN between the `package` table and the
`package_license` table. This is done entirely through SeaORM's query builder API
using the entity's column and relation definitions:

1. **JOIN construction:** The query joins `package` to `package_license` using the
   relationship defined in the `package_license` entity (or via SeaORM's
   `JoinType::InnerJoin` with explicit column matching).

2. **Filter application:** The `IN` clause produced by `apply_filter` (Reuse
   Candidate 1) is applied to `package_license::Column::LicenseId`, which is a
   typed column reference provided by the entity.

3. **No raw SQL:** Because the entity already defines the table structure, column
   names, and relationships, no raw SQL strings are needed for the JOIN or filter.
   The entire query is expressed through SeaORM's type-safe API.

**Why a new entity is NOT created:**
The `package_license` entity already exists and correctly models the join table. Creating
a new entity or writing raw SQL to achieve the same join would duplicate the existing
schema definition and bypass SeaORM's type safety guarantees.

**Illustrative query construction:**
```rust
use entity::package_license;

// Join package to package_license and filter on license identifier
let query = Package::find()
    .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
    .filter(package_license::Column::LicenseId.is_in(filter_values))
    .paginate(db, page_size);
```

---

## Summary Table

| Reuse Candidate | Source File | Used In | Purpose |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | `package/service/mod.rs` | Parse comma-separated license values and generate SQL IN clause |
| Advisory list filter pattern | `advisory/endpoints/list.rs` | `package/endpoints/list.rs` | Structural guide for Query struct, handler flow, and validation |
| `package_license` entity | `entity/src/package_license.rs` | `package/service/mod.rs` | JOIN table entity for filtering packages by license |

All three Reuse Candidates are applied. No new utility functions are created that
duplicate existing functionality.
