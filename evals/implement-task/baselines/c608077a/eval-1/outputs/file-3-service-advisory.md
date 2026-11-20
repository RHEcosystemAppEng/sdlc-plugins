# File 3 — MODIFY `modules/fundamental/src/advisory/service/advisory.rs`

Add `severity_summary` to `AdvisoryService`, following the signature pattern of `fetch`/`list` (`&self`, key, `tx: &Transactional<'_>`).

Pre-checks (Step 4):
- `find_symbol("AdvisoryService", include_body=true)` to confirm how `fetch` obtains a connection (`self.db.connection(tx)`) and what error type it returns.
- `find_referencing_symbols` not needed for existing symbols (pure addition, no signature changes).
- Grep `fundamental` crate for an existing "sbom exists" helper (e.g. `SbomService::fetch`). Reuse the entity `find_by_id` pattern used there; do not duplicate a helper.

## Added imports

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use entity::{advisory, sbom, sbom_advisory};
use sea_orm::{ColumnTrait, EntityTrait, QueryFilter, QuerySelect, RelationTrait, JoinType};
```
(only those not already imported)

## Added method (inside `impl AdvisoryService`)

```rust
    /// Aggregates unique advisories linked to the given SBOM into per-severity counts.
    ///
    /// Returns `Error::NotFound` if the SBOM does not exist. Advisories linked to the
    /// SBOM more than once via `sbom_advisory` are counted once.
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<SeveritySummary, Error> {
        let connection = self.db.connection(tx);

        // 404 when the SBOM does not exist, consistent with GET /api/v2/sbom/{id}
        sbom::Entity::find_by_id(sbom_id)
            .one(&connection)
            .await
            .context("failed to look up SBOM")?
            .ok_or(Error::NotFound(format!("SBOM {sbom_id}")))?;

        // One query: distinct (advisory id, severity) pairs linked to the SBOM.
        // DISTINCT deduplicates repeated sbom_advisory links in the database.
        let rows: Vec<(Id, Option<Severity>)> = sbom_advisory::Entity::find()
            .select_only()
            .column(advisory::Column::Id)
            .column(advisory::Column::Severity)
            .join(JoinType::InnerJoin, sbom_advisory::Relation::Advisory.def())
            .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
            .distinct()
            .into_tuple()
            .all(&connection)
            .await
            .context("failed to query advisories for SBOM")?;

        let summary = rows
            .iter()
            .fold(SeveritySummary::default(), |mut acc, (_, severity)| {
                acc.record(severity.as_ref());
                acc
            });

        Ok(summary)
    }
```

Notes:
- Error type/`NotFound` variant names are matched to what `fetch` uses (verified via Serena); `.context()` wrapping per `common/src/error.rs`.
- Selecting the advisory id alongside severity in a DISTINCT query ensures dedup is by advisory ID (two distinct advisories with the same severity are both counted).
- Query is scoped by `sbom_id` (query-scope verification) and is a single round trip; performance target (<200ms @ 500 advisories) met by the join on the indexed `sbom_advisory.sbom_id` column. If no such index exists, flag it (migration is out of scope).
- `severity` column name/type are taken from `entity/src/advisory.rs`; if severity lives only on the `AdvisorySummary` model (derived from another column), select that column instead and map with the same conversion the `list` method uses.
