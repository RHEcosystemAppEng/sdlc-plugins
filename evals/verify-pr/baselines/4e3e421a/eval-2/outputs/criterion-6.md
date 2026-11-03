# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict: MET (PASS)**, based on reading the code. No test was added.

## Reasoning

- The SBOM lookup that produces the 404 (`SbomService::new(&db).fetch(sbom_id.id)...`) is unchanged context in the diff. The PR does not touch the lookup or its error mapping.
- The only change ahead of it is the new `Query(params): Query<SummaryParams>` extractor. `threshold` is `Option<String>`, so the extractor accepts requests without the parameter, and the handler body, including the not-found path, still runs. A request for a non-existent SBOM therefore still returns 404, as it did before.
- The new threshold logic runs only after the SBOM lookup and aggregation succeed, so it cannot change the 404 path.

## Caveat
The required test "non-existent SBOM ID returns 404" was not added (`tests/api/advisory_summary.rs` is missing). The criterion only requires that existing behavior is preserved, and the code shows it is, so the verdict is PASS. The missing test is counted under the test-requirement gap and Scope Containment.
