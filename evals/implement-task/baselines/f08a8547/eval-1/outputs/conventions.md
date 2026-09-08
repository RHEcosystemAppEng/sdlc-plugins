# Conventions Discovered from Sibling Analysis

## Source

Conventions derived from analyzing the trustify-backend repository structure,
sibling modules (`sbom/`, `advisory/`, `package/`), and the documented key
conventions in the repository fixture.

---

## Naming Conventions

- **Files**: snake_case for all Rust source files (e.g., `severity_summary.rs`, `sbom_advisory.rs`).
- **Modules**: each domain concept gets its own submodule file under `model/`, `service/`, or `endpoints/`.
- **Structs**: PascalCase, named after the domain concept (e.g., `SbomSummary`, `AdvisoryDetails`, `PackageSummary`).
- **Service methods**: snake_case verbs matching the HTTP operation — `fetch`, `list`, `search`. New aggregation method should follow: `severity_summary`.
- **Endpoint handler functions**: snake_case matching the route purpose (e.g., `get`, `list`). The new handler should be named descriptively: `get_severity_summary` or `severity_summary`.
- **Test files**: named after the domain entity in `tests/api/` (e.g., `sbom.rs`, `advisory.rs`). New test file: `advisory_summary.rs`.
- **Test functions**: `test_<behavior>` pattern (e.g., `test_valid_sbom_severity_counts`).

## Module Structure

- Each domain module follows a strict three-directory pattern: `model/` + `service/` + `endpoints/`.
- `model/mod.rs` re-exports submodules with `pub mod <name>;`.
- `service/mod.rs` or a dedicated file (e.g., `advisory.rs`) contains the service struct with methods.
- `endpoints/mod.rs` registers routes and re-exports handler submodules.
- New concepts within a domain (e.g., severity summary within advisory) add files to each of the three directories rather than creating a new top-level module.

## Error Handling

- All endpoint handlers return `Result<T, AppError>`.
- Error wrapping uses `.context("descriptive message")` from the `anyhow` pattern, matching `common/src/error.rs`.
- 404 responses: return `AppError::NotFound` (or equivalent) when the target entity does not exist, consistent with existing SBOM and advisory endpoints.

## Endpoint Registration Pattern

- Routes are registered in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))`.
- `server/src/main.rs` mounts all module routers — no changes needed there since routes auto-mount via module registration.
- Path parameters use `Path<Id>` extractor from Axum.
- New routes follow the same `.route()` chaining pattern in the module's `endpoints/mod.rs`.

## Response Types

- Single-entity responses return the struct directly, wrapped by Axum's `Json` extractor for serialization.
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- The new severity summary endpoint returns a single aggregate object (not a list), so it should return `Json<SeveritySummary>` directly without pagination.

## Database / ORM Patterns

- SeaORM is used for database access.
- Join tables (e.g., `sbom_advisory`, `sbom_package`) connect entities in many-to-many relationships.
- Queries use SeaORM's query builder with `.filter()`, `.find_related()`, or raw joins as needed.
- Shared query helpers (filtering, pagination, sorting) live in `common/src/db/query.rs`.

## Service Method Signature Pattern

- Service methods take `&self` as the first parameter.
- Entity-fetching methods take an `id: Id` parameter and `tx: &Transactional<'_>` for transaction context.
- The `severity_summary` method should follow: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`.

## Import Organization

- Standard library imports first.
- External crate imports second.
- Internal crate/module imports last.
- Each group separated by a blank line.

## Test Conventions

- Integration tests live in `tests/api/` and hit a real PostgreSQL test database.
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` for status checks.
- Response body assertions: deserialize the response body and use `assert_eq!` on specific field values (value-based, not length-only).
- Each test function should have a `///` documentation comment explaining what it verifies (skill guidance — overrides sibling pattern if siblings lack doc comments).
- Non-trivial tests use given-when-then section comments (`// Given`, `// When`, `// Then`).

## Skill Guidance Overrides

- **Test documentation**: every test function gets a `///` doc comment regardless of whether sibling tests have them.
- **Value-based assertions**: assert on actual values, not just counts — this takes precedence if siblings use `.len()` checks alone.
- **Parameterized tests**: siblings do not appear to use parameterized tests (individual test functions per case), so this project convention is followed — no `rstest` parameterization introduced.
