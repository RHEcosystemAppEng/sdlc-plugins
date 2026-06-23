// SYNTHETIC TEST DATA — Migration for false-positive guard eval
// FALSE POSITIVE 7.6.4.1: Single-column index + multi-column index on same table
// The single-column index (component_name_idx on name) serves different
// query patterns than the composite index (component_name_category_idx on
// name, category_id). Both are legitimate and NOT redundant.

use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager.create_table(
            Table::create()
                .table(Component::Table)
                .col(ColumnDef::new(Component::Id).uuid().not_null().primary_key())
                .col(ColumnDef::new(Component::Name).string().not_null())
                .col(ColumnDef::new(Component::CategoryId).uuid().not_null())
                .to_owned(),
        ).await?;

        manager.create_table(
            Table::create()
                .table(StatusCode::Table)
                .col(ColumnDef::new(StatusCode::Id).integer().not_null().primary_key())
                .col(ColumnDef::new(StatusCode::Label).string().not_null())
                .to_owned(),
        ).await?;

        // Single-column index: used by queries filtering ONLY on name
        manager.create_index(
            Index::create()
                .name("component_name_idx")
                .table(Component::Table)
                .col(Component::Name)
                .to_owned(),
        ).await?;

        // Composite index: used by queries filtering on name + category_id
        // NOT redundant — serves different query patterns than the single-column index
        manager.create_index(
            Index::create()
                .name("component_name_category_idx")
                .table(Component::Table)
                .col(Component::Name)
                .col(Component::CategoryId)
                .to_owned(),
        ).await?;

        Ok(())
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager.drop_table(Table::drop().table(Component::Table).to_owned()).await?;
        manager.drop_table(Table::drop().table(StatusCode::Table).to_owned()).await?;
        Ok(())
    }
}

#[derive(Iden)]
enum Component { Table, Id, Name, CategoryId }

#[derive(Iden)]
enum StatusCode { Table, Id, Label }
