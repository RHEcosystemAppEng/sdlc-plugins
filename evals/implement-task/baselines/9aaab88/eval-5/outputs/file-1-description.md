# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

This file implements the `MigrationTrait` for SeaORM, following the pattern established in `migration/src/m0001_initial/mod.rs`.

### Structure

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration and is no longer read or written by any service code.
pub struct Migration;

impl MigrationName for Migration {
    fn name(&self) -> &str {
        "m0002_drop_advisory_status"
    }
}

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

    /// Re-adds the `status` column as a nullable string to allow rollback.
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

/// Identifiers for the advisory table and its columns used by this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Key Design Decisions

1. **Follows sibling pattern**: The structure mirrors `m0001_initial/mod.rs` -- implementing `MigrationName` and `MigrationTrait` using SeaORM's migration API.
2. **`up` method**: Uses `TableAlterStatement` with `drop_column` as specified in the Implementation Notes.
3. **`down` method**: Re-adds the column as `string().null()` to allow rollback without data loss or constraint violations, as specified in the Implementation Notes.
4. **Local `Iden` enum**: Defines a local `Advisory` enum with `Table` and `Status` variants for type-safe column references, following SeaORM migration conventions. This is separate from the entity definition since the entity no longer has the `Status` field.
5. **Documentation**: Every public symbol has a doc comment explaining its purpose.
