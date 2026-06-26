# Discovered Conventions

## Conventions from Sibling Analysis

The primary sibling for this task is `migration/src/m0001_initial/mod.rs`, which serves as the reference migration implementation.

### Migration Conventions (from m0001_initial/mod.rs)

- **Migration struct**: Each migration module defines a unit struct (e.g., `pub struct Migration;`) that implements `MigrationTrait`
- **Module naming**: Migration directories follow the pattern `m<NNNN>_<descriptive_name>/mod.rs` where NNNN is a zero-padded sequential number (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **Trait implementation**: Each migration implements `MigrationTrait` with two async methods:
  - `async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr>` -- applies the migration
  - `async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr>` -- rolls back the migration
- **Schema operations**: Use SeaORM's schema builder types (`Table`, `ColumnDef`, `TableAlterStatement`) for DDL operations
- **Entity references**: Use the entity enum variants (e.g., `Advisory::Table`, `Advisory::Status`) rather than raw string table/column names
- **Registration pattern**: Migrations are registered in `migration/src/lib.rs` by adding `Box::new(<module>::Migration)` to the `vec![]` returned by the `migrations()` function

### Project-Level Conventions (from repo-backend.md Key Conventions)

- **Framework**: Axum for HTTP, SeaORM for database ORM
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern

### CONVENTIONS.md

The repository structure indicates a `CONVENTIONS.md` file exists at the repository root. This would be read during Step 4 to extract:
- Any additional coding standards beyond what's listed in the Key Conventions
- CI check commands (for Step 9's CI verification sub-step)
- Code generation commands (if any)

### Test Conventions (from tests/api/ siblings)

- **Test location**: Integration tests live in `tests/api/<entity>.rs` (e.g., `tests/api/advisory.rs`)
- **Assertion style**: Tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern followed by body deserialization
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (inferred from Key Conventions)
- **Database**: Tests run against a real PostgreSQL test database (not mocked)

### Naming Conventions

- **Service methods**: Follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`, `list_sboms`)
- **File naming**: Rust snake_case for all file and directory names
- **Entity naming**: SeaORM entity files at `entity/src/<entity_name>.rs` with corresponding enum variants
