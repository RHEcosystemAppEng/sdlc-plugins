# Conventions Discovered from Sibling Analysis

## Migration pattern conventions (from `migration/src/m0001_initial/mod.rs`)

- **Directory structure**: Each migration lives in its own directory under `migration/src/` following the pattern `m<NNNN>_<descriptive_name>/mod.rs` (e.g., `m0001_initial/mod.rs`, `m0002_drop_advisory_status/mod.rs`)
- **Naming**: Migration names use zero-padded sequential numbering with underscore-separated descriptive suffixes
- **Struct pattern**: Each migration module exports a unit struct named `Migration` (no fields)
- **Trait implementation**: Every migration implements two traits:
  - `MigrationName` -- returns the migration directory name as a string (e.g., `"m0002_drop_advisory_status"`)
  - `MigrationTrait` -- provides `up` and `down` async methods for forward and rollback operations
- **Async pattern**: Uses `#[async_trait::async_trait]` attribute macro on the `MigrationTrait` impl block
- **Return type**: Both `up` and `down` return `Result<(), DbErr>`
- **Schema API**: Uses SeaORM's `Table::alter()`, `ColumnDef::new()`, and related builder APIs for schema changes
- **Iden enum**: Defines a local `#[derive(Iden)]` enum for table and column identifiers used in the migration

## Registration conventions (from `migration/src/lib.rs`)

- **Module declaration**: Each migration module is declared with `mod m<NNNN>_<name>;` at the top of `lib.rs`
- **Migration list**: Migrations are registered in a `migrations()` function that returns `Vec<Box<dyn MigrationTrait>>`
- **Ordering**: Migrations are listed sequentially in the vec, with newer migrations appended after older ones
- **Boxing pattern**: Each migration is wrapped as `Box::new(<module>::Migration)`

## Entity conventions (from `entity/src/advisory.rs`)

- **ORM**: Uses SeaORM for entity definitions
- **Column mapping**: Entity structs map to database columns; the `advisory` entity uses `severity` (not `status`)

## General project conventions (from repo structure)

- **Framework**: Axum for HTTP, SeaORM for database
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Module pattern**: Domain modules follow `model/ + service/ + endpoints/` structure
- **Testing**: Integration tests in `tests/api/` use a real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern

## Test conventions (from `tests/api/advisory.rs` and siblings)

- **Assertion style**: Use `assert_eq!` for status code checks and field value verification
- **Database tests**: Run against a real PostgreSQL test database (not mocked)
- **Test naming**: Follow `test_<action>_<scenario>` pattern
- **Response validation**: Validate both status codes and response body contents
