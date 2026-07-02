# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

New model struct representing the severity aggregation response for advisories linked to an SBOM.

## Detailed Changes

Create a new file with the following contents:

### Imports

```rust
use serde::{Deserialize, Serialize};
```

### SeveritySummary struct

```rust
/// Summary of advisory severity counts for an SBOM.
///
/// Contains the count of unique advisories at each severity level
/// and a total count, enabling dashboard widgets to render severity
/// breakdowns without client-side counting.
#[derive(Clone, Debug, Default, Deserialize, Serialize)]
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

## Conventions followed

- Derives match sibling model structs (`Serialize`, `Deserialize`, `Debug`, `Clone`)
- Added `Default` derive so all fields default to 0 (satisfying acceptance criterion: "all severity levels default to 0 when no advisories exist")
- Documentation comments on struct and every field (code quality practice from Step 6)
- File name matches the struct concept (`severity_summary.rs` for `SeveritySummary`)
