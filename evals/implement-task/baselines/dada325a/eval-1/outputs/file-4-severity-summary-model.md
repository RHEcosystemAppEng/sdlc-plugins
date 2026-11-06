# File 4 (CREATE): `modules/fundamental/src/advisory/model/severity_summary.rs`

## Purpose
The response struct for `GET /api/v2/sbom/{id}/advisory-summary`.

## Content
```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Counts of unique advisories affecting an SBOM, grouped by severity level.
///
/// Every level defaults to `0` when no advisory at that level is linked to the SBOM.
#[derive(Serialize, Deserialize, Debug, Clone, Default, PartialEq, Eq, ToSchema)]
pub struct SeveritySummary {
    /// Number of unique advisories with Critical severity.
    pub critical: u64,
    /// Number of unique advisories with High severity.
    pub high: u64,
    /// Number of unique advisories with Medium severity.
    pub medium: u64,
    /// Number of unique advisories with Low severity.
    pub low: u64,
    /// Total number of unique advisories linked to the SBOM.
    pub total: u64,
}
```

## Notes
- Field names serialize as `critical`, `high`, `medium`, `low`, `total`, which matches the API contract exactly.
  No `rename_all` is needed.
- `Default` provides the "all levels default to 0" acceptance criterion.
- The derive list mirrors `AdvisorySummary`. `ToSchema` is kept only if siblings derive it.
- `Deserialize` lets the integration tests deserialize the body and compare whole structs.
