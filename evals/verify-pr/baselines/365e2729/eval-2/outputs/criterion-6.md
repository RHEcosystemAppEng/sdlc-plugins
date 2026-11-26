# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict: MET (existing behavior preserved; not covered by a new test)**

## Reasoning
The PR does not change the SBOM lookup path. `SbomService::new(&db).fetch(sbom_id.id)` and the error handling after it are unchanged context lines. The new threshold logic runs only after the SBOM has been fetched and the severities aggregated, so the 404 behavior for a missing SBOM is untouched. The exact not-found mapping sits in lines outside the diff hunk. The PR does not modify them, so the pre-existing behavior stands.

Caveat: the Test Requirements call for a test that a non-existent SBOM ID returns 404. That test was not added, and `tests/api/advisory_summary.rs` is absent from the PR.

## Evidence
- `get.rs` (context, unchanged): `let sbom = SbomService::new(&db)` / `.fetch(sbom_id.id)`
- New code (`let filtered = match &params.threshold { ... }`) runs after the fetch and aggregation.
- No test file added.
