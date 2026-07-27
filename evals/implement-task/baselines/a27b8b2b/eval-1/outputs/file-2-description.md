# File 2: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` that queries advisories linked to a given SBOM, deduplicates by advisory ID, counts by severity level, and returns a `SeveritySummary`.

## Pre-implementation inspection

Before modifying, inspect this file using:
1. `mcp__serena_backend__get_symbols_overview` to see the struct and method layout of `AdvisoryService`.
2. `mcp__serena_backend__find_symbol("AdvisoryService::fetch", include_body=true)` to read the `fetch` method body and understand the service method pattern: parameter types, transactional context usage, error handling with `.context()`, and return type.
3. `mcp__serena_backend__find_symbol("AdvisoryService::list", include_body=true)` to read the `list` method as a second reference for the query-and-aggregate pattern.

Also inspect:
- `entity/src/sbom_advisory.rs` to understand the join table entity for querying advisories by SBOM ID.
- `modules/fundamental/src/advisory/model/summary.rs` to understand the `severity` field on `AdvisorySummary` and its type.

## Changes

Add a new `severity_summary` method to the `AdvisoryService` impl block. The method follows the same signature pattern as `fetch` and `list`:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;

impl AdvisoryService {
    // ... existing methods (fetch, list, search) ...

    /// Aggregates advisory severity counts for a given SBOM.
    ///
    /// Queries all advisories linked to the specified SBOM via the sbom_advisory
    /// join table, deduplicates by advisory ID, and returns counts per severity
    /// level (Critical, High, Medium, Low) along with a total.
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<SeveritySummary, anyhow::Error> {
        // 1. Verify the SBOM exists (return 404-compatible error if not)
        //    Follow the same pattern used in fetch() for entity existence checks.

        // 2. Query the sbom_advisory join table to find all advisory IDs
        //    linked to this SBOM.
        //    Use entity::sbom_advisory to build the query.

        // 3. Join with the advisory table to get severity for each advisory.
        //    Use the severity field from AdvisorySummary model.

        // 4. Deduplicate by advisory ID (use .distinct() or collect into
        //    a HashSet to ensure unique advisory IDs).

        // 5. Count advisories per severity level:
        //    - critical: count where severity == "critical"
        //    - high: count where severity == "high"
        //    - medium: count where severity == "medium"
        //    - low: count where severity == "low"
        //    - total: sum of all severity counts

        // 6. Return SeveritySummary with all counts.
        //    Wrap any query errors with .context("Failed to aggregate severity summary")

        Ok(SeveritySummary {
            critical,
            high,
            medium,
            low,
            total,
        })
    }
}
```

## Error handling

- If the SBOM ID does not exist, return an error that maps to a 404 response. Follow the same pattern used in existing `fetch` methods (likely returning `AppError::NotFound` or equivalent via `.context()`).
- All database query errors wrapped with `.context("Failed to aggregate advisory severity summary for SBOM")`.

## Conventions applied

- **Method signature:** `&self`, entity ID, `tx: &Transactional<'_>` -- matches `fetch` and `list` methods
- **Return type:** `Result<T, anyhow::Error>` with `.context()` wrapping -- matches sibling methods
- **Documentation:** `///` doc comment on the public method
- **Error handling:** `.context()` for error wrapping, matching `common/src/error.rs` pattern
