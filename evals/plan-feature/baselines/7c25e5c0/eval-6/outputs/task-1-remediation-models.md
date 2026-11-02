## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add response model structs for the remediation tracking feature. Create a `RemediationSummary` struct that holds aggregated vulnerability counts grouped by severity (Critical, High, Medium, Low) and status (Open, In Progress, Resolved). Create a `RemediationByProduct` struct that holds per-product remediation breakdown with total, open, and resolved counts.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — remediation domain module root
- `modules/fundamental/src/remediation/model/mod.rs` — model sub-module with re-exports
- `modules/fundamental/src/remediation/model/summary.rs` — RemediationSummary struct with severity × status matrix
- `modules/fundamental/src/remediation/model/by_product.rs` — RemediationByProduct and ProductRemediationEntry structs

## Files to Modify
- `modules/fundamental/src/lib.rs` — add `pub mod remediation;` declaration

## Implementation Notes
Follow the existing domain module pattern established by `sbom/model/summary.rs` (SbomSummary) and `advisory/model/summary.rs` (AdvisorySummary). Both use `#[derive(Clone, Debug, Serialize, Deserialize)]` with `utoipa::ToSchema` for OpenAPI generation.

Key patterns to follow:
- Use `serde` derives with `#[serde(rename_all = "camelCase")]` matching existing model conventions
- Derive `utoipa::ToSchema` for automatic OpenAPI spec generation (see `modules/fundamental/src/sbom/model/summary.rs` for the pattern)
- RemediationSummary should contain a `Vec<SeverityStatusCount>` where each entry has severity, status, and count fields
- RemediationByProduct should contain a `Vec<ProductRemediationEntry>` where each entry has product name, total, open, and resolved counts

Per docs/constraints.md §5 (Code Change Rules): keep changes scoped to model definitions only — no service or endpoint logic in this task.

## Acceptance Criteria
- [ ] RemediationSummary struct is defined with severity × status count fields
- [ ] RemediationByProduct struct is defined with per-product total/open/resolved counts
- [ ] Both structs derive Serialize, Deserialize, Clone, Debug, and utoipa::ToSchema
- [ ] Module is declared in fundamental lib.rs
- [ ] Structs compile without errors

## Test Requirements
- [ ] Unit tests verify serialization/deserialization round-trip for RemediationSummary
- [ ] Unit tests verify serialization/deserialization round-trip for RemediationByProduct
- [ ] Verify struct fields match the API contract (camelCase JSON keys)

## Dependencies
- None (first task)
