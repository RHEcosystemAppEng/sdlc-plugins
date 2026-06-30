# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New SeaORM migration module that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

This file implements the `MigrationTrait` following the same pattern as the existing `m0001_initial/mod.rs` migration.

### Structure

```rust
use sea_orm_migration::prelude::*;

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

/// Identifiers for the advisory table and its columns used in this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Key Design Decisions

1. **`up` method**: Uses `TableAlterStatement` to drop the `status` column, matching the pattern specified in the Implementation Notes.
2. **`down` method**: Re-adds the column as a nullable string (`string().null()`) to allow clean rollback without data loss constraints.
3. **`Advisory` enum**: Defines local `Iden` variants for `Table` and `Status` to reference the advisory table and status column. This is the standard SeaORM pattern for type-safe table/column references in migrations.
4. **Documentation**: The `Advisory` enum gets a doc comment explaining its purpose in this migration context.

### Conventions Followed

- Follows the `MigrationTrait` pattern from `m0001_initial/mod.rs`
- Uses `DeriveMigrationName` for automatic migration naming from the module path
- Uses `async_trait` for the async migration methods
- Defines a local `Iden` enum rather than importing from the entity crate (migrations should be self-contained to avoid breakage when entities change)
