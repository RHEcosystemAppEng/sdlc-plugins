# File 5: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries the database for advisories linked to a given SBOM, groups them by severity, deduplicates by advisory ID, and returns a `SeveritySummary`.

## Detailed Changes

### Add import

At the top of the file, add an import for the new model:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

### Add `severity_summary` method to `AdvisoryService` impl block

Add the following method to the existing `impl AdvisoryService` block, following the pattern of the existing `fetch` and `list` methods:

```rust
/// Aggregate severity counts for advisories linked to a given SBOM.
///
/// Returns a `SeveritySummary` with counts per severity level and total.
/// Deduplicates advisories by advisory ID to avoid double-counting
/// when multiple join table entries exist.
pub async fn severity_summary(
    &self,
    sbom_id: &str,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists; return 404 if not found.
    //    Follow the pattern used by SbomService::fetch — query the sbom
    //    entity table and return AppError::NotFound if no row matches.
    let sbom = entity::sbom::Entity::find_by_id(sbom_id)
        .one(self.db.connection(tx))
        .await
        .context("Failed to query SBOM")?
        .ok_or_else(|| AppError::NotFound(format!("SBOM {} not found", sbom_id)))?;

    // 2. Query the sbom_advisory join table to find all advisory IDs
    //    linked to this SBOM.
    let advisory_links = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom.id))
        .all(self.db.connection(tx))
        .await
        .context("Failed to query SBOM advisory links")?;

    // 3. Collect unique advisory IDs to deduplicate.
    let unique_advisory_ids: HashSet<_> = advisory_links
        .iter()
        .map(|link| link.advisory_id.clone())
        .collect();

    // 4. Fetch the advisory records for the unique IDs.
    //    Use AdvisorySummary (which has the severity field) to get
    //    severity information.
    let advisories = entity::advisory::Entity::find()
        .filter(entity::advisory::Column::Id.is_in(unique_advisory_ids))
        .all(self.db.connection(tx))
        .await
        .context("Failed to query advisories")?;

    // 5. Build the summary by counting each severity level.
    let mut summary = SeveritySummary::default();
    for advisory in &advisories {
        // The severity field on the advisory entity is expected to be
        // a string like "critical", "high", "medium", "low" (case-insensitive).
        match advisory.severity.as_deref().unwrap_or("").to_lowercase().as_str() {
            "critical" => summary.critical += 1,
            "high" => summary.high += 1,
            "medium" => summary.medium += 1,
            "low" => summary.low += 1,
            _ => { /* Unknown or missing severity — not counted in named buckets */ }
        }
    }
    summary.total = advisories.len() as u64;

    Ok(summary)
}
```

### Additional imports needed

```rust
use std::collections::HashSet;
use anyhow::Context;  // if not already imported; provides the .context() method
```

## Conventions Followed

- **Method signature**: Follows the same `(&self, id: &str, tx: &Transactional<'_>) -> Result<T, AppError>` pattern as `fetch` and `list` methods on `AdvisoryService`.
- **Database access**: Uses `self.db.connection(tx)` for transaction-aware database access, matching the existing service methods.
- **Entity queries**: Uses SeaORM's `Entity::find()`, `.filter()`, `.all()` pattern consistent with other service queries.
- **Error handling**: Uses `.context()` wrapping on all fallible operations, producing `AppError` results consistent with `common/src/error.rs`.
- **404 handling**: Returns `AppError::NotFound` when the SBOM does not exist, matching the behavior of existing SBOM endpoints.
- **Deduplication**: Uses `HashSet` to collect unique advisory IDs before fetching, ensuring duplicate join table entries don't inflate counts.
- **Case-insensitive matching**: Converts severity to lowercase before matching, providing resilience against inconsistent casing in the database.

## Notes

- The exact field name for severity on the advisory entity (`advisory.severity`) depends on the SeaORM entity definition in `entity/src/advisory.rs`. If the field is named differently or uses an enum type, the match logic would need adjustment. The implementation assumes it's an `Option<String>` field.
- The `total` field counts all unique advisories regardless of whether their severity matches a known level, which means advisories with unknown/null severity are included in `total` but not in any named bucket. This is a deliberate design choice for transparency.
