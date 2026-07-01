# File 4: `modules/fundamental/src/advisory/service/advisory.rs`

**Action**: Modify existing file

## Purpose

Add the `severity_summary` method to `AdvisoryService` that queries the database for advisories linked to a given SBOM, deduplicates by advisory ID, counts by severity level, and returns a `SeveritySummary` struct.

## Conventions Applied

- **Method signature**: Follows the pattern of existing `fetch` and `list` methods: `&self, <params>, tx: &Transactional<'_>` -> `Result<T, AppError>`.
- **Method naming**: Uses `severity_summary` following the `verb_noun` / descriptive naming convention (consistent with `fetch`, `list`, `search`).
- **Error handling**: Uses `.context()` wrapping for all fallible operations, matching sibling methods.
- **Query pattern**: Uses SeaORM entities and the `sbom_advisory` join table, consistent with how other service methods query related entities.

## Detailed Changes

Add the following method to the `impl AdvisoryService` block:

```rust
use std::collections::HashSet;
use crate::advisory::model::severity_summary::SeveritySummary;

impl AdvisoryService {
    // ... existing methods (fetch, list, search) ...

    /// Aggregates advisory severity counts for a given SBOM.
    ///
    /// Queries all advisories linked to the SBOM via the `sbom_advisory` join table,
    /// deduplicates by advisory ID, and counts each severity level. Returns a
    /// `SeveritySummary` with counts for critical, high, medium, and low severities.
    ///
    /// Returns an error (mapping to HTTP 404) if the SBOM does not exist.
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<SeveritySummary, AppError> {
        // Verify the SBOM exists; return 404 if not found
        // (Follow the same existence-check pattern used by fetch())
        let _sbom = self
            .sbom_service
            .fetch(sbom_id.clone(), tx)
            .await
            .context("Failed to verify SBOM existence")?
            .ok_or_else(|| AppError::not_found(format!("SBOM {} not found", sbom_id)))?;

        // Query advisories linked to this SBOM via the join table
        let advisory_links = entity::sbom_advisory::Entity::find()
            .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
            .find_also_related(entity::advisory::Entity)
            .all(tx.connection())
            .await
            .context("Failed to query SBOM advisories")?;

        // Deduplicate by advisory ID and count by severity
        let mut seen = HashSet::new();
        let mut summary = SeveritySummary::default();

        for (_link, advisory_opt) in advisory_links {
            if let Some(advisory) = advisory_opt {
                if seen.insert(advisory.id.clone()) {
                    // Map the advisory's severity to the appropriate counter
                    match advisory.severity.as_deref() {
                        Some("critical") | Some("Critical") => summary.critical += 1,
                        Some("high") | Some("High") => summary.high += 1,
                        Some("medium") | Some("Medium") => summary.medium += 1,
                        Some("low") | Some("Low") => summary.low += 1,
                        _ => {} // Unknown or missing severity -- not counted in named buckets
                    }
                    summary.total += 1;
                }
            }
        }

        Ok(summary)
    }
}
```

## Design Decisions

- **SBOM existence check first**: Verifies the SBOM exists before querying advisories, returning a 404 immediately if not found. This matches the acceptance criterion "Returns 404 when SBOM ID does not exist."
- **`HashSet` for deduplication**: Uses a `HashSet<advisory_id>` to track already-counted advisories, satisfying "Counts only unique advisories (deduplicates by advisory ID)." An alternative would be `SELECT DISTINCT` in the SQL query, but the in-memory approach is simpler and sufficient for the expected data volume (up to 500 advisories per the performance criterion).
- **Case-insensitive severity matching**: Matches both lowercase and title-case severity values to handle potential data inconsistencies. The actual implementation would inspect the `AdvisorySummary.severity` field type to determine the exact variant names.
- **`total` counts all unique advisories**: Includes advisories with unknown/missing severity in the total count but not in the named buckets, ensuring `total >= critical + high + medium + low`.
- **Performance consideration**: A single query with a join is used rather than N+1 queries. For up to 500 advisories, this easily meets the "Response time under 200ms" criterion. If performance were a concern at larger scales, this could be refactored to use `COUNT(*) GROUP BY severity` in SQL.

## Alternative Approach (SQL-based aggregation)

For better performance at scale, the query could be written as a raw SQL or SeaORM group-by:

```sql
SELECT a.severity, COUNT(DISTINCT a.id) as count
FROM sbom_advisory sa
JOIN advisory a ON sa.advisory_id = a.id
WHERE sa.sbom_id = $1
GROUP BY a.severity
```

This would eliminate the in-memory deduplication and reduce data transfer. The choice between approaches depends on the existing query patterns in the codebase -- the implementation should match whichever pattern sibling service methods use.
