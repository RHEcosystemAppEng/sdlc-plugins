# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose
New migration that drops the deprecated `status` column from the `advisory` table.

## Changes

Create this file following the pattern from `migration/src/m0001_initial/mod.rs`:

```rust
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drops the deprecated `status` column from the advisory table.
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

#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Patterns followed
- `MigrationTrait` implementation with `up`/`down` matching `m0001_initial/mod.rs`
- `DeriveMigrationName` derive macro for automatic migration naming
- `TableAlterStatement` for DDL operations as specified in Implementation Notes
- Local `Iden` enum for table/column references (avoids dependency on entity crate)
- `down` method re-adds column as `string().null()` per acceptance criteria
