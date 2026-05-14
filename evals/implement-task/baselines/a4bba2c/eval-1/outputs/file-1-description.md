# File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose

Define the `SeveritySummary` response struct returned by the advisory severity aggregation endpoint. This struct represents the count of advisories grouped by severity level for a given SBOM.

## Sibling Reference

- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct for derive macro conventions, field naming, and attribute patterns
- `modules/fundamental/src/advisory/model/details.rs` — `AdvisoryDetails` struct for structural reference

## Content

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: i64,
    /// Number of advisories with High severity.
    pub high: i64,
    /// Number of advisories with Medium severity.
    pub medium: i64,
    /// Number of advisories with Low severity.
    pub low: i64,
    /// Total number of unique advisories across all severity levels.
    pub total: i64,
}

impl SeveritySummary {
    /// Create a new SeveritySummary, automatically computing the total.
    pub fn new(critical: i64, high: i64, medium: i64, low: i64) -> Self {
        Self {
            critical,
            high,
            medium,
            low,
            total: critical + high + medium + low,
        }
    }
}
```

## Conventions Followed

- Derives match sibling model structs: `Clone`, `Debug`, `Serialize`, `Deserialize`, `ToSchema`
- `Default` derive ensures all fields zero-initialize (all severity levels default to 0)
- Field type `i64` matches PostgreSQL `bigint` and SeaORM count conventions
- Snake_case field names map directly to JSON keys via serde
- Doc comments on struct and each field enable OpenAPI schema generation via utoipa
- Constructor computes `total` from the four severity counts to avoid inconsistency
