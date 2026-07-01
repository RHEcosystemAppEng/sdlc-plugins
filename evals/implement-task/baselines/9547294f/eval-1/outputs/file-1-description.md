# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to an SBOM.

## Detailed Changes

Create a new file with the following content:

```rust
//! Severity summary model for advisory aggregation.
//!
//! Provides a response struct that contains counts of advisories
//! grouped by severity level for a given SBOM.

use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Each field represents the number of unique advisories at that severity level.
/// The `total` field is the sum of all severity levels. All fields default to 0
/// when no advisories exist at that level.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
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

## Conventions Applied

- File named after the concept it represents (`severity_summary.rs`), matching `summary.rs` and `details.rs` siblings
- Struct derives `Clone, Debug, Default, Serialize, Deserialize, ToSchema` matching sibling model structs
- Documentation comment on the struct and each field using `///` convention
- `Default` derive ensures all fields initialize to 0, satisfying the acceptance criterion that severity levels default to 0
- Located in the `model/` directory following the `model/ + service/ + endpoints/` module structure convention
