# File 2 (Create): migration/src/m0002_drop_advisory_status/mod.rs

## Purpose
Database migration that drops the deprecated `status` column from the `advisory` table.

## Content

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the advisory table.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drop the `status` column from the `advisory` table.
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

    /// Re-add the `status` column as a nullable string for rollback.
    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(Advisory::Table)
                    .add_column(
                        ColumnDef::new(Advisory::Status)
                            .string()
                            .null()
                            .to_owned(),
                    )
                    .to_owned(),
            )
            .await
    }
}

#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Conventions followed
- Implements `MigrationTrait` following the `m0001_initial` pattern
- Uses `#[derive(DeriveMigrationName)]` for automatic migration name
- `up` drops the column using `TableAlterStatement`
- `down` re-adds the column as `string().null()` for rollback
- Uses local `Iden` enum for table/column references as shown in sibling migration
- Documentation comments on the struct and both methods
