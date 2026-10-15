# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

## Operation: CREATE

## Purpose

Define the `SeveritySummary` response struct used by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. This struct represents the aggregated severity counts for advisories linked to a given SBOM.

## Sibling Reference

Follows the pattern established in `modules/fundamental/src/advisory/model/summary.rs` (AdvisorySummary) and `modules/fundamental/src/advisory/model/details.rs` (AdvisoryDetails) for struct definition, derive macros, and documentation style.

## Detailed Changes

### Imports

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;
```

### Struct Definition

```rust
/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the number of unique advisories at that severity level.
/// The `total` field is the sum of all severity levels.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of advisories with critical severity.
    pub critical: u32,
    /// Number of advisories with high severity.
    pub high: u32,
    /// Number of advisories with medium severity.
    pub medium: u32,
    /// Number of advisories with low severity.
    pub low: u32,
    /// Total number of unique advisories across all severity levels.
    pub total: u32,
}
```

## Design Decisions

- **`Default` derive**: Ensures all fields initialize to 0, satisfying the acceptance criterion that all severity levels default to 0 when no advisories exist at that level.
- **`ToSchema` derive**: Enables automatic OpenAPI schema generation, consistent with other model structs.
- **`u32` type**: Counts are non-negative integers; `u32` is the idiomatic Rust choice for counts that will not exceed 4 billion.
- **Doc comments on every field**: Follows skill guidance requiring documentation on all new public symbols.
- **No `impl` block needed**: The struct is a plain data transfer object. Construction will happen in the service method using field initialization syntax.

## Conventions Applied

- PascalCase struct name (`SeveritySummary`)
- snake_case field names (`critical`, `high`, `medium`, `low`, `total`)
- Derive macro set matches sibling models (`Clone, Debug, Serialize, Deserialize, ToSchema`)
- Added `Default` to support zero-initialization pattern
- Doc comment on the struct and each public field
