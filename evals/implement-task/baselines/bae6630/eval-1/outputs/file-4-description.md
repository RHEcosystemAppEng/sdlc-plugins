# File 4: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: Create (new file)

## Pre-Implementation Inspection

Before creating, inspect sibling model files for pattern conformance:
- `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` to see the derive macros, field types, and documentation style
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/details.rs` and `modules/fundamental/src/sbom/model/summary.rs` to confirm model conventions

## File Contents

Create a new `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to an SBOM.

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All fields default to 0 when no advisories exist at a given level.
#[derive(Clone, Debug, Serialize, Deserialize, Default, PartialEq, Eq)]
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

- Derives match sibling model structs: `Clone`, `Debug`, `Serialize`, `Deserialize`
- Added `Default` to support zero-initialization for all fields
- Added `PartialEq` and `Eq` for use in test assertions
- Used `u32` for counts (sufficient for advisory counts, consistent with typical counter types in the codebase)
- Every field has a `///` doc comment per the skill's code quality requirements
- The struct-level doc comment explains what the struct represents and its zero-default behavior
