// SYNTHETIC TEST DATA — SeaORM model with false positive for eval
use sea_orm::entity::prelude::*;

#[derive(Clone, Debug, DeriveEntityModel)]
#[sea_orm(table_name = "products")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: String,
    pub name: String,
    pub description: String,
    pub price: f64,
    pub category: String,
    pub vendor_id: String,
    pub sku: String,
    pub weight_kg: f64,
    pub created_at: DateTimeUtc,
    pub updated_at: DateTimeUtc,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {}

impl ActiveModelBehavior for ActiveModel {}

// FALSE POSITIVE: SeaORM load_one is a batch query (single WHERE id IN (...))
// This is NOT N+1 — it collects all IDs and issues one query
// Step 9.1-B2 should discard this as false positive
pub async fn load_product_vendors(
    db: &DatabaseConnection,
    products: Vec<Model>,
) -> Vec<(Model, Option<VendorModel>)> {
    products
        .load_one(Vendor, db)
        .await
        .unwrap()
        .into_iter()
        .zip(products)
        .map(|(vendor, product)| (product, vendor))
        .collect()
}

// Minimal vendor entity for the load_one call
#[derive(Clone, Debug, DeriveEntityModel)]
#[sea_orm(table_name = "vendors")]
pub struct VendorModel {
    #[sea_orm(primary_key)]
    pub id: String,
    pub name: String,
}
