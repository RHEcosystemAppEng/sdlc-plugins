# Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

## Verdict: PASS

## Reasoning

The changes to existing files are backward compatible:

1. **summary.rs**: A new field `vulnerability_count: i64` is added to `PackageSummary`. In Rust with serde, adding a new field to a struct is an additive change for serialization (new field appears in JSON output). For deserialization of existing test data, the field would need a default -- however, since the service layer constructs all `PackageSummary` instances explicitly with the field populated, existing deserialization patterns are not affected.

2. **service/mod.rs**: The existing query logic is preserved. The change adds a post-processing step that maps query results into `PackageSummary` structs with the new field included. The original query, filtering, pagination, and sorting behavior are unchanged.

3. **endpoints/list.rs**: The only change is a comment addition on the existing service call line. No functional change to the endpoint signature, parameters, or response handling.

4. **Test file**: `tests/api/package_vuln_count.rs` is entirely new (ADDITIVE) and does not modify any existing test files.

The PR does not modify existing test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`, `tests/api/search.rs`). No existing endpoint contracts are changed. The CI status is reported as passing, which is consistent with backward compatibility.

This criterion is satisfied.
