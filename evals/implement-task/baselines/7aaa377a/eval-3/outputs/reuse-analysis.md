# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Reuse Candidates from Task Description

The task description lists three Reuse Candidates. All three are adopted for the
implementation. No candidate is duplicated or reimplemented from scratch.

---

### 1. `common/src/db/query.rs::apply_filter`

**What it provides:**
Handles comma-separated multi-value query parameter parsing and SQL IN clause
generation. This is a shared utility already used by other endpoints in the codebase.

**How it will be reused:**
- **Direct reuse** — call `apply_filter` from the `PackageService::list()` method
  when the `license` query parameter is present.
- Pass the raw `license` string (e.g., `"MIT,Apache-2.0"`) to `apply_filter`, which
  will split on commas, trim whitespace, and produce the SQL `IN` clause.
- No modifications to `apply_filter` are needed — it already supports the exact
  usage pattern required (single-value degrades to `= ?`, multi-value produces
  `IN (?, ?, ...)`).

**Reuse decision rationale:**
`common` is already a dependency of `modules/fundamental` (it provides
`PaginatedResults`, `AppError`, and other shared types). No new dependency is
introduced. Following the "Reuse over duplication" principle (Skill Step 6), since
the dependency already exists, reusing the function directly is correct.

**Alternative considered:**
Writing inline comma-splitting and SQL generation logic in the service layer.
Rejected because `apply_filter` already does this correctly, handles edge cases
(empty strings, whitespace), and is tested. Duplicating it would violate DRY and
risk inconsistency with how other endpoints handle multi-value filters.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:**
The advisory list endpoint implements a `severity` query parameter filter using the
same structural pattern needed for the license filter: an optional field on a `Query`
struct, extraction from the request, and delegation to the service layer.

**How it will be reused:**
- **Structural pattern reuse** — follow the identical Query struct pattern with an
  optional `license: Option<String>` field, mirroring how the advisory endpoint
  declares `severity: Option<String>`.
- Match the handler's flow: extract the query parameter, validate it, and pass it to
  the service method as an additional parameter.
- Match the service-level integration pattern: how the advisory service applies the
  severity filter informs how the package service should apply the license filter.

**Reuse decision rationale:**
This is convention conformance — the advisory filter is the established pattern in
this codebase for adding query parameter filters to list endpoints. Inventing a
different approach would break consistency and make the codebase harder to maintain.
The Implementation Notes explicitly direct following this pattern.

**What is NOT reused:**
The actual code from the advisory endpoint is not imported or called. This is
pattern reuse (following the same structural approach), not code reuse. Each module
has its own Query struct and service method — they are structurally parallel but
independent.

---

### 3. `entity/src/package_license.rs` (package-license join entity)

**What it provides:**
The existing SeaORM entity definition for the `package_license` join table, which
maps packages to their declared licenses. Includes the entity struct, column
definitions, and relation definitions needed for SeaORM query building.

**How it will be reused:**
- **Direct reuse** — import and use the `package_license` entity in the
  `PackageService::list()` method to construct a JOIN query.
- Use SeaORM's `JoinType::InnerJoin` (or `LeftJoin` if appropriate) with the
  `package_license` relation to join the package table to the license mapping table.
- Apply the `apply_filter`-generated condition on the license column of this entity.
- No modifications to the entity itself are needed — it already maps the correct
  table structure.

**Reuse decision rationale:**
The entity already exists and correctly models the database join table. Using it
with SeaORM's relation-based query building avoids raw SQL, maintains type safety,
and follows the codebase convention of using SeaORM entities for all database
operations. The `entity` crate is already a dependency of `modules/fundamental`.

**Alternative considered:**
Writing a raw SQL JOIN query. Rejected because the codebase convention is to use
SeaORM entities, and the entity already exists. Raw SQL would bypass SeaORM's
type checking and be inconsistent with how all other queries in the project are
constructed.

---

## Additional Reuse Opportunities Discovered

Beyond the three listed Reuse Candidates, the following existing code would also
be reused:

### `common/src/model/paginated.rs::PaginatedResults<T>`

The response wrapper type. The task explicitly states "Response shape
(PaginatedResults<PackageSummary>) remains unchanged." The existing `PaginatedResults`
generic is already used by the package list endpoint and requires no changes.

### `common/src/error.rs::AppError`

All handlers return `Result<T, AppError>`. The validation logic for invalid license
values (returning 400 Bad Request) will use `AppError` to construct the error
response, following the same error handling pattern used throughout the codebase.

### Test infrastructure from sibling tests

The test file will reuse:
- Database seeding utilities used by `tests/api/advisory.rs` and `tests/api/sbom.rs`
- The test HTTP client setup pattern
- The `assert_eq!(resp.status(), StatusCode::OK)` assertion style
- The response body deserialization approach (`resp.json::<PaginatedResults<PackageSummary>>()`)

---

## Summary Table

| Reuse Candidate | Reuse Type | Modifications Needed | New Dependency? |
|---|---|---|---|
| `common/src/db/query.rs::apply_filter` | Direct function call | None | No (already a dep) |
| `advisory/endpoints/list.rs` severity pattern | Structural pattern | N/A (pattern, not import) | No |
| `entity/src/package_license.rs` | Direct entity import for JOIN | None | No (already a dep) |
| `common/src/model/paginated.rs` | Existing response wrapper | None | No (already a dep) |
| `common/src/error.rs::AppError` | Existing error type | None | No (already a dep) |

**No code duplication is introduced.** Every piece of logic that exists in the
codebase is reused rather than reimplemented. The only new code is the
license-specific glue: the Query struct field, the service method parameter, the
JOIN+filter query construction, and the integration tests.
