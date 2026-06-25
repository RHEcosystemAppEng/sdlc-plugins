# File 1: `migration/src/m0002_drop_advisory_status/mod.rs` (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Pattern Reference

Follows the existing migration pattern from `migration/src/m0001_initial/mod.rs`, implementing the `MigrationTrait` trait with `up` and `down` methods.

## Detailed Changes

Create the file with the following structure:

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a prior
/// migration and is no longer read or written by any service code.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
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
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}
```

## Key Implementation Details

- **`up` method**: Uses `Table::alter().drop_column()` to remove the `status` column. This matches the SeaORM pattern specified in the Implementation Notes.
- **`down` method**: Re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback. The column is nullable because existing rows would not have a value after re-adding.
- **`Advisory` enum**: Defines local `DeriveIden` identifiers for the table and column names used in this migration. This is the standard SeaORM migration pattern -- each migration defines its own identifiers rather than importing from the entity module, ensuring migrations remain self-contained and immutable.
- **Documentation**: A doc comment explains the purpose of the migration and why the column is being dropped.
