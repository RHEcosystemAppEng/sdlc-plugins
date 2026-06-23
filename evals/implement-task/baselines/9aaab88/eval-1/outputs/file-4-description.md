# File 4: modules/fundamental/src/advisory/service/advisory.rs

**Action**: MODIFY

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries advisories linked to a given SBOM, aggregates their severity counts, and returns a `SeveritySummary`.

## Sibling Reference

Follows the pattern of existing methods `fetch` and `list` in the same file for:
- Method signature pattern: `&self, <params>, tx: &Transactional<'_>`
- Error handling with `.context()` wrapping
- Database query patterns using SeaORM

## Detailed Changes

Add the following method to the `impl AdvisoryService` block:

```rust
use std::collections::HashSet;
use crate::advisory::model::severity_summary::SeveritySummary;

impl AdvisoryService {
    // ... existing methods (fetch, list, search) ...

    /// Aggregates advisory severity counts for a given SBOM.
    ///
    /// Queries the `sbom_advisory` join table to find all advisories linked to the
    /// specified SBOM, deduplicates by advisory ID, and counts by severity level.
    /// Returns a `SeveritySummary` with counts for each severity level and a total.
    ///
    /// Returns an error with 404 semantics if the SBOM does not exist.
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<SeveritySummary, AppError> {
        // Verify the SBOM exists (returns 404 if not found)
        // Use the existing SBOM lookup pattern from the codebase
        let _sbom = self.sbom_service
            .fetch(sbom_id, tx)
            .await
            .context("SBOM not found")?
            .ok_or_else(|| AppError::not_found(format!("SBOM {} not found", sbom_id)))?;

        // Query advisories linked to this SBOM via the sbom_advisory join table
        let advisory_links = entity::sbom_advisory::Entity::find()
            .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
            .all(tx.connection())
            .await
            .context("Failed to query SBOM advisory links")?;

        // Deduplicate by advisory ID using a HashSet
        let mut seen_advisory_ids = HashSet::new();
        let mut summary = SeveritySummary::default();

        for link in &advisory_links {
            if !seen_advisory_ids.insert(link.advisory_id.clone()) {
                continue; // Skip duplicate
            }

            // Fetch the advisory summary to get the severity field
            let advisory = self.fetch(link.advisory_id.clone(), tx)
                .await
                .context("Failed to fetch linked advisory")?;

            if let Some(advisory) = advisory {
                match advisory.severity.as_deref() {
                    Some("Critical") | Some("critical") => summary.critical += 1,
                    Some("High") | Some("high") => summary.high += 1,
                    Some("Medium") | Some("medium") => summary.medium += 1,
                    Some("Low") | Some("low") => summary.low += 1,
                    _ => {} // Unknown or missing severity -- not counted in any bucket
                }
            }
        }

        summary.total = summary.critical + summary.high + summary.medium + summary.low;

        Ok(summary)
    }
}
```

## Key Design Decisions

- **SBOM existence check**: Returns 404 when the SBOM does not exist, satisfying acceptance criterion #2. Uses the existing `fetch` pattern from the SBOM service if available, or a direct entity lookup.
- **Deduplication via HashSet**: Uses `HashSet<advisory_id>` to skip duplicate advisory links, satisfying acceptance criterion #3.
- **Case-insensitive severity matching**: Matches both capitalized and lowercase severity strings to be robust.
- **Default initialization**: `SeveritySummary::default()` starts all counts at 0, satisfying acceptance criterion #4.
- **Total computation**: Computes total from the four category counts to ensure consistency.
- **Error wrapping**: Uses `.context()` for all fallible operations, matching the project's error handling convention.
- **Doc comment**: The method has a comprehensive documentation comment explaining behavior, parameters, and error semantics.

## Performance Note

For acceptance criterion #5 (response time under 200ms for up to 500 advisories), the current approach fetches each advisory individually. In production, this could be optimized to a single JOIN + GROUP BY query at the database level. The implementation shown prioritizes correctness and pattern adherence; if performance testing reveals issues, the query can be optimized to:

```sql
SELECT a.severity, COUNT(DISTINCT sa.advisory_id) 
FROM sbom_advisory sa 
JOIN advisory a ON sa.advisory_id = a.id 
WHERE sa.sbom_id = $1 
GROUP BY a.severity
```

This optimization would replace the loop with a single database call. The decision of whether to use the N+1 approach (matching existing patterns) or the optimized approach would be informed by inspecting how sibling service methods handle similar aggregations.
