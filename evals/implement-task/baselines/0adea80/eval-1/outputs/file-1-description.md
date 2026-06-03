# File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to an SBOM.

## Detailed Changes

### Struct definition

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
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

- Derives mirror the pattern used by `AdvisorySummary` and `SbomSummary` in sibling model files: `Clone, Debug, Serialize, Deserialize, ToSchema`.
- `Default` is derived so all counts start at 0 when no advisories exist, satisfying the acceptance criterion that all severity levels default to 0.
- Field types use `u64` to match Rust idioms for non-negative counts (consistent with common count/pagination fields in the codebase).
- Doc comments on each field for OpenAPI schema generation via `utoipa::ToSchema`.
- The struct is placed in its own file under `model/`, following the one-struct-per-file convention seen with `summary.rs` and `details.rs`.
