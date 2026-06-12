# File 1 -- CREATE: modules/fundamental/src/advisory/model/severity_summary.rs

## Purpose

Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for a given SBOM.

## Conventions Applied

- **Module structure:** Follows the pattern of sibling model files (`summary.rs`, `details.rs`) in the same directory -- one struct per file.
- **Naming:** Struct name follows `<Concept><Role>` pattern consistent with `AdvisorySummary`, `AdvisoryDetails`, `SbomSummary`.
- **Derive macros:** Uses `#[derive(Clone, Debug, Serialize, Deserialize)]` consistent with sibling model structs.
- **Documentation:** Every public struct and field has a `///` doc comment per skill Step 6 code quality requirements.

## Detailed Changes

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Provides a breakdown of advisory counts by severity level, enabling
/// dashboard widgets to render severity distributions without client-side counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
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

## Key Design Decisions

- `Default` derive ensures all fields initialize to 0 when no advisories exist at a given severity level (acceptance criterion #4).
- `u32` chosen for count fields -- sufficient range, matches unsigned nature of counts.
- `total` is a separate field rather than computed, allowing the service to set it explicitly after deduplication (acceptance criterion #3).
- Struct is kept flat (no nested objects) matching the API contract: `{ critical: N, high: N, medium: N, low: N, total: N }`.
