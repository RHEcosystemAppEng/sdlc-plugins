# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: Create new file

## Purpose

Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for a given SBOM. This struct is returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Detailed Changes

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated advisory severity counts for a given SBOM.
///
/// Contains the number of unique advisories at each severity level
/// (Critical, High, Medium, Low) and a total count across all levels.
#[derive(Clone, Debug, Default, Deserialize, Serialize, ToSchema)]
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

## Conventions Applied

- **Naming**: follows `<Entity><Role>` pattern consistent with `AdvisorySummary`, `AdvisoryDetails`, `SbomSummary`
- **Derives**: matches sibling model structs (`Serialize`, `Deserialize`, `Debug`, `Clone`, `ToSchema`)
- **Default derive**: ensures all fields default to 0 when no advisories exist (satisfies acceptance criterion)
- **Documentation**: doc comments on the struct and each field per the code quality practices requirement
- **Module location**: placed in `advisory/model/` alongside sibling model files (`summary.rs`, `details.rs`)
