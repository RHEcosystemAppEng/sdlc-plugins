// SYNTHETIC TEST DATA — Backend handler with planted anti-patterns for eval
// PLANTED ANTI-PATTERN: Step 7.6.2 enhancement — Recursive CTE Risk Flagging
//
// This handler uses a WITH RECURSIVE query on item_relates_to_item,
// which is a junction/relationship table (compound PK with 2 FK columns).
// The depth limit is 50, which the skill should detect as Medium severity
// (junction table + depth limit present).

use actix_web::{get, web, HttpResponse, Responder};
use sea_orm::*;
use uuid::Uuid;

#[get("/api/v2/components/{id}/ancestors")]
pub async fn get_ancestors(
    db: web::Data<DatabaseConnection>,
    path: web::Path<Uuid>,
) -> actix_web::Result<impl Responder> {
    let component_id = path.into_inner();

    let sql = r#"
WITH RECURSIVE ancestors AS (
    SELECT
        p.parent_id,
        p.child_id,
        p.relationship,
        1 AS depth,
        ARRAY[p.child_id] AS visited
    FROM item_relates_to_item p
    WHERE p.child_id = $1
      AND p.relationship != 'ancestor_of'

    UNION ALL

    SELECT
        p.parent_id,
        p.child_id,
        p.relationship,
        a.depth + 1,
        a.visited || p.child_id
    FROM item_relates_to_item p
    JOIN ancestors a ON p.child_id = a.parent_id
    WHERE a.depth < 50
      AND NOT (p.child_id = ANY(a.visited))
)
SELECT DISTINCT parent_id, child_id, relationship
FROM ancestors
ORDER BY parent_id
"#;

    let result = ItemRelation::find_by_statement(Statement::from_sql_and_values(
        DatabaseBackend::Postgres,
        sql,
        [component_id.into()],
    ))
    .all(db.get_ref())
    .await
    .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    Ok(HttpResponse::Ok().json(result))
}
