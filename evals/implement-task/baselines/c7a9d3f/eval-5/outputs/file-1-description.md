# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

Create a new file implementing the `MigrationTrait` from SeaORM, following the pattern established by the sibling migration `m0001_initial/mod.rs`.

### Structure

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration and is no longer read or written by any service code.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drops the `status` column from the `advisory` table.
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

/// Iden enum for referencing advisory table and columns in SeaORM migrations.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Key Decisions

- **`DeriveMigrationName`**: Uses the derive macro to auto-generate the migration name from the module path, following the same pattern as `m0001_initial`.
- **`up` method**: Uses `TableAlterStatement` with `drop_column` as specified in the Implementation Notes.
- **`down` method**: Re-adds the column as `string().null()` (nullable string) to allow rollback without data loss. The column is nullable because data will have been lost during the `up` migration.
- **`Iden` enum**: Defines local `Advisory` enum with `Table` and `Status` variants for type-safe column references in the migration, rather than importing from the entity crate (since the entity no longer defines `Status`).
- **Documentation**: Every public symbol has a doc comment per the skill's code quality requirements.
