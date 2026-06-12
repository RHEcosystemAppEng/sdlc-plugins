// SYNTHETIC TEST DATA — Backend handler with planted anti-patterns for eval
use actix_web::{web, HttpResponse};
use sea_orm::{EntityTrait, DatabaseConnection};

use crate::models::product::{Entity as Product, Model as ProductModel};

// PLANTED ANTI-PATTERN: Missing pagination (Step 7.4)
// Returns all products without limit/offset
pub async fn list_products(
    db: web::Data<DatabaseConnection>,
) -> HttpResponse {
    let products: Vec<ProductModel> = Product::find()
        .all(db.get_ref())
        .await
        .unwrap_or_default();

    HttpResponse::Ok().json(products)
}

// PLANTED ANTI-PATTERN: True N+1 query (Step 7.3)
// Sequential query in loop — each iteration hits the database
pub async fn get_product_details(
    db: web::Data<DatabaseConnection>,
    path: web::Path<String>,
) -> HttpResponse {
    let product_id = path.into_inner();
    let product = Product::find_by_id(&product_id)
        .one(db.get_ref())
        .await
        .unwrap();

    if let Some(p) = product {
        // N+1: fetch related items one by one
        let mut related = Vec::new();
        let related_ids = vec!["rel-1", "rel-2", "rel-3", "rel-4", "rel-5"];
        for id in related_ids {
            let item = Product::find_by_id(id)
                .one(db.get_ref())
                .await
                .unwrap();
            if let Some(r) = item {
                related.push(r);
            }
        }
        HttpResponse::Ok().json(serde_json::json!({
            "product": p,
            "related": related
        }))
    } else {
        HttpResponse::NotFound().finish()
    }
}
