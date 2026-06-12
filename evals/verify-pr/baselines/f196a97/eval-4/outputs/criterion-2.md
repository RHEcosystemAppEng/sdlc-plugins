# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Verdict: FAIL

## Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows:

```rust
let items = items.into_iter().map(|p| {
    PackageSummary {
        id: p.id,
        name: p.name,
        version: p.version,
        license: p.license,
        vulnerability_count: 0, // TODO: implement subquery
    }
}).collect();
```

The `vulnerability_count` is hardcoded to `0` for ALL packages, regardless of whether they have vulnerabilities or not. While this technically means packages with no vulnerabilities will show `vulnerability_count: 0`, the implementation is deceptive: it satisfies the zero-count case only because it returns zero for every package indiscriminately.

However, when considered alongside criterion 3 (which requires the count to reflect unique advisories), it becomes clear the implementation is incomplete. The hardcoded zero is a placeholder, not a correct implementation. The `// TODO: implement subquery` comment explicitly confirms this is unfinished work.

A test exists (`test_package_without_vulnerabilities_has_zero_count`) that asserts `vulnerability_count == 0` for a package with no vulnerabilities. This test would pass with the hardcoded zero, but only coincidentally -- the implementation does not actually compute the count.

Despite the test passing coincidentally for the zero case, the criterion requires that the zero reflects an actual computation (i.e., that the system correctly determines there are no vulnerabilities). Since the implementation does not perform any computation and simply hardcodes zero, this criterion is considered not properly satisfied. The implementation must compute the count and return zero when no vulnerabilities exist, not hardcode zero regardless of actual vulnerability state.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- The TODO comment explicitly acknowledges the subquery is not implemented.
- The value is hardcoded, not computed from database joins.
