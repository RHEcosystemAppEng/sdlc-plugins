## Repository
trustify-backend

## Target Branch
main

## Description
Create the remediation module with model types for the aggregation API responses. This establishes the data structures used by the remediation summary and by-product endpoints, following the existing module pattern (model/ + service/ + endpoints/).

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — remediation module root, re-exports submodules
- `modules/fundamental/src/remediation/model/mod.rs` — model submodule root
- `modules/fundamental/src/remediation/model/summary.rs` — RemediationSummary struct: aggregated counts by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- `modules/fundamental/src/remediation/model/by_product.rs` — ProductRemediation struct: per-product breakdown with total, open, resolved counts

## Files to Modify
- `modules/fundamental/src/lib.rs` — add `pub mod remediation;` to expose the new module

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/advisory/model/summary.rs` for struct definitions. Response types should derive `Serialize`, `Deserialize`, `Clone`, `Debug` as seen in sibling model types. Use `common/src/model/paginated.rs::PaginatedResults<T>` as the wrapper for the by-product endpoint response, consistent with how `modules/fundamental/src/sbom/endpoints/list.rs` returns paginated results.

Per CONVENTIONS.md §Module pattern: follow model/ + service/ + endpoints/ structure.
Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's `.rs` module file scope.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults<T>` — paginated response wrapper for the by-product listing
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for struct layout and derives with severity field

## Acceptance Criteria
- [ ] RemediationSummary struct represents counts grouped by severity and status
- [ ] ProductRemediation struct represents per-product breakdown with total, open, and resolved counts
- [ ] Module compiles and is exported from `modules/fundamental/src/lib.rs`
- [ ] Struct derives match sibling model patterns (Serialize, Deserialize, Clone, Debug)

## Test Requirements
- [ ] Unit tests for model struct construction and serialization round-trip
