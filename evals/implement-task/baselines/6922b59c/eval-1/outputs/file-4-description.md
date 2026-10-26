# File 4: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for an SBOM.

## Pre-Implementation Inspection

Before creating, would:
1. `mcp__serena_backend__get_symbols_overview` on `model/summary.rs` to understand the struct derive pattern, field visibility, and serde configuration
2. `mcp__serena_backend__get_symbols_overview` on `model/details.rs` to confirm consistency across model siblings
3. `mcp__serena_backend__search_for_pattern` for `SeveritySummary` across the entire repository to verify no existing definition (symbol deduplication check)
4. Check `common/src/model/` for any shared response types that could be reused

## File Content

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated advisory severity counts for an SBOM.
///
/// Provides a breakdown of vulnerability advisory counts by severity level,
/// enabling dashboard widgets to render severity distributions without
/// client-side counting.
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

## Notes

- **Derive macros:** Follow the sibling pattern from `summary.rs` and `details.rs`. The exact set of derives would be confirmed by inspecting siblings. `Default` is included to ensure all fields default to 0 (satisfying AC: "All severity levels default to 0 when no advisories exist at that level"). `ToSchema` is included if the project uses `utoipa` for OpenAPI documentation (would verify from siblings).
- **Serde configuration:** If siblings use `#[serde(rename_all = "camelCase")]`, this struct would also use it, which would rename fields to `critical`, `high`, `medium`, `low`, `total` (already lowercase, so no change). If siblings use snake_case JSON output, the field names are already snake_case.
- **u64 type:** Chosen for count fields. If siblings use `i64` or `usize` for counts, would match that type for consistency.
- **Documentation comments:** Every public struct and field has a `///` doc comment as required by the skill's code quality practices.
- **Defensive design:** `Default` derive ensures that a default-constructed `SeveritySummary` has all zeros, which handles the "no advisories" case cleanly.
