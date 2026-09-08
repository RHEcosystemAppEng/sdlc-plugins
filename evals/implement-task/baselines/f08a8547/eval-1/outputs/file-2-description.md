# File 2: AdvisoryService -- severity_summary Method

**File**: `modules/fundamental/src/advisory/service/advisory.rs`
**Action**: MODIFY

## Current State

The `AdvisoryService` struct has methods `fetch`, `list`, and `search`. Each method
follows a consistent pattern:
- Takes `&self`, an identifier or query parameters, and `tx: &Transactional<'_>`
- Queries the database using SeaORM
- Returns `Result<T, AppError>` where T is a model struct

## Changes

Add a `severity_summary` method to `AdvisoryService`:

```rust
/// Returns an aggregated count of advisory severities for the given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, reads each advisory's severity
/// level, and returns counts per severity level along with a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists; return 404 if not found
    //    Use SbomService::fetch or direct entity lookup to confirm existence.
    //    Pattern: match against None => return Err(AppError::NotFound("SBOM not found"))

    // 2. Query sbom_advisory join table for all advisory IDs linked to this SBOM
    //    Use: entity::sbom_advisory::Entity::find()
    //         .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
    //         .all(tx)
    //    This retrieves all join records.

    // 3. Collect unique advisory IDs (deduplicate)
    //    Use a HashSet<Id> to ensure each advisory is counted once even if
    //    multiple join records exist.

    // 4. For each unique advisory, fetch the AdvisorySummary to read its severity
    //    Use: entity::advisory::Entity::find_by_id(advisory_id)
    //    Extract the `severity` field from the fetched advisory.

    // 5. Count by severity level
    //    Initialize counters: critical=0, high=0, medium=0, low=0
    //    Match severity string (case-insensitive) to increment the appropriate counter.
    //    Use defensive matching: unknown severity levels are logged but not counted
    //    in any bucket (or optionally counted in a separate "other" field if needed).

    // 6. Compute total as sum of all severity counts

    // 7. Construct and return SeveritySummary
    Ok(SeveritySummary {
        critical,
        high,
        medium,
        low,
        total,
    })
}
```

## Required Imports

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;
```

## Error Handling

- SBOM not found: return `Err(AppError::NotFound(...))` or equivalent, matching
  how existing `fetch` methods handle missing entities.
- Database errors: use `.context("Failed to fetch advisory severity summary")` to
  wrap SeaORM errors into `AppError`.

## Performance Considerations

- For SBOMs with up to 500 advisories (per acceptance criteria), the query should
  complete well under 200ms. If performance is a concern, consider a single SQL
  query with `GROUP BY severity` and `COUNT(DISTINCT advisory_id)` instead of
  fetching individual advisories in a loop.
- Optimized single-query approach (preferred):

```sql
SELECT a.severity, COUNT(DISTINCT sa.advisory_id) as count
FROM sbom_advisory sa
JOIN advisory a ON sa.advisory_id = a.id
WHERE sa.sbom_id = $1
GROUP BY a.severity
```

This can be expressed via SeaORM's query builder or a raw SQL query, and is more
efficient than N+1 individual fetches.

## Convention Adherence

- Method signature matches `fetch` and `list` patterns: `&self`, entity ID, `&Transactional<'_>`.
- Error handling uses `Result<T, AppError>` with `.context()` wrapping.
- Documentation comment on the public method.
