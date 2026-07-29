# File 4: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add the `severity_summary` method to the existing `AdvisoryService` struct.

## Pre-implementation analysis

Before modifying this file, inspect it and related files:
- Use `mcp__serena_backend__get_symbols_overview` on this file to see the full structure of `AdvisoryService` and all its existing methods.
- Use `mcp__serena_backend__find_symbol("AdvisoryService::fetch", include_body=true)` to read the `fetch` method body and understand the exact parameter types, return type, transaction usage, and error handling pattern.
- Use `mcp__serena_backend__find_symbol("AdvisoryService::list", include_body=true)` to read the `list` method body for the query builder pattern.
- Use `mcp__serena_backend__find_referencing_symbols("AdvisoryService")` to understand all callers and ensure the change does not break existing usage.
- Read `entity/src/sbom_advisory.rs` via `mcp__serena_backend__get_symbols_overview` to understand the join table entity structure for querying SBOM-advisory relationships.
- Read `modules/fundamental/src/advisory/model/summary.rs` via `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` to understand the `severity` field type and values.

## Detailed changes

Add a new `severity_summary` method to the `impl AdvisoryService` block:

```rust
/// Computes aggregated severity counts for advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts by severity level.
/// Returns a 404 error if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists (return 404 if not)
    // Query sbom_advisory join table for this SBOM's advisories
    // Join with advisory table to get severity levels
    // Deduplicate by advisory ID (SELECT DISTINCT or GROUP BY)
    // Count by severity level
    // Build and return SeveritySummary struct
}
```

Also add the necessary import at the top of the file:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

## Conventions applied

- Method signature matches existing `fetch` and `list` methods: `&self`, entity ID, and `&Transactional<'_>`
- Returns `Result<T, AppError>` with `.context()` wrapping for all database operations
- Uses SeaORM query builder patterns consistent with existing service methods
- Verifies entity existence before querying (returning 404 for non-existent SBOM, matching sibling endpoint behavior)
- Deduplication via SQL (GROUP BY or DISTINCT) rather than in-memory filtering
- `///` doc comment on the method explaining behavior
