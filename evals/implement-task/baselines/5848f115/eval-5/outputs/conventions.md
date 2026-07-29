# Conventions Discovered from Sibling Analysis

## Source: migration/src/m0001_initial/mod.rs (sibling migration)

### Migration structure conventions
- **Struct naming**: All migrations export a public `Migration` struct with no fields
- **Trait implementation**: Implement `MigrationName` and `MigrationTrait` (async) on the struct
- **Migration name**: The `name()` method returns a string matching the module directory name (e.g., `"m0001_initial"`)
- **Module organization**: Each migration lives in its own directory under `migration/src/` with a `mod.rs` file
- **Naming pattern**: Migration directories follow `m<NNNN>_<description>` format (zero-padded 4-digit sequence number, underscore, snake_case description)

### SeaORM patterns
- **Table/column references**: Use a local `#[derive(Iden)]` enum within the migration file to reference table and column names, rather than importing from the entity crate (migrations must be self-contained since entities may change over time)
- **Alter table**: Use `Table::alter().table(Enum::Table).drop_column(Enum::Column).to_owned()` for column operations
- **Column definitions**: Use `ColumnDef::new(Enum::Column)` with chained type and constraint methods
- **Manager calls**: All operations go through `manager.alter_table()` or similar `SchemaManager` methods, returning `Result<(), DbErr>`

### Async patterns
- **Async trait**: Uses `#[async_trait::async_trait]` attribute on the `MigrationTrait` impl
- **Await chaining**: Manager operations are `.await`-ed directly

## Source: migration/src/lib.rs (migration registry)

### Registration conventions
- **Module declarations**: Each migration module is declared with `mod m<NNNN>_<name>;` at the top of the file
- **Migration ordering**: Migrations are registered in the `migrations()` function as `Box::new(m<NNNN>::Migration)` entries in a `vec![]`, ordered by sequence number
- **Sequential ordering**: New migrations must appear after all existing migrations in the vec

## Source: entity/src/advisory.rs (advisory entity)

### Entity conventions
- **SeaORM entity**: Uses `#[derive(DeriveEntityModel)]` with column definitions
- **Column enum**: Columns are defined in a derived enum; the `status` column is confirmed absent (already removed in a prior change)

## Source: Repository-wide (Key Conventions from repo-backend.md)

### Error handling
- All handlers return `Result<T, AppError>` with `.context()` wrapping

### Module structure
- Each domain module follows `model/ + service/ + endpoints/` structure

### Testing
- Integration tests in `tests/api/` use a real PostgreSQL test database
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)`

## Test Conventions (from sibling test analysis)

### Test file organization
- Integration tests live in `tests/api/` directory
- Test files are named after the domain entity (e.g., `advisory.rs`, `sbom.rs`)
- Tests use a real PostgreSQL test database (not mocks)

### Assertion patterns
- Status code assertions: `assert_eq!(resp.status(), StatusCode::OK)`
- Response body validation through deserialization followed by field-level assertions
- Migration tests should verify both `up` and `down` operations succeed without error
