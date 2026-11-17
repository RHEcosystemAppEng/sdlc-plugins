// SYNTHETIC TEST DATA — SeaORM migration without index on package_id (F3)
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .create_table(
                Table::create()
                    .table(Advisories::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(Advisories::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(ColumnDef::new(Advisories::PackageId).integer().not_null())
                    .col(ColumnDef::new(Advisories::Title).string().not_null())
                    .to_owned(),
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .drop_table(Table::drop().table(Advisories::Table).to_owned())
            .await
    }
}

#[derive(DeriveIden)]
enum Advisories {
    Table,
    Id,
    PackageId,
    Title,
}
