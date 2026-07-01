# Discovered Conventions

## Conventions from CONVENTIONS.md

The repository structure (repo-backend.md) indicates a `CONVENTIONS.md` file exists at the repository root (`trustify-backend/CONVENTIONS.md`). Per Step 4 of the SKILL.md methodology, this file would be read and its conventions followed. The repo-backend.md Key Conventions section provides the following explicit project conventions:

- **Framework**: Axum for HTTP, SeaORM for database
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Caching**: Uses `tower-http` caching middleware; cache configuration in endpoint route builders

## Discovered Conventions from Sibling Analysis

### Migration Conventions (from `migration/src/m0001_initial/mod.rs`)

The sibling migration file `m0001_initial/mod.rs` is the primary reference for establishing migration conventions:

- **Module structure**: Each migration lives in its own subdirectory under `migration/src/` named `m<NNNN>_<descriptive_name>/mod.rs`
- **Naming**: Migration directories follow the pattern `m<four-digit-sequence>_<snake_case_description>` (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **Trait implementation**: Each migration module implements `MigrationTrait` from SeaORM with two required methods:
  - `async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr>` -- applies the migration forward
  - `async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr>` -- rolls back the migration
- **Registration**: Migrations are registered in `migration/src/lib.rs` by adding them to the `vec![]` returned by the `migrations()` function
- **Import pattern**: Migrations use `sea_orm_migration::prelude::*` for access to SeaORM migration types
- **Table/Column references**: Use SeaORM enum-based identifiers (e.g., `Advisory::Table`, `Advisory::Status`) rather than raw string table/column names
- **Alter operations**: Use `TableAlterStatement` via `Table::alter()` for column modifications (add/drop)

### Entity Conventions (from `entity/src/advisory.rs`)

- **Entity definitions**: SeaORM entity files define a `Model` struct with `#[derive(Clone, Debug, PartialEq, DeriveEntityModel)]`
- **Column enums**: Each entity has an enum with variants for each column, used for type-safe column references in queries and migrations
- **Verification**: The `advisory.rs` entity should NOT reference the `status` column (it was replaced by `severity` in a prior migration) -- this must be verified before proceeding

### Test Conventions (from `tests/api/advisory.rs`)

- **Test location**: Integration tests for advisory functionality reside in `tests/api/advisory.rs`
- **Assertion style**: Tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Database tests**: Tests run against a real PostgreSQL test database (not mocked)
- **Test naming**: Tests follow `test_<action>_<scenario>` pattern
- **Documentation**: Per SKILL.md Step 7, every test function must have a documentation comment (`///`) explaining what it verifies, and non-trivial tests should include given-when-then section comments

### Registration Conventions (from `migration/src/lib.rs`)

- **Migration list**: The `lib.rs` file contains a `migrations()` function that returns a `Vec<Box<dyn MigrationTrait>>` with all registered migrations
- **Ordering**: Migrations are listed in sequential order by their numeric prefix
- **Module declaration**: Each migration module is declared with `mod m<NNNN>_<name>;` at the top of `lib.rs`
- **Boxed instances**: Each migration is added as `Box::new(m<NNNN>::Migration)` in the vec
