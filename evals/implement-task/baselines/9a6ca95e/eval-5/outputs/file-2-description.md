# File 2: migration/src/m0002_drop_advisory_status/mod.rs (Create)

## Purpose

Create a new SeaORM migration that drops the deprecated `status` column from the `advisory` table and provides a rollback mechanism to re-add it.

## Pre-Implementation Inspection

Before creating this file, read `migration/src/m0001_initial/mod.rs` using Serena (`mcp__serena_backend__find_symbol` with `include_body=true`) or the Read tool to:
- Understand the `MigrationTrait` implementation pattern (struct definition, `name()`, `up()`, `down()` methods)
- Confirm the import structure (`use sea_orm_migration::prelude::*;`)
- Observe how table and column identifiers are defined (the `Iden` derive pattern)
- Note the async signature and return type for `up` and `down`

Also verify in `entity/src/advisory.rs` that the `status` column is no longer referenced in the entity definition.

## File Contents

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

## Key Design Decisions

1. **`#[derive(DeriveMigrationName)]`**: Automatically generates the migration name from the module path, consistent with SeaORM conventions.

2. **`Advisory` enum with `Iden` derive**: Defines table and column identifiers locally within the migration module. This follows SeaORM's pattern of self-contained migrations that do not depend on entity definitions (which may change over time).

3. **`down` method re-adds as nullable string**: The column is re-added as `.string().null()` to allow rollback without data loss concerns. Existing rows will have `NULL` for the re-added column.

4. **Documentation comments**: Every public symbol and method has a `///` doc comment explaining its purpose, following the skill's code quality practices.

## Conventions Applied

- Follow the exact structure observed in `m0001_initial/mod.rs` for imports, struct definition, trait implementation, and identifier enums
- Use `Table::alter()` with method chaining as specified in the Implementation Notes
- Use `to_owned()` to finalize the statement builder, consistent with SeaORM patterns
- Place the `Iden` enum at the bottom of the file, after the trait implementation
