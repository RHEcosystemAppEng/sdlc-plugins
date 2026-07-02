# File 4: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries the database for advisory severity counts linked to a given SBOM.

## Detailed Changes

### Inspection before modification

Use `mcp__serena_backend__get_symbols_overview` on this file to see the AdvisoryService struct and its existing methods (`fetch`, `list`, `search`). Use `mcp__serena_backend__find_symbol` with `include_body=true` on the `list` method to understand the query pattern.

Also inspect:
- `entity/src/sbom_advisory.rs` for the join table entity structure
- `modules/fundamental/src/advisory/model/summary.rs` to understand the `severity` field on `AdvisorySummary`

### New method

Add the following method to the `impl AdvisoryService` block:

```rust
/// Aggregates advisory severity counts for a given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and groups counts by severity
/// level. Returns a `SeveritySummary` with counts for each severity level and
/// a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists (return 404 if not)
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // 3. Join with advisory table to get severity field
    // 4. Use SELECT DISTINCT advisory_id to deduplicate
    // 5. Group by severity, COUNT each group
    // 6. Map severity values to SeveritySummary fields
    // 7. Compute total as sum of all severity counts
    // 8. Return SeveritySummary with .context() wrapping on any errors

    // Implementation would use SeaORM query builder following the pattern
    // established by the existing `list` and `fetch` methods.
}
```

### Key implementation details

- **SBOM existence check**: First verify the SBOM exists by querying the sbom entity. If not found, return an `AppError` that maps to 404, consistent with existing SBOM endpoints.
- **Deduplication**: Use `SELECT DISTINCT advisory_id` or equivalent SeaORM method to ensure each advisory is counted only once even if linked to the SBOM multiple times.
- **Severity mapping**: The `severity` field from `AdvisorySummary` contains string values like "Critical", "High", "Medium", "Low". Map these to the corresponding `SeveritySummary` fields. Unknown severity values would be excluded from per-level counts but included in total.
- **Default to zero**: The `Default` derive on `SeveritySummary` ensures all fields start at 0. Severity levels with no advisories naturally remain at 0.

## Conventions followed

- Method signature matches sibling methods: `&self`, `Id` param, `&Transactional<'_>`
- Returns `Result<T, AppError>` with `.context()` wrapping
- Uses SeaORM for database queries, consistent with the rest of the service layer
- Documentation comment on the method
