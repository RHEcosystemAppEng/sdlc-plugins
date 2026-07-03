# File 4: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Inspection performed

Used `mcp__serena_backend__get_symbols_overview` on sibling model files to understand the pattern:
- `modules/fundamental/src/advisory/model/summary.rs` -- `AdvisorySummary` struct with `severity` field
- `modules/fundamental/src/advisory/model/details.rs` -- `AdvisoryDetails` struct
- `modules/fundamental/src/sbom/model/summary.rs` -- `SbomSummary` struct

All model structs derive `Debug, Clone, Serialize, Deserialize` and include doc comments.

## File content

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for advisories linked to a specific SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// The `total` field is the sum of all severity-level counts, representing the
/// total number of unique advisories regardless of severity.
#[derive(Debug, Clone, Default, Serialize, Deserialize, PartialEq)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: i64,
    /// Number of advisories with High severity.
    pub high: i64,
    /// Number of advisories with Medium severity.
    pub medium: i64,
    /// Number of advisories with Low severity.
    pub low: i64,
    /// Total number of unique advisories across all severity levels.
    pub total: i64,
}
```

## Rationale

- **Derive macros**: `Debug, Clone, Serialize, Deserialize` match the pattern used by `AdvisorySummary` and `AdvisoryDetails`. `PartialEq` is added for test assertions. `Default` provides zero-initialization per acceptance criteria ("all severity levels default to 0").
- **Field type `i64`**: Matches the numeric field types used in sibling model structs (consistent with database integer types in SeaORM).
- **Doc comments**: Every struct and field has a `///` doc comment per the skill's code quality requirements.
- **Serde serialization**: Fields will serialize to the JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` matching the API specification.
