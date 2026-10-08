# File 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

## Action: CREATE

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. Follows the existing migration pattern established by `m0001_initial/mod.rs`.

## Full File Content

```rust
//! Migration to drop the deprecated `status` column from the `advisory` table.
//!
//! The `status` column was replaced by the `severity` enum field in a previous
//! migration and is no longer read or written by any service code. Removing it
//! reduces confusion and prevents accidental usage.

use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drop the `status` column from the `advisory` table.
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

    /// Re-add the `status` column as a nullable string to allow rollback.
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

1. **`#[derive(DeriveMigrationName)]`**: Automatically derives the migration name from the module path, following SeaORM convention. This ensures the name stored in the migrations table matches the module directory name.

2. **`Advisory` enum defined locally**: The migration defines its own `Advisory` Iden enum rather than importing from the entity crate. This is standard practice for migrations because:
   - The entity crate's `Advisory` may no longer have the `Status` variant (since the column is being dropped)
   - Migrations must be self-contained and not break when entities evolve

3. **`down()` re-adds as nullable string**: The rollback adds the column back as `.string().null()` per the Implementation Notes. This allows rollback without data loss concerns -- the column will be empty after rollback since existing data was not preserved.

4. **Module-level documentation**: Added `//!` doc comments explaining the purpose of this migration, following the skill's documentation requirement for all new symbols.

5. **Method documentation**: Added `///` doc comments on `up()` and `down()` methods describing what each does.
