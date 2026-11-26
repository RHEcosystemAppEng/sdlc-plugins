# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

**Verdict: PASS (vacuously; see caveat)**

## What was checked
- How `vulnerability_count` is filled in `modules/fundamental/src/package/service/mod.rs`.
- The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs`.

## What was found
The service maps every row to a `PackageSummary` with a hardcoded value:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

A package with no vulnerabilities will therefore return `vulnerability_count: 0`, so the literal wording of this criterion holds. The new test `test_package_without_vulnerabilities_has_zero_count` asserts exactly this.

## Caveat
The criterion holds only because **every** package returns 0, whatever its real advisory count. The code does not compute anything that tells a vulnerable package apart from a clean one. This criterion is marked PASS because its wording is satisfied. The missing computation is a hard failure under Criterion 3, and it also defeats the task's main goal (see the Description section of TC-9104). Once the real subquery is in place, this criterion needs re-checking: `COUNT(...)` from a correlated subquery returns 0 when nothing matches, but a LEFT JOIN plus GROUP BY approach could return NULL and would need `COALESCE(..., 0)`.
