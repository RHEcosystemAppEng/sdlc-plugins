# File 4: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Pre-Implementation Inspection

Read sibling model files `summary.rs` and `details.rs` in the same directory to understand struct patterns, derive macros used, and documentation conventions.

## New File Content

```rust
//! Advisory severity summary model for SBOM severity aggregation.

use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Summary of advisory severity counts for an SBOM.
///
/// Provides per-severity-level counts of unique advisories linked to a
/// specific SBOM, enabling dashboard widgets to render severity breakdowns
/// without client-side counting.
#[derive(Debug, Clone, Default, Serialize, Deserialize, PartialEq, ToSchema)]
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

All fields default to 0 via `Default` derive, satisfying the acceptance criterion that all severity levels default to 0 when no advisories exist.
