# File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to an SBOM.

## Detailed Changes

Create a new file with the following content:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
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

## Conventions Followed

- **Model pattern**: derives `Serialize`, `Deserialize` for JSON serialization, matching `SbomSummary`, `AdvisoryDetails`, and other model structs in the same module.
- **Documentation**: every struct and field has a `///` doc comment explaining its purpose.
- **Default derivation**: `Default` derive ensures all counts initialize to 0, satisfying the acceptance criterion that severity levels default to 0 when no advisories exist.
- **Naming**: `SeveritySummary` follows the `<Domain>Summary` naming pattern used by `AdvisorySummary`, `SbomSummary`.
- **ToSchema**: derives `utoipa::ToSchema` for OpenAPI spec generation, consistent with other model structs if the project uses utoipa.
