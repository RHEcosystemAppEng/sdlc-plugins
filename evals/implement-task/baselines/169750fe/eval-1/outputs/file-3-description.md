# File 3: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose
Add `severity_summary` method to `AdvisoryService`.

## Changes

Add the following method to the `impl AdvisoryService` block, after the existing `list` method:

```rust
/// Computes severity counts for advisories linked to a given SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists
    let sbom = sbom::Entity::find_by_id(sbom_id)
        .one(&self.db.connection(tx))
        .await?
        .ok_or_else(|| AppError::NotFound("SBOM not found".into()))?;

    // Query advisories linked to this SBOM via sbom_advisory join table,
    // deduplicating by advisory ID
    let advisories = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom.id))
        .find_also_related(advisory::Entity)
        .all(&self.db.connection(tx))
        .await
        .context("querying SBOM advisories")?;

    let mut summary = SeveritySummary::default();
    let mut seen_ids = std::collections::HashSet::new();

    for (_link, advisory) in advisories {
        if let Some(adv) = advisory {
            if seen_ids.insert(adv.id) {
                match adv.severity.as_deref() {
                    Some("critical") => summary.critical += 1,
                    Some("high") => summary.high += 1,
                    Some("medium") => summary.medium += 1,
                    Some("low") => summary.low += 1,
                    _ => {}
                }
                summary.total += 1;
            }
        }
    }

    Ok(summary)
}
```

## Rationale
- Method signature follows existing `fetch` and `list` patterns: `&self, id: Id, tx: &Transactional<'_>` → `Result<T, AppError>`
- Uses `sbom_advisory` join table entity from `entity/src/sbom_advisory.rs` as referenced in Implementation Notes
- Deduplicates advisories by ID using `HashSet` to count unique advisories only
- Returns `AppError::NotFound` for non-existent SBOM, matching existing 404 pattern
- Error wrapping with `.context()` follows `common/src/error.rs` pattern
- `SeveritySummary::default()` initializes all counts to 0
