// SYNTHETIC TEST DATA — Advisory handler with missing index query (F3) and deep chain (F4)
use sea_orm::*;

pub async fn get_advisories(
    db: &DatabaseConnection,
    pkg_id: i32,
) -> Result<Vec<Advisory>, DbErr> {
    // F3: Missing Index — WHERE filter on package_id without index
    // F4: Deep Service Chain — 3-level handler -> service -> enrichment
    let pkg = package::Entity::find_by_id(pkg_id).one(&db).await?;
    let advisories = advisory_service::resolve_advisories(&db, &pkg).await?;
    let enriched = enrichment_service::enrich(&db, &advisories).await?;
    Ok(enriched)
}

struct Advisory;
mod package {
    pub mod Entity {
        pub fn find_by_id(_id: i32) -> FindByIdBuilder {
            FindByIdBuilder
        }
    }
}
mod advisory_service {
    use super::*;
    pub async fn resolve_advisories(
        _db: &DatabaseConnection,
        _pkg: &Option<PackageModel>,
    ) -> Result<Vec<Advisory>, DbErr> {
        Ok(vec![])
    }
}
mod enrichment_service {
    use super::*;
    pub async fn enrich(
        _db: &DatabaseConnection,
        _advisories: &Vec<Advisory>,
    ) -> Result<Vec<Advisory>, DbErr> {
        Ok(vec![])
    }
}
struct PackageModel;
struct FindByIdBuilder;
impl FindByIdBuilder {
    async fn one(self, _db: &DatabaseConnection) -> Result<Option<PackageModel>, DbErr> {
        Ok(None)
    }
}
