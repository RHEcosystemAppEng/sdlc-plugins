# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

## Action: CREATE

## Purpose
Define the `SeveritySummary` response struct that the severity aggregation endpoint returns. This struct holds per-severity counts and a total count.

## Detailed Changes

Create a new file with the following content:

### Imports
- `serde::Serialize` — for JSON serialization via Axum's `Json` extractor
- `utoipa::ToSchema` — for OpenAPI schema generation (following sibling model patterns like `SbomSummary`, `AdvisorySummary`)

### Struct: `SeveritySummary`

```rust
use serde::Serialize;
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field holds the count of unique advisories at that severity level.
/// The `total` field is the sum of all severity-level counts.
#[derive(Debug, Clone, Serialize, ToSchema)]
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

### Default Implementation

```rust
impl Default for SeveritySummary {
    /// Returns a SeveritySummary with all counts set to zero.
    fn default() -> Self {
        Self {
            critical: 0,
            high: 0,
            medium: 0,
            low: 0,
            total: 0,
        }
    }
}
```

## Conventions Applied
- **Naming**: Follows `<Entity>Summary` pattern (like `AdvisorySummary`, `SbomSummary`)
- **Derives**: `Debug, Clone, Serialize, ToSchema` matching sibling model structs
- **Documentation**: Doc comments on struct and every field per skill requirements
- **Default**: All severity levels default to 0 (per acceptance criteria)
