# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. Follows the existing migration pattern established by `m0001_initial/mod.rs`.

## Detailed Implementation

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
                    .add_column(
                        ColumnDef::new(Advisory::Status)
                            .string()
                            .null(),
                    )
                    .to_owned(),
            )
            .await
    }
}

/// Iden enum referencing the advisory table and status column.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Patterns Followed

- **MigrationTrait implementation**: matches the pattern from `m0001_initial/mod.rs`
- **up method**: drops the column using `TableAlterStatement`
- **down method**: re-adds the column as nullable string (`string().null()`) to support rollback
- **DeriveMigrationName**: auto-derives migration name from module path
- **Documentation**: doc comments on the struct and Iden enum explaining the purpose
