# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Verdict: PASS (with caveat)

## Analysis

The service layer in `modules/fundamental/src/package/service/mod.rs` constructs `PackageSummary` with `vulnerability_count: 0`. For packages with no vulnerabilities, this produces the correct observable result: `vulnerability_count: 0`.

However, this result is achieved by hardcoding the value to 0 for ALL packages (see the `// TODO: implement subquery` comment), not by computing the count from the database. For packages without vulnerabilities, the behavior is coincidentally correct. The underlying implementation gap is captured in Criterion 3.

The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` asserts `pkg.vulnerability_count == 0` for a package seeded without advisories, which would pass given the current implementation.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- The observable behavior for zero-vulnerability packages is correct (returns 0)
- Test coverage exists: `test_package_without_vulnerabilities_has_zero_count`
