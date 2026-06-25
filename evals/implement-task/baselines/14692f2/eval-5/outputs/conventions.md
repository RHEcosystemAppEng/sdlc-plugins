# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Migration pattern (from `migration/src/m0001_initial/mod.rs`)

- **Trait implementation**: Each migration implements `MigrationTrait` with `up` and `down` async methods.
- **Derive macro**: Migration structs use `#[derive(DeriveMigrationName)]` for automatic name generation based on the module path.
- **Async trait**: Methods are annotated with `#[async_trait::async_trait]`.
- **Return type**: Both `up` and `down` return `Result<(), DbErr>`.
- **Schema operations**: Use SeaORM's `SchemaManager` with builder-pattern statements (`Table::alter()`, `Table::create()`, etc.), calling `.to_owned()` before passing to the manager.
- **Self-contained identifiers**: Each migration defines its own `#[derive(DeriveIden)]` enum for table and column identifiers rather than importing from the entity crate. This keeps migrations immutable and independent of entity changes.

### Migration registration (from `migration/src/lib.rs`)

- **Module declarations**: Each migration module is declared with `mod m0NNN_<name>;` at the top of `lib.rs`.
- **Migration list**: A `migrations()` function returns `Vec<Box<dyn MigrationTrait>>`, with each migration boxed and listed in chronological order.
- **Naming convention**: Migration directories follow the pattern `m<sequence>_<descriptive_name>` (e.g., `m0001_initial`, `m0002_drop_advisory_status`).

### General Rust conventions (from repository structure)

- **Framework**: Axum for HTTP, SeaORM for database ORM and migrations.
- **Module pattern**: Domain modules follow `model/ + service/ + endpoints/` structure.
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` for error wrapping.
- **Response types**: List endpoints return `PaginatedResults<T>` from the common module.
- **Import organization**: SeaORM migration prelude is imported with `use sea_orm_migration::prelude::*;`.

## Test Conventions

### Integration test pattern (from `tests/api/advisory.rs` and siblings)

- **Test database**: Integration tests hit a real PostgreSQL test database (not mocks).
- **Assertion style**: Tests use `assert_eq!(resp.status(), StatusCode::OK)` for status code checks, followed by body deserialization.
- **Test naming**: Tests follow `test_<action>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).
- **Migration tests**: Would verify that `up` runs without error, that `down` rolls back correctly, and that existing queries continue to function after the migration.

## CONVENTIONS.md

A `CONVENTIONS.md` file exists at the repository root. Its contents would be read and followed during implementation, including any CI check commands listed for verification in Step 9.
