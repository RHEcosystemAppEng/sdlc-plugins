# File 4: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for a given SBOM.

## Pre-Implementation Inspection

1. `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` in `modules/fundamental/src/advisory/model/summary.rs` to see the sibling struct pattern (derives, field types, documentation).
2. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/details.rs` to see additional model struct patterns.
3. Check `common/src/model/paginated.rs` for the `PaginatedResults<T>` pattern -- not needed for this struct but informs the general model conventions.

## Sibling Analysis

The sibling `AdvisorySummary` struct in `summary.rs` likely uses:
- `#[derive(Debug, Clone, Serialize)]` (at minimum)
- Possibly `#[derive(utoipa::ToSchema)]` for OpenAPI documentation
- Field-level documentation comments
- `serde` rename attributes if field naming differs from Rust conventions

## File Contents

```rust
use serde::Serialize;

/// Aggregated advisory severity counts for a given SBOM.
///
/// Each field represents the count of unique advisories at that severity level
/// linked to the queried SBOM. All counts default to zero when no advisories
/// exist at that level.
#[derive(Debug, Clone, Serialize)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: u64,
    /// Number of advisories with High severity.
    pub high: u64,
    /// Number of advisories with Medium severity.
    pub medium: u64,
    /// Number of advisories with Low severity.
    pub low: u64,
    /// Total number of unique advisories across all severity levels.
    pub total: u64,
}

impl Default for SeveritySummary {
    fn default() -> Self {
        Self {
            critical: 0,
            high: 0,
            medium: 0,
            low: 0,
            total: 0,
        }
    }
}
```

### Notes

- If sibling models derive `utoipa::ToSchema`, add it here as well for OpenAPI spec generation consistency.
- `Default` implementation ensures all fields start at zero, satisfying the acceptance criterion that all severity levels default to 0.
- `u64` chosen for count type; may need to match the sibling pattern (could be `i64` or `usize` depending on codebase convention -- inspect siblings first).
- Documentation comment on every field and the struct itself per skill Step 6 code quality practices.

## Symbol Deduplication Check

Before declaring `SeveritySummary`, search the target package:
- `mcp__serena_backend__search_for_pattern("SeveritySummary")` across `modules/fundamental/`
- If an identical or equivalent struct already exists, reuse it instead of creating a new one.

## Convention Compliance

- Derive macros match sibling model pattern (`Debug, Clone, Serialize`)
- PascalCase struct name with descriptive suffix (`Summary`)
- Public fields with `pub` visibility
- Documentation comments on struct and all fields
- `Default` implementation for zero-value initialization
