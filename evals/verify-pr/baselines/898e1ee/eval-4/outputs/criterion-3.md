# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

This is the critical failure in the PR. The acceptance criterion requires that `vulnerability_count` reflects the actual count of unique advisories affecting a package, computed via a correlated subquery joining through `sbom_package -> sbom_advisory -> advisory` tables using `COUNT(DISTINCT a.id)`.

None of this is implemented. The vulnerability count is hardcoded to `0` with an explicit TODO comment:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

This means:
1. A package with 3 vulnerabilities would incorrectly report `vulnerability_count: 0`
2. The deduplication logic (COUNT DISTINCT) across SBOMs is entirely absent
3. The correlated subquery specified in the Implementation Notes is not present anywhere in the diff

The tests written in `tests/api/package_vuln_count.rs` actually expose this failure:
- `test_package_with_vulnerabilities_has_count` asserts `pkg.vulnerability_count == 3` but the code would return 0 -- this test would FAIL at runtime
- `test_vulnerability_count_deduplicates_across_sboms` asserts `pkg.vulnerability_count == 2` but the code would return 0 -- this test would also FAIL at runtime

The fact that the tests are written correctly but the implementation is a stub with a TODO creates a contradiction: if CI truly passes, either the tests are not being compiled/run, or the CI status report is inaccurate.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Code: `vulnerability_count: 0, // TODO: implement subquery`
- Missing: The required correlated subquery `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`
- Two out of three integration tests would fail at runtime due to asserting non-zero counts against the hardcoded zero
