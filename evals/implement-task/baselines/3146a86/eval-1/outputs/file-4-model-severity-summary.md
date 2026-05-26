# File 4 — Create: `modules/fundamental/src/advisory/model/severity_summary.rs`

## Purpose

Define the `SeveritySummary` response struct that is returned by `GET /api/v2/sbom/{id}/advisory-summary`.

## Full File Content

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Advisory severity count summary for a given SBOM.
///
/// Contains the count of unique advisories at each severity level and
/// a total count. All fields default to 0 when no advisories are linked
/// to the SBOM.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of advisories rated Critical.
    pub critical: u64,

    /// Number of advisories rated High.
    pub high: u64,

    /// Number of advisories rated Medium.
    pub medium: u64,

    /// Number of advisories rated Low.
    pub low: u64,

    /// Total number of unique advisories across all severity levels.
    pub total: u64,
}
```

## Design Decisions

- **`#[derive(Default)]`**: enables `SeveritySummary::default()` to produce all-zeros in the service method without manual construction, satisfying the acceptance criterion "all severity levels default to 0".
- **`u64` fields**: advisory counts are non-negative integers. `u64` avoids signed arithmetic and matches JSON number semantics for dashboard consumers.
- **`pub` fields**: consistent with sibling model structs (`AdvisorySummary`, `SbomSummary`) which expose fields publicly for JSON serialization.
- **`ToSchema` derive**: required for OpenAPI spec generation via `utoipa` (matches `AdvisorySummary` sibling pattern).
- **`Clone, Debug`**: standard derives for model structs in this codebase.

## JSON Representation (example)

```json
{
  "critical": 2,
  "high": 5,
  "medium": 3,
  "low": 1,
  "total": 11
}
```

## Inspection Steps

1. `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` — verify exact derive macros used (Clone, Debug, Serialize, Deserialize, ToSchema).
2. `mcp__serena_backend__find_symbol` on `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` — cross-check field visibility and derive pattern.
3. Write the file using the Write tool (new file, no existing content).
