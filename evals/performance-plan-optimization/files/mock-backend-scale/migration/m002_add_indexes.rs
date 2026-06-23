// SYNTHETIC TEST DATA — Valid indexes (non-redundant) to ensure no false positives
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // Valid: GIN trigram index on sbom_node.name (different type from PK btree)
        manager.exec_stmt(
            sea_query::Query::select()
                .expr(sea_query::Expr::cust(
                    "CREATE INDEX sbomnodenameginidx ON sbom_node USING gin ((name) gin_trgm_ops)"
                ))
                .to_owned(),
        ).await?;

        // Valid: index on component.category_id (not a duplicate)
        manager.create_index(
            Index::create()
                .name("component_category_id_idx")
                .table(Component::Table)
                .col(Component::CategoryId)
                .to_owned(),
        ).await?;

        // Valid: index on item_relates_to_item.child_id for reverse lookups
        manager.create_index(
            Index::create()
                .name("item_relates_child_id_idx")
                .table(ItemRelatesToItem::Table)
                .col(ItemRelatesToItem::ChildId)
                .to_owned(),
        ).await?;

        Ok(())
    }

    async fn down(&self, _manager: &SchemaManager) -> Result<(), DbErr> {
        Ok(())
    }
}

#[derive(Iden)]
enum Component { Table, CategoryId }

#[derive(Iden)]
enum ItemRelatesToItem { Table, ChildId }
