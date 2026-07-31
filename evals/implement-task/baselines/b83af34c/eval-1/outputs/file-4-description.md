# File 4: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Pre-implementation Inspection

Before creating, would inspect sibling model files to match conventions:

1. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/model/summary.rs")` -- see AdvisorySummary struct fields, derives, and doc comments.
2. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/model/details.rs")` -- see AdvisoryDetails struct for additional pattern reference.
3. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/sbom/model/summary.rs")` -- cross-module sibling for comparison.

## File Content

```rust
//! Advisory severity summary model.
//!
//! Provides the response type for the SBOM advisory severity aggregation endpoint.

use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
#[derive(Clone, Debug, Default, Deserialize, Serialize, ToSchema)]
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

## Rationale

- **Derives**: `Serialize` is required for JSON response serialization via Axum. `Deserialize` included for symmetry and potential test deserialization. `ToSchema` for OpenAPI documentation. `Clone`, `Debug` follow the pattern from sibling model structs (`AdvisorySummary`, `SbomSummary`). `Default` provides zero-initialization for all fields, satisfying acceptance criterion 4.
- **Field type `u64`**: unsigned integer appropriate for counts; cannot be negative.
- **Documentation**: every field and the struct itself have doc comments per skill Step 6 code quality requirements.
- **Module doc comment**: follows Rust convention with `//!` at the top of the file.
- **No `id` or `sbom_id` field**: the response is scoped to the SBOM via the URL path parameter; including the ID in the response body is unnecessary and would violate the API spec `{ critical, high, medium, low, total }`.
