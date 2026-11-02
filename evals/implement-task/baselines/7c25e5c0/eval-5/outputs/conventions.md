# Convention Conformance Analysis — TC-9205

## Sibling analysis

Analyzed sibling migration file `migration/src/m0001_initial/mod.rs` and registration in `migration/src/lib.rs`.

## Discovered conventions

### Migration structure
- Migrations implement `MigrationTrait` from SeaORM
- Each migration lives in its own module directory: `migration/src/m<NNNN>_<description>/mod.rs`
- Naming follows sequential numbering with descriptive suffix: `m0001_initial`, `m0002_drop_advisory_status`

### Migration methods
- `up` method performs the forward migration (create table, add column, drop column)
- `down` method performs the reverse for rollback capability
- Both methods are async and return `Result<(), DbErr>`
- Use SeaORM's schema manager for DDL operations (`manager.alter_table(...)`, `manager.create_table(...)`)

### Migration registration
- All migrations are listed in `migration/src/lib.rs` in the `migrations()` function
- Each migration is `Box::new(<module>::Migration)` added to a `vec![]`
- Migrations are ordered sequentially

### Error handling
- Migrations use SeaORM's `DbErr` error type
- Service code throughout the project uses `Result<T, AppError>` with `.context()` wrapping from anyhow/eyre
- The migration crate has its own error handling separate from the service error pattern

### Module pattern
- Domain modules follow `model/ + service/ + endpoints/` structure
- Entity definitions live in `entity/src/` as standalone files
- Migrations are separate from entity definitions

### Entity column conventions
- SeaORM entity columns are defined as enum variants (e.g., `Advisory::Status`)
- Column types use SeaORM's `ColumnDef` builder pattern
- Nullable columns use `.null()`, required columns use `.not_null()`
