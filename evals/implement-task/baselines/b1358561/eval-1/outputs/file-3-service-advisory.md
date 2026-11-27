# File 3 (MODIFY): `modules/fundamental/src/advisory/service/advisory.rs`

Add `severity_summary` to `AdvisoryService`, placed after `fetch`/`list`, same signature
style (`&self, <args>, tx: &Transactional<'_>`).

Before editing: `find_referencing_symbols` on `AdvisoryService` (no existing signatures
change, so callers are unaffected); `find_symbol` with body on `fetch` to copy the
connection/error idioms.

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use sea_orm::{ColumnTrait, EntityTrait, QueryFilter, QuerySelect, JoinType, RelationTrait};
use trustify_entity::{advisory, sbom, sbom_advisory};

impl AdvisoryService {
    // ... existing fetch / list / search ...

    /// Aggregates severity counts of the unique advisories linked to an SBOM.
    ///
    /// Returns `Ok(None)` when the SBOM does not exist (the endpoint maps this to 404),
    /// otherwise a `SeveritySummary` where every level defaults to 0. Advisories linked
    /// to the SBOM multiple times via `sbom_advisory` are counted once.
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<Option<SeveritySummary>, Error> {
        let connection = self.db.connection(tx);

        // 404 semantics: verify the SBOM exists, same as SbomService::fetch.
        if sbom::Entity::find_by_id(sbom_id)
            .one(&connection)
            .await
            .context("failed to look up SBOM")?
            .is_none()
        {
            return Ok(None);
        }

        // One query: unique advisories linked to the SBOM with their severity.
        // DISTINCT on advisory id deduplicates repeated join rows.
        let rows: Vec<(Uuid, Option<String>)> = sbom_advisory::Entity::find()
            .select_only()
            .column(advisory::Column::Id)
            .column(advisory::Column::Severity)
            .join(JoinType::InnerJoin, sbom_advisory::Relation::Advisory.def())
            .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
            .distinct()
            .into_tuple()
            .all(&connection)
            .await
            .context("failed to load advisories for SBOM")?;

        let mut summary = SeveritySummary::default();
        for (_id, severity) in &rows {
            summary.record(severity.as_deref());
        }
        Ok(Some(summary))
    }
}
```

Design notes:
- Filtering happens in the DB (`sbom_id = ?`, DISTINCT) — not loading all advisories (Query scope check).
- Single indexed join query keeps the 500-advisory case well under 200ms; alternative is
  `GROUP BY severity` with `COUNT(DISTINCT advisory.id)` if siblings use aggregate queries
  in `common/src/db/query.rs` — prefer that helper if one exists (Reuse rule).
- Column/relation names (`Severity`, `Relation::Advisory`, `SbomId`) to be confirmed via
  `find_symbol` on `entity/src/sbom_advisory.rs` and `entity/src/advisory.rs`; the
  severity value source matches `AdvisorySummary.severity`.
- Errors wrapped with `.context(...)`, matching `common/src/error.rs` usage.
