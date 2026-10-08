# File 4: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct for the advisory severity aggregation endpoint.

## Pre-Implementation Analysis

Before creating, would analyze sibling model files:
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/summary.rs` -- understand `AdvisorySummary` struct pattern (derives, fields, visibility)
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/details.rs` -- understand `AdvisoryDetails` struct pattern
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/model/summary.rs` -- cross-module model comparison

### Symbol deduplication check

Before declaring `SeveritySummary`, would search the target package for existing definitions:
- `mcp__serena_backend__search_for_pattern` for `SeveritySummary`, `severity_summary`, `SeverityCount`
- Grep for `critical.*high.*medium.*low` patterns to find any existing severity aggregation struct
- If found, reuse the existing definition instead of creating a new one

## File Content

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Summary of advisory severity counts for an SBOM.
///
/// Aggregates the number of linked vulnerability advisories by severity level,
/// enabling dashboard widgets to render severity breakdowns without client-side
/// counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
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

## Key Decisions

- **Derives**: `Serialize`, `Deserialize` for JSON serialization (matching sibling models); `Default` to provide all-zeros baseline per acceptance criteria; `Clone`, `Debug` for standard Rust ergonomics; `ToSchema` for OpenAPI spec generation if utoipa is used (following sibling patterns)
- **Field types**: `u64` for counts (non-negative integers, sufficient range)
- **Default**: All fields default to 0 via `Default` derive, satisfying "all severity levels default to 0 when no advisories exist"
- **Documentation**: Doc comments on struct and every field per skill quality requirements
- **Visibility**: `pub` fields matching sibling model conventions
