# File 4: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: Create (new file)

## Purpose

Define the `SeveritySummary` response struct used by the advisory severity aggregation endpoint. This struct represents the count of advisories at each severity level for a given SBOM.

## Content

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Summary of advisory severity counts for an SBOM.
///
/// Aggregates the number of advisories at each severity level (Critical, High,
/// Medium, Low) linked to a specific SBOM, along with the total count. All
/// counts default to zero when no advisories exist at that level.
#[derive(Serialize, Deserialize, Debug, Clone, Default, ToSchema)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: u64,
    /// Number of advisories with High severity.
    pub high: u64,
    /// Number of advisories with Medium severity.
    pub medium: u64,
    /// Number of advisories with Low severity.
    pub low: u64,
    /// Total number of unique advisories across all severity levels.
    pub total: u64,
}
```

## Design Decisions

- **`u64` for counts**: Matches Rust conventions for non-negative counts; consistent with other counter types in the codebase.
- **`Default` derive**: Ensures all fields default to 0, satisfying the acceptance criterion that all severity levels default to 0 when no advisories exist.
- **`ToSchema` derive**: Enables automatic OpenAPI schema generation via utoipa, consistent with other model structs in the project.
- **Serialization**: `Serialize` and `Deserialize` enable JSON response serialization via Axum's `Json` extractor and potential request deserialization.
- **Documentation comments**: Every struct and field has a `///` doc comment per the code quality practices requirement.
