# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

**Action:** CREATE

## Purpose

Define the `SeveritySummary` response struct returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Detailed Changes

### SeveritySummary struct

```rust
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for a given SBOM.
///
/// Aggregates the number of unique advisories per severity level
/// (Critical, High, Medium, Low) along with the total count.
#[derive(Debug, Clone, Serialize, Deserialize)]
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

### Design rationale

- **Derive macros:** `Serialize`, `Deserialize`, `Debug`, `Clone` — matching the pattern from sibling model structs (`AdvisorySummary`, `SbomSummary`, `AdvisoryDetails`).
- **Field types:** `u32` for counts — non-negative integers, sufficient range for advisory counts.
- **Default behavior:** All fields default to 0 in the service method when constructing the struct (no `Default` derive needed since the service explicitly constructs it with computed values).
- **Documentation:** Every field and the struct itself has a doc comment per the skill's code quality requirements.

### Conventions followed

- File named after the concept (`severity_summary.rs`), consistent with `summary.rs` and `details.rs` siblings.
- Struct is self-contained with no dependencies beyond serde, consistent with other model structs.
- Will be re-exported via `model/mod.rs` (see file-6-description.md).
