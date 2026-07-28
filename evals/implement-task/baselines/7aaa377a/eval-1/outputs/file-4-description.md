# File 4: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to an SBOM.

## Content

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// The `total` field is the sum of all severity counts. All fields default to 0
/// when no advisories exist at a given level.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: u32,

    /// Count of advisories with High severity.
    pub high: u32,

    /// Count of advisories with Medium severity.
    pub medium: u32,

    /// Count of advisories with Low severity.
    pub low: u32,

    /// Total count of unique advisories across all severity levels.
    pub total: u32,
}
```

## Pattern Compliance

- **Derive macros**: follows sibling model structs (`AdvisorySummary`, `AdvisoryDetails`, `SbomSummary`) which derive `Clone`, `Debug`, `Serialize`, `Deserialize`, and `ToSchema`
- **Naming**: follows `<Domain><Role>` convention (e.g., `SeveritySummary` alongside `AdvisorySummary`, `SbomSummary`)
- **Documentation**: every struct and field has a doc comment per the skill's code quality requirements
- **Default derive**: implements `Default` so all counts initialize to 0, satisfying the acceptance criterion that all severity levels default to 0 when no advisories exist
- **Field types**: uses `u32` for counts (non-negative integers)
- **Serialization**: field names serialize as lowercase (`critical`, `high`, `medium`, `low`, `total`) matching the API spec `{ critical: N, high: N, medium: N, low: N, total: N }`

## Impact

- New file, no existing code affected
- Struct is used by `AdvisoryService::severity_summary` (file 2) and the endpoint handler (file 5)
