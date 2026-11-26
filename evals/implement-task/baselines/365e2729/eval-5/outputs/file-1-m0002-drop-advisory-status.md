# File 1 (Create): `migration/src/m0002_drop_advisory_status/mod.rs`

Follows the sibling pattern in `migration/src/m0001_initial/mod.rs`: a `Migration` unit struct
deriving `DeriveMigrationName`, an `#[async_trait::async_trait] impl MigrationTrait` with `up` and
`down`, and a module-local `DeriveIden` enum for table/column identifiers.

## Full content

```rust
//! Migration that drops the deprecated `status` column from the `advisory` table.
//!
//! The column was superseded by the `severity` enum field and is no longer read or
//! written by any service or entity code.

use sea_orm_migration::prelude::*;

/// Drops `advisory.status`; rollback re-adds it as a nullable string.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Removes the deprecated `status` column from the `advisory` table.
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

    /// Re-adds the `status` column as a nullable string so the migration can be rolled back.
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
    /// The `advisory` table.
    Table,
    /// The deprecated `status` column.
    Status,
}

#[cfg(test)]
mod tests {
    use crate::Migrator;
    use sea_orm::{ConnectionTrait, DatabaseConnection, FromQueryResult, Statement};
    use sea_orm_migration::MigratorTrait;

    /// Column metadata for `advisory.status` read from `information_schema`.
    #[derive(Debug, PartialEq, Eq, FromQueryResult)]
    struct ColumnInfo {
        data_type: String,
        is_nullable: String,
    }

    /// Returns the metadata of `advisory.status`, or `None` when the column does not exist.
    async fn status_column(db: &DatabaseConnection) -> Option<ColumnInfo> {
        ColumnInfo::find_by_statement(Statement::from_string(
            db.get_database_backend(),
            "SELECT data_type, is_nullable FROM information_schema.columns \
             WHERE table_name = 'advisory' AND column_name = 'status'",
        ))
        .one(db)
        .await
        .expect("query information_schema")
    }

    /// Verifies that applying all migrations removes the `status` column from `advisory`.
    #[tokio::test]
    async fn up_drops_advisory_status_column() {
        // Given a fresh test database
        let db = test_db().await;

        // When all migrations are applied
        Migrator::up(&db, None).await.expect("migrations apply");

        // Then the advisory.status column no longer exists
        assert_eq!(status_column(&db).await, None);
    }

    /// Verifies that rolling back m0002 re-adds `status` as a nullable varchar column.
    #[tokio::test]
    async fn down_restores_nullable_status_column() {
        // Given a database with all migrations applied
        let db = test_db().await;
        Migrator::up(&db, None).await.expect("migrations apply");

        // When the latest migration (m0002) is rolled back
        Migrator::down(&db, Some(1)).await.expect("rollback succeeds");

        // Then advisory.status exists again as a nullable string column
        assert_eq!(
            status_column(&db).await,
            Some(ColumnInfo {
                data_type: "character varying".to_string(),
                is_nullable: "YES".to_string(),
            })
        );
    }
}
```

## Notes

- `test_db()` refers to the project's existing PostgreSQL test-database bootstrap helper
  (as used by `tests/api/*.rs`); the exact helper name/import would be confirmed with
  `mcp__serena_backend__search_for_pattern` before writing. If the migration crate has no
  access to such a helper (dev-dependency), the up/down assertions would move to the
  integration test crate — which would require user approval as an out-of-scope file.
- The `Advisory` iden enum is intentionally local: m0001's iden enum is private and
  migrations should stay self-contained/frozen; this matches standard SeaORM practice.
- Value-based assertions (`assert_eq!` on the exact column metadata) are used instead of
  existence/count checks, per skill guidance.
