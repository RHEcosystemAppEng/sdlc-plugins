# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (with caveat)

## Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows that the service maps all packages with a hardcoded `vulnerability_count: 0`:

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

Packages with no vulnerabilities will indeed show `vulnerability_count: 0`. This specific criterion is technically satisfied by the current implementation.

However, there is a significant caveat: the value is hardcoded to 0 for ALL packages, not just those without vulnerabilities. The `// TODO: implement subquery` comment explicitly acknowledges that the actual computation is not implemented. This means the criterion is satisfied only trivially -- every package returns 0 regardless of its actual vulnerability count. This incomplete implementation directly causes the failure of Criterion 3.

The test `test_package_without_vulnerabilities_has_zero_count` in the new test file confirms this behavior by asserting `pkg.vulnerability_count == 0` for a package seeded without advisories. This test would pass with the current implementation.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- hardcoded `vulnerability_count: 0`
- The `// TODO: implement subquery` comment confirms the implementation is incomplete
- Test file `tests/api/package_vuln_count.rs` includes `test_package_without_vulnerabilities_has_zero_count` which validates this specific case
