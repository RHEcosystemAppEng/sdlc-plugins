# File 4: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for a given SBOM.

## Full File Contents

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// The `total` field is the sum of all severity counts. When no advisories exist
/// for a given severity level, its count defaults to 0.
#[derive(Debug, Clone, Serialize, Deserialize)]
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

## Conventions Followed

- **Derive macros**: `Debug`, `Clone`, `Serialize`, `Deserialize` matching sibling model structs (`AdvisorySummary`, `SbomSummary`)
- **Naming**: Follows `<Purpose>` naming pattern for response structs (analogous to `AdvisorySummary`, `SbomDetails`)
- **Documentation**: Every struct and field has a `///` doc comment
- **Field types**: Uses `u64` for counts, consistent with unsigned integer usage in Rust for non-negative counters
- **Serde**: Derives both `Serialize` (for JSON response) and `Deserialize` (for potential future use/testing)
- **Module location**: Placed in `model/` directory alongside sibling model files `summary.rs` and `details.rs`
