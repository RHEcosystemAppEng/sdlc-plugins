# File 1: `migration/src/m0002_drop_advisory_status/mod.rs` (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. This follows the established pattern from `migration/src/m0001_initial/mod.rs`.

## Pre-Implementation Inspection

Before creating this file, inspect the sibling migration `m0001_initial/mod.rs` using Serena:

```
mcp__serena_backend__find_symbol("MigrationTrait", include_body=true)
```

This confirms the exact imports, struct naming, and method signatures used in existing migrations.

## Detailed Changes

### Imports

The file should import the same dependencies as `m0001_initial/mod.rs`, adapting for the alter-table operation:

```rust
use sea_orm_migration::prelude::*;
```

### Migration Struct

Define the migration struct following the naming convention from m0001_initial:

```rust
#[derive(DeriveMigrationName)]
pub struct Migration;
```

### MigrationTrait Implementation

Implement `MigrationTrait` with both `up` and `down` methods:

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

### Iden Enum

Define the `Advisory` enum for table/column references (following SeaORM convention):

```rust
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Conventions Applied

- Follow the `MigrationTrait` pattern from `m0001_initial/mod.rs` (struct + trait implementation)
- Use `#[derive(DeriveMigrationName)]` for automatic migration naming
- Use SeaORM's `TableAlterStatement` API for schema modifications
- The `down` method re-adds the column as `string().null()` to allow rollback without breaking existing data
- Use `Iden` derive macro for type-safe table/column references

## Contract Verification

- `MigrationTrait` requires both `up` and `down` methods — both are implemented
- Both methods return `Result<(), DbErr>` matching the trait contract
- Both methods take `&self` and `&SchemaManager` matching the trait signatures
