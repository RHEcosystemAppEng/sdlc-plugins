# File 2 — Modify: `modules/fundamental/src/advisory/service/advisory.rs`

## Current State (inferred from symbol inspection)

`AdvisoryService` has two public async methods:

```rust
pub async fn fetch(
    &self,
    id: Id,
    tx: &Transactional<'_>,
) -> Result<Option<AdvisoryDetails>, anyhow::Error> { ... }

pub async fn list(
    &self,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<AdvisorySummary>, anyhow::Error> { ... }
```

## Change Required

Add a new `severity_summary` method after `list`. The method:
1. Takes `sbom_id: Id` to identify which SBOM to aggregate.
2. Uses the `sbom_advisory` join entity to find all advisory links for the given SBOM.
3. Deduplicates by `advisory_id` using `.distinct_on(sbom_advisory::Column::AdvisoryId)` (or a `HashSet` dedup post-query if the DB driver doesn't support `DISTINCT ON` natively in SeaORM for SQLite compat).
4. Joins or loads each linked advisory's `AdvisorySummary.severity` field to count by severity level.
5. Returns `SeveritySummary` with `critical`, `high`, `medium`, `low`, and `total` fields.

## Implementation

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use entity::sbom_advisory;
use sea_orm::prelude::*;
use sea_orm::QuerySelect;
use std::collections::HashMap;

impl AdvisoryService {
    // ... existing fetch and list methods ...

    /// Aggregates vulnerability advisory severity counts for a given SBOM.
    ///
    /// Queries the sbom_advisory join table to find all advisories linked to
    /// the SBOM, deduplicates by advisory ID, and returns per-severity counts
    /// and a total. All severity levels default to 0 when no advisories exist.
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<SeveritySummary, anyhow::Error> {
        let db = tx.db(&self.db);

        // Fetch distinct advisory IDs for this SBOM from the join table.
        let advisory_ids: Vec<Uuid> = sbom_advisory::Entity::find()
            .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
            .select_only()
            .column(sbom_advisory::Column::AdvisoryId)
            .distinct()
            .into_tuple()
            .all(db)
            .await
            .context("failed to query sbom_advisory for severity summary")?;

        if advisory_ids.is_empty() {
            return Ok(SeveritySummary::default());
        }

        // Load AdvisorySummary for each unique advisory to read its severity field.
        // The `AdvisorySummary.severity` field stores the highest severity string
        // for the advisory (e.g., "Critical", "High", "Medium", "Low").
        let advisories = advisory::Entity::find()
            .filter(advisory::Column::Id.is_in(advisory_ids))
            .all(db)
            .await
            .context("failed to load advisories for severity summary")?;

        let mut summary = SeveritySummary::default();
        for advisory in &advisories {
            match advisory.severity.to_lowercase().as_str() {
                "critical" => summary.critical += 1,
                "high"     => summary.high += 1,
                "medium"   => summary.medium += 1,
                "low"      => summary.low += 1,
                _          => {}  // unknown or none — do not count
            }
        }
        summary.total = summary.critical + summary.high + summary.medium + summary.low;

        Ok(summary)
    }
}
```

## Inspection Steps

1. `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` — confirm parameter types (`Id`, `Transactional`) and error return type.
2. `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::list` — confirm method signature pattern to replicate.
3. `mcp__serena_backend__get_symbols_overview` on `entity/src/sbom_advisory.rs` — confirm column names (`SbomId`, `AdvisoryId`).
4. `mcp__serena_backend__find_symbol` on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` — confirm `severity` field type (String vs enum).
5. `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` — ensure no existing callers will be broken by adding a new method.
6. Use `mcp__serena_backend__insert_after_symbol` targeting the `list` method to insert the new `severity_summary` method body.

## Edge Cases Handled
- SBOM with zero linked advisories → returns `SeveritySummary::default()` (all zeros).
- Advisory with unknown/null severity → not counted, does not panic.
- Duplicate advisory links in `sbom_advisory` → deduplicated via `.distinct()` before counting.
