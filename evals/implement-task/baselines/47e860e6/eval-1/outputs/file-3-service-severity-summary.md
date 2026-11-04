# File 3 — MODIFY `modules/fundamental/src/advisory/service/advisory.rs`

Add `severity_summary` to `AdvisoryService`, inserted after `list` via `mcp__serena_backend__insert_after_symbol` (name_path `AdvisoryService/list`). Signature mirrors `fetch`/`list`.

Before writing: `find_referencing_symbols` not needed (new symbol); `find_symbol AdvisoryService/fetch include_body=true` to copy the connection/transaction idiom; grep for existing severity aggregation helpers to avoid duplication.

## New imports

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use sea_orm::{ColumnTrait, EntityTrait, QueryFilter, QuerySelect, JoinType, RelationTrait, FromQueryResult};
use trustify_entity::{advisory, sbom, sbom_advisory};
```
(only those not already imported)

## New method

```rust
impl AdvisoryService {
    // ... existing fetch, list, search ...

    /// Aggregates unique advisories linked to the given SBOM into per-severity counts.
    ///
    /// Returns `Ok(None)` when the SBOM does not exist so the endpoint can respond 404.
    /// Advisories linked more than once to the SBOM are counted once.
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<Option<SeveritySummary>, Error> {
        let connection = self.db.connection(tx);

        // 404 semantics: verify the SBOM exists first (same lookup as SbomService::fetch)
        if sbom::Entity::find_by_id(sbom_id)
            .one(&connection)
            .await
            .context("failed to look up SBOM")?
            .is_none()
        {
            return Ok(None);
        }

        /// Row produced by the grouped severity count query.
        #[derive(FromQueryResult)]
        struct SeverityCount {
            severity: Option<Severity>,
            count: i64,
        }

        // Single grouped query; COUNT(DISTINCT advisory.id) dedups repeated sbom_advisory links
        let rows = sbom_advisory::Entity::find()
            .select_only()
            .join(JoinType::InnerJoin, sbom_advisory::Relation::Advisory.def())
            .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
            .column_as(advisory::Column::Severity, "severity")
            .column_as(advisory::Column::Id.count_distinct(), "count")
            .group_by(advisory::Column::Severity)
            .into_model::<SeverityCount>()
            .all(&connection)
            .await
            .context("failed to aggregate advisory severities for SBOM")?;

        let mut summary = SeveritySummary::default();
        for row in rows {
            summary.add(row.severity.as_ref(), row.count.max(0) as u64);
        }

        Ok(Some(summary))
    }
}
```

Notes:
- Column names (`SbomId`, `Severity`) and the relation name are confirmed against `entity/src/sbom_advisory.rs` and `entity/src/advisory.rs` before writing. If severity lives only on the `AdvisorySummary` model (derived, not a column), fall back to selecting distinct advisory IDs and building `AdvisorySummary` via the existing conversion, then counting — still one query, deduped with `.distinct()`.
- Since each advisory has one severity, grouping by severity with `COUNT(DISTINCT id)` produces a deduped `total` equal to the sum of groups.
- Error type/`.context()` style matches `fetch`/`list` and `common/src/error.rs`.
- Performance: one indexed query on `sbom_advisory.sbom_id` + one PK lookup — well within 200ms for 500 advisories.
