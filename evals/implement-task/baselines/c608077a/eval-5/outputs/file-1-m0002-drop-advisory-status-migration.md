# File 1 (CREATE): `migration/src/m0002_drop_advisory_status/mod.rs`

Purpose: SeaORM migration that drops the deprecated `status` column from the `advisory` table,
with a `down` that re-adds it as a nullable string.

Pattern source: `migration/src/m0001_initial/mod.rs` (`DeriveMigrationName` struct + `#[async_trait]
impl MigrationTrait` with `up`/`down`, `DeriveIden` enums for identifiers).

## Content

```rust
use sea_orm_migration::prelude::*;

/// Migration that drops the deprecated `status` column from the `advisory` table,
/// which was superseded by the `severity` enum field.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drops the `advisory.status` column.
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

    /// Re-adds `advisory.status` as a nullable string column to allow rollback.
    /// Data previously stored in the column is not restored.
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

/// Identifiers for the `advisory` table columns touched by this migration.
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}
```

Notes:
- The `Advisory` Iden enum is declared locally (frozen at migration time) rather than imported
  from `entity` — the entity no longer has a `Status` column, and migrations must not depend on
  evolving entity code. Before finalizing, `find_symbol("Advisory")` in `migration/src` is run; if
  `m0001_initial` exposes a `pub` `Advisory` Iden enum that contains `Status`, follow whichever
  pattern m0001 establishes (sibling convention) — the expected SeaORM convention is per-migration
  local enums.
- Imports and `async_trait` usage mirror m0001 exactly (if m0001 uses `#[async_trait::async_trait]`
  vs `use sea_orm_migration::async_trait`, match it).

## Tests (in the same file, in scope)

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use crate::Migrator;
    use sea_orm::{ConnectionTrait, Statement};
    use sea_orm_migration::MigratorTrait;

    /// Returns (data_type, is_nullable) for advisory.status, or None if the column is absent.
    async fn status_column(db: &sea_orm::DatabaseConnection) -> Option<(String, String)> {
        let row = db
            .query_one(Statement::from_string(
                db.get_database_backend(),
                "SELECT data_type, is_nullable FROM information_schema.columns \
                 WHERE table_name = 'advisory' AND column_name = 'status'",
            ))
            .await
            .expect("query information_schema");
        row.map(|r| {
            (
                r.try_get::<String>("", "data_type").unwrap(),
                r.try_get::<String>("", "is_nullable").unwrap(),
            )
        })
    }

    /// Verifies that applying all migrations removes the status column from advisory.
    #[tokio::test]
    async fn test_up_drops_advisory_status() {
        // Given a fresh test database
        let db = test_db().await; // project test-DB helper, per CONVENTIONS.md

        // When all migrations are applied
        Migrator::up(&db, None).await.expect("migrate up");

        // Then advisory.status no longer exists
        assert_eq!(status_column(&db).await, None);
    }

    /// Verifies that rolling back m0002 re-adds status as a nullable varchar column.
    #[tokio::test]
    async fn test_down_readds_advisory_status_nullable() {
        // Given a database with all migrations applied
        let db = test_db().await;
        Migrator::up(&db, None).await.expect("migrate up");

        // When the latest migration (m0002) is rolled back
        Migrator::down(&db, Some(1)).await.expect("migrate down");

        // Then advisory.status exists as a nullable character varying column
        assert_eq!(
            status_column(&db).await,
            Some(("character varying".to_string(), "YES".to_string()))
        );
    }
}
```

`test_db()` = the project's existing PostgreSQL test-database bootstrap helper (identified in
Step 4 from CONVENTIONS.md / `tests/` crate); no new helper is invented if one exists.
