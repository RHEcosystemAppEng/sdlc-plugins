# File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity
counts for advisories linked to an SBOM.

## Detailed Changes

### Struct definition

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the number of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
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

### Design decisions

- **Derive `Default`**: ensures all counts initialize to 0, satisfying the acceptance
  criterion that missing severity levels default to zero.
- **Derive `Serialize`**: required for Axum's `Json` extractor to serialize the response.
- **Derive `ToSchema`**: follows the pattern of sibling model structs (`AdvisorySummary`,
  `SbomSummary`) which derive `ToSchema` for OpenAPI spec generation.
- **`u64` for counts**: matches the typical count type in the codebase; counts cannot
  be negative.
- **Doc comments on every field**: follows the code quality practice requiring
  documentation on all new public symbols.

### Conventions followed

- File naming matches sibling pattern: `summary.rs`, `details.rs` -> `severity_summary.rs`.
- Struct naming matches sibling pattern: `AdvisorySummary`, `AdvisoryDetails` -> `SeveritySummary`.
- Derive list matches sibling model structs.
