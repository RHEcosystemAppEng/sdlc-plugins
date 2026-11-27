# File 1 (CREATE): `migration/src/m0002_drop_advisory_status/mod.rs`

Purpose: a migration that drops the deprecated `status` column from the `advisory` table, with rollback support. It follows the structure of `migration/src/m0001_initial/mod.rs`.

```rust
use sea_orm_migration::prelude::*;

/// Migration that drops the deprecated `status` column from the `advisory` table.
///
/// The column was superseded by the `severity` enum field and is no longer read or
/// written by any service code. `down` re-adds it as a nullable string for rollback.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drops `advisory.status`.
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

    /// Re-adds `advisory.status` as a nullable string column (data is not restored).
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

#[cfg(test)]
mod tests {
    use super::*;
    use crate::Migrator;
    use sea_orm::{ConnectionTrait, Database, DbBackend, Statement};

    /// Returns (column_name, data_type, is_nullable) rows for the advisory table.
    async fn advisory_columns(db: &sea_orm::DatabaseConnection) -> Vec<(String, String, String)> {
        db.query_all(Statement::from_string(
            DbBackend::Postgres,
            "SELECT column_name, data_type, is_nullable FROM information_schema.columns \
             WHERE table_name = 'advisory' ORDER BY column_name",
        ))
        .await
        .expect("query columns")
        .into_iter()
        .map(|r| (
            r.try_get("", "column_name").unwrap(),
            r.try_get("", "data_type").unwrap(),
            r.try_get("", "is_nullable").unwrap(),
        ))
        .collect()
    }

    /// Verifies the up migration removes the status column from the advisory table.
    #[tokio::test]
    async fn test_up_drops_advisory_status() {
        // Given a fresh test database
        let db = Database::connect(test_db_url()).await.unwrap();
        Migrator::fresh(&db).await.unwrap();

        // When all migrations (including m0002) have been applied
        let columns = advisory_columns(&db).await;

        // Then the status column is absent while severity is still present
        let names: Vec<&str> = columns.iter().map(|c| c.0.as_str()).collect();
        assert!(!names.contains(&"status"), "status still present: {names:?}");
        assert!(names.contains(&"severity"), "severity missing: {names:?}");
    }

    /// Verifies the down migration re-adds status as a nullable string column.
    #[tokio::test]
    async fn test_down_readds_advisory_status() {
        // Given a database with all migrations applied
        let db = Database::connect(test_db_url()).await.unwrap();
        Migrator::fresh(&db).await.unwrap();

        // When the latest migration (m0002) is rolled back
        Migrator::down(&db, Some(1)).await.unwrap();

        // Then status exists again as a nullable character varying column
        let status = advisory_columns(&db)
            .await
            .into_iter()
            .find(|c| c.0 == "status");
        assert_eq!(
            status,
            Some(("status".into(), "character varying".into(), "YES".into()))
        );
    }

    /// Test database URL, taken from the same env var the integration tests use.
    fn test_db_url() -> String {
        std::env::var("DATABASE_URL").expect("DATABASE_URL must be set for migration tests")
    }
}
```

Notes:
- `Advisory` is a local `DeriveIden` enum. It is not imported from m0001, so migrations stay frozen snapshots. It matches m0001's Iden style. If m0001 uses the older `#[derive(Iden)]` or a manual `Iden` impl, I would match that form instead (sibling parity).
- If m0001 uses `#[async_trait::async_trait]` versus a re-exported `async_trait`, I would mirror whichever import path m0001 uses.
- The test helper for the DB URL and connection would reuse whatever helper the repo's tests already use, if one exists (Reuse rule). The `DATABASE_URL` above is a placeholder pending Step 4 inspection.
- Rollback restores the column only, not its historical data. This is documented on `down`.
