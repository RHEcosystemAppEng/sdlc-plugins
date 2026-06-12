# File 5 -- MODIFY: modules/fundamental/src/advisory/service/advisory.rs

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries and aggregates advisory severity counts for a given SBOM.

## Conventions Applied

- **Service method pattern:** Follows the existing `fetch` and `list` methods -- takes `&self`, an entity ID, and `tx: &Transactional<'_>`.
- **Error handling:** Uses `AppError` with `.context()` wrapping.
- **Return type:** Returns `Result<SeveritySummary, AppError>`.
- **Naming:** Method name follows `verb_noun` pattern used by sibling methods (`fetch`, `list`, `search`).
- **Documentation:** Method has a `///` doc comment.

## Detailed Changes

Add the following method to the `impl AdvisoryService` block, after the existing `list` or `search` method:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;

impl AdvisoryService {
    // ... existing methods (fetch, list, search) ...

    /// Aggregates advisory severity counts for the specified SBOM.
    ///
    /// Queries the `sbom_advisory` join table to find all advisories linked to
    /// the given SBOM, deduplicates by advisory ID, and returns counts per
    /// severity level (Critical, High, Medium, Low) along with a total.
    ///
    /// Returns `AppError::NotFound` if the SBOM ID does not exist.
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<SeveritySummary, AppError> {
        // Verify the SBOM exists; return 404 if not found
        // (Following the pattern used by existing SBOM endpoints)
        let _sbom = self
            .sbom_service
            .fetch(sbom_id.clone(), tx)
            .await
            .context("Failed to verify SBOM existence")?
            .ok_or_else(|| AppError::NotFound(format!("SBOM {} not found", sbom_id)))?;

        // Query advisories linked to this SBOM via the sbom_advisory join table
        let advisories = entity::sbom_advisory::Entity::find()
            .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
            .find_also_related(entity::advisory::Entity)
            .all(tx.connection())
            .await
            .context("Failed to query SBOM advisories")?;

        // Deduplicate by advisory ID and count by severity level
        let mut seen = HashSet::new();
        let mut summary = SeveritySummary::default();

        for (_sbom_adv, advisory) in advisories {
            if let Some(adv) = advisory {
                if seen.insert(adv.id.clone()) {
                    // Count by severity level using the severity field
                    // from AdvisorySummary pattern
                    match adv.severity.as_deref() {
                        Some("Critical") => summary.critical += 1,
                        Some("High") => summary.high += 1,
                        Some("Medium") => summary.medium += 1,
                        Some("Low") => summary.low += 1,
                        _ => {} // Unknown or missing severity -- not counted in breakdown
                    }
                    summary.total += 1;
                }
            }
        }

        Ok(summary)
    }
}
```

## Key Design Decisions

- **SBOM existence check first:** Returns 404 before querying advisories, matching the acceptance criterion and existing SBOM endpoint behavior.
- **HashSet deduplication:** Ensures unique advisories per acceptance criterion #3. Uses in-memory deduplication after query -- alternatively could use `DISTINCT` in the SQL query, but the HashSet approach is simpler and matches the Rust idiomatic pattern.
- **Match on severity string:** Maps severity level strings to count fields. Unknown or null severity values are included in total but not in any specific severity bucket. This is a reasonable default; the `total` field counts all unique advisories regardless of severity.
- **Performance:** Single query with JOIN avoids N+1 problem, satisfying the 200ms performance criterion for up to 500 advisories.
- **Error propagation:** All fallible operations use `.context()` for descriptive error messages.
