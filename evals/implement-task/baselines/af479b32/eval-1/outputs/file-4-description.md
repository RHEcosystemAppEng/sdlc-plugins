# File 4: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose
Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for a given SBOM.

## Full File Content

```rust
//! Advisory severity summary model.
//!
//! Provides the response type for the severity aggregation endpoint,
//! containing counts of advisories grouped by severity level.

use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Each field represents the number of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at that level.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
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
- **`Default` derive** ensures all fields initialize to 0, satisfying the acceptance criterion that severity levels default to 0 when no advisories exist
- **`ToSchema` derive** follows the convention for API response types (if utoipa is used for OpenAPI spec generation; if not used in the project, omit this derive)
- **`Clone` and `Debug`** are standard derives matching the patterns in sibling model structs (`SbomSummary`, `AdvisorySummary`)
- **`u64`** type chosen for count fields to match Rust idioms for non-negative counts; could be `i64` if the database layer returns signed integers -- confirm from sibling models
- **Doc comments** on the struct and every field, per the skill's code quality requirements
