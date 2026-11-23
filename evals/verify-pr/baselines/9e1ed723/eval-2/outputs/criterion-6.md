# Criterion 6 — PASS

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## What was checked
- The SBOM lookup at the top of `advisory_summary` in `modules/fundamental/src/advisory/endpoints/get.rs`.

## What was found
- The lookup `SbomService::new(&db).fetch(sbom_id.id)...` appears only as unchanged context in the diff. The PR does not touch it.
- The new code (query parameter extraction and post-aggregation filtering) runs only after the SBOM has been fetched. A missing SBOM still exits early through the existing error path, which uses `AppError`. Before this PR that path produced 404, and it still does.
- The new `Query<SummaryParams>` extractor cannot cause a 404. With `threshold: Option<String>`, it does not fail for any valid query string.

## Caveats
- No test for the 404 case was added (Test Requirement "Test non-existent SBOM ID returns 404" is not met, and `tests/api/advisory_summary.rs` is missing). The verdict is based on the existing behavior being left untouched.

**Verdict: PASS**
