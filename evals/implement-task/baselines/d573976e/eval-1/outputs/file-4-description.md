# File 4: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` that aggregates advisory severity counts for a given SBOM.

## Detailed Changes

Add the following method to the `impl AdvisoryService` block, following the existing `fetch` and `list` method patterns:

```rust
/// Aggregates advisory severity counts for all unique advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the SBOM,
/// deduplicates by advisory ID, and counts by severity level. Returns a `SeveritySummary`
/// with counts for Critical, High, Medium, Low, and a total. Returns a 404 error if the
/// SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify SBOM exists — return 404 if not found
    // (follow the pattern used by other service methods that validate entity existence)

    // Query sbom_advisory join table for advisories linked to this SBOM
    // Use DISTINCT on advisory ID to deduplicate
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(tx.connection())
        .await
        .context("querying advisories for SBOM")?;

    // Fetch each unique advisory's summary to get severity
    let mut seen_ids = std::collections::HashSet::new();
    let mut summary = SeveritySummary::default();

    for sa in &advisories {
        if !seen_ids.insert(sa.advisory_id) {
            continue; // skip duplicate
        }

        // Fetch AdvisorySummary to get the severity field
        let advisory = self.fetch(sa.advisory_id, tx)
            .await
            .context("fetching advisory for severity")?;

        if let Some(advisory) = advisory {
            match advisory.severity.as_deref() {
                Some("Critical") | Some("critical") => summary.critical += 1,
                Some("High") | Some("high") => summary.high += 1,
                Some("Medium") | Some("medium") => summary.medium += 1,
                Some("Low") | Some("low") => summary.low += 1,
                _ => {} // Unknown severity — not counted in any bucket
            }
        }
    }

    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

## Import Additions

Add to the imports at the top of the file:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;
```

## Conventions Followed

- **Method signature**: follows the same pattern as `fetch` and `list` — takes `&self, id: Id, tx: &Transactional<'_>` and returns `Result<T, AppError>`.
- **Error handling**: uses `.context()` wrapping on all fallible operations, matching the established pattern.
- **Naming**: `severity_summary` follows the `verb_noun` service method naming convention.
- **Documentation**: `///` doc comment on the method explaining behavior, parameters, and error conditions.
- **Deduplication**: uses `HashSet` to track seen advisory IDs, satisfying the acceptance criterion for unique advisory counting.
- **Default initialization**: `SeveritySummary::default()` ensures all counts start at 0.
- **Total calculation**: computed from the sum of individual severity counts rather than a separate counter, ensuring consistency.

## Alternative Implementation Note

For better performance with large advisory sets (acceptance criterion: under 200ms for 500 advisories), the query could be optimized to use a SQL `GROUP BY` with `COUNT(DISTINCT advisory_id)` to push aggregation to the database rather than iterating in application code. The SQL approach would look like:

```sql
SELECT severity, COUNT(DISTINCT a.id) as count
FROM sbom_advisory sa
JOIN advisory a ON sa.advisory_id = a.id
WHERE sa.sbom_id = $1
GROUP BY severity
```

This would be implemented using SeaORM's query builder with `group_by` and `column_as` for the count. The choice between application-level and database-level aggregation depends on the existing patterns in the codebase — if sibling service methods use raw SQL or query builder aggregations, this approach should follow suit.
