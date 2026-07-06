# File 1: Create `modules/fundamental/src/advisory/model/severity_summary.rs`

## Purpose

Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for a given SBOM. This struct is returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Pre-Implementation Inspection

Before creating this file, inspect:
- **`modules/fundamental/src/advisory/model/summary.rs`** — Examine the `AdvisorySummary` struct to understand the model pattern: derive macros used, serde attributes, field types, and documentation style.
- **`modules/fundamental/src/advisory/model/details.rs`** — Examine the `AdvisoryDetails` struct as a second sibling for comparison.
- **`modules/fundamental/src/sbom/model/summary.rs`** — Cross-module sibling for additional pattern confirmation.

## Changes

Create a new file with the following content:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to a specific SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// The `total` field is the sum of all severity levels.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
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
```

## Conventions Applied

- **Derive macros**: `Clone`, `Debug`, `Default`, `Serialize`, `Deserialize`, `ToSchema` — matching the pattern from sibling model structs like `AdvisorySummary`.
- **Default derive**: Ensures all fields default to `0` when no advisories exist, satisfying the acceptance criterion that all severity levels default to 0.
- **Documentation**: Every struct and field has a doc comment (`///`), following the code quality practice requirement for new symbols.
- **File naming**: Named after the struct it contains (`severity_summary.rs` for `SeveritySummary`), matching the convention of `summary.rs` for `AdvisorySummary`.
