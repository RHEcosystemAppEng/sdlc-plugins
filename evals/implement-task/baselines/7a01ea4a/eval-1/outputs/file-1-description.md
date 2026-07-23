# File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated advisory severity counts for a given SBOM. This struct is the return type for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Pre-implementation inspection

Before creating this file, inspect these sibling files to understand the established model patterns:

- **`modules/fundamental/src/advisory/model/summary.rs`** -- Read via `mcp__serena_backend__get_symbols_overview` to see the `AdvisorySummary` struct, its derives, its fields (including the `severity` field we will aggregate), and its documentation style.
- **`modules/fundamental/src/advisory/model/details.rs`** -- Read via `mcp__serena_backend__get_symbols_overview` to confirm the struct pattern is consistent across sibling model files (derives, visibility, documentation).
- **`modules/fundamental/src/sbom/model/summary.rs`** -- Read to verify cross-module consistency in model struct conventions.

## Detailed changes

Create the file with the following content:

```rust
use serde::{Deserialize, Serialize};

/// Aggregated advisory severity counts for a specific SBOM.
///
/// Contains the number of unique advisories at each severity level
/// (Critical, High, Medium, Low) plus a total count, enabling dashboard
/// widgets to render severity breakdowns without client-side counting.
#[derive(Debug, Clone, Serialize, Deserialize, Default, PartialEq, Eq)]
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

## Conventions followed

- Derives match sibling model structs (`Debug, Clone, Serialize, Deserialize`)
- Added `Default` for zero-initialization and `PartialEq, Eq` for test assertions
- Documentation comment on struct and each field
- `pub` visibility on all fields, consistent with sibling models
- snake_case field names
