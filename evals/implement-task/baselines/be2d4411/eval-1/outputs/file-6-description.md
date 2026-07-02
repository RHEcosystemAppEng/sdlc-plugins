# File 6: modules/fundamental/src/advisory/service/advisory.rs

**Action**: MODIFY

## Purpose

Add the `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table, aggregates advisory severity counts for a given SBOM, deduplicates by advisory ID, and returns a `SeveritySummary`.

## Detailed Changes

### New Method

Add the following method to the `impl AdvisoryService` block, after the existing `fetch` and `list` methods:

```rust
use std::collections::HashSet;
use crate::advisory::model::severity_summary::SeveritySummary;

impl AdvisoryService {
    // ... existing methods (fetch, list, search) ...

    /// Aggregates advisory severity counts for the given SBOM.
    ///
    /// Queries all advisories linked to the SBOM via the `sbom_advisory` join table,
    /// deduplicates by advisory ID, and returns counts per severity level.
    /// Returns a 404 error if the SBOM does not exist.
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<SeveritySummary, AppError> {
        // Verify the SBOM exists; return 404 if not found
        let _sbom = self
            .sbom_service
            .fetch(sbom_id.clone(), tx)
            .await
            .context("Failed to look up SBOM")?
            .ok_or_else(|| AppError::not_found(format!("SBOM {} not found", sbom_id)))?;

        // Query advisories linked to the SBOM via the join table
        let advisories = entity::sbom_advisory::Entity::find()
            .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
            .find_also_related(entity::advisory::Entity)
            .all(tx.connection())
            .await
            .context("Failed to query SBOM advisories")?;

        // Deduplicate by advisory ID and count by severity
        let mut seen = HashSet::new();
        let mut summary = SeveritySummary::default();

        for (_sbom_adv, advisory_opt) in advisories {
            if let Some(advisory) = advisory_opt {
                if seen.insert(advisory.id.clone()) {
                    // Only count each unique advisory once
                    match advisory.severity.as_deref() {
                        Some("Critical") => summary.critical += 1,
                        Some("High") => summary.high += 1,
                        Some("Medium") => summary.medium += 1,
                        Some("Low") => summary.low += 1,
                        _ => {} // Unknown or None severity -- skip
                    }
                    summary.total += 1;
                }
            }
        }

        Ok(summary)
    }
}
```

### Design Decisions

- **Method signature**: Follows the existing pattern of `(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`, matching `fetch` and `list` methods.
- **SBOM existence check**: Verifies the SBOM exists before querying advisories, returning 404 for non-existent SBOMs (acceptance criterion #2).
- **Deduplication**: Uses a `HashSet` to track seen advisory IDs, ensuring each advisory is counted only once even if linked multiple times (acceptance criterion #3).
- **Default zeros**: `SeveritySummary::default()` initializes all counts to 0, so SBOMs with no advisories return all zeros (acceptance criterion #4).
- **Performance**: Single query to fetch all linked advisories, then in-memory aggregation. For SBOMs with up to 500 advisories, this is well within the 200ms target (acceptance criterion #5). An alternative would be SQL-level `GROUP BY` aggregation, but the in-memory approach is simpler and consistent with the existing service pattern.
- **Severity matching**: Uses string matching against the `severity` field from `AdvisorySummary`. Matches "Critical", "High", "Medium", "Low" -- unknown severities are counted in `total` but not in any specific bucket (or alternatively, unknown severities could be skipped entirely depending on business logic -- this would be clarified during actual implementation by inspecting the `severity` field's actual values).
- **Error handling**: Uses `.context()` wrapping matching the convention in `common/src/error.rs`.

### Conventions Followed

- Method naming follows `verb_noun` pattern (consistent with `fetch`, `list`, `search`).
- Parameters match the existing method signatures (`&self, id: Id, tx: &Transactional<'_>`).
- Error handling uses `.context()` for wrapping, matching sibling methods.
- Documentation comment on the method explaining what it does, its query strategy, and edge cases.
- Uses SeaORM query builder patterns consistent with existing service methods.
