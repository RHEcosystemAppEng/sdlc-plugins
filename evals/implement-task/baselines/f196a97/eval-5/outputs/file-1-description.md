# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration file that drops the deprecated `status` column from the `advisory` table. This follows the pattern established by the sibling migration `m0001_initial/mod.rs`.

## Detailed Changes

### Full file content (new file)

```rust
//! Migration to drop the deprecated `status` column from the `advisory` table.
//!
//! The `status` column was replaced by the `severity` enum field in a previous
//! migration (m0001_initial) and is no longer read or written by any service code.
//! Removing it reduces confusion and prevents accidental usage.

use sea_orm_migration::prelude::*;

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

/// Identifiers for the `advisory` table and its columns used in this migration.
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}
```

### Design Decisions

1. **`MigrationTrait` implementation**: Follows the exact same pattern as `m0001_initial/mod.rs` -- implementing `up` and `down` methods with SeaORM's schema manager.

2. **`up` method**: Uses `TableAlterStatement` to drop the column, as specified in the Implementation Notes: `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`.

3. **`down` method**: Re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` -- nullable string to allow rollback without data loss concerns, as specified in the Implementation Notes.

4. **`Advisory` enum**: A local `DeriveIden` enum scoped to this migration module, providing type-safe identifiers for the table and column names. This is standard SeaORM migration practice -- each migration defines its own identifiers to avoid coupling to the entity module's definitions (which may change over time).

5. **Module documentation**: `//!` doc comment explaining the purpose and rationale for the migration.

6. **Method documentation**: `///` doc comments on both `up` and `down` methods describing what each does.
