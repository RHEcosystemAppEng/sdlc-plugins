# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. This migration is part of the cleanup after the `severity` enum field replaced the `status` column in a previous migration.

## Detailed Changes

This file would be created following the pattern discovered in the sibling migration `migration/src/m0001_initial/mod.rs`.

### Structure

```rust
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drops the deprecated `status` column from the `advisory` table.
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(Advisory::Table)
                    .drop_column(Advisory::Status)
                    .to_owned(),
            )
            .await
    }

    /// Re-adds the `status` column as a nullable string for rollback support.
    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(Advisory::Table)
                    .add_column(ColumnDef::new(Advisory::Status).string().null())
                    .to_owned(),
            )
            .await
    }
}

/// Identifiers for the advisory table and its columns used in this migration.
///
/// Defined locally rather than imported from the entity crate to ensure migration
/// stability as entities evolve over time.
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}
```

### Key Design Decisions

1. **`up()` method**: Uses `TableAlterStatement` via `Table::alter()` to drop the `Status` column from the `Advisory` table, exactly as specified in the task's Implementation Notes.

2. **`down()` method**: Re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` -- a nullable string column. This matches the original column type and allows rollback. The column data is lost during `up`, so the re-added column will be empty/null after rollback.

3. **`Advisory` enum**: A local `DeriveIden` enum is defined within this migration module to reference the table and column names. This is standard SeaORM migration practice -- each migration defines its own identifier enums to remain self-contained and not depend on entity definitions that may change over time. This pattern would be confirmed by inspecting `m0001_initial/mod.rs`.

4. **`DeriveMigrationName`**: The struct uses SeaORM's `DeriveMigrationName` derive macro, which automatically generates the migration name from the module path (yielding `m0002_drop_advisory_status`).

5. **Module directory**: The migration lives in a directory named `m0002_drop_advisory_status` with a `mod.rs` file, following the `m<NNNN>_<snake_case_description>` naming pattern established by `m0001_initial`.

6. **Documentation comments**: Doc comments are added to the `up()` and `down()` methods and the `Advisory` enum, following the skill's code quality practice requiring documentation on new symbols (Step 6).

### Conventions Applied

- Follows the same import style as `m0001_initial` (using `sea_orm_migration::prelude::*`)
- Follows the same `MigrationTrait` implementation pattern with `up()` and `down()`
- Follows the same error handling (returning `Result<(), DbErr>`, propagating with `.await`)
- Includes documentation comments on the `Advisory` enum and migration methods
- Module directory name follows the `m<NNNN>_<description>` naming pattern
- Uses `#[async_trait::async_trait]` attribute consistent with sibling migration
- Sequential numbering: `m0002` follows `m0001`
- Self-contained identifiers: defines `Advisory` enum locally rather than importing from entity crate
