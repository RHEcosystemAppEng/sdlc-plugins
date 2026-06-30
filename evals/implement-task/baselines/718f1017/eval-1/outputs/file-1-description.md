# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose
Define the `SeveritySummary` response struct used by the new endpoint.

## Detailed Changes

Create a new file with the following content:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Summary of advisory severity counts for a given SBOM.
///
/// Contains the number of unique advisories at each severity level
/// linked to the SBOM, plus a total count across all levels.
#[derive(Clone, Debug, Default, Deserialize, Eq, PartialEq, Serialize, ToSchema)]
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

## Rationale
- Derives follow the pattern of sibling model structs (`AdvisorySummary`, `SbomSummary`)
- `Default` derive ensures all fields initialize to 0, satisfying the acceptance criterion that missing severity levels default to 0
- `ToSchema` enables automatic OpenAPI spec generation
- Doc comments on the struct and each field for discoverability
