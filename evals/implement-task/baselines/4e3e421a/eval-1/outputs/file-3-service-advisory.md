# File 3 (MODIFY): `modules/fundamental/src/advisory/service/advisory.rs`

Add `severity_summary` to `AdvisoryService`, following the signature pattern of `fetch` / `list`
(`&self, <id>, tx: &Transactional<'_>`). Inserted with `mcp__serena_backend__insert_after_symbol`
after `AdvisoryService/list` (or the last method in the impl).

## Imports to add (merge with existing groups)

```rust
use sea_orm::{ColumnTrait, EntityTrait, JoinType, QueryFilter, QuerySelect, RelationTrait};
use trustify_entity::{advisory, sbom, sbom_advisory};
use crate::advisory::model::severity_summary::SeveritySummary;
```
(Only the items not already imported; exact crate paths copied from existing imports in the file.)

## New method

```rust
    /// Aggregates unique advisories linked to an SBOM into counts per severity level.
    ///
    /// Returns `AppError::NotFound` when the SBOM does not exist. Advisories linked to the
    /// SBOM more than once are counted once (deduplicated by advisory ID). Severity levels
    /// with no advisories are reported as 0.
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<SeveritySummary, AppError> {
        let connection = self.db.connection(tx);

        // 404 when the SBOM does not exist, consistent with GET /api/v2/sbom/{id}
        let sbom_exists = sbom::Entity::find_by_id(sbom_id)
            .one(&connection)
            .await
            .context("failed to look up SBOM for advisory severity summary")?
            .is_some();
        if !sbom_exists {
            return Err(AppError::NotFound(format!("SBOM {sbom_id} not found")));
        }

        // One query: unique advisories linked to this SBOM, with their severity
        let rows: Vec<(Id, Option<String>)> = advisory::Entity::find()
            .select_only()
            .column(advisory::Column::Id)
            .column(advisory::Column::Severity)
            .join(JoinType::InnerJoin, advisory::Relation::SbomAdvisory.def())
            .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
            .distinct()
            .into_tuple()
            .all(&connection)
            .await
            .context("failed to query advisories linked to SBOM")?;

        let summary = rows
            .iter()
            .fold(SeveritySummary::default(), |mut summary, (_, severity)| {
                summary.record(severity.as_deref());
                summary
            });

        Ok(summary)
    }
```

## Notes
- `self.db.connection(tx)`, `Id` type, the `AppError::NotFound` variant, and the `.context()` extension trait are taken exactly from how `fetch` is written in this file / `common/src/error.rs`; adjust names if they differ (e.g. if `fetch` returns `Option` and the handler maps to 404, the existence check stays here because the task requires 404 for unknown SBOMs specifically).
- `DISTINCT` on `(advisory.id, advisory.severity)` is equivalent to dedup by advisory ID since severity is a column of the advisory row.
- Relation name (`advisory::Relation::SbomAdvisory`) verified against `entity/src/advisory.rs` / `entity/src/sbom_advisory.rs`; if only the reverse relation exists, start the query from `sbom_advisory::Entity` and join `advisory`.
- If `AdvisorySummary.severity` is a typed enum, the tuple uses that type instead of `Option<String>` and `SeveritySummary::record` matches on it.
- Performance: one SBOM lookup by primary key + one join filtered on `sbom_advisory.sbom_id` (indexed FK); ≤500 rows folded in memory — well within 200ms.
