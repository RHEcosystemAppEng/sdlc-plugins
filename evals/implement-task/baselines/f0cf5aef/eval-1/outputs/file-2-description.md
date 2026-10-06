# File 2: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated advisory
severity counts for a given SBOM. This is the response type for the new
`GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Pre-implementation inspection

Before creating, inspect sibling model files to confirm patterns:
```
mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/model/summary.rs")
mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/model/details.rs")
```

Also check for existing `SeveritySummary` or `severity_summary` symbols to avoid
duplication:
```
mcp__serena_backend__search_for_pattern("SeveritySummary")
mcp__serena_backend__search_for_pattern("severity_summary")
```

## Content

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated advisory severity counts for a single SBOM.
///
/// Each field represents the number of unique advisories at that severity level
/// linked to the SBOM. The `total` field is the sum of all severity counts.
#[derive(Debug, Clone, Default, Serialize, Deserialize, ToSchema)]
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

## Design decisions

- **`Default` derive**: All fields default to 0, satisfying AC "All severity levels default to 0 when no advisories exist at that level."
- **`ToSchema` derive**: Include if siblings use utoipa for OpenAPI spec generation (inspect `AdvisorySummary` in `summary.rs` to confirm). If siblings do not use utoipa, omit.
- **`u64` type**: Matches the expected unsigned count semantics. If siblings use `i64` or `usize`, adjust to match.
- **Doc comments**: Every public symbol has a doc comment per skill guidance.
- **Field ordering**: Critical > High > Medium > Low > Total, matching the natural severity ordering and the API contract in the task description.

## Convention conformance

- Derive list order matches sibling pattern (Debug, Clone, then Serialize/Deserialize)
- Doc comment style uses `///` as standard Rust convention
- File-level organization: imports, then struct definition (no extra logic in model files)
