# File 1: CREATE — `modules/fundamental/src/advisory/model/severity_summary.rs`

## Purpose
Define the `SeveritySummary` response struct that holds per-severity advisory counts.

## Changes

Create a new file with:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Summary of advisory severity counts for a given SBOM.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    pub critical: u32,
    pub high: u32,
    pub medium: u32,
    pub low: u32,
    pub total: u32,
}
```

## Conventions Applied

- Follows the same struct pattern as `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`
- Derives `Serialize`, `Deserialize`, `ToSchema` matching sibling model structs
- Includes `Default` derive so all counts initialize to 0 when no advisories exist
- Documentation comment on the struct following code quality practices
