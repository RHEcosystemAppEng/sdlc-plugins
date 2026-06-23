# File 1: Create `modules/fundamental/src/advisory/model/severity_summary.rs`

## Action: CREATE

## Purpose
Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for a given SBOM.

## Conventions Applied
- Model struct derives `Serialize, Deserialize, Debug, Clone` (sibling pattern from `summary.rs`, `details.rs`)
- Struct lives in its own file named after its role (`severity_summary.rs`)
- PascalCase type name (`SeveritySummary`)
- Documentation comment on the struct explaining its purpose

## Detailed Changes

Create a new file with the following content:

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// The `total` field is the sum of all severity levels.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: u64,
    /// Count of advisories with High severity.
    pub high: u64,
    /// Count of advisories with Medium severity.
    pub medium: u64,
    /// Count of advisories with Low severity.
    pub low: u64,
    /// Total count of unique advisories across all severity levels.
    pub total: u64,
}

impl Default for SeveritySummary {
    fn default() -> Self {
        Self {
            critical: 0,
            high: 0,
            medium: 0,
            low: 0,
            total: 0,
        }
    }
}
```

## Rationale
- The struct mirrors the API response shape: `{ critical: N, high: N, medium: N, low: N, total: N }`
- `Default` impl ensures all counts start at 0, satisfying the acceptance criterion that all severity levels default to 0 when no advisories exist
- Using `u64` for counts is consistent with typical Rust patterns for non-negative integer counters
- Documentation comments on every field follow the code quality practice from the skill specification
