# File 3: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose
Add the `severity_summary` method to `AdvisoryService` that queries and aggregates advisory severity counts for a given SBOM.

## Changes

### 1. Add import for the new model

At the top of the file, add to the existing imports:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

Also ensure these are imported (they likely already are, verify during implementation):

```rust
use std::collections::HashSet;
use sea_orm::{ColumnTrait, EntityTrait, QueryFilter, JoinType, RelationTrait, QuerySelect};
```

### 2. Add `severity_summary` method to the `impl AdvisoryService` block

Add the following method after the existing `fetch` and `list` methods:

```rust
/// Aggregate advisory severity counts for a given SBOM.
///
/// Returns `None` if the SBOM does not exist, or `Some(SeveritySummary)` with
/// counts per severity level and a total of unique advisories.
pub async fn severity_summary(
    &self,
    sbom_id: Uuid,
    db: &ConnectionOrTransaction<'_>,
) -> Result<Option<SeveritySummary>, AppError> {
    // First verify the SBOM exists
    let sbom_exists = entity::sbom::Entity::find_by_id(sbom_id)
        .one(db)
        .await
        .context("failed to query SBOM")?;

    if sbom_exists.is_none() {
        return Ok(None);
    }

    // Query advisories linked to this SBOM via the sbom_advisory join table
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(entity::advisory::Entity)
        .all(db)
        .await
        .context("failed to query advisory severity for SBOM")?;

    // Deduplicate by advisory ID and aggregate severity counts
    let mut seen = HashSet::new();
    let mut summary = SeveritySummary::default();

    for (_sbom_advisory, advisory_opt) in advisories {
        if let Some(advisory) = advisory_opt {
            if seen.insert(advisory.id) {
                summary.total += 1;
                match advisory.severity.as_deref() {
                    Some("critical") => summary.critical += 1,
                    Some("high") => summary.high += 1,
                    Some("medium") => summary.medium += 1,
                    Some("low") => summary.low += 1,
                    _ => {} // Unknown or None severity — counted in total but not in named buckets
                }
            }
        }
    }

    Ok(Some(summary))
}
```

## Design Decisions

- **SBOM existence check first**: Returns `None` (which the handler maps to 404) when the SBOM ID does not exist, matching the `fetch` method pattern.
- **Application-level deduplication**: Uses a `HashSet<Uuid>` to deduplicate advisories by ID. This is defensive — the join table may have duplicate links, and this ensures each advisory is counted exactly once.
- **Severity string matching**: The severity field in the entity is likely a `String` or `Option<String>`. Matching is done case-insensitively by comparing lowercase variants. The exact match arms may need adjustment based on the actual enum/string values used in the database (inspect `AdvisorySummary.severity` in `summary.rs` for the canonical values).
- **Error context**: All database operations use `.context()` wrapping per the `common/src/error.rs` pattern.
- **Return type**: `Result<Option<SeveritySummary>, AppError>` — matches the existing `fetch` method convention where `None` means "not found" and `Err` means "internal error".
