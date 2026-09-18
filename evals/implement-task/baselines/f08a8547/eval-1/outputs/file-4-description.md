# File 4: SeveritySummary Response Struct

**File**: `modules/fundamental/src/advisory/model/severity_summary.rs`
**Action**: CREATE

## Purpose

Defines the `SeveritySummary` struct used as the response type for the
`GET /api/v2/sbom/{id}/advisory-summary` endpoint. Contains counts of advisories
by severity level.

## Full File Content

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated advisory severity counts for an SBOM.
///
/// Each field represents the number of unique advisories at that severity level
/// linked to the target SBOM. The `total` field is the sum of all severity counts.
#[derive(Debug, Clone, Default, Serialize, Deserialize, ToSchema)]
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

1. **`Default` derive**: ensures all fields default to 0, satisfying the acceptance
   criterion that severity levels default to 0 when no advisories exist.

2. **`u64` type**: advisory counts are non-negative integers. `u64` is appropriate
   for counts and matches idiomatic Rust (avoids signed integer for a value that
   cannot be negative).

3. **`ToSchema` derive**: enables OpenAPI spec generation via `utoipa`, following
   the project's convention for API response types.

4. **`Serialize` + `Deserialize`**: `Serialize` is required for JSON response
   serialization. `Deserialize` is included for symmetry and test deserialization
   of response bodies.

5. **Documentation comments**: every field has a `///` doc comment, following
   the skill's code quality practice for new symbols.

## Convention Adherence

- Follows the struct-per-file pattern from siblings (`summary.rs`, `details.rs`).
- Uses the same derive macro set as sibling model structs.
- Field naming uses snake_case (Rust convention), which serializes to snake_case
  JSON by default via serde. The API response format `{ critical: N, high: N, ... }`
  specified in the task matches this default behavior.

## Sibling Comparison

| Aspect | AdvisorySummary (sibling) | SeveritySummary (new) |
|--------|--------------------------|----------------------|
| Derives | Debug, Clone, Serialize, Deserialize, ToSchema | Debug, Clone, Default, Serialize, Deserialize, ToSchema |
| Fields | id, severity, title, etc. | critical, high, medium, low, total |
| Purpose | Represents a single advisory | Aggregated counts across advisories |

The `Default` derive is added because this struct needs a zero-value state (no
advisories case), which is not typical for entity-representing structs like
`AdvisorySummary`.
