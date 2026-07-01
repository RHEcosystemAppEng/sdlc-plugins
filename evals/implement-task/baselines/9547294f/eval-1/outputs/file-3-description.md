# File 3: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` that aggregates advisory severity counts for a given SBOM.

## Detailed Changes

### New method on AdvisoryService

Add the `severity_summary` method to the `impl AdvisoryService` block, following the existing pattern of `fetch` and `list` methods:

```rust
/// Compute aggregated severity counts for advisories linked to a given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories associated
/// with the specified SBOM, deduplicates by advisory ID, and counts each
/// severity level. Returns a `SeveritySummary` with the counts.
///
/// Returns `AppError::NotFound` if the SBOM ID does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, Error> {
    // Verify the SBOM exists; return 404 if not found
    let _sbom = self.sbom_service.fetch(sbom_id.clone(), tx)
        .await?
        .ok_or_else(|| Error::NotFound(format!("SBOM with ID {} not found", sbom_id)))?;

    // Query advisories linked to this SBOM via the sbom_advisory join table
    let advisory_links = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .all(tx.connection())
        .await
        .context("failed to query sbom_advisory join table")?;

    // Collect unique advisory IDs to deduplicate
    let unique_advisory_ids: HashSet<_> = advisory_links
        .iter()
        .map(|link| link.advisory_id.clone())
        .collect();

    // Fetch advisory summaries for the unique IDs and count by severity
    let mut summary = SeveritySummary::default();

    for advisory_id in &unique_advisory_ids {
        let advisory = advisory::Entity::find_by_id(advisory_id.clone())
            .one(tx.connection())
            .await
            .context("failed to fetch advisory")?;

        if let Some(adv) = advisory {
            match adv.severity.as_deref() {
                Some("critical") => summary.critical += 1,
                Some("high") => summary.high += 1,
                Some("medium") => summary.medium += 1,
                Some("low") => summary.low += 1,
                _ => {} // Unknown or missing severity -- still counted in total
            }
            summary.total += 1;
        }
    }

    Ok(summary)
}
```

### New imports required

Add at the top of the file (alongside existing imports):

```rust
use std::collections::HashSet;
use crate::advisory::model::severity_summary::SeveritySummary;
use entity::sbom_advisory;
```

## Conventions Applied

- **Method signature**: follows the same pattern as `fetch` and `list` -- takes `&self`, domain-specific ID (`Id`), and `tx: &Transactional<'_>`
- **Return type**: `Result<SeveritySummary, Error>` matching sibling methods
- **Error handling**: uses `.context()` wrapping on fallible operations, matching `common/src/error.rs` pattern
- **Naming**: `severity_summary` follows the `verb_noun` naming convention (though this is more `noun_noun`, it matches the domain concept; alternatively could be `get_severity_summary`)
- **Documentation**: `///` doc comment explaining the method's purpose, parameters, and error behavior
- **Deduplication**: uses `HashSet` to collect unique advisory IDs before counting, satisfying the acceptance criterion
- **SBOM existence check**: validates that the SBOM exists before querying advisories, returning 404 if not found

## Performance Note

For SBOMs with up to 500 advisories (per acceptance criteria), this approach of fetching individual advisories could be optimized with a single SQL query using GROUP BY. An optimized version would use:

```sql
SELECT a.severity, COUNT(DISTINCT sa.advisory_id) as count
FROM sbom_advisory sa
JOIN advisory a ON sa.advisory_id = a.id
WHERE sa.sbom_id = $1
GROUP BY a.severity
```

This would satisfy the "Response time under 200ms" acceptance criterion more reliably. The implementation should prefer the SQL aggregation approach if SeaORM supports it cleanly, or use the iterative approach shown above for clarity.
