# File 5: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: Create (new file)

## Purpose

Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for an SBOM. This struct is serialized to JSON by Axum's `Json` extractor for the API response.

## Full File Content

```rust
//! Advisory severity summary model.
//!
//! Provides the response type for the SBOM advisory severity aggregation endpoint.

use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated count of advisories by severity level for a given SBOM.
///
/// Each field represents the number of unique advisories at that severity level.
/// The `total` field is the sum of all severity counts. All fields default to 0
/// when no advisories exist at that level.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of critical-severity advisories.
    pub critical: i64,
    /// Number of high-severity advisories.
    pub high: i64,
    /// Number of medium-severity advisories.
    pub medium: i64,
    /// Number of low-severity advisories.
    pub low: i64,
    /// Total number of unique advisories across all severity levels.
    pub total: i64,
}
```

## Rationale

- **Derives**: `Clone, Debug, Serialize, Deserialize` match the sibling model structs (`AdvisorySummary`, `SbomSummary`). `Default` is added to ensure all counts initialize to 0, satisfying the acceptance criterion that all severity levels default to 0. `ToSchema` enables OpenAPI spec generation if utoipa is used.
- **Field types**: `i64` used for counts, consistent with database integer types and SeaORM count results.
- **Documentation**: Every public symbol has a doc comment per skill guidance (Step 6 code quality practices).
- **Module doc comment**: File starts with `//!` module-level documentation per Rust conventions.

## Convention Conformance

- Struct naming: `SeveritySummary` follows `PascalCase` + descriptive name pattern (cf. `AdvisorySummary`, `SbomSummary`)
- Derive attributes: matches sibling model structs
- Field visibility: `pub` fields for direct serialization (matches sibling pattern)
- File placement: in `advisory/model/` directory following the module pattern
