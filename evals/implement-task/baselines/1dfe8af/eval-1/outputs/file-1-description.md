# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose
Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for an SBOM.

## Detailed Changes

### Pre-implementation inspection
- Read `modules/fundamental/src/advisory/model/summary.rs` (sibling) to understand derive macros, field types, serde attributes, and documentation style used for model structs.
- Read `modules/fundamental/src/advisory/model/details.rs` (sibling) for additional pattern confirmation.
- Confirm derive conventions: `#[derive(Clone, Debug, Serialize, Deserialize, PartialEq, Eq)]` or similar from sibling analysis.

### New struct: `SeveritySummary`

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
#[derive(Clone, Debug, Default, Serialize, Deserialize, PartialEq, Eq, ToSchema)]
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

### Conventions followed
- Derives match sibling model structs (Serialize, Deserialize, Clone, Debug, PartialEq, Eq).
- `ToSchema` derive for OpenAPI spec generation (if utoipa is used in siblings).
- `Default` derive ensures all fields default to 0 (satisfies acceptance criterion for zero defaults).
- Doc comments on the struct and every field (code quality practice from Step 6).
- Flat struct with typed fields (not nested), matching response type conventions.
