# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: Create

## Purpose

Define the `SeveritySummary` response struct for the advisory severity aggregation endpoint.
This model represents the JSON response body for `GET /api/v2/sbom/{id}/advisory-summary`.

## Pre-implementation inspection

Before creating this file, would inspect siblings using Serena:

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/summary.rs` -- understand AdvisorySummary struct shape, its `severity` field type, derive macros used
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/model/summary.rs` -- understand sibling model pattern (derives, documentation style)
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/details.rs` -- understand AdvisoryDetails struct pattern
- `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisorySummary` -- read the severity field to understand its type for counting

Also search for existing severity-related types to avoid symbol duplication:
- `mcp__serena_backend__search_for_pattern` for `SeveritySummary` across the codebase
- `mcp__serena_backend__search_for_pattern` for `severity_summary` across the codebase
- Grep for `SEVERITY` constants or enums in the entity and model packages

## Detailed changes

```rust
use serde::Serialize;
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the number of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
#[derive(Clone, Debug, Default, Serialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of critical-severity advisories.
    pub critical: u64,
    /// Number of high-severity advisories.
    pub high: u64,
    /// Number of medium-severity advisories.
    pub medium: u64,
    /// Number of low-severity advisories.
    pub low: u64,
    /// Total number of unique advisories across all severity levels.
    pub total: u64,
}
```

## Conventions applied

- Derive macros match sibling model pattern: `Clone, Debug, Serialize, ToSchema`
- Added `Default` derive to support all-zeros initialization when no advisories exist
- `///` doc comments on the struct and every public field (per SKILL.md and Rust convention)
- PascalCase struct name following `<Domain><Purpose>` pattern (matches `AdvisorySummary`, `SbomSummary`)
- `u64` for counts, consistent with typical Rust count types
- File placed in `model/` subdirectory, matching the module structure convention
