# File 2: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose
Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for an SBOM.

## Full File Content

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
#[derive(Clone, Debug, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: u32,
    /// Number of advisories with High severity.
    pub high: u32,
    /// Number of advisories with Medium severity.
    pub medium: u32,
    /// Number of advisories with Low severity.
    pub low: u32,
    /// Total number of unique advisories.
    pub total: u32,
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

## Design Decisions

- **Derive macros**: `Serialize`, `Deserialize`, `Clone`, `Debug`, `ToSchema` — matching sibling models like `AdvisorySummary` in `summary.rs`.
- **`u32` for counts**: Advisory counts will never be negative; `u32` provides a natural fit. Consistent with Rust conventions for non-negative counts.
- **`Default` impl**: Provides a zero-initialized struct, which simplifies the aggregation logic (start with default, increment as advisories are iterated).
- **`total` field**: Included as a convenience for consumers so they do not need to sum the individual severity counts. Also accounts for advisories with unknown/none severity that do not fall into the four named buckets.
- **Doc comments**: Each field has a doc comment for OpenAPI schema generation via `utoipa`.
