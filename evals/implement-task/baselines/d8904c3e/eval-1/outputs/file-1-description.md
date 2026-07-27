# File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to a given SBOM.

## Detailed Changes

Create a new file with the following content:

### Imports

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;
```

### Struct Definition

```rust
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

- **`Default` derive**: Ensures all fields initialize to 0, satisfying the acceptance criterion that all severity levels default to 0 when no advisories exist.
- **`u32` type**: Non-negative counts; `u32` is sufficient for advisory counts (max ~4 billion).
- **`ToSchema` derive**: If the project uses `utoipa` for OpenAPI generation, this makes the struct available in the API spec. If not used, this derive can be omitted.
- **`Serialize` + `Deserialize`**: Required for Axum's `Json` extractor to serialize the response and for tests to deserialize it.
- **Documentation comments**: Every field has a `///` doc comment per the skill's code quality practices requirement.

### Sibling Parity

Follows the same pattern as `AdvisorySummary` in `model/summary.rs` and `AdvisoryDetails` in `model/details.rs`:
- Same derive macros
- Same field documentation style
- Same file-level module structure
