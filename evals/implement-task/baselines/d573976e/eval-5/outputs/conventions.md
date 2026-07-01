# Discovered Conventions from Sibling Analysis

## Production Code Conventions

### Migration module structure
- Each migration lives in its own subdirectory under `migration/src/` following the pattern `m<NNNN>_<description>/mod.rs`
- The directory name serves as both the module name and (via `DeriveMigrationName`) the migration identifier
- Numbering is sequential: `m0001`, `m0002`, etc.

### MigrationTrait implementation pattern
- Migrations implement `MigrationTrait` from `sea_orm_migration::prelude::*`
- The `async_trait` attribute is used for the async trait implementation
- Both `up` and `down` methods are required and must return `Result<(), DbErr>`
- The `Migration` struct uses `#[derive(DeriveMigrationName)]` for automatic name generation

### Table/Column identifiers
- Each migration defines its own local `DeriveIden` enum for table and column identifiers
- Identifiers are self-contained within the migration (not imported from entity modules)
- This ensures migrations remain stable even when entity definitions evolve

### Schema modification pattern
- Table alterations use the builder pattern: `Table::alter().table(...).drop_column(...).to_owned()`
- Column definitions use the builder pattern: `ColumnDef::new(...).string().null()`
- The `.to_owned()` call finalizes the builder and produces an owned statement

### Migration registration
- All migrations are registered in `migration/src/lib.rs` in the `migrations()` function
- Registration uses `Box::new(<module>::Migration)` wrapping in a `vec![]`
- Migrations must be registered in sequential order

### Error handling (project-wide)
- All handlers use `Result<T, AppError>` with `.context()` for error wrapping
- SeaORM operations return `Result<_, DbErr>`

### Framework conventions (project-wide)
- **HTTP framework**: Axum
- **ORM**: SeaORM for database access
- **Module pattern**: Domain modules follow `model/ + service/ + endpoints/` structure
- **Response types**: List endpoints return `PaginatedResults<T>`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`

### Naming conventions
- Service methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`)
- Migration directories use `m<NNNN>_<snake_case_description>` pattern
- Entity files use singular noun names (e.g., `advisory.rs`, `sbom.rs`)

## Test Conventions

### Integration test structure
- Integration tests live in `tests/api/` and test against a real PostgreSQL test database
- Test files are organized by domain entity (e.g., `advisory.rs`, `sbom.rs`, `search.rs`)

### Assertion patterns
- Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Response body is deserialized and specific field values are checked

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)

### Error case coverage
- Endpoint tests include error case tests (e.g., 404 for missing resources)
