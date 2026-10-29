# File 2: migration/src/m0002_drop_advisory_status/mod.rs (Create)

## Purpose

New database migration that drops the deprecated `status` column from the `advisory`
table. Implements both the forward migration (`up`) and rollback (`down`).

## File Content

The file follows the exact pattern of the sibling migration
`migration/src/m0001_initial/mod.rs`, implementing the `MigrationTrait` trait
from SeaORM.

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

/// Identifiers for the advisory table and its columns used in this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Design Decisions

### `up` method
- Uses `Table::alter().drop_column()` to remove the `status` column, following
  the SeaORM `TableAlterStatement` pattern specified in the Implementation Notes.
- Returns `Result<(), DbErr>` per the `MigrationTrait` contract.

### `down` method
- Re-adds the `status` column as a nullable string (`string().null()`) per the
  Implementation Notes, allowing rollback without data loss constraints.
- Uses `Table::alter().add_column()` with `ColumnDef::new()`.

### Local `Iden` enum
- Declares a local `Advisory` enum implementing `Iden` for table/column identifiers.
  This is a common SeaORM migration pattern that avoids coupling migrations to the
  entity crate (entity definitions may evolve, but migrations must remain stable).

### Documentation
- The `Migration` struct has a doc comment explaining what the migration does and why,
  per the skill's code quality practices (every new struct must have a documentation
  comment).
- The `Advisory` enum has a brief doc comment explaining its role.

## Conventions Applied

- Same import pattern as `m0001_initial`: `use sea_orm_migration::prelude::*;`
- Same struct naming: `pub struct Migration;`
- Same trait implementation: `#[async_trait::async_trait] impl MigrationTrait for Migration`
- Same error handling: returns `Result<(), DbErr>` (no `.context()` wrapping in
  migrations, as they use SeaORM's error type directly)
- Uses `#[derive(DeriveMigrationName)]` to auto-derive the migration name from the
  module path, matching the sibling pattern
