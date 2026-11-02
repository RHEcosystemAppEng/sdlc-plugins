# File 1 — Modify: `modules/fundamental/src/advisory/service/advisory.rs`

## What changes

Add a `severity_summary` method to `AdvisoryService`.

## Code inspection

Before modifying, inspect with `mcp__serena_backend__find_symbol(name_path_pattern="AdvisoryService")` with `include_body=true` to read the existing `fetch` and `list` methods and understand the method signature pattern.

Also inspect `advisory/model/summary.rs` to understand the `AdvisorySummary` struct and its `severity` field, and `entity/src/sbom_advisory.rs` for the join table structure.

## Detailed changes

Add a new method to the `impl AdvisoryService` block:

```rust
/// Returns aggregated severity counts for advisories linked to the given SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    // JOIN with advisory table to get severity field
    // GROUP BY severity, COUNT DISTINCT advisory_id
    // Map results into SeveritySummary struct with defaults of 0
    
    let db = self.db(tx);
    
    // Verify SBOM exists first (404 if not)
    let _sbom = sbom::Entity::find_by_id(sbom_id)
        .one(db)
        .await?
        .ok_or_else(|| AppError::NotFound("SBOM not found".to_string()))
        .context("fetching SBOM for severity summary")?;
    
    // Query distinct advisories with their severity
    let results = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .inner_join(advisory::Entity)
        .select_only()
        .column(advisory::Column::Severity)
        .column_as(advisory::Column::Id.count(), "count")
        .group_by(advisory::Column::Severity)
        .into_tuple::<(String, i64)>()
        .all(db)
        .await
        .context("querying advisory severity counts")?;
    
    let mut summary = SeveritySummary::default();
    for (severity, count) in results {
        match severity.to_lowercase().as_str() {
            "critical" => summary.critical = count as u32,
            "high" => summary.high = count as u32,
            "medium" => summary.medium = count as u32,
            "low" => summary.low = count as u32,
            _ => {} // Unknown severity levels are ignored
        }
    }
    summary.total = summary.critical + summary.high + summary.medium + summary.low;
    
    Ok(summary)
}
```

## Patterns followed

- Method signature matches `fetch` and `list`: `&self, id: Id, tx: &Transactional<'_>` → `Result<T, AppError>`
- Error handling uses `.context()` wrapping (matches `common/src/error.rs` pattern)
- Uses `self.db(tx)` for database access (matches existing service methods)
