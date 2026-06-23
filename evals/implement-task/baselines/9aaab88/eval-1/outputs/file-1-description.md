# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: CREATE

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to an SBOM. This is the response body for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Sibling Reference

Follows the pattern of `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`) and `modules/fundamental/src/advisory/model/details.rs` (`AdvisoryDetails`) for derive macros, documentation, and struct layout.

## Detailed Changes

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
#[derive(Clone, Debug, Default, Deserialize, Serialize, PartialEq, Eq, ToSchema)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: u64,
    /// Count of advisories with High severity.
    pub high: u64,
    /// Count of advisories with Medium severity.
    pub medium: u64,
    /// Count of advisories with Low severity.
    pub low: u64,
    /// Total count of unique advisories across all severity levels.
    pub total: u64,
}
```

## Key Design Decisions

- **`Default` derive**: Ensures all fields initialize to 0, satisfying acceptance criterion #4 ("all severity levels default to 0 when no advisories exist")
- **`Serialize`/`Deserialize`**: Required for JSON response serialization via Axum's `Json` extractor and for test deserialization
- **`ToSchema`**: Required for OpenAPI spec generation (consistent with other model structs in the project)
- **`PartialEq, Eq`**: Enables `assert_eq!` in tests
- **`u64` for counts**: Matches the project's convention for count fields; unsigned since counts are non-negative
- **Documentation**: Every field and the struct itself has a doc comment per the skill's code quality requirements

## Integration

This file is registered in the module system by the change to `modules/fundamental/src/advisory/model/mod.rs` (see file-6-description.md).
