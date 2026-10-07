# File 4: Create `modules/fundamental/src/advisory/model/severity_summary.rs`

**Action:** Create new file

## Pre-implementation inspection

Before writing this file, inspect the sibling model file `modules/fundamental/src/advisory/model/summary.rs` using `mcp__serena_backend__find_symbol` to understand the `AdvisorySummary` struct's derive macros, field types, and serialization approach. Also inspect `modules/fundamental/src/advisory/model/details.rs` for a second reference point on model struct patterns.

## Contents

Define the `SeveritySummary` response struct:

```rust
use serde::{Deserialize, Serialize};

/// Aggregated advisory severity counts for a given SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to 0 when no advisories exist at a given level.
#[derive(Debug, Clone, Serialize, Deserialize, Default)]
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

**Pattern conformance:**
- Derives `Debug, Clone, Serialize, Deserialize` matching the pattern in `AdvisorySummary` and `SbomSummary`
- Also derives `Default` so an empty summary with all-zero counts can be created easily
- Uses `u32` for counts (non-negative integer)
- Includes `///` documentation comments on the struct and every field
- Field naming uses snake_case matching Rust conventions and the JSON response format specified in the task (`{ critical: N, high: N, medium: N, low: N, total: N }`)

**Serde configuration:**
- If sibling structs use `#[serde(rename_all = "camelCase")]`, apply the same attribute. Otherwise, snake_case field names will serialize directly, matching the task's API spec.
