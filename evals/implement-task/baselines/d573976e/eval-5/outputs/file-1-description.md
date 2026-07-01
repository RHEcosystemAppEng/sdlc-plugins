# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

Create a new file implementing `MigrationTrait` following the pattern established by `migration/src/m0001_initial/mod.rs`.

### Full Implementation

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

/// Identifiers for the `advisory` table and its columns used in this migration.
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}
```

### Design Decisions

1. **`DeriveMigrationName`**: Uses the derive macro to automatically generate the migration name from the module path, matching the pattern in `m0001_initial`.

2. **`Advisory` enum with `DeriveIden`**: Defines local identifiers for the table and column names used in this migration. This is standard SeaORM practice — each migration defines its own identifiers rather than importing from the entity module, ensuring migrations remain self-contained and do not break when entity definitions change.

3. **`up` method**: Uses `TableAlterStatement` to drop the `status` column, exactly as specified in the Implementation Notes.

4. **`down` method**: Re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` — a nullable string — to allow rollback without data loss concerns. This matches the task's specification for the rollback behavior.

5. **Documentation comments**: Every public symbol (`Migration` struct, `up` method, `down` method, `Advisory` enum) has a `///` doc comment explaining its purpose, following Rust documentation conventions and the skill's requirement for documentation on new symbols.

### Conventions Applied

- Follows the `MigrationTrait` implementation pattern from `m0001_initial/mod.rs`
- Uses `async_trait` for the async trait implementation
- Uses `DeriveIden` for table/column identifiers (self-contained migration)
- Error type is `DbErr` from SeaORM
- Uses builder pattern with `.to_owned()` for table alter statements
