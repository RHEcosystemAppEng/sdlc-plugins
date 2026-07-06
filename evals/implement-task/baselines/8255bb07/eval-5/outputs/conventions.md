# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Migration pattern (from `migration/src/m0001_initial/mod.rs`)

- **Struct definition**: Each migration defines a unit struct named `Migration` (e.g., `pub struct Migration;`)
- **Trait implementation**: Implements `MigrationTrait` from SeaORM with three required methods:
  - `fn name(&self) -> &str` -- returns a descriptive name for the migration (typically formatted as `"m{number}_{description}"`)
  - `async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr>` -- applies the migration
  - `async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr>` -- rolls back the migration
- **Schema operations**: Uses SeaORM's schema manager and table alteration/creation APIs (`Table::alter()`, `Table::create()`, etc.)
- **Module organization**: Each migration lives in its own directory under `migration/src/`, named `m{number}_{snake_case_description}/mod.rs`
- **Registration**: Migrations are registered in `migration/src/lib.rs` by adding to a `vec![]` in the `migrations()` function, in sequential order
- **Entity references**: Uses entity enums (e.g., `Advisory::Table`, `Advisory::Status`) for type-safe table and column references rather than raw strings

### Error handling (from modules and common crate)

- **Return type**: All service methods and handlers return `Result<T, AppError>` with `.context()` wrapping for error messages
- **Error type**: `AppError` is defined in `common/src/error.rs` and implements `IntoResponse`

### Naming conventions

- **Service methods**: Follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`, `list_advisories`)
- **File naming**: Snake case throughout (e.g., `sbom_advisory.rs`, `package_license.rs`)
- **Module structure**: Each domain module follows `model/ + service/ + endpoints/` structure

### Framework conventions

- **HTTP framework**: Axum for HTTP routing
- **ORM**: SeaORM for database operations
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`

### Import organization

- Standard library imports first
- External crate imports second
- Internal crate imports last
- Grouped by source with blank lines between groups

## Test Conventions (from `tests/api/`)

### Assertion style

- All endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code verification
- Response body is deserialized and individual fields are checked

### Response validation

- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- Individual entity tests validate key fields after deserialization

### Error cases

- All endpoint test suites include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`

### Test naming

- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)

### Test infrastructure

- Integration tests in `tests/api/` hit a real PostgreSQL test database
- Tests use database fixtures for setup

### Database testing

- Migrations are tested by running them against the test PostgreSQL database
- The migration runner executes all registered migrations in order during test setup
