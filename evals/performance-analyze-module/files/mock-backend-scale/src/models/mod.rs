// SYNTHETIC TEST DATA — Model stubs for eval fixture
use sea_orm::entity::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Serialize, Deserialize)]
#[sea_orm(table_name = "component")]
pub struct ComponentModel {
    #[sea_orm(primary_key)]
    pub id: Uuid,
    pub name: String,
    pub version: String,
    pub sbom_id: Uuid,
}

#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Serialize, Deserialize)]
#[sea_orm(table_name = "sbom_node")]
pub struct SbomNodeModel {
    #[sea_orm(primary_key)]
    pub sbom_id: Uuid,
    #[sea_orm(primary_key)]
    pub node_id: String,
    pub name: String,
}

#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Serialize, Deserialize)]
#[sea_orm(table_name = "cpe")]
pub struct CpeModel {
    #[sea_orm(primary_key)]
    pub id: Uuid,
    pub vendor: String,
    pub product: String,
    pub version: String,
}

#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Serialize, Deserialize)]
#[sea_orm(table_name = "category")]
pub struct CategoryModel {
    #[sea_orm(primary_key)]
    pub id: Uuid,
    pub name: String,
}

#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Serialize, Deserialize)]
#[sea_orm(table_name = "item_relates_to_item")]
pub struct ItemRelationModel {
    #[sea_orm(primary_key)]
    pub parent_id: Uuid,
    #[sea_orm(primary_key)]
    pub child_id: Uuid,
    pub relationship: String,
}

pub struct PaginatedResults<T> {
    pub items: Vec<T>,
    pub total: usize,
}

pub fn paginate_array<T: Clone>(items: &[T], offset: usize, limit: usize) -> PaginatedResults<T> {
    let total = items.len();
    let end = (offset + limit).min(total);
    PaginatedResults {
        items: items[offset..end].to_vec(),
        total,
    }
}
