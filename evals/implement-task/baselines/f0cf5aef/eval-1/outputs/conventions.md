# Conventions Discovered from Sibling Analysis

Conventions identified by analyzing sibling files in the `trustify-backend` repository,
organized by category. These serve as a binding reference during implementation and
test writing.

## Source Files Analyzed

### Production code siblings
- `modules/fundamental/src/advisory/endpoints/get.rs` -- sibling endpoint handler (GET /api/v2/advisory/{id})
- `modules/fundamental/src/advisory/endpoints/list.rs` -- sibling endpoint handler (GET /api/v2/advisory)
- `modules/fundamental/src/advisory/model/summary.rs` -- sibling model (AdvisorySummary)
- `modules/fundamental/src/advisory/model/details.rs` -- sibling model (AdvisoryDetails)
- `modules/fundamental/src/advisory/service/advisory.rs` -- service being modified (AdvisoryService)
- `modules/fundamental/src/sbom/endpoints/get.rs` -- cross-module sibling (SBOM endpoint patterns)
- `modules/fundamental/src/sbom/model/summary.rs` -- cross-module sibling (SbomSummary)

### Test code siblings
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

### Project-level conventions
- `CONVENTIONS.md` at repository root (if present)

## Discovered Conventions

### Naming Conventions

- **Files**: snake_case for all Rust source files (e.g., `severity_summary.rs`, `sbom_advisory.rs`)
- **Structs**: PascalCase (e.g., `AdvisorySummary`, `SbomDetails`, `PackageSummary`)
- **Functions**: snake_case with `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `get_advisory`)
- **Endpoint handlers**: named after the HTTP action, e.g., `get_advisory`, `list_advisories`
- **Test functions**: `test_` prefix with descriptive snake_case name (e.g., `test_get_advisory_by_id`)
- **Modules**: snake_case matching the domain concept (e.g., `severity_summary`)

### Module Structure

- Each domain module follows `model/ + service/ + endpoints/` structure
- `model/mod.rs` re-exports sub-modules via `pub mod <name>;`
- `service/mod.rs` re-exports the service implementation
- `endpoints/mod.rs` contains route registration using `Router::new().route(...)` pattern

### Error Handling

- All handlers return `Result<T, AppError>` where `AppError` is from `common/src/error.rs`
- Error wrapping uses `.context("descriptive message")` (anyhow-style)
- 404 errors: return `AppError` with appropriate context when entity not found
- Pattern: `service.fetch(id, &tx).await.context("failed to fetch advisory")?`

### Endpoint Patterns

- Path parameters extracted via `Path<Id>` (Axum extractor)
- Service injected via Axum state or extension
- Transaction context passed as `&Transactional<'_>`
- JSON responses returned directly via Axum's `Json<T>` wrapper
- Route registration: `Router::new().route("/api/v2/path", get(handler_fn))`
- List endpoints return `PaginatedResults<T>` from common module
- Single-resource endpoints return the model struct directly wrapped in `Json`

### Model/Struct Patterns

- Response structs derive `Serialize, Deserialize, Debug, Clone`
- May also derive `Default` for structs with sensible zero-value defaults
- May derive `utoipa::ToSchema` for OpenAPI spec generation
- Fields use standard Rust types (`u64`, `String`, `Option<T>`)
- Doc comments on structs and public fields

### Service Method Patterns

- Service methods are `pub async fn` on the service struct
- Common signature: `pub async fn method_name(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`
- Use SeaORM query builders for database access
- Entity joins use SeaORM's `find_also_linked` or manual join queries
- Results mapped from entity types to model types

### Import Organization

- Standard library imports first
- External crate imports second (serde, axum, sea_orm, etc.)
- Internal crate imports last (common, entity, model types)
- Grouped by blank lines between sections

### Test Conventions

- Integration tests in `tests/api/` directory
- Tests hit a real PostgreSQL test database
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` for status checks
- Response body parsed as JSON and fields asserted individually with `assert_eq!`
- Test setup creates required entities (SBOMs, advisories) in the test database
- Each test function is independent (no shared mutable state between tests)
- Tests use `#[tokio::test]` for async test functions

### Skill Guidance Overrides

The following skill guidance overrides conflicting sibling patterns:

- **Value-based assertions**: Skill requires asserting on actual values, not just collection lengths. If siblings use `.len()` checks or `.any()` checks alone, the implementation will use `assert_eq!` on specific field values instead.
- **Test documentation**: Every test function must have a `///` doc comment explaining what it verifies, even if sibling tests lack doc comments.
- **Given-when-then comments**: Non-trivial tests include `// Given`, `// When`, `// Then` section comments inside the test body.
