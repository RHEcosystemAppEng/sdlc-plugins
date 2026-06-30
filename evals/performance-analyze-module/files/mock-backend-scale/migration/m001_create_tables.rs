// SYNTHETIC TEST DATA — Migration with planted anti-patterns for eval
// PLANTED ANTI-PATTERN: Step 7.6.4.1 — Redundant Index
//
// The sbom_node table has a PRIMARY KEY on (sbom_id, node_id) AND a
// separate btree index on the same columns. The duplicate index wastes
// disk space and buffer cache.

use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager.create_table(
            Table::create()
                .table(SbomNode::Table)
                .col(ColumnDef::new(SbomNode::SbomId).uuid().not_null())
                .col(ColumnDef::new(SbomNode::NodeId).string().not_null())
                .col(ColumnDef::new(SbomNode::Name).string().not_null())
                .primary_key(Index::create().col(SbomNode::SbomId).col(SbomNode::NodeId))
                .to_owned(),
        ).await?;

        // PLANTED: This index duplicates the primary key exactly
        manager.create_index(
            Index::create()
                .name("sbom_node_sbom_id_node_id_idx")
                .table(SbomNode::Table)
                .col(SbomNode::SbomId)
                .col(SbomNode::NodeId)
                .to_owned(),
        ).await?;

        // item_relates_to_item — junction table for recursive CTE detection
        manager.create_table(
            Table::create()
                .table(ItemRelatesToItem::Table)
                .col(ColumnDef::new(ItemRelatesToItem::ParentId).uuid().not_null())
                .col(ColumnDef::new(ItemRelatesToItem::ChildId).uuid().not_null())
                .col(ColumnDef::new(ItemRelatesToItem::Relationship).string().not_null())
                .primary_key(
                    Index::create()
                        .col(ItemRelatesToItem::ParentId)
                        .col(ItemRelatesToItem::ChildId)
                )
                .to_owned(),
        ).await?;

        manager.create_table(
            Table::create()
                .table(Component::Table)
                .col(ColumnDef::new(Component::Id).uuid().not_null().primary_key())
                .col(ColumnDef::new(Component::Name).string().not_null())
                .col(ColumnDef::new(Component::Version).string().not_null())
                .col(ColumnDef::new(Component::CategoryId).uuid().not_null())
                .col(ColumnDef::new(Component::Active).boolean().not_null().default(true))
                .to_owned(),
        ).await?;

        Ok(())
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager.drop_table(Table::drop().table(SbomNode::Table).to_owned()).await?;
        manager.drop_table(Table::drop().table(ItemRelatesToItem::Table).to_owned()).await?;
        manager.drop_table(Table::drop().table(Component::Table).to_owned()).await?;
        Ok(())
    }
}

#[derive(Iden)]
enum SbomNode { Table, SbomId, NodeId, Name }

#[derive(Iden)]
enum ItemRelatesToItem { Table, ParentId, ChildId, Relationship }

#[derive(Iden)]
enum Component { Table, Id, Name, Version, CategoryId, Active }
