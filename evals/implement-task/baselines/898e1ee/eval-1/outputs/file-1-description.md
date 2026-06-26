# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents aggregated severity counts for advisories linked to an SBOM.

## Sibling files inspected

- `modules/fundamental/src/advisory/model/summary.rs` -- `AdvisorySummary` struct (has `severity` field, derives Serialize/Deserialize, includes doc comments)
- `modules/fundamental/src/advisory/model/details.rs` -- `AdvisoryDetails` struct (similar derive pattern)
- `modules/fundamental/src/sbom/model/summary.rs` -- `SbomSummary` struct (cross-module sibling, same derive pattern)

## Conventions applied

- Struct uses PascalCase naming: `SeveritySummary`
- Derives `Serialize`, `Deserialize`, `Debug`, `Clone`, `Default` (matching sibling model structs)
- All fields are `u64` (unsigned integer counts), defaulting to 0 via `Default` derive
- Documentation comment on the struct explaining its purpose

## Detailed changes

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to 0 when no advisories exist at a given level.
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
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

## Rationale

- `Default` derive ensures all counts start at 0, satisfying the acceptance criterion that "all severity levels default to 0 when no advisories exist at that level."
- `u64` is used for counts (matching typical Rust conventions for non-negative counters).
- The struct is returned directly as a JSON response via Axum's `Json` extractor, so `Serialize` is required.
- `Deserialize` is included for symmetry and testability (parsing response bodies in tests).
