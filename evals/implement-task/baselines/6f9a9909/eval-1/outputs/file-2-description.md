# File 2: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct returned by the new aggregation endpoint.

## Content

```rust
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for an SBOM.
///
/// Contains the number of unique advisories at each severity level
/// linked to a given SBOM, plus a total count.
#[derive(Debug, Clone, Serialize, Deserialize, Default, PartialEq, Eq)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: u64,
    /// Number of advisories with High severity.
    pub high: u64,
    /// Number of advisories with Medium severity.
    pub medium: u64,
    /// Number of advisories with Low severity.
    pub low: u64,
    /// Total number of unique advisories across all severity levels.
    pub total: u64,
}
```

## Design Decisions

- **`Default` derive**: All fields default to `0`, satisfying the acceptance criterion
  that missing severity levels default to 0.
- **`PartialEq, Eq`**: Enables direct comparison in tests with `assert_eq!`.
- **`Serialize, Deserialize`**: Required for JSON serialization via Axum's `Json` extractor
  and for potential use as an input type in other contexts.
- **`u64`**: Unsigned integer matches the domain (counts cannot be negative) and aligns
  with SeaORM's typical count return types.
- **Doc comments**: Every field and the struct itself have `///` doc comments per the
  skill's code quality requirement and Rust convention.

## Conventions Applied

- File naming: `snake_case.rs` matching sibling `summary.rs` and `details.rs`
- Struct naming: `PascalCase` domain noun, matching `AdvisorySummary`, `AdvisoryDetails`
- Derive order: matches common Rust convention (Debug, Clone, Serialize, ...)
