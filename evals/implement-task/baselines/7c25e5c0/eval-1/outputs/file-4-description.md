# File 4 — Create: `modules/fundamental/src/advisory/model/severity_summary.rs`

## What changes

Define the `SeveritySummary` response struct.

## Code inspection

Before creating, inspect sibling model files with `mcp__serena_backend__get_symbols_overview` on `advisory/model/summary.rs` and `advisory/model/details.rs` to understand struct patterns (derive macros, serde attributes, documentation conventions).

## Detailed changes

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of critical-severity advisories.
    pub critical: u32,
    /// Number of high-severity advisories.
    pub high: u32,
    /// Number of medium-severity advisories.
    pub medium: u32,
    /// Number of low-severity advisories.
    pub low: u32,
    /// Total number of unique advisories across all severity levels.
    pub total: u32,
}
```

## Patterns followed

- Derive macros match sibling models: `Clone, Debug, Serialize, Deserialize, ToSchema`
- Added `Default` for zero-initialized counts
- Documentation comments on struct and fields (following sibling patterns)
- Located in `advisory/model/` alongside `summary.rs` and `details.rs`
