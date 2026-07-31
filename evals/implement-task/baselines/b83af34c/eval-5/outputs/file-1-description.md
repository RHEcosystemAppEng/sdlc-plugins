# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose
New migration module that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

This file would be created from scratch, following the pattern established in `m0001_initial/mod.rs`.

### Structure

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration (m0001_initial) and is no longer read or written by any service code.
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

    /// Re-adds the `status` column as a nullable string for rollback.
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
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Key decisions
- Uses `#[derive(DeriveMigrationName)]` to auto-generate the migration name from the module path (convention from m0001_initial)
- The `Advisory` enum is locally defined with only the identifiers needed for this migration (`Table` and `Status`), not imported from entity crate -- this is the standard SeaORM migration pattern to keep migrations self-contained
- The `down` method re-adds the column as `.string().null()` to allow rollback without data loss concerns
- Documentation comments on the struct and both methods explain the purpose
