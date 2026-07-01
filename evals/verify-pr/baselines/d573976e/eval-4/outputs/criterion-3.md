# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Criterion Text
The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows the `vulnerability_count` field being set to a hardcoded value:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The criterion requires that the count "reflects unique advisories only (no duplicates from multiple SBOMs)." This implies the implementation must:
1. Actually query the database for advisories related to the package
2. Use `COUNT(DISTINCT a.id)` or equivalent to deduplicate across SBOMs
3. Return the correct count per package

None of this is implemented. The value is hardcoded to `0` with a TODO comment explicitly acknowledging the subquery has not been implemented. The task's Implementation Notes specified a correlated subquery (`SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`), but this subquery is entirely absent from the diff.

The count does NOT reflect unique advisories -- it reflects nothing. It is always 0 regardless of how many advisories exist. This criterion is not satisfied.

Additionally, the test `test_vulnerability_count_deduplicates_across_sboms` in `tests/api/package_vuln_count.rs` asserts `pkg.vulnerability_count == 2`, which would fail at runtime since the hardcoded value is always 0. The test `test_package_with_vulnerabilities_has_count` asserts `pkg.vulnerability_count == 3`, which would also fail. These tests cannot pass with the current implementation.

## Evidence
- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0, // TODO: implement subquery`
- No database subquery is present in the diff
- The correlated subquery from the Implementation Notes is not implemented
- Tests in `tests/api/package_vuln_count.rs` assert non-zero counts (3 and 2) that would fail with the hardcoded 0
- The TODO comment is explicit acknowledgment that the implementation is incomplete
