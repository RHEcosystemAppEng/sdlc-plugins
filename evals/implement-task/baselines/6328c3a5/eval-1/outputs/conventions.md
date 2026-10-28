# Conventions Discovered from Sibling Analysis

## Source

Conventions extracted from sibling files in the `trustify-backend` repository, organized
by category. These serve as binding references during implementation and test writing.

### CONVENTIONS.md

The repository root contains a `CONVENTIONS.md` file. Its contents would be read during
Step 4 to extract any CI check commands (formatting, linting, compilation) and code
generation commands. Verification commands found there would be recorded for use in
Step 9's CI checks sub-step.

---

## Naming Conventions

- **Files**: snake_case for all Rust source files (e.g., `summary.rs`, `details.rs`, `sbom.rs`)
- **Modules**: snake_case module names matching the file name (e.g., `mod summary;`)
- **Structs**: PascalCase (e.g., `SbomSummary`, `AdvisoryDetails`, `PackageSummary`)
- **Methods**: snake_case verb_noun pattern (e.g., `fetch`, `list`, `search`, `ingest`)
- **Endpoints**: snake_case handler function names (e.g., `get_sbom`, `list_advisories`)
- **Test files**: snake_case matching the domain entity (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)
- **Test functions**: `test_` prefix with snake_case description

Sources: `modules/fundamental/src/sbom/model/summary.rs`, `modules/fundamental/src/advisory/service/advisory.rs`, `tests/api/sbom.rs`

## Module Structure

- Each domain module follows the `model/ + service/ + endpoints/` tri-partition
- `model/mod.rs` re-exports sub-module structs via `pub mod <name>;`
- `service/mod.rs` re-exports the service module
- `endpoints/mod.rs` registers routes and re-exports handler modules
- New model files are added as siblings to existing model files (e.g., `summary.rs`, `details.rs`)
- New endpoint files are added as siblings to existing endpoint files (e.g., `list.rs`, `get.rs`)

Sources: `modules/fundamental/src/sbom/`, `modules/fundamental/src/advisory/`, `modules/fundamental/src/package/`

## Error Handling

- All handlers return `Result<T, AppError>` where `AppError` is from `common/src/error.rs`
- Error wrapping uses `.context("descriptive message")` (anyhow-style)
- `AppError` implements `IntoResponse` for automatic HTTP error conversion
- 404 responses use appropriate `AppError` variant for "not found" cases, consistent with existing SBOM endpoints

Sources: `common/src/error.rs`, `modules/fundamental/src/advisory/endpoints/get.rs`

## Endpoint Patterns

- Route registration in `endpoints/mod.rs` uses `Router::new().route("/path", get(handler))` pattern
- Path parameters extracted via `Path<Id>` extractor (Axum)
- Service methods called with `(&self, id: Id, tx: &Transactional<'_>)` signature pattern
- Responses returned directly as structs (Axum's `Json` extractor handles serialization)
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Single-entity endpoints return the struct directly wrapped in `Json`

Sources: `modules/fundamental/src/sbom/endpoints/get.rs`, `modules/fundamental/src/advisory/endpoints/get.rs`

## Response Types

- Structs derive `Serialize` and `Deserialize` (serde)
- Struct fields use snake_case (Rust convention; serde default)
- Response structs are defined in `model/` directory alongside the domain module
- The `AdvisorySummary` struct in `model/summary.rs` includes a `severity` field -- this is the field we count by

Sources: `modules/fundamental/src/advisory/model/summary.rs`, `modules/fundamental/src/sbom/model/summary.rs`

## Service Layer Patterns

- Service structs (e.g., `AdvisoryService`) have methods like `fetch`, `list`, `search`
- Methods take `&self`, an identifier parameter, and `tx: &Transactional<'_>` for database context
- Services use SeaORM for database queries
- Join tables (e.g., `sbom_advisory`) are used for cross-entity relationships
- Queries use shared helpers from `common/src/db/query.rs` for filtering, pagination, sorting

Sources: `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/sbom/service/sbom.rs`

## Import Organization

- Standard library imports first
- External crate imports second
- Internal crate imports third (using `crate::` paths)
- Sibling module imports using `super::` paths

Sources: inferred from standard Rust project conventions and module structure

## Test Patterns

- Integration tests live in `tests/api/` directory, one file per domain entity
- Tests hit a real PostgreSQL test database (not mocked)
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` for status checks
- Response body parsed as JSON and fields asserted individually
- Error cases tested (e.g., 404 for non-existent IDs)
- Test structure follows arrange-act-assert pattern

Sources: `tests/api/sbom.rs`, `tests/api/advisory.rs`, `tests/api/search.rs`

## Skill Guidance Overrides

The following skill guidance takes precedence over sibling patterns:

- **Value-based assertions**: Prefer asserting on actual values over length-only checks, even if siblings use `.len()` checks
- **Test documentation**: Every test function gets a `///` doc comment explaining what it verifies, even if siblings lack doc comments
- **Given-when-then comments**: Non-trivial tests include `// Given`, `// When`, `// Then` section comments

## Framework and Dependencies

- **HTTP framework**: Axum
- **ORM**: SeaORM
- **Serialization**: serde (Serialize, Deserialize)
- **Error handling**: anyhow-style `.context()` wrapping via `AppError`
- **Caching**: tower-http middleware
- **Database**: PostgreSQL
