# File 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

## Action: CREATE

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. Follows the established pattern from `m0001_initial/mod.rs`.

## Detailed Changes

The file implements a SeaORM migration with `MigrationTrait`:

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
                    .add_column(
                        ColumnDef::new(Advisory::Status)
                            .string()
                            .null()
                            .to_owned(),
                    )
                    .to_owned(),
            )
            .await
    }
}

/// Enum referencing the `advisory` table and its columns for SeaORM schema operations.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Key Design Decisions

1. **`Advisory` enum defined locally**: The migration defines its own `Advisory` Iden enum rather than importing from the entity crate. This is standard SeaORM migration practice -- migrations should be self-contained and not depend on entity definitions that may change over time.

2. **Nullable string for rollback**: The `down` method re-adds `status` as `.string().null()` -- nullable because existing rows will have no value for this column after rollback. This matches the task's acceptance criteria.

3. **Documentation comments**: Added `///` doc comments on the struct, `up`, and `down` methods per skill guidance on documentation for new symbols.

4. **Pattern conformance**: Follows the exact structure of `m0001_initial/mod.rs` -- same trait implementations, same builder pattern usage, same `.to_owned()` calls.
