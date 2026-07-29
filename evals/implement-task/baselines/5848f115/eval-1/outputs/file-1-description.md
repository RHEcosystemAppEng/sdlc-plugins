# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

New file defining the `SeveritySummary` response struct used by the severity aggregation endpoint.

## Pre-implementation analysis

Before creating this file, inspect sibling model files to discover conventions:
- Read `modules/fundamental/src/advisory/model/summary.rs` via `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` to see struct definition patterns, derive macros, and the `severity` field that will be used for counting.
- Read `modules/fundamental/src/advisory/model/details.rs` via `mcp__serena_backend__get_symbols_overview` to confirm the derive macro and documentation patterns.
- Read `modules/fundamental/src/sbom/model/summary.rs` via `mcp__serena_backend__get_symbols_overview` for cross-module model convention confirmation.

## Detailed changes

Create the file with the following content:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// The `total` field is the sum of all severity levels.
#[derive(Clone, Debug, Default, Deserialize, Serialize, ToSchema)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: i64,
    /// Count of advisories with High severity.
    pub high: i64,
    /// Count of advisories with Medium severity.
    pub medium: i64,
    /// Count of advisories with Low severity.
    pub low: i64,
    /// Total count of unique advisories across all severity levels.
    pub total: i64,
}
```

## Conventions applied

- Derive macros match sibling models: `Clone`, `Debug`, `Default`, `Deserialize`, `Serialize`, `ToSchema`
- `///` doc comments on the struct and each field (per skill Step 6 code quality guidance)
- Field type (`i64`) matches the integer type convention used in sibling database-backed structs
- `Default` derive ensures all counts start at zero (satisfying acceptance criterion: "All severity levels default to 0")
