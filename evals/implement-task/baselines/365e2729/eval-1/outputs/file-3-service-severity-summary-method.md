# File 3 (MODIFY): `modules/fundamental/src/advisory/service/advisory.rs`

## Purpose
Add `AdvisoryService::severity_summary`, which aggregates the severity counts of unique advisories
linked to an SBOM.

## Pre-edit inspection (Serena)
- `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/service/advisory.rs")`
- `mcp__serena_backend__find_symbol("AdvisoryService/fetch", include_body=true)` and
  `AdvisoryService/list`, to copy the signature, the DB-connection access and the error style.
- `mcp__serena_backend__find_symbol("Model", relative_path="entity/src/sbom_advisory.rs", include_body=true)`
  to confirm the join columns (`sbom_id`, `advisory_id`) and the `Relation` definitions.
- `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` to see how `severity`
  is sourced from `entity::advisory`.
- `mcp__serena_backend__search_for_pattern("severity")` across `modules/` and `common/` for any
  existing severity aggregation or enum helper, so it can be reused.
- `find_referencing_symbols` is not needed. The change only adds a method and does not modify
  existing symbols.

## Change: new method on `impl AdvisoryService` (inserted after `list`, via `insert_after_symbol`)

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use sea_orm::{ColumnTrait, EntityTrait, QueryFilter, QuerySelect, RelationTrait, JoinType};
use trustify_entity::{advisory, sbom, sbom_advisory};

impl AdvisoryService {
    // ... existing fetch / list / search ...

    /// Aggregates the severity counts of all unique advisories linked to the given SBOM.
    ///
    /// Returns `Ok(None)` when no SBOM with `sbom_id` exists, so the endpoint can answer 404.
    /// Advisories linked to the SBOM more than once are counted once, because results are
    /// deduplicated by advisory ID. Severity levels with no advisories are reported as 0.
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<Option<SeveritySummary>, Error> {
        let connection = self.db.connection(tx);

        // Make sure the SBOM exists so a missing SBOM gives 404, not an all-zero summary.
        let sbom_exists = sbom::Entity::find_by_id(sbom_id.try_as_uid()?)
            .one(&connection)
            .await?
            .is_some();
        if !sbom_exists {
            return Ok(None);
        }

        // Fetch (advisory_id, severity) for every advisory linked to the SBOM.
        // DISTINCT on the advisory ID drops duplicate links in the database, so the response
        // only carries the small aggregated payload, even for SBOMs with 500+ advisories.
        let rows: Vec<(Uuid, Option<String>)> = sbom_advisory::Entity::find()
            .select_only()
            .column(advisory::Column::Id)
            .column(advisory::Column::Severity)
            .join(JoinType::InnerJoin, sbom_advisory::Relation::Advisory.def())
            .filter(sbom_advisory::Column::SbomId.eq(sbom_id.try_as_uid()?))
            .distinct()
            .into_tuple()
            .all(&connection)
            .await?;

        let summary = rows
            .iter()
            .fold(SeveritySummary::default(), |mut acc, (_, severity)| {
                acc.record(severity.as_deref());
                acc
            });

        Ok(Some(summary))
    }
}
```

## Design notes
- **Signature** follows the `fetch`/`list` pattern from Implementation Notes:
  `&self, sbom_id: Id, tx: &Transactional<'_>`.
- **Option for not-found**: this mirrors `fetch`, which returns `Option<T>` and leaves the 404
  decision to the handler (the same pattern `SbomService::fetch` uses for `/api/v2/sbom/{id}`).
- **Deduplication**: `SELECT DISTINCT advisory.id, advisory.severity` over the
  `sbom_advisory` join (`entity/src/sbom_advisory.rs`) means a repeated link counts once.
- **Severity source**: this uses the same `advisory` column that backs `AdvisorySummary.severity`
  (`model/summary.rs`). Before finalizing, confirm the column name and type with `find_symbol`.
  If `AdvisorySummary` computes severity some other way (e.g. from a related score table), reuse
  that conversion rather than duplicating it.
- **Defensive access**: severity is treated as `Option<String>` (it may be NULL in the DB), and
  `record(None)` adds to `total` only.
- **Performance (< 200 ms for 500 advisories)**: one indexed existence lookup plus one
  join query filtered by `sbom_id`, with deduplication done in SQL. There are no N+1 queries.
  Another option is `GROUP BY severity` with `COUNT(DISTINCT advisory.id)`, which would return at
  most about five rows. It is not needed at this scale, and the chosen approach keeps the
  case-insensitive mapping in one Rust function (`SeveritySummary::record`).
- **Query scope**: the query is filtered at the data source to the target SBOM, not
  `advisory::Entity::find().all()`.
- **Error handling**: `?` propagates the service `Error`. The handler converts it to `AppError`
  with `.context()`.
- **Reuse**: no pagination or sort is needed, so the `common/src/db/query.rs` helpers do not
  apply. If a shared "find by id or not-found" helper exists there (checked via
  `search_for_pattern`), use it for the existence check.
