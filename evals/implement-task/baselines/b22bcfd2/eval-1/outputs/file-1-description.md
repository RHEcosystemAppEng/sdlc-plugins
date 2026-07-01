# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for an SBOM.

## Pre-Implementation Inspection

Before creating this file, inspect sibling model files to match conventions:
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/summary.rs` to see `AdvisorySummary` struct shape, derive macros, and field types
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/details.rs` to see `AdvisoryDetails` struct shape
- `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisorySummary` to inspect the `severity` field type and understand how severity levels are represented

## Detailed Changes

Create a new file with the following content:

```rust
//! Severity summary model for advisory severity aggregation.

use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// The `total` field is the sum of all severity levels.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: u32,
    /// Count of advisories with High severity.
    pub high: u32,
    /// Count of advisories with Medium severity.
    pub medium: u32,
    /// Count of advisories with Low severity.
    pub low: u32,
    /// Total count of unique advisories across all severity levels.
    pub total: u32,
}
```

## Notes

- Derive macros match the pattern from sibling model files (`Serialize`, `Deserialize`, `Debug`, `Clone`)
- `Default` is derived so all fields default to 0, satisfying acceptance criterion "All severity levels default to 0"
- `ToSchema` is included if sibling models use it for OpenAPI spec generation (verify during inspection)
- Every struct and field has a doc comment per the SKILL.md code quality requirement
- Field type `u32` is appropriate for non-negative counts
