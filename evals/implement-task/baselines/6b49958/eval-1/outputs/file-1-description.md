# File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for a given SBOM.

## Detailed Changes

Create a new file with the following contents:

### Imports

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;
```

### Struct Definition

```rust
/// Aggregated advisory severity counts for an SBOM.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: u32,
    /// Number of advisories with High severity.
    pub high: u32,
    /// Number of advisories with Medium severity.
    pub medium: u32,
    /// Number of advisories with Low severity.
    pub low: u32,
    /// Total number of unique advisories.
    pub total: u32,
}
```

### Design Decisions

- **`Default` derive:** Ensures all fields initialize to 0, satisfying the acceptance criterion that all severity levels default to 0 when no advisories exist.
- **`u32` type:** Advisory counts are non-negative integers; `u32` is sufficient and avoids the overhead of `i64` from database count queries (cast on aggregation).
- **`ToSchema` derive:** Follows the project convention of including OpenAPI schema generation for all response types.
- **`Serialize` + `Deserialize`:** `Serialize` is required for JSON responses; `Deserialize` follows the convention of making model types round-trippable and testable.
- **No `#[serde(rename_all)]`:** The field names (`critical`, `high`, `medium`, `low`, `total`) are already lowercase snake_case, which is serde's default. The JSON output matches the API contract directly.

### JSON Output Shape

```json
{
  "critical": 2,
  "high": 5,
  "medium": 3,
  "low": 1,
  "total": 11
}
```
