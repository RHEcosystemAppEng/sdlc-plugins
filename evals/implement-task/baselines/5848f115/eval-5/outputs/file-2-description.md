# File 2: migration/src/m0002_drop_advisory_status/mod.rs (Create)

## Pre-creation Inspection

Before creating this file, read the sibling migration `migration/src/m0001_initial/mod.rs` using `mcp__serena_backend__find_symbol` with `include_body=true` on the `Migration` struct and its `MigrationTrait` impl. This reveals:
- The exact import paths for SeaORM migration types
- How `MigrationName`, `up`, and `down` are implemented
- The table/column enum patterns used

Also verify by reading `entity/src/advisory.rs` that the `status` column is no longer referenced in the Advisory entity definition.

## Changes

### Create the full migration file

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field and is no longer
/// referenced by any entity or service code.
pub struct Migration;

impl MigrationName for Migration {
    fn name(&self) -> &str {
        "m0002_drop_advisory_status"
    }
}

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

/// Enum referencing the `advisory` table and its `status` column for use in
/// migration statements.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Design Decisions

1. **Follows m0001_initial pattern**: The struct name `Migration`, trait implementations, and async patterns all mirror the existing migration.
2. **`down` method re-adds as nullable string**: Using `.string().null()` ensures the column can be re-added without breaking existing rows that would have NULL values.
3. **Local `Advisory` Iden enum**: Defined locally in the migration file rather than importing from entity, since the entity no longer has the `Status` variant. This is standard practice for migrations that reference columns that may not exist in the current entity definition.
4. **Documentation comment**: Added a doc comment on the `Migration` struct explaining what the migration does and why, per the skill's code quality practices.

## Verification

- `cargo check -p migration` should compile successfully
- The `up` method should drop the `status` column when run against a database
- The `down` method should re-add the column as a nullable string
- The migration name string matches the module directory name
