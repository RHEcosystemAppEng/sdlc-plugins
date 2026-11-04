# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

**Verdict: PASS (by accident; do not take this as evidence the feature works)**

`modules/fundamental/src/package/service/mod.rs` sets `vulnerability_count: 0, // TODO: implement subquery` for every package. A package with no vulnerabilities therefore does return 0, so the criterion is literally met. The test `test_package_without_vulnerabilities_has_zero_count` would pass.

The 0 comes from a hardcoded placeholder, not from a count that came back empty. The same code returns 0 for packages that do have advisories. Once the real subquery is in place, this criterion needs checking again: `COUNT(DISTINCT ...)` in a correlated subquery returns 0, not NULL, for no rows, which keeps the `i64` (non-Option) type valid.
