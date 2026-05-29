# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. This follows the pattern established by the sibling migration `m0001_initial/mod.rs`.

## Detailed Changes

The file implements the `MigrationTrait` trait from SeaORM with two methods:

### Imports

```rust
use sea_orm_migration::prelude::*;
```

Following the import convention from `m0001_initial/mod.rs`.

### Struct Declaration

```rust
#[derive(DeriveMigrationName)]
pub struct Migration;
```

The `DeriveMigrationName` derive macro generates the migration name from the module path, matching the sibling pattern.

### MigrationTrait Implementation

```rust
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
                    .add_column(ColumnDef::new(Advisory::Status).string().null())
                    .to_owned(),
            )
            .await
    }
}
```

- `up()`: Uses `TableAlterStatement` via `Table::alter()` to drop the `status` column from the `advisory` table
- `down()`: Re-adds the column as a nullable string (`ColumnDef::new(Advisory::Status).string().null()`) for rollback safety

### Iden Enum

```rust
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

The `Iden` derive macro maps `Advisory::Table` to the table name `advisory` and `Advisory::Status` to the column name `status`. This follows SeaORM's convention for referencing database objects in migrations without coupling to entity definitions.

## Conventions Applied

- Module naming follows the `m<NNNN>_<description>` pattern established by `m0001_initial`
- Uses `DeriveMigrationName` for automatic migration name generation
- Uses `async_trait` for the async trait implementation
- Uses local `Iden` enum rather than importing from the entity module (migrations must be self-contained for reproducibility)
- Both `up()` and `down()` return `Result<(), DbErr>`
