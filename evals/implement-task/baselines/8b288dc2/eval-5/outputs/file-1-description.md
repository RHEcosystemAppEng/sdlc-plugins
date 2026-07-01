# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. This is a new file following the pattern established by `migration/src/m0001_initial/mod.rs`.

## Detailed Changes

### Full file content to create:

```rust
//! Migration to drop the deprecated `status` column from the `advisory` table.
//!
//! The `status` column was replaced by the `severity` enum field in a previous
//! migration (`m0001_initial`) and is no longer read or written by any service
//! or entity code. Removing it reduces confusion and prevents accidental usage.

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

    /// Re-adds the `status` column as a nullable string to support rollback.
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

/// Iden enum for the `advisory` table and its columns used in this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Conventions Applied

- **Module structure**: File placed in `migration/src/m0002_drop_advisory_status/mod.rs` following the `m<NNNN>_<snake_case_description>/mod.rs` pattern from `m0001_initial`
- **Trait implementation**: Implements `MigrationTrait` with both `up()` and `down()` methods, matching sibling pattern
- **SeaORM imports**: Uses `sea_orm_migration::prelude::*` consistent with `m0001_initial`
- **Table/Column references**: Uses `Advisory::Table` and `Advisory::Status` enum-based identifiers via the `Iden` derive macro, not raw strings
- **Derive macro**: Uses `#[derive(DeriveMigrationName)]` on the `Migration` struct, matching sibling pattern
- **Async trait**: Uses `#[async_trait::async_trait]` attribute on the `MigrationTrait` impl
- **Documentation**: Module-level doc comment explains the migration purpose; method-level doc comments on `up()` and `down()` describe their behavior (per SKILL.md Step 6 code quality practices and Step 7 documentation requirements)
- **Alter table pattern**: Uses `Table::alter().table(...).drop_column(...)` and `Table::alter().table(...).add_column(...)` as specified in the Implementation Notes
- **Rollback safety**: The `down()` method re-adds the column as `.string().null()` (nullable) to allow rollback without data loss concerns

## Implementation Notes Adherence

- Follows the existing migration pattern in `migration/src/m0001_initial/mod.rs` as instructed
- Uses `TableAlterStatement` to drop the column as specified: `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
- The `down` method re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` as specified
