// SYNTHETIC TEST DATA — Model stubs for false-positive guard eval
use sea_orm::entity::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Serialize, Deserialize)]
#[sea_orm(table_name = "component")]
pub struct ComponentModel {
    #[sea_orm(primary_key)]
    pub id: Uuid,
    pub name: String,
    pub category_id: Uuid,
}

#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Serialize, Deserialize)]
#[sea_orm(table_name = "status_code")]
pub struct StatusCodeModel {
    #[sea_orm(primary_key)]
    pub id: i32,
    pub label: String,
}
