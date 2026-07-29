# Task 2 — Add remediation aggregation model structs

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Define the data model structs for the remediation aggregation results. These structs represent the aggregated remediation status grouped by severity and by product, used by the remediation service (Task 3) and serialized as JSON responses by the remediation endpoints (Task 4). No new database tables are introduced; these are computed aggregation structs derived from existing vulnerability and SBOM relationship data.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — Remediation module root with `pub mod model; pub mod service; pub mod endpoints;`
- `modules/fundamental/src/remediation/model/mod.rs` — Model module root re-exporting all model structs
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary` struct with severity-by-status counts: fields for total_open, total_in_progress, total_resolved, and a Vec of `SeverityBreakdown` entries (severity: String, open: u64, in_progress: u64, resolved: u64)
- `modules/fundamental/src/remediation/model/by_product.rs` — `ProductRemediation` struct with fields: product_name: String, total: u64, open: u64, in_progress: u64, resolved: u64

## Files to Modify
- `modules/fundamental/src/lib.rs` — Add `pub mod remediation;` to expose the new remediation module

## Implementation Notes
- Follow the existing module pattern from `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/advisory/model/summary.rs` for struct definition conventions (derive macros, serde attributes, field naming).
- `RemediationSummary` contains aggregate counts and a `breakdowns` field of type `Vec<SeverityBreakdown>` where `SeverityBreakdown` has severity (Critical/High/Medium/Low) and per-status counts.
- `ProductRemediation` contains per-product counts (total, open, in_progress, resolved) plus `product_name`.
- All structs must derive `Serialize`, `Deserialize`, `Clone`, `Debug` and use `#[serde(rename_all = "camelCase")]` to match the API contract.
- No new database tables — these are computed structs, not SeaORM entities. The non-functional requirement explicitly forbids new tables.
- Per Key Conventions (Module pattern): follow the `model/ + service/ + endpoints/` directory structure for the new remediation module.
  Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's Rust module file scope.
- Per Key Conventions (Error handling): all public functions that may fail should return `Result<T, AppError>`.
  Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Example of model struct pattern with serde derives and field naming
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains severity field pattern to reference
- `common/src/model/paginated.rs::PaginatedResults` — Response wrapper pattern for list endpoints (relevant for by-product endpoint)

## Acceptance Criteria
- [ ] `RemediationSummary` struct is defined with total_open, total_in_progress, total_resolved counts and a Vec of `SeverityBreakdown` entries
- [ ] `SeverityBreakdown` struct is defined with severity, open, in_progress, resolved fields
- [ ] `ProductRemediation` struct is defined with product_name, total, open, in_progress, resolved fields
- [ ] All structs derive Serialize/Deserialize/Clone/Debug
- [ ] Remediation module is re-exported from `modules/fundamental/src/lib.rs`

## Test Requirements
- [ ] Verify `RemediationSummary` can be serialized to JSON matching the expected response shape
- [ ] Verify `ProductRemediation` can be serialized to JSON with correct field naming
- [ ] Verify an empty `RemediationSummary` (zero counts, empty breakdowns) serializes correctly

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main

## Parent Epic
TC-9006: trustify-backend
