# File 4: Create `modules/fundamental/src/advisory/model/severity_summary.rs`

## Change Type
Create new file

## Description
Define the `SeveritySummary` response struct that represents an aggregated count of advisory severities for a given SBOM. This struct is returned by the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Full File Content

```rust
//! Advisory severity summary model for SBOM-level severity aggregation.

use serde::{Deserialize, Serialize};

/// Aggregated count of advisory severities linked to a specific SBOM.
///
/// Each field represents the number of unique advisories at that severity level.
/// The `total` field is the sum of all severity counts. All fields default to 0
/// when no advisories exist at that level.
#[derive(Debug, Clone, Default, Serialize, Deserialize, PartialEq, Eq)]
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

## Conventions Followed
- Derives match sibling model structs: `Debug, Clone, Serialize, Deserialize`
- Added `Default` derive to support zero-initialization (acceptance criterion: all severity levels default to 0)
- Added `PartialEq, Eq` for test assertions with `assert_eq!`
- Documentation comment on the struct and every public field (code quality practice)
- Module-level doc comment (`//!`) consistent with Rust conventions
- File placed in `model/` directory following the `model/ + service/ + endpoints/` module pattern
- Snake_case file name matching the struct concept
- Uses `u32` for counts (non-negative integers, sufficient range for advisory counts)
