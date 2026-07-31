# File 4: Create `modules/fundamental/src/advisory/model/severity_summary.rs`

## Purpose
Define the `SeveritySummary` response struct for the severity aggregation endpoint.

## Pattern Reference
Follows the pattern of sibling model files `summary.rs` (AdvisorySummary) and `details.rs` (AdvisoryDetails) in the same directory.

## Content

```rust
use serde::Serialize;
use utoipa::ToSchema;

/// Summary of advisory severity counts for an SBOM.
///
/// Contains counts of advisories grouped by severity level (Critical, High,
/// Medium, Low) and a total count. All severity levels default to 0 when no
/// advisories exist at that level.
#[derive(Debug, Clone, Serialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of critical-severity advisories.
    pub critical: u64,
    /// Number of high-severity advisories.
    pub high: u64,
    /// Number of medium-severity advisories.
    pub medium: u64,
    /// Number of low-severity advisories.
    pub low: u64,
    /// Total number of unique advisories across all severity levels.
    pub total: u64,
}
```

## Notes
- Uses `#[derive(Serialize)]` for JSON serialization via Axum's `Json` extractor
- Uses `#[derive(ToSchema)]` for OpenAPI spec generation (utoipa), matching sibling model patterns
- All fields are `u64` to match count semantics; default to 0 when no advisories exist
- Documentation comments on every field and the struct itself, following skill guidance on documentation for new symbols
