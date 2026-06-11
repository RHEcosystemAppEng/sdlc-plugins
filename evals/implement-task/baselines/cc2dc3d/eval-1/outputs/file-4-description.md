# File 4: modules/fundamental/src/advisory/service/advisory.rs

**Action**: Modify existing file

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` struct. This method queries advisories linked to a given SBOM via the `sbom_advisory` join table, deduplicates by advisory ID, counts by severity level, and returns a `SeveritySummary`.

## Detailed Changes

### Add import for new model

At the top of the file, add:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;
```

### Add `severity_summary` method to `impl AdvisoryService`

Add the following method to the existing `impl AdvisoryService` block, following the pattern of the existing `fetch` and `list` methods:

```rust
/// Retrieve aggregated advisory severity counts for a given SBOM.
///
/// Queries all advisories linked to the specified SBOM via the `sbom_advisory`
/// join table, deduplicates by advisory ID, and counts the number of advisories
/// at each severity level (Critical, High, Medium, Low).
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
        .context("Failed to fetch SBOM")?
        .ok_or_else(|| AppError::NotFound("SBOM not found".to_string()))?;

    // Query advisories linked to this SBOM via sbom_advisory join table
    let advisory_links = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(&self.db.connection(tx))
        .await
        .context("Failed to query SBOM advisory links")?;

    // Deduplicate by advisory ID using a HashSet
    let mut seen_ids = HashSet::new();
    let mut summary = SeveritySummary::default();

    for link in advisory_links {
        if !seen_ids.insert(link.advisory_id) {
            continue; // Skip duplicate advisory links
        }

        // Fetch the advisory to get its severity
        let advisory = self
            .fetch(link.advisory_id.into(), tx)
            .await
            .context("Failed to fetch advisory details")?;

        if let Some(advisory) = advisory {
            match advisory.severity.as_deref() {
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

## Conventions Applied

- **Method signature**: follows the same pattern as existing `fetch` and `list` methods -- takes `&self, id: Id, tx: &Transactional<'_>`
- **Error handling**: uses `Result<SeveritySummary, AppError>` with `.context()` wrapping on every fallible operation
- **404 handling**: returns `AppError::NotFound` when the SBOM does not exist, consistent with existing SBOM endpoints
- **Database access**: uses `self.db.connection(tx)` for transaction-aware database access, matching sibling service methods
- **SeaORM queries**: uses `Entity::find().filter().all()` pattern consistent with existing queries
- **Deduplication**: uses `HashSet` on advisory ID to count unique advisories only (acceptance criterion)
- **Documentation**: doc comment on the method explaining parameters and behavior
- **Naming**: follows `verb_noun` pattern for the method name (`severity_summary`)

## Notes

- The exact field names on the join table entity (`sbom_advisory::Column::SbomId`, `link.advisory_id`) and the severity field path on AdvisorySummary would be confirmed by reading the actual entity and model files via Serena before implementation
- The SBOM existence check approach (calling `sbom_service.fetch`) would be confirmed by examining how sibling methods handle not-found cases
- For performance (acceptance criterion: under 200ms for 500 advisories), a single joined query with GROUP BY would be more efficient than the N+1 pattern shown above; the actual implementation would optimize this based on the SeaORM patterns found in the codebase
