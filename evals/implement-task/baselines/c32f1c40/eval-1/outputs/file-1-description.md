# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

## Action: CREATE

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity
counts for advisories linked to a given SBOM.

## Detailed Changes

### Struct Definition

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
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

### Design Decisions

- **Derives `Default`**: ensures all fields initialize to 0, satisfying the acceptance
  criterion that missing severity levels default to zero.
- **Derives `Serialize`/`Deserialize`**: enables Axum's `Json` extractor to serialize
  the response automatically, matching the convention in sibling models like
  `AdvisorySummary` and `SbomSummary`.
- **Derives `ToSchema`**: enables OpenAPI spec generation if the project uses `utoipa`.
- **Uses `u32`**: counts are non-negative integers; `u32` is idiomatic for counts in Rust
  and matches the expected JSON number output.
- **Doc comments on every field**: follows the skill's code quality practice requiring
  documentation on all new public symbols.

### Convention Conformance

- File naming: `severity_summary.rs` follows snake_case convention matching siblings
  `summary.rs` and `details.rs`.
- Struct naming: `SeveritySummary` follows PascalCase convention matching `AdvisorySummary`,
  `SbomSummary`, `PackageSummary`.
- Derive order follows Rust convention: std traits first, then serde, then utoipa.
