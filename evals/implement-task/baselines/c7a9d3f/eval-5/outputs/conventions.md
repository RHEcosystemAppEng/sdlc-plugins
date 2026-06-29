# Conventions Discovered from Sibling Analysis

## Project-Level Conventions (from repo Key Conventions)

- **Framework**: Axum for HTTP, SeaORM for database
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Caching**: Uses `tower-http` caching middleware; cache configuration in endpoint route builders

## Migration Conventions (from sibling: `m0001_initial/mod.rs`)

- **Directory naming**: Migrations follow `m<NNNN>_<snake_case_description>/mod.rs` pattern (e.g., `m0001_initial/mod.rs`)
- **Trait implementation**: Each migration implements `MigrationTrait` with `up` and `down` methods
- **Migration registration**: Migrations are registered in `migration/src/lib.rs` by adding them to the `vec![]` in the `migrations()` function
- **SeaORM API usage**: Migrations use SeaORM's `SchemaManager` and table alteration statements (e.g., `TableAlterStatement`, `TableCreateStatement`)
- **Column references**: Columns are referenced via entity enum variants (e.g., `Advisory::Status`, `Advisory::Table`)
- **Rollback support**: `down` methods must undo the `up` migration to support rollback

## Entity Conventions (from `entity/src/advisory.rs`)

- **SeaORM entities**: Entity files define structs with SeaORM derive macros
- **Column mapping**: Entity fields map to database columns via SeaORM attributes
- **Verification**: The `advisory.rs` entity no longer references the `status` column (confirmed per task description), which validates that the column can be safely dropped

## Test Conventions (from sibling: `tests/api/advisory.rs`)

- **Assertion style**: Integration tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Test database**: Tests run against a real PostgreSQL test database
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern
- **Test location**: Integration tests live in `tests/api/` directory, organized by domain entity
- **Migration testing**: Migration tests should verify both `up` (column dropped) and `down` (column re-added) operations
- **Query verification**: Tests should verify that existing queries still work after schema changes
