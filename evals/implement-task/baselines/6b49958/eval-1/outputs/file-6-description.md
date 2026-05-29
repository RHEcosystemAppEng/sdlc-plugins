# File 6: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries the database for advisories linked to a given SBOM, aggregates their severity levels, deduplicates by advisory ID, and returns a `SeveritySummary`.

## Current State (Expected)

The file contains the `AdvisoryService` struct with existing methods like `fetch` and `list`. The methods follow a consistent pattern:

```rust
impl AdvisoryService {
    pub async fn fetch(
        &self,
        id: Id,
        tx: &Transactional<'_>,
    ) -> Result<Option<AdvisoryDetails>, AppError> {
        // ... query logic ...
    }

    pub async fn list(
        &self,
        query: Query,
        paginated: Paginated,
        tx: &Transactional<'_>,
    ) -> Result<PaginatedResults<AdvisorySummary>, AppError> {
        // ... query logic ...
    }
}
```

## Change

Add the `severity_summary` method to the `impl AdvisoryService` block, along with necessary imports at the top of the file.

### New Imports (added at top of file)

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;
```

### New Method

```rust
impl AdvisoryService {
    // ... existing methods ...

    /// Aggregate advisory severity counts for a given SBOM.
    ///
    /// Returns `None` if the SBOM does not exist.
    /// Deduplicates advisories by ID before counting.
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<Option<SeveritySummary>, AppError> {
        // 1. Verify the SBOM exists; return None if not found
        let sbom = sbom::Entity::find_by_id(sbom_id.clone())
            .one(tx.connection())
            .await
            .context("looking up SBOM")?;

        if sbom.is_none() {
            return Ok(None);
        }

        // 2. Query advisories linked to this SBOM via sbom_advisory join table
        let advisory_links = sbom_advisory::Entity::find()
            .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
            .find_also_related(advisory::Entity)
            .all(tx.connection())
            .await
            .context("fetching advisories for SBOM")?;

        // 3. Deduplicate by advisory ID and aggregate severity counts
        let mut seen = HashSet::new();
        let mut summary = SeveritySummary::default();

        for (_link, advisory) in advisory_links {
            if let Some(adv) = advisory {
                if !seen.insert(adv.id.clone()) {
                    continue; // Skip duplicate
                }

                // Fetch the AdvisorySummary to access the severity field
                // (or read severity directly from the advisory entity if available)
                match adv.severity.as_deref() {
                    Some("Critical") | Some("critical") => summary.critical += 1,
                    Some("High") | Some("high") => summary.high += 1,
                    Some("Medium") | Some("medium") => summary.medium += 1,
                    Some("Low") | Some("low") => summary.low += 1,
                    _ => {} // Unknown or None severity is not counted in named buckets
                }

                summary.total += 1;
            }
        }

        Ok(Some(summary))
    }
}
```

## Design Decisions

- **Return type `Option<SeveritySummary>`:** Returns `None` when the SBOM does not exist, allowing the endpoint handler to map this to a 404 response. This follows the same pattern as the `fetch` method which returns `Option<AdvisoryDetails>`.

- **SBOM existence check first:** The method first verifies the SBOM exists before querying advisories. This ensures a 404 is returned for non-existent SBOMs even if the join table happens to have no rows (which would otherwise return an empty but successful response).

- **Deduplication with `HashSet`:** Advisory IDs are tracked in a `HashSet` to ensure each advisory is counted exactly once, even if the `sbom_advisory` join table contains duplicate entries. This satisfies the "deduplicates by advisory ID" acceptance criterion.

- **Case-insensitive severity matching:** The match statement handles both capitalized and lowercase severity strings to be defensive against data inconsistencies, though the project likely stores them in a consistent format.

- **`total` counts all unique advisories:** The total includes advisories with unknown/null severity, providing an accurate total count even if some advisories lack severity classification.

- **`.context()` wrapping:** All database operations are wrapped with `.context()` for error tracing, following the project's error handling convention.

## Performance Consideration

For SBOMs with up to 500 advisories (per acceptance criteria), this in-memory aggregation approach is efficient. The database query fetches all linked advisories in a single query, and the in-memory deduplication and counting is O(n). If performance becomes a concern for larger datasets, this could be replaced with a SQL `COUNT(DISTINCT ...) GROUP BY severity` query, but the current approach is simpler and well within the 200ms response time target for 500 advisories.

## Alternative Approach Considered

A pure SQL aggregation query using `SELECT severity, COUNT(DISTINCT advisory_id) FROM sbom_advisory JOIN advisory ... GROUP BY severity` would push the deduplication and counting to the database. This would be more efficient for very large datasets but adds complexity in mapping SQL results back to the struct. The in-memory approach was chosen for clarity and because the expected data volume (up to 500) is well within acceptable bounds. The SQL approach can be adopted later if profiling reveals a need.
