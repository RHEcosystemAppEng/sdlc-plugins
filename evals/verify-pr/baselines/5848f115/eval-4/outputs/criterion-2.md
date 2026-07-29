## Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

### Verdict: FAIL

### Analysis

The acceptance criterion requires that packages without associated vulnerabilities display a `vulnerability_count` of 0. The intent is that the vulnerability counting mechanism correctly computes zero when no advisories are linked to a package.

### Evidence

In `modules/fundamental/src/package/service/mod.rs`, the vulnerability count is set as follows:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `vulnerability_count` is hardcoded to `0` for ALL packages, regardless of whether they have vulnerabilities or not. The `// TODO: implement subquery` comment explicitly confirms that the counting logic was never implemented.

While the value produced for packages with no vulnerabilities is technically `0` (matching the criterion's expected value), this is not the result of a correct computation. The zero is a placeholder value, not a computed result from the database. The same hardcoded zero is returned for packages that DO have vulnerabilities, which means the counting mechanism is entirely absent.

The implementation notes specified a correlated subquery (`SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`) that was never implemented.

### Why this is FAIL and not PASS

Although the output value (0) coincidentally matches the expected value for zero-vulnerability packages, the criterion's intent requires a working counting mechanism that correctly yields zero when there are no vulnerabilities. A hardcoded placeholder that always returns zero regardless of actual vulnerability state does not satisfy this requirement. The test `test_package_with_vulnerabilities_has_count` confirms this gap: it expects `vulnerability_count == 3` for a package with 3 advisories, but would receive `0` because the subquery is unimplemented.

### Conclusion

The criterion is not satisfied. The zero value is a hardcoded placeholder, not a correctly computed result. The vulnerability counting subquery was never implemented.
