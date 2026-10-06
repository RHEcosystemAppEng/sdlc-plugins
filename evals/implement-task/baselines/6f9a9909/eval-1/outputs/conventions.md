# Conventions Discovered from Sibling Analysis

## Source

Conventions derived from sibling files in the `modules/fundamental/src/advisory/` and
`modules/fundamental/src/sbom/` module directories, as well as the repository-wide
conventions listed in `repo-backend.md` and `CONVENTIONS.md` (if present).

## Production Code Conventions

### Naming Conventions

- **Files**: lowercase `snake_case` (e.g., `summary.rs`, `details.rs`, `get.rs`, `list.rs`)
- **Structs**: `PascalCase`, domain-prefixed (e.g., `AdvisorySummary`, `SbomDetails`, `PackageSummary`)
- **Service methods**: `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `severity_summary`)
- **Endpoint handlers**: named after the HTTP verb or action (e.g., `get`, `list`)
- **Modules**: `mod.rs` re-exports with `pub mod <name>;` declarations

### Module Structure

- Each domain module follows a strict `model/ + service/ + endpoints/` tripartite structure
- `model/mod.rs` registers sub-modules with `pub mod <name>;`
- `service/mod.rs` re-exports the main service file
- `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))`

### Error Handling

- All handler functions return `Result<T, AppError>`
- Errors wrapped with `.context("descriptive message")` for traceability
- `AppError` enum defined in `common/src/error.rs`, implements `IntoResponse`

### Response Types

- Single-entity endpoints return the struct directly via Axum's `Json` extractor
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Serialization handled by `serde::Serialize` derive on response structs

### Endpoint Registration Pattern

- Routes defined in each module's `endpoints/mod.rs`
- Pattern: `Router::new().route("/path", get(handler_function))`
- `server/main.rs` mounts all module routers (auto-mount via module registration)

### Path Parameter Extraction

- Path parameters extracted via Axum's `Path<Id>` extractor
- Service methods receive the extracted ID plus `&Transactional<'_>` for DB access

### Import Organization

- Framework imports (axum, serde) first
- Internal crate imports second
- Local module imports last

### Documentation

- Public structs and functions must have doc comments using `///`
- One-line description of purpose is sufficient for simple types

## Test Conventions

### File Location and Naming

- Integration tests live in `tests/api/` directory
- Test files named after the domain (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)
- New test file: `advisory_summary.rs` following the existing `advisory.rs` sibling

### Assertion Style

- Status code assertions: `assert_eq!(resp.status(), StatusCode::OK)`
- Value-based assertions preferred over length-only checks (per skill guidance)
- Response body parsed as JSON and fields compared with `assert_eq!`

### Test Structure

- Tests hit a real PostgreSQL test database
- Each test function is annotated with `#[test]` or `#[tokio::test]`
- Given-when-then section comments for non-trivial tests (per skill guidance)
- Doc comments on every test function (per skill guidance, overrides sibling pattern if absent)

### Error Case Coverage

- 404 tests for non-existent resource IDs
- Empty-result tests (e.g., SBOM with no advisories)
- Edge case tests (e.g., duplicate deduplication)

## Convention Conflicts

- **Test documentation**: Sibling test files may not consistently have doc comments on
  test functions. Per skill guidance, doc comments are mandatory on AI-generated tests
  regardless of sibling practice. This is noted as a skill override.
