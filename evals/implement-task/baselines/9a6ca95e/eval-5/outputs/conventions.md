# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Migration structure (from `migration/src/m0001_initial/mod.rs`)
- Each migration lives in its own directory under `migration/src/` following the naming pattern `m<NNNN>_<description>/mod.rs`
- Migrations are sequentially numbered (m0001, m0002, etc.)
- Each migration module exports a `pub struct Migration;` decorated with `#[derive(DeriveMigrationName)]`
- Implements `MigrationTrait` with async `up` and `down` methods
- Uses `sea_orm_migration::prelude::*` as the standard import

### Identifier pattern (from `migration/src/m0001_initial/mod.rs`)
- Table and column identifiers are defined as local `enum` types with `#[derive(Iden)]`
- Identifiers are scoped to the migration module, not shared across migrations
- This ensures migrations remain self-contained and do not break if entity definitions change

### Error handling (from project conventions)
- All handlers return `Result<T, AppError>` with `.context()` for wrapping
- Migrations return `Result<(), DbErr>` as required by SeaORM's `MigrationTrait`

### Module registration (from `migration/src/lib.rs`)
- Each migration module is declared with `mod m<NNNN>_<description>;`
- Migrations are registered in a `migrations()` function returning `Vec<Box<dyn MigrationTrait>>`
- Entries are added to the `vec![]` in sequential order

### Naming conventions
- Migration directories follow `m<NNNN>_<snake_case_description>` pattern
- Service methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`)

### Framework and ORM patterns
- Framework: Axum for HTTP, SeaORM for database
- Module structure: `model/ + service/ + endpoints/` for domain modules
- Entity definitions in `entity/src/` using SeaORM derive macros
- Response types: List endpoints return `PaginatedResults<T>`
- Query helpers: Shared filtering, pagination, sorting via `common/src/db/query.rs`

## Test Conventions

### Test structure (from `tests/api/advisory.rs` and siblings)
- Integration tests in `tests/api/` directory test endpoints against a real PostgreSQL test database
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Test naming: follows `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- Error cases: endpoint tests include 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`

### Documentation conventions
- Public symbols should have `///` doc comments
- Test functions should have `///` doc comments explaining what they verify
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments
