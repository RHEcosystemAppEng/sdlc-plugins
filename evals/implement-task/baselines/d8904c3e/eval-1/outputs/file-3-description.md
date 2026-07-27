# File 3: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries the database for advisories linked to a given SBOM, counts them by severity level (deduplicating by advisory ID), and returns a `SeveritySummary`.

## Current State

The `AdvisoryService` struct has existing methods `fetch`, `list`, and `search` that follow a consistent pattern:
- Accept `&self` as receiver
- Take domain-specific parameters (e.g., an ID)
- Take `tx: &Transactional<'_>` for transaction context
- Return `Result<T, AppError>`
- Use `.context()` for error wrapping

## Changes

### New Import

Add import for the new model type and the join table entity:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use entity::sbom_advisory;
```

Also import `HashSet` from the standard library for deduplication:

```rust
use std::collections::HashSet;
```

### New Method: `severity_summary`

Add the following method to the `impl AdvisoryService` block:

```rust
/// Compute aggregated severity counts for advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories associated with
/// the specified SBOM ID, deduplicates by advisory ID, and counts by severity level.
/// Returns a `SeveritySummary` with counts for Critical, High, Medium, and Low,
/// plus a total. Returns 404 if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Given: an SBOM ID, verify the SBOM exists
    // Use SbomService or a direct entity lookup to confirm the SBOM exists.
    // If not found, return a 404 AppError consistent with existing SBOM endpoints.

    // When: query advisories linked to this SBOM
    // Join sbom_advisory with advisory to get severity information.
    // Use SeaORM query builder to:
    // 1. SELECT from sbom_advisory WHERE sbom_id = <sbom_id>
    // 2. JOIN with advisory table to get severity field
    // 3. Collect results

    // Deduplicate by advisory ID using a HashSet
    let mut seen_ids = HashSet::new();
    let mut summary = SeveritySummary::default();

    // For each advisory linked to the SBOM:
    // - Skip if advisory ID already seen (deduplication)
    // - Match severity level and increment the appropriate counter
    // - Increment total for each unique advisory
    //
    // Severity matching (case-insensitive):
    //   "critical" => summary.critical += 1
    //   "high"     => summary.high += 1
    //   "medium"   => summary.medium += 1
    //   "low"      => summary.low += 1
    //
    // summary.total = number of unique advisories

    Ok(summary)
}
```

### Design Decisions

- **Deduplication**: Uses `HashSet<Id>` to track seen advisory IDs, ensuring duplicate links in `sbom_advisory` are counted only once. This satisfies the acceptance criterion "Counts only unique advisories (deduplicates by advisory ID)."
- **SBOM existence check**: Before querying advisories, verify the SBOM exists. If not found, return a 404 `AppError` consistent with how `SbomService::fetch` handles missing SBOMs. This satisfies "Returns 404 when SBOM ID does not exist."
- **Default zeros**: `SeveritySummary::default()` initializes all counts to 0, so SBOMs with no advisories naturally return all zeros.
- **Performance**: The query joins `sbom_advisory` with `advisory` in a single database round-trip. For SBOMs with up to 500 advisories, this should complete well under 200ms.
- **Error handling**: Uses `.context("Failed to fetch advisory severity summary")` on the query result, following the existing pattern.
- **Method signature**: Matches sibling methods (`fetch`, `list`) with `&self`, `Id`, and `&Transactional<'_>` parameters.

### Sibling Parity

- Follows the same method signature pattern as `fetch` and `list`
- Uses the same error wrapping with `.context()`
- Uses the same transaction parameter pattern
