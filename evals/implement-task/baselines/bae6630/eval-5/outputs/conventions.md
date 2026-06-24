# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Migration Structure (from `migration/src/m0001_initial/mod.rs`)
- **Module layout**: Each migration lives in its own directory under `migration/src/` with a `mod.rs` file (e.g., `m0001_initial/mod.rs`)
- **Naming**: Migration directories use the pattern `m<NNNN>_<descriptive_name>` with zero-padded sequential numbering
- **Struct**: Each migration module exports a public `Migration` struct
- **Trait implementation**: Implements `MigrationName` (returns directory name as string) and `MigrationTrait` (provides async `up` and `down` methods)
- **Imports**: Uses `use sea_orm_migration::prelude::*;` as the standard import
- **Error handling**: Migration methods return `Result<(), DbErr>`
- **Iden enums**: Table and column identifiers are defined as local `#[derive(Iden)]` enums for type-safe references

### Migration Registration (from `migration/src/lib.rs`)
- **Module declarations**: Each migration module is declared with `mod m<NNNN>_<name>;` at the top of `lib.rs`
- **Registration**: Migrations are registered via `Box::new(module::Migration)` entries in a `vec![]` returned by the `migrations()` function
- **Ordering**: Migrations are listed in chronological order (ascending by sequence number)

### Entity Patterns (from `entity/src/advisory.rs` and siblings)
- **ORM**: SeaORM is used for entity definitions
- **Column mapping**: Each entity field maps to a database column via SeaORM derive macros
- **Module structure**: Entity files are flat under `entity/src/` (no subdirectories)

### General Code Patterns (from repository conventions)
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping (from `common/src/error.rs`)
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`)
- **Module pattern**: Domain modules follow `model/ + service/ + endpoints/` structure
- **Response types**: List endpoints return `PaginatedResults<T>`

## Test Conventions

### Integration Tests (from `tests/api/advisory.rs` and siblings)
- **Assertion style**: Use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Database**: Integration tests hit a real PostgreSQL test database
- **Test location**: API integration tests live in `tests/api/` with one file per domain entity
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern

### Migration Tests
- **Test execution**: Migration tests verify that `up` runs successfully against a test database
- **Rollback testing**: Migration tests also verify that `down` (rollback) executes without error
- **Post-migration queries**: After running the migration, existing queries are executed to confirm they still work without the dropped column
