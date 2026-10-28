# File 4: modules/fundamental/src/advisory/model/severity_summary.rs

## Action: CREATE

## Pre-implementation Inspection

Before creating, would inspect sibling model files for convention conformance:

1. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/model/summary.rs")` -- see `AdvisorySummary` struct shape, derives, field types
2. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/model/details.rs")` -- see `AdvisoryDetails` struct shape for comparison
3. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/sbom/model/summary.rs")` -- cross-module comparison of model struct pattern

### Symbol deduplication check

Before declaring `SeveritySummary`, would search:
- `mcp__serena_backend__find_symbol(name_path_pattern="SeveritySummary")` -- confirm no existing definition
- Grep for `severity_summary` and `SeveritySummary` across the codebase

## File Content

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
#[derive(Clone, Debug, Default, Serialize, Deserialize, PartialEq, Eq)]
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

## Design Decisions

- **Derives**: `Serialize` and `Deserialize` for JSON serialization (matches sibling model structs). `Default` for zero-initialization. `Clone`, `Debug` for standard Rust ergonomics. `PartialEq`, `Eq` for test assertions.
- **Field type**: `u32` for counts -- sufficient range, non-negative by type. Matches the JSON response shape `{ critical: N, high: N, medium: N, low: N, total: N }`.
- **Default**: Deriving `Default` gives all fields `0`, satisfying the acceptance criterion that all severity levels default to 0 when no advisories exist.
- **Documentation**: Every field and the struct itself has a `///` doc comment per the skill's code quality practices.

## Convention conformance

- File name: snake_case matching the struct concept (`severity_summary.rs`)
- Struct name: PascalCase (`SeveritySummary`), consistent with `AdvisorySummary`, `SbomSummary`
- Derives: matches the derive set used by sibling model structs (would confirm exact set during inspection)
- Field naming: snake_case, consistent with Rust and serde defaults
- Uses `serde` for serialization, matching all other model structs
