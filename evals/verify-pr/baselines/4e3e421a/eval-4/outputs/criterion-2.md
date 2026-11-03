# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

**Verdict: PASS (met only by the hardcoded placeholder, see caveat)**

## What was checked
- `modules/fundamental/src/package/service/mod.rs`, where `PackageSummary` values are built for the list endpoint.
- `tests/api/package_vuln_count.rs::test_package_without_vulnerabilities_has_zero_count`.

## Evidence
The service maps every package to:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

So a package with no linked advisories does get `vulnerability_count: 0` in the response. The new test
`test_package_without_vulnerabilities_has_zero_count` seeds a package with no advisories and asserts the
count is `0`. That test would pass.

## Caveat
The criterion is met only because **every** package returns `0`. No real computation exists. The zero comes
from a hardcoded value, not from a count over `sbom_package` → `sbom_advisory` → `advisory` that happens to
return 0. Once the subquery is implemented (needed for Criterion 3), this behavior must be checked again. A
`COUNT(...)` subquery returns 0 when no rows match, so the correlated subquery the task asks for would keep
this behavior. A LEFT JOIN plus GROUP BY approach would need `COALESCE`.

## Conclusion
The observable behavior matches the criterion, so it is marked PASS. The reason it matches is the placeholder
that makes Criterion 3 fail.
