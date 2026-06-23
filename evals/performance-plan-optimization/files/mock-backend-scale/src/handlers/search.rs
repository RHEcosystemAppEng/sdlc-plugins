// SYNTHETIC TEST DATA — Backend handler with planted anti-patterns for eval
// PLANTED ANTI-PATTERN: Step 7.6.7 — Cross-Table OR Filter
//
// This handler builds a search query that registers columns from multiple
// entities (sbom_node, cpe, qualified_purl) and applies a bare-value filter
// via filtering_with(). When the user passes q=openssl without a field
// qualifier, the filter generates ILIKE OR conditions across ALL string
// columns from ALL registered entities, including LEFT JOINed tables.
// This defeats index usage on sbom_node.name because PostgreSQL cannot
// use the GIN trigram index when OR spans LEFT JOINed tables.

use actix_web::{get, web, HttpResponse, Responder};
use sea_orm::*;
use sea_query::JoinType;

use crate::models::{SbomNodeModel, CpeModel, PaginatedResults, paginate_array};

fn q_columns() -> Columns {
    sbom_node::Entity
        .columns()
        .add_columns(cpe::Entity.columns())
        .add_columns(qualified_purl::Entity.columns())
}

#[get("/api/v2/analysis/component")]
pub async fn search_component(
    db: web::Data<DatabaseConnection>,
    query: web::Query<SearchQuery>,
    paginated: web::Query<Paginated>,
) -> actix_web::Result<impl Responder> {
    let search_subquery = sbom_node::Entity::find()
        .join(JoinType::Join, sbom_node::Relation::Package.def())
        .join(JoinType::LeftJoin, sbom_package::Relation::Purl.def())
        .join(JoinType::LeftJoin, sbom_package::Relation::Cpe.def())
        .join(JoinType::LeftJoin, sbom_package_cpe_ref::Relation::Cpe.def())
        .join(JoinType::LeftJoin, sbom_package_purl_ref::Relation::Purl.def())
        .select_only()
        .column(sbom_node::Column::SbomId)
        .filtering_with(query.q.clone(), q_columns())?
        .distinct()
        .into_query();

    let results = load_all_matching(db.get_ref(), search_subquery).await?;

    Ok(HttpResponse::Ok().json(results))
}
