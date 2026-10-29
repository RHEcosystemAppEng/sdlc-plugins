# File 2: modules/fundamental/src/advisory/service/advisory.rs

**Action**: Modify (existing file)

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table, groups advisories by severity, deduplicates by advisory ID, and returns a `SeveritySummary` struct.

## Changes

### New imports

Add imports at the top of the file:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use entity::sbom_advisory;
use std::collections::HashSet;
```

### New method: `severity_summary`

Add a new method to the `impl AdvisoryService` block, following the pattern of existing `fetch` and `list` methods:

```rust
/// Aggregate advisory severity counts for a given SBOM.
///
/// Queries the sbom_advisory join table for all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and returns counts per
/// severity level (critical, high, medium, low) plus a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists first — return 404 if not found
    let sbom = self.sbom_service.fetch(sbom_id, tx)
        .await?
        .ok_or_else(|| AppError::NotFound(format!("SBOM with id {} not found", sbom_id)))?;

    // Query advisories linked to this SBOM via the join table
    let advisory_links = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(tx.connection())
        .await
        .context("Failed to fetch advisory links for SBOM")?;

    // Deduplicate by advisory ID
    let mut seen_ids = HashSet::new();
    let mut critical = 0i64;
    let mut high = 0i64;
    let mut medium = 0i64;
    let mut low = 0i64;

    for link in &advisory_links {
        if !seen_ids.insert(link.advisory_id) {
            continue; // Skip duplicate advisory links
        }

        // Fetch the advisory summary to get its severity
        if let Some(advisory) = self.fetch(link.advisory_id, tx).await? {
            match advisory.severity.as_deref().unwrap_or_default() {
                "critical" | "Critical" => critical += 1,
                "high" | "High" => high += 1,
                "medium" | "Medium" => medium += 1,
                "low" | "Low" => low += 1,
                _ => {} // Unknown severity levels are ignored
            }
        }
    }

    let total = critical + high + medium + low;

    Ok(SeveritySummary {
        critical,
        high,
        medium,
        low,
        total,
    })
}
```

**Alternative implementation (single SQL query, preferred for performance):**

If SeaORM supports it, the query could be done as a single GROUP BY query for better performance with large advisory sets:

```rust
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists — return 404 if not
    // Use the SbomService or direct entity lookup
    let _sbom = entity::sbom::Entity::find_by_id(sbom_id)
        .one(tx.connection())
        .await
        .context("Failed to look up SBOM")?
        .ok_or_else(|| AppError::NotFound(format!("SBOM with id {} not found", sbom_id)))?;

    // Query severity counts with deduplication via DISTINCT advisory_id
    // Using a raw SQL query or SeaORM select with group_by
    let rows = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .inner_join(entity::advisory::Entity)
        .select_only()
        .column(entity::advisory::Column::Severity)
        .column_as(entity::advisory::Column::Id.count(), "count")
        .group_by(entity::advisory::Column::Severity)
        .distinct_on([entity::advisory::Column::Id])
        .into_tuple::<(Option<String>, i64)>()
        .all(tx.connection())
        .await
        .context("Failed to aggregate advisory severities")?;

    let mut summary = SeveritySummary::default();
    for (severity, count) in rows {
        match severity.as_deref().unwrap_or_default() {
            "critical" | "Critical" => summary.critical = count,
            "high" | "High" => summary.high = count,
            "medium" | "Medium" => summary.medium = count,
            "low" | "Low" => summary.low = count,
            _ => {}
        }
    }
    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

## Rationale

- Follows the existing method signature pattern (`&self, id: Id, tx: &Transactional<'_>`)
- Uses `.context()` error wrapping consistent with existing error handling
- Returns `Result<T, AppError>` as all service methods do
- Deduplicates by advisory ID per acceptance criteria
- Returns 404 for non-existent SBOM per acceptance criteria
- Defaults all counts to 0 when no advisories exist (struct default initialization)

## Convention Conformance

- Method signature matches `fetch` and `list` patterns
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Uses SeaORM query patterns consistent with existing service code
- Doc comment on public method explaining parameters and behavior
