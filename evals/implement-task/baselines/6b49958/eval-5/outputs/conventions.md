# Discovered Conventions (from sibling analysis)

## Source: `migration/src/m0001_initial/mod.rs`

### Migration Module Structure
- Each migration lives in its own subdirectory under `migration/src/` following the naming pattern `m<NNNN>_<snake_case_description>/mod.rs`
- Migrations use `#[derive(DeriveMigrationName)]` on a unit struct named `Migration`
- The `MigrationTrait` is implemented with `#[async_trait::async_trait]`
- Both `up()` and `down()` methods are required, returning `Result<(), DbErr>`

### Import Conventions
- Single wildcard import: `use sea_orm_migration::prelude::*;`
- No explicit imports of individual SeaORM types -- the prelude provides them all

### Table/Column Referencing
- Migrations define a local `#[derive(Iden)]` enum for table and column references rather than importing from `entity/` modules
- This keeps migrations self-contained and reproducible regardless of future entity changes
- The enum variant `Table` maps to the table name; other variants map to column names

### Schema Operations
- Table alterations use the builder pattern: `Table::alter().table(...).drop_column(...).to_owned()`
- Column definitions use the builder pattern: `ColumnDef::new(...).string().null()`
- All schema operations go through the `SchemaManager` parameter

## Source: `migration/src/lib.rs`

### Module Registration
- Each migration module is declared with `mod m<NNNN>_<description>;`
- Module declarations are ordered sequentially by migration number
- The `migrations()` function returns `Vec<Box<dyn MigrationTrait>>`
- Migrations are registered in sequential order inside a `vec![]` macro
- Each entry is `Box::new(<module>::Migration)`

## Source: `entity/src/advisory.rs`

### Entity Convention (verified, not applied)
- The `Advisory` entity no longer includes a `Status` field or column mapping
- This confirms the `status` column is safe to drop -- no entity code references it
- Searched for `Status` variants, `status` string literals, and column mappings -- none found

## Test Conventions (from Test Requirements)

No sibling test files for migrations were identified in the fixture. The test requirements specify:
- Test that the migration runs successfully against a test database
- Test that the rollback (down) re-adds the column
- Verify that existing advisory queries still work after the column is dropped

These would follow SeaORM's migration testing patterns, typically using an in-memory SQLite database or a test PostgreSQL instance with the migration runner.
