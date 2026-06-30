# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents aggregated severity counts for advisories linked to an SBOM.

## Detailed Changes

Create a new file with the following contents:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: u32,
    /// Number of advisories with High severity.
    pub high: u32,
    /// Number of advisories with Medium severity.
    pub medium: u32,
    /// Number of advisories with Low severity.
    pub low: u32,
    /// Total number of unique advisories across all severity levels.
    pub total: u32,
}
```

## Conventions Applied

- **Module structure**: Placed in `model/` directory following the project's `model/ + service/ + endpoints/` pattern
- **File naming**: Named `severity_summary.rs` matching the `summary.rs` and `details.rs` naming pattern in sibling model directories
- **Derive macros**: Uses `Serialize`, `Deserialize` (serde) and `ToSchema` (utoipa) consistent with `AdvisorySummary` and `SbomSummary` siblings
- **Default derive**: `Default` ensures all counts initialize to zero, satisfying the acceptance criterion that severity levels default to 0
- **Documentation**: Every struct and field has a doc comment (`///`) per the skill's code quality requirement
- **No business logic**: Pure data struct -- business logic lives in the service layer, consistent with other model files
