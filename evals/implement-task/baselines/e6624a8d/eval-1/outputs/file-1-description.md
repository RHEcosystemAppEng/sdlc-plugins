# File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to an SBOM. This struct is the return type of the `AdvisoryService::severity_summary` method and the response body of the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Detailed Changes

### Struct definition

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Each severity level contains the count of unique advisories at that level.
/// The `total` field is the sum of all unique advisories across all severity levels,
/// including any advisories with unknown or unset severity.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: u64,
    /// Count of advisories with High severity.
    pub high: u64,
    /// Count of advisories with Medium severity.
    pub medium: u64,
    /// Count of advisories with Low severity.
    pub low: u64,
    /// Total count of unique advisories across all severity levels.
    pub total: u64,
}
```

## Conventions Followed

- **Derives mirror sibling models**: `Clone, Debug, Serialize, Deserialize, ToSchema` matches the pattern used by `AdvisorySummary` and `SbomSummary` in sibling model files. `Default` is added so all counts initialize to 0, satisfying the acceptance criterion that all severity levels default to 0 when no advisories exist.
- **Field types**: Uses `u64` for non-negative counts, consistent with common count and pagination fields in the codebase.
- **Doc comments on each field**: Enables OpenAPI schema generation via `utoipa::ToSchema`, and provides documentation for consumers of the API.
- **One struct per file**: Follows the one-struct-per-file convention observed in sibling model files (`summary.rs`, `details.rs`).
- **File location**: Placed under `model/` in the advisory module, consistent with the domain module pattern.
