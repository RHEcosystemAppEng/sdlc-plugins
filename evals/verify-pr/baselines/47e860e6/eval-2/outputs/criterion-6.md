# Criterion 6 — PASS

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## What was checked
The SBOM lookup at the top of `advisory_summary` (`SbomService::new(&db).fetch(sbom_id.id)...`) and whether the PR changes it.

## What was found
- The SBOM fetch and its error propagation are unchanged context lines in the diff. The PR adds only the `Query(params)` extractor to the signature and the filtering block after aggregation.
- The fetch runs before any threshold handling, so the existing not-found path, which returns `AppError` and maps to 404, is still reached first for unknown SBOM IDs, with or without a threshold.

Caveat: the Test Requirements include "Test non-existent SBOM ID returns 404", but no test was added. `tests/api/advisory_summary.rs` was not created. The behavior is preserved, but this PR does not test it.

**Verdict: PASS.** The existing 404 behavior is preserved.
