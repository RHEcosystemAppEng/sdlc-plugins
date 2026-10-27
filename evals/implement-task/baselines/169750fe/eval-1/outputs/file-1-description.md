# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose
Define the `SeveritySummary` response struct returned by the new severity aggregation endpoint.

## Changes

Create new file with the following content:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Summary of advisory severity counts for a given SBOM.
#[derive(Debug, Clone, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    pub critical: u32,
    pub high: u32,
    pub medium: u32,
    pub low: u32,
    pub total: u32,
}
```

## Rationale
- Follows the derive macro pattern from sibling `AdvisorySummary` in `model/summary.rs`: `Debug, Clone, Serialize, Deserialize, ToSchema`
- Added `Default` derive to support initializing all counts to 0 when no advisories exist
- Fields are `u32` since counts are always non-negative
- Snake_case field names match the JSON response contract: `{ critical, high, medium, low, total }`
