// SYNTHETIC TEST DATA — Backend handlers with over-fetching (F1) and unused JOIN (F5)
use sea_orm::*;

pub async fn list_packages(db: &DatabaseConnection) -> Result<Vec<PackageModel>, DbErr> {
    // F5: Unused LEFT JOIN — handler only returns name and version from packages table
    let packages = package::Entity::find()
        .find_also_related(package_metadata::Entity)
        .all(db)
        .await?;

    Ok(packages.into_iter().map(|(pkg, _meta)| pkg).collect())
}

pub async fn get_package_with_advisories(
    db: &DatabaseConnection,
    pkg_id: i32,
) -> Result<Vec<AdvisoryModel>, DbErr> {
    // F1: Over-Fetching — returns full Advisory model with 12 fields
    let advisories = advisory::Entity::find()
        .filter(advisory::Column::PackageId.eq(pkg_id))
        .all(db)
        .await?;

    Ok(advisories)
}
