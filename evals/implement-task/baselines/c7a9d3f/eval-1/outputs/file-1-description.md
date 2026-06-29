# File 1: Create `modules/fundamental/src/advisory/model/severity_summary.rs`

## Action: CREATE

## Purpose

Define the `SeveritySummary` response struct for the advisory severity aggregation endpoint.

## Detailed Changes

Create a new file with the following contents:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Summary of advisory severity counts for a given SBOM.
///
/// Each field represents the number of unique advisories at that severity level
/// linked to the SBOM. The `total` field is the sum of all severity counts.
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

- **Naming**: follows `<Concept>Summary` naming convention consistent with `AdvisorySummary`, `SbomSummary`, `PackageSummary`.
- **Derives**: uses `Serialize, Deserialize` for JSON serialization (consistent with sibling model structs), `ToSchema` for OpenAPI spec generation, and `Default` to ensure all counts start at 0.
- **Documentation**: every struct and field has a doc comment as required by the skill.
- **Location**: placed in `model/` directory following the module pattern.
