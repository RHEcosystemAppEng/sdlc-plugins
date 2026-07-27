# File 4: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to an SBOM.

## Pre-implementation inspection

Before creating, inspect sibling model files to understand the pattern:
1. `modules/fundamental/src/advisory/model/summary.rs` -- AdvisorySummary struct: derive macros, field types, serde attributes, documentation style.
2. `modules/fundamental/src/advisory/model/details.rs` -- AdvisoryDetails struct: same patterns.
3. `modules/fundamental/src/sbom/model/summary.rs` -- SbomSummary struct: cross-module sibling for additional pattern confirmation.

## File contents

```rust
use serde::Serialize;
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to 0 when no advisories exist at a given level.
#[derive(Clone, Debug, Default, Serialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of critical-severity advisories.
    pub critical: u32,

    /// Number of high-severity advisories.
    pub high: u32,

    /// Number of medium-severity advisories.
    pub medium: u32,

    /// Number of low-severity advisories.
    pub low: u32,

    /// Total number of unique advisories across all severity levels.
    pub total: u32,
}
```

## Design decisions

- **`Default` derive:** Ensures all severity counts initialize to 0, satisfying the acceptance criterion that "all severity levels default to 0 when no advisories exist at that level."
- **`u32` field type:** Non-negative counts; `u32` is appropriate for advisory counts and matches typical Rust patterns for counters.
- **`Serialize` only (no `Deserialize`):** This struct is only used for outgoing responses, never parsed from incoming requests.
- **`ToSchema` derive:** For OpenAPI/utoipa schema generation if the project uses it (following patterns seen in sibling model structs).
- **`Clone` and `Debug` derives:** Standard Rust patterns for data structs; enables use in tests and logging.
- **Doc comments on every field:** Follows the SKILL.md requirement that every new public symbol has documentation.

## Conventions applied

- **Derive macro order:** `Clone, Debug, Default, Serialize, ToSchema` -- alphabetical, matching sibling models
- **Documentation:** `///` doc comments on the struct and every field
- **Module imports:** `serde::Serialize` and `utoipa::ToSchema` -- matching sibling model import patterns
- **Field naming:** Lowercase severity level names matching the JSON response format `{ critical: N, high: N, medium: N, low: N, total: N }`
