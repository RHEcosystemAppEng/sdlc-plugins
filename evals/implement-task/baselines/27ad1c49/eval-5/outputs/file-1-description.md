# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

Create a new file implementing the SeaORM `MigrationTrait`, following the pattern established
in `migration/src/m0001_initial/mod.rs`.

### Structure

```rust
use sea_orm_migration::prelude::*;

/// Migration that drops the deprecated `status` column from the `advisory` table.
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

    /// Re-adds the `status` column as a nullable string to support rollback.
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

/// Iden enum for the advisory table and its columns used by this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Key decisions

1. **Pattern adherence**: follows the exact structure of `m0001_initial/mod.rs` with `MigrationName` and `MigrationTrait` implementations
2. **Up method**: uses `TableAlterStatement::drop_column` as specified in Implementation Notes
3. **Down method**: re-adds the column as `string().null()` per Implementation Notes, ensuring rollback does not break existing data (nullable allows rows without a value)
4. **Local Iden enum**: declares `Advisory` enum locally within the migration module rather than importing from the entity crate, which is the standard pattern for migrations (migrations should be self-contained and not depend on entity definitions that may change over time)
5. **Documentation**: every public symbol and method has a doc comment per skill Step 6 code quality practices

### Pre-implementation verification

Before creating this file, verify:
- Inspect `migration/src/m0001_initial/mod.rs` using `mcp__serena_backend__find_symbol` to confirm the exact MigrationTrait implementation pattern (import paths, async_trait usage, error types)
- Search for `Advisory::Status` across the codebase using `mcp__serena_backend__search_for_pattern` to confirm it is not referenced in service or entity code
- Inspect `entity/src/advisory.rs` using `mcp__serena_backend__get_symbols_overview` to confirm the `status` field is absent from the entity definition
