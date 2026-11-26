# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

**Verdict: PASS (satisfied only by accident, see caveat)**

## What was checked
- How `modules/fundamental/src/package/service/mod.rs` builds `PackageSummary` in `PackageService::list`.
- `tests/api/package_vuln_count.rs::test_package_without_vulnerabilities_has_zero_count`.

## What was found
The service maps every package row to:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

So a package with no vulnerabilities does return `vulnerability_count: 0`, and the zero-count test asserts exactly that. Read literally, the criterion is met.

## Caveat
The 0 is hard-coded for **every** package, not computed. The criterion passes because the value never changes, not because the code handles the "no advisories" case correctly. For example, it does not use `COALESCE` or a `COUNT` that returns 0 when the join finds no rows. Once the real subquery is written (see Criterion 3), check this criterion again. A correlated `COUNT(DISTINCT ...)` subquery returns 0 when nothing matches, so the planned approach should still satisfy it.
