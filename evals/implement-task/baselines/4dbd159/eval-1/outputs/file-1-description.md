# File 1: Create `modules/fundamental/src/advisory/model/severity_summary.rs`

## Purpose

Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for a given SBOM.

## Detailed Changes

Create a new file with the following content:

### Imports

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;
```

Following the sibling pattern from `summary.rs` and `details.rs` which derive these traits on all model structs.

### SeveritySummary Struct

```rust
/// Aggregated advisory severity counts for an SBOM.
///
/// Each field represents the count of unique advisories at that severity level
/// linked to the SBOM. All counts default to zero when no advisories exist
/// at a given level.
#[derive(Clone, Debug, Default, Deserialize, Serialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of critical-severity advisories.
    pub critical: u64,
    /// Number of high-severity advisories.
    pub high: u64,
    /// Number of medium-severity advisories.
    pub medium: u64,
    /// Number of low-severity advisories.
    pub low: u64,
    /// Total number of unique advisories across all severity levels.
    pub total: u64,
}
```

### Design Decisions

- **`Default` derive**: Ensures all fields initialize to 0, satisfying AC "all severity levels default to 0 when no advisories exist"
- **`u64` type**: Matches typical count types in Rust; large enough for any realistic advisory count
- **`ToSchema` derive**: Follows sibling model pattern for OpenAPI spec generation
- **Doc comments on every field and struct**: Required by skill Step 6 code quality practices -- every new struct and public field gets a documentation comment
- **Snake_case field names**: Matches the JSON response shape `{ critical: N, high: N, medium: N, low: N, total: N }` specified in the task, and follows sibling model conventions
