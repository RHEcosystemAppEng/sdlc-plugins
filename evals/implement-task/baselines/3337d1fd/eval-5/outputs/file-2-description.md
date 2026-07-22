# File 2: migration/src/m0002_drop_advisory_status/mod.rs (Create)

## Purpose

Database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer referenced by any entity or service code.

## Full File Content

```rust
//! Migration to drop the deprecated `status` column from the `advisory` table.
//!
//! The `status` column was replaced by the `severity` enum field and is no longer
//! read or written by any service code. Removing it reduces confusion and prevents
//! accidental usage.

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

/// Identifiers for the `advisory` table and its columns used in this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Design Decisions

1. **`DeriveMigrationName` macro**: Automatically derives the migration name from the module path, consistent with the pattern in `m0001_initial/mod.rs`.

2. **`up` method**: Uses `Table::alter()` with `drop_column()` to remove the `status` column. This matches the SeaORM `TableAlterStatement` pattern specified in the Implementation Notes.

3. **`down` method**: Re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` — a nullable string. This allows rollback without losing data integrity (the column will be empty after rollback since the data was not preserved).

4. **Local `Advisory` enum**: Defines a local `Iden` enum with only `Table` and `Status` variants needed for this migration, rather than importing from the entity crate. This is standard practice for migrations — they should be self-contained and not depend on the current entity definitions, which may change over time.

5. **Documentation**: Module-level doc comment explains the purpose. Each method has a doc comment describing what it does.

## Conventions Followed

- Follows the same `MigrationTrait` implementation pattern as `m0001_initial/mod.rs`
- Uses `sea_orm_migration::prelude::*` import
- Uses `#[derive(DeriveMigrationName)]` for automatic naming
- Uses `async_trait` for async trait methods
- Defines local `Iden` enum for table/column identifiers
- Directory structure matches naming convention: `m0002_drop_advisory_status/mod.rs`
