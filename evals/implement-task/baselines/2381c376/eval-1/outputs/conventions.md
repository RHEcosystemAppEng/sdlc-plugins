# Conventions Discovered from Sibling Analysis

## Source of Conventions

Conventions were gathered from the following sibling files and repository documentation:

- `modules/fundamental/src/advisory/endpoints/get.rs` (sibling endpoint)
- `modules/fundamental/src/advisory/endpoints/list.rs` (sibling endpoint)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (route registration)
- `modules/fundamental/src/advisory/model/summary.rs` (sibling model)
- `modules/fundamental/src/advisory/model/details.rs` (sibling model)
- `modules/fundamental/src/advisory/service/advisory.rs` (service methods)
- `modules/fundamental/src/sbom/endpoints/get.rs` (cross-module sibling)
- `modules/fundamental/src/sbom/endpoints/list.rs` (cross-module sibling)
- `tests/api/advisory.rs` (sibling test file)
- `tests/api/sbom.rs` (sibling test file)
- `CONVENTIONS.md` at repository root
- `common/src/error.rs` (error handling pattern)

## Naming Conventions

- **Files**: snake_case for all Rust source files (e.g., `severity_summary.rs`, `sbom_advisory.rs`)
- **Structs**: PascalCase (e.g., `AdvisorySummary`, `SbomDetails`, `PaginatedResults`)
- **Functions/methods**: snake_case with verb_noun pattern (e.g., `fetch`, `list`, `search`, `severity_summary`)
- **Modules**: snake_case, matching the file name (e.g., `pub mod summary;`, `pub mod details;`)
- **Endpoints**: route path segments use kebab-case (e.g., `/api/v2/sbom/{id}/advisory-summary`)
- **Test functions**: `test_` prefix followed by descriptive snake_case (e.g., `test_get_advisory`, `test_list_advisories`)
- **Test files**: snake_case matching the domain concept (e.g., `advisory.rs`, `sbom.rs`, `advisory_summary.rs`)

## Module Structure

- Each domain module follows the `model/ + service/ + endpoints/` tripartite structure
- Models are registered in their parent `model/mod.rs` via `pub mod <name>;`
- Endpoints are registered in their parent `endpoints/mod.rs` via route builder patterns
- Services contain methods that accept `&self`, entity IDs, and a `tx: &Transactional<'_>` parameter

## Error Handling

- All endpoint handlers return `Result<T, AppError>`
- Errors are wrapped with `.context("descriptive message")` for context propagation
- `AppError` is defined in `common/src/error.rs` and implements `IntoResponse`
- 404 responses are produced by returning `AppError::NotFound` or equivalent when an entity lookup returns `None`

## Endpoint Patterns

- Path parameters extracted via `Path<Id>` (Axum extractor)
- Service called to perform business logic
- Response returned as `Json<T>` (Axum serializes automatically)
- Route registration pattern: `Router::new().route("/path", get(handler))`
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Single-entity endpoints return the domain struct directly wrapped in `Json`

## Service Patterns

- Service methods follow the signature: `async fn method_name(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`
- The `fetch` and `list` methods are the canonical patterns to follow
- Database queries use SeaORM with entity modules from `entity/src/`
- Join tables (e.g., `sbom_advisory`) are used to resolve relationships between entities

## Response Types

- Custom response structs derive `Serialize` and `Deserialize` (serde)
- Structs also typically derive `Clone`, `Debug`, `utoipa::ToSchema` for OpenAPI
- Fields use snake_case in Rust; serde serialization to JSON preserves snake_case

## Import Organization

- Standard library imports first
- External crate imports second (axum, serde, sea_orm, etc.)
- Internal crate imports third (crate::, super::)
- Grouped by blank lines between sections

## Test Conventions

- Integration tests live in `tests/api/` and hit a real PostgreSQL test database
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` for status checks
- Response body parsed via `.json::<T>()` for value-based assertions
- Error cases tested with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404s
- Tests are async functions annotated with `#[tokio::test]` (or project test macro)
- Test setup uses shared test fixtures/helpers for database seeding

## CONVENTIONS.md Findings

- Repository root contains `CONVENTIONS.md` with project-specific rules
- CI check commands would be extracted from CONVENTIONS.md for verification in Step 9
- Any code generation commands would also be extracted and run before committing

## Skill Guidance Overrides

- **Test documentation**: Every test function must have a `///` doc comment (skill standard overrides sibling absence)
- **Value-based assertions**: Prefer asserting on actual values, not just collection lengths (skill standard)
- **Given-when-then comments**: Non-trivial tests include `// Given`, `// When`, `// Then` section comments (skill standard)
