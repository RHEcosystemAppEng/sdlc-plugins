# File 3 — MODIFY `modules/fundamental/src/advisory/service/advisory.rs`

**Purpose**: add `AdvisoryService::severity_summary`.

**Inspect first** (Serena `serena_backend`):
- `get_symbols_overview` on the file
- `find_symbol("AdvisoryService/fetch", include_body=true)` and `find_symbol("AdvisoryService/list", include_body=true)` to see how `tx` becomes a connection, and the `.context()` style
- `find_symbol` on `entity::sbom_advisory::{Model, Relation}` and `entity::advisory::Model` for the column names
- `find_symbol("SbomService/fetch", include_body=true)` to copy how a missing SBOM becomes `AppError::NotFound`
- `find_referencing_symbols("AdvisoryService")` to confirm the change is additive and no caller breaks

**Insertion point**: `insert_after_symbol("AdvisoryService/list")` (or after `search`), inside the
existing `impl AdvisoryService`.

**New imports** (only where they are not already present):
`trustify_entity::{sbom, sbom_advisory, advisory}`, `sea_orm::{EntityTrait, QueryFilter, QuerySelect, ColumnTrait, JoinType, RelationTrait, FromQueryResult}`,
`sea_query::Expr`, `crate::advisory::model::severity_summary::SeveritySummary`.

```rust
/// Row returned by the severity aggregation query.
#[derive(Debug, FromQueryResult)]
struct SeverityCountRow {
    severity: Option<String>,
    count: i64,
}

impl AdvisoryService {
    // ... existing fetch / list / search ...

    /// Returns per-severity counts of the unique advisories linked to the given SBOM.
    ///
    /// Returns `AppError::NotFound` if the SBOM does not exist. Advisories linked more than
    /// once through `sbom_advisory` are counted once (`COUNT(DISTINCT advisory.id)`).
    /// Severity levels with no advisories are reported as `0`.
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<SeveritySummary, AppError> {
        let connection = self.db.connection(tx);

        // 404 when the SBOM is unknown, consistent with SbomService::fetch
        sbom::Entity::find_by_id(sbom_id)
            .one(&connection)
            .await
            .context("failed to look up SBOM for advisory severity summary")?
            .ok_or_else(|| AppError::NotFound(format!("SBOM {sbom_id} not found")))?;

        // One aggregate query: sbom_advisory JOIN advisory, grouped by severity,
        // counting distinct advisories to deduplicate repeated links.
        let rows = sbom_advisory::Entity::find()
            .select_only()
            .join(JoinType::InnerJoin, sbom_advisory::Relation::Advisory.def())
            .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
            .column_as(advisory::Column::Severity, "severity")
            .column_as(Expr::col((advisory::Entity, advisory::Column::Id)).count_distinct(), "count")
            .group_by(advisory::Column::Severity)
            .into_model::<SeverityCountRow>()
            .all(&connection)
            .await
            .context("failed to aggregate advisory severities for SBOM")?;

        let mut summary = SeveritySummary::default();
        for row in rows {
            if let Some(severity) = row.severity.as_deref() {
                summary.add(severity, u64::try_from(row.count).unwrap_or_default());
            }
        }
        Ok(summary)
    }
}
```

Design notes:
- **AC #3 (dedup)**: `COUNT(DISTINCT advisory.id)` handles duplicate `sbom_advisory` rows.
- **AC #4 (zeros)**: the starting point is `SeveritySummary::default()`.
- **AC #5 (<200 ms)**: one grouped query (at most 4–5 rows returned) plus a PK lookup. There is no N+1 and no advisory rows are loaded into memory. It relies on an index on `sbom_advisory.sbom_id` (check the migration; if one is missing, flag it, since migrations are out of scope).
- **Defensive access**: a `NULL` severity (`Option<String>`) is skipped and a negative count falls back to 0. Both values come from the DB across a module boundary, so they are guarded.
- The exact connection idiom (`self.db.connection(tx)` vs `tx.connection(&self.db)`), the `Id` → column conversion, and the `AppError::NotFound` variant shape are copied from `fetch` and `common/src/error.rs` as found during inspection. The code above is the planned shape.
- If severity is a DB enum or `Severity` type, the row field uses that type and `SeveritySummary::add` matches on its variants.
- Query scope: filtered by `sbom_id`, so this is not a full-table scan.
