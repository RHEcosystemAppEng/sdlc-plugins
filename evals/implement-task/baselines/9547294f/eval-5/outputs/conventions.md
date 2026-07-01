# Discovered Conventions

## Conventions from CONVENTIONS.md

The repository root contains a `CONVENTIONS.md` file. Key conventions to follow:
- **Framework**: Axum for HTTP, SeaORM for database ORM
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Response types**: List endpoints return `PaginatedResults<T>`
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database

## Discovered Conventions from Sibling Analysis

### Migration conventions (from `migration/src/m0001_initial/mod.rs`)

- **Struct naming**: Migration struct is named `Migration` (unqualified) within each module — the module path provides the namespace (e.g., `m0001_initial::Migration`)
- **Module naming**: Migration modules follow the pattern `m<NNNN>_<descriptive_name>` where `NNNN` is a zero-padded sequence number (e.g., `m0001_initial`, so the next would be `m0002_drop_advisory_status`)
- **Trait implementation**: Each migration implements `MigrationTrait` from `sea_orm_migration::prelude::*`
- **Required methods**: `name()` returns a `&str` identifier, `up()` applies the migration, `down()` rolls it back
- **Imports**: Use `sea_orm_migration::prelude::*` for all SeaORM migration types
- **Table/column references**: Use SeaORM enum variants (e.g., `Advisory::Table`, `Advisory::Status`) rather than raw strings
- **DDL operations**: Use SeaORM's builder pattern for DDL — `Table::alter()`, `Table::create()`, etc.
- **Async methods**: Both `up` and `down` are async, taking `&SchemaManager` as parameter

### Migration registration conventions (from `migration/src/lib.rs`)

- **Module declarations**: Each migration module is declared with `mod m<NNNN>_<name>;` at the top of `lib.rs`
- **Registration**: Migrations are registered by adding `Box::new(m<NNNN>_<name>::Migration)` to the `vec![]` returned by the `migrations()` function in `MigratorTrait` impl
- **Ordering**: Migrations are listed in sequential order in the vec

### Entity conventions (from `entity/src/advisory.rs`)

- **SeaORM entities**: Use `DeriveEntityModel` derive macro
- **Column enums**: Each entity has a column enum (e.g., `Advisory::Status`, `Advisory::Severity`)
- **Verification**: The `advisory.rs` entity no longer includes `Status` in its column enum — confirms the column is deprecated and safe to drop

### Test conventions (from `tests/api/advisory.rs`)

- **Assertion style**: Use `assert_eq!(resp.status(), StatusCode::OK)` for status code checks
- **Response validation**: Deserialize response body and check specific field values
- **Test naming**: Follow `test_<action>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Database setup**: Tests run against a real PostgreSQL test database with migrations applied
- **Error cases**: Tests include 404/not-found scenarios
- **Integration test location**: Tests live in `tests/api/` directory, organized by domain entity

### General code conventions

- **Error handling**: Use `Result<T, AppError>` with `.context()` for error wrapping
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`)
- **Import organization**: Group standard library, external crate, and local imports separately
- **Documentation**: Public symbols have doc comments using `///` Rust convention
