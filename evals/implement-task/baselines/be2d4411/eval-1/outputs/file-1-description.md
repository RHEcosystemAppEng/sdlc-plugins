# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: CREATE

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to a given SBOM. This struct is returned by the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Detailed Changes

### Struct Definition

```rust
use serde::Serialize;
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field contains the count of unique advisories at that severity level.
/// The `total` field is the sum of all severity counts.
#[derive(Clone, Debug, Default, Serialize, ToSchema)]
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

### Design Decisions

- **`Default` derive**: Ensures all fields initialize to 0, satisfying acceptance criterion "all severity levels default to 0 when no advisories exist."
- **`Serialize` derive**: Required for Axum's `Json` response serialization.
- **`ToSchema` derive**: For OpenAPI spec generation if the project uses `utoipa`.
- **`u32` type**: Counts are non-negative integers; `u32` is sufficient for advisory counts.
- **No `Deserialize`**: This struct is response-only (not used for request parsing).

### Conventions Followed

- Struct naming follows PascalCase domain convention (matches `AdvisorySummary`, `SbomSummary`).
- Documentation comment on the struct and each field (code quality practice from Step 6).
- Placed in `model/` directory following the module pattern.
- File named after the struct in snake_case (`severity_summary.rs`), matching `summary.rs`, `details.rs`.
