# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: CREATE

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to a given SBOM. This struct is the response body for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Detailed Changes

### Struct Definition

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to 0 when no advisories exist at a given level.
#[derive(Clone, Debug, Default, Serialize, Deserialize, PartialEq, Eq)]
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

### Design Decisions

- **Derives**: `Serialize` and `Deserialize` for JSON serialization via Axum's `Json` extractor. `Default` so all fields start at 0. `Clone`, `Debug` for standard Rust patterns. `PartialEq`, `Eq` for test assertions.
- **Field types**: `u32` for counts -- advisory counts will not exceed u32 range.
- **Default**: deriving `Default` ensures all severity levels default to 0 when no advisories exist at that level, satisfying acceptance criterion #4.
- **Follows sibling pattern**: mirrors the structure of `summary.rs` and `details.rs` in the same `model/` directory.

### Convention Compliance

- Doc comments on the struct and all public fields (per code quality practices in Step 6)
- snake_case field names matching JSON output format
- Placed in `model/` directory following the module structure convention
