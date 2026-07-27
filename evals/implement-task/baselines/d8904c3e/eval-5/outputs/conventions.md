# Discovered Conventions from Sibling Analysis

## Migration Conventions (from `migration/src/m0001_initial/mod.rs`)

- **Module structure**: Each migration lives in its own directory under `migration/src/` following the naming pattern `m<NNNN>_<descriptive_name>/mod.rs`
- **Trait implementation**: All migrations implement `MigrationTrait` from `sea_orm_migration::prelude::*` using `#[async_trait::async_trait]`
- **Migration name derivation**: Use `#[derive(DeriveMigrationName)]` on the `Migration` struct to auto-generate a unique name from the module path
- **Identifier enums**: Define table and column identifiers using `#[derive(DeriveIden)] enum` locally within the migration module, rather than importing from the entity crate -- this decouples migrations from the current entity state
- **Builder pattern**: Use SeaORM's builder pattern with `.to_owned()` at the end of statement chains before passing to `manager`
- **Registration**: Migrations are registered in `migration/src/lib.rs` via `mod` declaration and `Box::new(ModuleName::Migration)` in the `migrations()` vec, maintaining chronological order
- **Reversibility**: Both `up` and `down` methods must be implemented; `down` should reverse the `up` operation to allow rollback

## Error Handling Conventions (from `common/src/error.rs` and service modules)

- **Error type**: All handlers and services return `Result<T, AppError>` where `AppError` is the shared error enum from `common/src/error.rs`
- **Error wrapping**: Use `.context()` for wrapping lower-level errors with descriptive messages

## General Code Conventions (from repository Key Conventions)

- **Framework**: Axum for HTTP, SeaORM for database ORM
- **Module pattern**: Domain modules follow `model/ + service/ + endpoints/` structure
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`

## Test Conventions (from `tests/api/advisory.rs` and siblings)

- **Test type**: Integration tests in `tests/api/` hit a real PostgreSQL test database
- **Assertion style**: Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for response status verification
- **Test scope**: Tests are organized by domain entity (e.g., `advisory.rs`, `sbom.rs`, `search.rs`)

## CONVENTIONS.md

The repository contains a `CONVENTIONS.md` file at the root. Its contents should be read during implementation (Step 4) and any CI check commands extracted for use in Step 9. Any additional conventions discovered there take precedence over the sibling analysis above.
