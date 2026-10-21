# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New database migration that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

This file is created from scratch, following the pattern established in `migration/src/m0001_initial/mod.rs`.

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

/// Iden enum for type-safe table and column references.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Key Design Decisions

1. **`Advisory` Iden enum defined locally**: The migration defines its own `Advisory` enum with `Table` and `Status` variants rather than importing from `entity::advisory`. This is intentional -- migrations should be self-contained so they remain correct even as entity definitions evolve over time. The entity model has already removed the `Status` column, so importing from there would fail.

2. **`down` method re-adds as nullable string**: The rollback re-adds `status` as `.string().null()` so that rolling back does not break existing rows (they will have NULL in the re-added column). This matches the task's acceptance criteria.

3. **Documentation comments**: Every public symbol and method has a doc comment per the skill's code quality requirements.

4. **Follows sibling pattern**: The structure (imports, trait implementations, Iden enum) mirrors `m0001_initial/mod.rs` exactly.

### Conventions Applied

- snake_case module directory naming (`m0002_drop_advisory_status`)
- `MigrationTrait` implementation with `up` and `down` methods
- SeaORM `Table::alter()` API for schema changes
- Local `Iden` enum for table/column references
- `Result<(), DbErr>` return type
- `async_trait` macro for async trait methods
