# File 2: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose
Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to a given SBOM.

## Full File Content

```rust
//! Advisory severity summary model.
//!
//! Provides the response type for the severity aggregation endpoint,
//! containing counts of advisories at each severity level for a given SBOM.

use serde::{Deserialize, Serialize};

/// Aggregated severity counts for advisories linked to a specific SBOM.
///
/// Each field contains the count of unique advisories at that severity level.
/// The `total` field is the sum of all severity-level counts.
#[derive(Debug, Clone, Default, Serialize, Deserialize, PartialEq, Eq)]
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
- Derives `Serialize`, `Deserialize` for Axum JSON response compatibility.
- Derives `Debug`, `Clone`, `Default` matching sibling model structs (`AdvisorySummary`, `SbomSummary`).
- Derives `PartialEq`, `Eq` to support assertion comparisons in tests.
- Module-level and struct-level doc comments using `///` convention.
- Field-level doc comments describing each count.
- Default implementation ensures all counts start at 0 when no advisories are present (satisfying acceptance criterion: "All severity levels default to 0 when no advisories exist at that level").
