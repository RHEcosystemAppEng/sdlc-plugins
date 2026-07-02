# File 1: Create `modules/fundamental/src/advisory/model/severity_summary.rs`

## Purpose
Define the `SeveritySummary` response struct that represents aggregated severity counts for advisories linked to an SBOM.

## Reference Files to Inspect First
- `modules/fundamental/src/advisory/model/summary.rs` -- Sibling model file; inspect for struct definition patterns, derive macros, and field naming conventions.

## Changes

Create a new file with the following content:

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to 0 when no advisories exist at a given level.
#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: i64,
    /// Count of advisories with High severity.
    pub high: i64,
    /// Count of advisories with Medium severity.
    pub medium: i64,
    /// Count of advisories with Low severity.
    pub low: i64,
    /// Total count of unique advisories across all severity levels.
    pub total: i64,
}
```

## Notes
- The `Default` derive ensures all fields start at 0, satisfying the acceptance criterion that severity levels default to 0 when no advisories exist.
- The integer type (`i64`) should match whatever the sibling `AdvisorySummary` or database count types use -- adjust after inspecting sibling model files.
- Derive macros (`Serialize`, `Deserialize`, `Debug`, `Clone`, `PartialEq`) follow the pattern observed in sibling model structs like `AdvisorySummary`.
