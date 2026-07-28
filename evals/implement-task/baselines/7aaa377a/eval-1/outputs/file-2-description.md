# File 2: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Purpose

Add the `severity_summary` method to `AdvisoryService` that queries the database for advisories linked to a given SBOM and aggregates their severity counts.

## Current State

The file contains `AdvisoryService` with methods `fetch`, `list`, and `search`, each following the pattern:
- Take `&self`, entity-specific parameters, and `tx: &Transactional<'_>`
- Query the database using SeaORM entities
- Return `Result<T, AppError>` with `.context()` error wrapping

## Changes

Add a new `severity_summary` method to the `impl AdvisoryService` block:

```rust
/// Returns an aggregated severity summary of all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the SBOM,
/// deduplicates by advisory ID, and counts advisories per severity level.
/// Returns a `SeveritySummary` with counts for Critical, High, Medium, Low, and total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists (return 404 if not found)
    //    Use the same pattern as existing fetch methods to check SBOM existence
    //    e.g., query sbom entity by ID, return AppError (404) if None

    // 2. Query sbom_advisory join table filtered by sbom_id
    //    Join with advisory table to access AdvisorySummary severity field
    //    Use entity::sbom_advisory for the join table

    // 3. Collect advisory IDs into a HashSet for deduplication
    //    Iterate over results, deduplicate by advisory ID

    // 4. Count severities from deduplicated advisories
    //    Initialize counters: critical=0, high=0, medium=0, low=0
    //    Match each advisory's severity field to increment the appropriate counter

    // 5. Compute total as sum of all severity counts

    // 6. Return SeveritySummary struct
    Ok(SeveritySummary {
        critical,
        high,
        medium,
        low,
        total,
    })
}
```

### Required Imports

Add at the top of the file:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;
```

## Pattern Compliance

- **Method signature**: follows `fetch`/`list` pattern with `&self, id: Id, tx: &Transactional<'_>`
- **Error handling**: uses `Result<T, AppError>` with `.context()` wrapping on database errors
- **SBOM existence check**: returns 404 (via AppError) when SBOM not found, consistent with existing SBOM endpoints
- **Deduplication**: uses `HashSet<advisory_id>` to ensure unique advisory counts per acceptance criteria

## Impact

- Adds one new public method to `AdvisoryService`
- No changes to existing methods
- No breaking changes
