# File 1: modules/fundamental/src/advisory/service/advisory.rs

## Action: MODIFY

## Pre-implementation Inspection

Before modifying, would use Serena to inspect:

1. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/service/advisory.rs")` -- see all methods on `AdvisoryService`
2. `mcp__serena_backend__find_symbol(name_path_pattern="AdvisoryService::fetch", include_body=true)` -- read the `fetch` method body to understand the exact pattern (parameter types, return type, error handling, transactional usage)
3. `mcp__serena_backend__find_symbol(name_path_pattern="AdvisoryService::list", include_body=true)` -- read `list` for comparison
4. `mcp__serena_backend__find_referencing_symbols(name_path_pattern="AdvisoryService")` -- check all callers to ensure no conflicts

## Changes

Add a `severity_summary` method to the `AdvisoryService` impl block. The method follows the same pattern as `fetch` and `list`.

### New imports needed

At the top of the file, add imports for:
- `SeveritySummary` from `crate::advisory::model::severity_summary`
- `sbom_advisory` entity from the entity crate (if not already imported)
- `HashSet` from `std::collections` (for deduplication)

### New method: `severity_summary`

```rust
/// Returns aggregated severity counts for advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts by severity level. Returns
/// a `SeveritySummary` with counts for critical, high, medium, low, and total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists first (return 404 if not)
    // Follow the pattern from existing fetch methods that check entity existence

    // Query sbom_advisory join table for all advisories linked to this SBOM
    // Join to advisory table to get severity information
    // Use AdvisorySummary's severity field for classification

    // Deduplicate by advisory ID using HashSet or .distinct() in query
    // Count occurrences per severity level (Critical, High, Medium, Low)

    // Build and return SeveritySummary with counts, defaulting to 0
    // for any severity level with no advisories

    // Error handling: wrap all fallible operations with .context()
    // matching the pattern in existing service methods
}
```

### Detailed logic

1. **SBOM existence check**: Query the SBOM entity by `sbom_id`. If not found, return an `AppError` "not found" variant with `.context("SBOM not found")`. This ensures 404 response for non-existent SBOMs, consistent with existing SBOM endpoints.

2. **Query advisories**: Use SeaORM to query the `sbom_advisory` join table filtered by `sbom_id`, joining to the advisory table to retrieve severity information. The query should select advisory IDs and their severity values.

3. **Deduplication**: Collect results, deduplicate by advisory ID (using a `HashSet<Id>` to track seen IDs, or use SQL `DISTINCT` on advisory_id in the query itself -- prefer the SQL approach for efficiency).

4. **Counting**: Iterate over the deduplicated advisory severities and count by level:
   - Match severity string/enum to `"Critical"`, `"High"`, `"Medium"`, `"Low"`
   - Increment the corresponding counter
   - Compute total as sum of all four

5. **Return**: Construct `SeveritySummary { critical, high, medium, low, total }` and return `Ok(summary)`.

### Defensive property access

When reading the severity field from `AdvisorySummary`, use `.unwrap_or_default()` or pattern matching to handle cases where severity might be `None` or an unrecognized value. Unrecognized severity values should not be counted in any named bucket but should still contribute to the total.

### Convention conformance

- Method signature matches existing `fetch`/`list` pattern: `&self`, domain-specific ID, `&Transactional<'_>`
- Return type: `Result<SeveritySummary, AppError>` (matches convention)
- Error wrapping: `.context()` on all fallible operations
- Uses same transactional context pattern as sibling methods
