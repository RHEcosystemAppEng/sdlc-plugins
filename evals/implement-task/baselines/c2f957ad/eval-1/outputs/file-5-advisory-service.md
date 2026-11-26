# File 5 (MODIFY): `modules/fundamental/src/advisory/service/advisory.rs`

Add `severity_summary` to `AdvisoryService`, following the `fetch`/`list` signature pattern
(`&self, <args>, tx: &Transactional<'_>`), inserted after `fetch` via `insert_after_symbol`.

## New imports (merged into existing `use` groups)
```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use sea_orm::{ColumnTrait, EntityTrait, JoinType, QueryFilter, QuerySelect, RelationTrait};
use trustify_entity::{advisory, sbom, sbom_advisory};
```
(Only those not already imported.)

## New method
```rust
impl AdvisoryService {
    // ... existing fetch / list / search ...

    /// Counts unique advisories linked to an SBOM, grouped by severity level.
    ///
    /// Returns `Ok(None)` when the SBOM does not exist so the endpoint can respond with 404.
    /// Advisories linked to the SBOM multiple times are counted once (deduplicated by advisory ID).
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<Option<SeveritySummary>, Error> {
        let connection = self.db.connection(tx);

        // Ensure the SBOM exists, matching 404 behavior of the SBOM endpoints.
        let sbom_exists = sbom::Entity::find_by_id(sbom_id.clone())
            .one(&connection)
            .await
            .context("failed to look up SBOM")?
            .is_some();
        if !sbom_exists {
            return Ok(None);
        }

        // One query: distinct advisories linked to this SBOM with their severity.
        let rows: Vec<(Uuid, Option<String>)> = advisory::Entity::find()
            .select_only()
            .column(advisory::Column::Id)
            .column(advisory::Column::Severity)
            .join(JoinType::InnerJoin, advisory::Relation::SbomAdvisory.def())
            .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
            .distinct()
            .into_tuple()
            .all(&connection)
            .await
            .context("failed to load advisories for SBOM")?;

        let mut summary = SeveritySummary::default();
        for (_advisory_id, severity) in &rows {
            summary.record(severity.as_deref());
        }

        Ok(Some(summary))
    }
}
```

## Notes
- Signature exactly as in Implementation Notes: `&self, sbom_id: Id, tx: &Transactional<'_>`.
- Connection acquisition (`self.db.connection(tx)`), error type (`Error`), and the `Id` -> column
  conversion are copied from `fetch`; snippet shows intended shape. `Id`/`Uuid` handling matches how
  `fetch` resolves IDs.
- Deduplication: `DISTINCT advisory.id` at the DB level; filtering by `sbom_id` happens in SQL
  (query-scope check: no full-table load).
- Performance: two indexed queries total regardless of advisory count (no N+1); bucketing is O(n) in
  memory -> comfortably under 200ms for 500 advisories.
- Alternative considered: `GROUP BY severity` with `COUNT(DISTINCT advisory.id)` in SQL. Equivalent;
  chosen approach keeps case-insensitive bucketing in one tested place (`SeveritySummary::record`).
  Either is acceptable; pick whichever matches sibling query style in `common/src/db/query.rs`.
- Severity source: the `severity` column surfaced by `AdvisorySummary.severity` (`model/summary.rs`).
  If it is an enum type, select it as that type and pass to `record`.
- Additive change only — no existing callers affected (`find_referencing_symbols` on `AdvisoryService`).
