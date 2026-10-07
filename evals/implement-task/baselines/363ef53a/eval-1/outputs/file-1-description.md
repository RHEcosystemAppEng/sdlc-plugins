# File 1: Modify `modules/fundamental/src/advisory/service/advisory.rs`

**Action:** Modify (add new method)

## Pre-implementation inspection

Before modifying this file, inspect it using `mcp__serena_backend__get_symbols_overview` to understand the existing `AdvisoryService` struct and its methods (`fetch`, `list`, `search`). Then use `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` method to read its full implementation as the pattern reference for the new method.

Also inspect `modules/fundamental/src/advisory/model/summary.rs` to understand the `AdvisorySummary` struct and its `severity` field, which will be used for counting.

## Changes

Add a new `severity_summary` method to `AdvisoryService`:

```rust
/// Returns a severity summary aggregating advisory severity counts for a given SBOM.
///
/// Queries the sbom_advisory join table to find all advisories linked to the specified
/// SBOM, deduplicates by advisory ID, and counts occurrences of each severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    // Deduplicate by advisory ID
    // Count by severity level (Critical, High, Medium, Low)
    // Return SeveritySummary with counts and total
    // Use .context("failed to fetch advisory severity summary") for error wrapping
}
```

**Pattern conformance:**
- Follows the same signature pattern as `fetch` and `list`: `(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`
- Uses `.context()` wrapping for error handling, matching existing service methods
- Returns `Result<SeveritySummary, AppError>` consistent with the `Result<T, AppError>` convention
- Includes a `///` documentation comment describing purpose and behavior

**Import additions:**
- Add `use super::model::severity_summary::SeveritySummary;` (or adjust path as needed once the model module is created)
- Add any necessary SeaORM entity imports for `sbom_advisory` join table queries

**Defensive property access:**
- Use `.unwrap_or_default()` on severity field access in case advisories have null/missing severity values
- Default all severity counts to 0 when no advisories exist at a given level
