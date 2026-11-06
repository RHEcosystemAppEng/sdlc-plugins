# File 1 (MODIFY): `modules/fundamental/src/advisory/service/advisory.rs`

## Purpose
Add a `severity_summary` method to `AdvisoryService`, using the same signature pattern as `fetch` and `list`
(`&self, <id>: Id, tx: &Transactional<'_>`).

## Pre-checks (Serena)
- `find_symbol("AdvisoryService/fetch", include_body=true)`: copy the connection idiom (`self.db.connection(tx)`)
  and the error type (`Error` / `anyhow::Error`)
- `find_symbol("AdvisorySummary", include_body=true)`: confirm the type of the `severity` field and which entity
  column backs it (`entity::advisory::Column::Severity`)
- `find_referencing_symbols("AdvisoryService")`: the change is purely additive, so no callers are affected

## Imports to add (merged into existing groups)
```rust
use sea_orm::{ColumnTrait, EntityTrait, QueryFilter, QuerySelect, JoinType, RelationTrait, FromQueryResult};
use sea_query::{Expr, Func};
use trustify_entity::{advisory, sbom, sbom_advisory};
use crate::advisory::model::severity_summary::SeveritySummary;
```
(Only the imports that aren't already present get added.)

## Code to add (inserted after `fetch`/`list` via `insert_after_symbol`)
```rust
/// Row produced by the severity aggregation query.
#[derive(Debug, FromQueryResult)]
struct SeverityCount {
    severity: Option<String>,
    count: i64,
}

impl AdvisoryService {
    /// Aggregates the unique advisories linked to an SBOM by severity level.
    ///
    /// Returns `Ok(None)` when the SBOM does not exist, so the endpoint can respond 404.
    /// Advisories linked more than once to the same SBOM are counted once
    /// (`COUNT(DISTINCT advisory.id)`). Advisories with a missing or unrecognized
    /// severity count toward `total` but not toward any level.
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<Option<SeveritySummary>, Error> {
        let connection = self.db.connection(tx);

        // Existence check: the same lookup SbomService::fetch performs.
        if sbom::Entity::find_by_id(sbom_id)
            .one(&connection)
            .await
            .context("failed to look up SBOM")?
            .is_none()
        {
            return Ok(None);
        }

        // One grouped aggregate query scoped to this SBOM, with no N+1 and no row loading.
        let rows = sbom_advisory::Entity::find()
            .select_only()
            .join(JoinType::InnerJoin, sbom_advisory::Relation::Advisory.def())
            .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
            .column_as(Func::lower(Expr::col((advisory::Entity, advisory::Column::Severity))), "severity")
            .column_as(Expr::col((advisory::Entity, advisory::Column::Id)).count_distinct(), "count")
            .group_by(Func::lower(Expr::col((advisory::Entity, advisory::Column::Severity))))
            .into_model::<SeverityCount>()
            .all(&connection)
            .await
            .context("failed to aggregate advisory severities")?;

        let mut summary = SeveritySummary::default();
        for row in rows {
            let count = u64::try_from(row.count).unwrap_or_default();
            summary.total += count;
            match row.severity.as_deref() {
                Some("critical") => summary.critical += count,
                Some("high") => summary.high += count,
                Some("medium") => summary.medium += count,
                Some("low") => summary.low += count,
                // Unknown or missing severity: included in total only.
                _ => {}
            }
        }

        Ok(Some(summary))
    }
}
```

## Notes
- If `AdvisorySummary.severity` is an enum (e.g. `Severity::Critical`) rather than a string, the `match` uses that
  existing enum's variants, and the `lower()` call is dropped. No new severity type is declared (symbol deduplication).
- Grouping by severity with `COUNT(DISTINCT id)` deduplicates within each bucket. An advisory has exactly one
  severity, so the sum across buckets is also the distinct count, which makes `total` correct.
- `Id` conversion: if `Id` is an enum wrapping a UUID (as in trustify), use the same `match`/`try_as_uid()` helper
  `fetch` uses to build the filter condition.
- Methods are added to the existing `impl AdvisoryService` block. The separate `impl` above is only for readability.
