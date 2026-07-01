# File 1: `modules/fundamental/src/advisory/model/severity_summary.rs`

**Action**: Create new file

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to a given SBOM. This struct is returned directly by the endpoint as JSON.

## Conventions Applied

- **Struct naming**: Follows `<Domain><Purpose>` pattern consistent with siblings `AdvisorySummary`, `AdvisoryDetails`.
- **Derive macros**: Uses `Serialize`, `Deserialize` (serde) matching sibling model structs.
- **Single struct per file**: Follows the pattern in `summary.rs` and `details.rs`.
- **Documentation**: Every new public struct and field gets a doc comment.

## Detailed Changes

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at the given level.
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

## Design Decisions

- **`Default` derive**: Ensures all fields start at 0, satisfying the acceptance criterion "All severity levels default to 0 when no advisories exist at that level."
- **`u32` type**: Counts are non-negative integers; `u32` provides sufficient range for advisory counts.
- **`ToSchema` derive**: If the project uses `utoipa` for OpenAPI generation (common in Axum projects), this enables automatic schema documentation. If not present, this derive would be omitted based on what sibling models use.
- **`Clone` and `Debug`**: Standard derives matching sibling model structs for debuggability and flexibility.
